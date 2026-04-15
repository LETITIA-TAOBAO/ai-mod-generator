import dashscope
import os


# ===== API Key 设置 =====
# ⚠️ 注意：这里必须写成 DASHSCOPE_API_KEY（不是你的key本身）
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


# ===============================
# 🟢 探索模式（对话引导用）
# ===============================
EXPLORE_SYSTEM_PROMPT = """
你是一个游戏设计AI助手（Don't Starve Mod方向）。

你的任务：
帮助用户逐步完善想法，而不是直接给答案。

规则：
1. 只用自然语言对话（绝对不要输出JSON）
2. 不要写代码
3. 多提问，引导用户思考
4. 一次最多问2-3个关键问题
5. 可以提出设计建议，但不要完整设计
6. 风格偏游戏策划（机制、体验、世界观）

目标：
帮助用户从“模糊想法” → “清晰设计”
"""


def explore_with_llm(messages):
    """
    用于探索模式（多轮对话）
    输入：messages（聊天历史）
    输出：自然语言回复
    """

    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=[{"role": "system", "content": EXPLORE_SYSTEM_PROMPT}] + messages,
        result_format="message"
    )

    return response.output.choices[0].message.content


# ===============================
# 🔵 生成模式（结构化输出）
# ===============================
SYSTEM_PROMPT = """
你是一个游戏Mod设计AI助手（Don't Starve）。

你需要根据用户输入，生成结构化设计。

规则：
1. 用游戏设计语言回答
2. 记住上下文
3. 不要生成代码
4. 输出必须是JSON（不能有额外文本）

格式如下：

{
  "concept": "核心概念描述",
  "entity": "Boss / 怪物 / 物品",
  "mechanics": ["机制1", "机制2"],
  "questions": ["需要补充的问题"]
}
"""


def design_with_llm(messages):
    """
    用于最终生成结构化设计
    输入：可以是字符串 或 messages列表
    输出：JSON字符串
    """

    # 👉 兼容两种输入方式（很重要）
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        result_format="message"
    )

    return response.output.choices[0].message.content


# ===============================
# 🔍 Debug（可选）
# ===============================
if __name__ == "__main__":
    print("qwen_client loaded")
