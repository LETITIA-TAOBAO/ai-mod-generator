import dashscope

dashscope.api_key = "sk-17d34dca1acf4922a910d737f51567e6"


SYSTEM_PROMPT = """
你是一个游戏Mod设计AI助手（Don't Starve）。
你需要帮助用户逐步完善Boss/怪物/物品设计。

规则：
1. 用游戏设计语言回答
2. 记住用户之前说过的信息
3. 不要一次性生成完整代码
4. 要引导用户补全缺失信息
5. 输出必须是JSON：

{
  "concept": "",
  "entity": "",
  "mechanics": [],
  "questions": []
}
"""


def call_qwen(messages):
    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format="message"
    )

    return response.output.choices[0].message.content


def design_with_llm(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    return call_qwen(messages)