from .api_map import API_MAP

STEP_MAP = {
    "entity": {
        "creature": ["创建怪物Prefab"]
    },
    "trigger": {
        "night": ["监听夜晚（TheWorld.state.isnight）"]
    },
    "behavior": {
        "light": [
            "添加光源组件（inst.entity:AddLight()）"
        ],
        "buff": [
            "添加combat组件",
            "提升攻击力（SetDamage）"
        ]
    }
}

def recommend(intent):
    apis = []
    steps = []

    # ===== API 推荐 =====
    for trigger in intent.triggers:
        if trigger in API_MAP:
            apis.extend(API_MAP[trigger]["apis"])

    for behavior in intent.behaviors:
        if behavior in API_MAP:
            apis.extend(API_MAP[behavior]["apis"])

    apis = list(set(apis))

    # ===== 智能步骤生成 =====

    # 实体
    if intent.entity in STEP_MAP["entity"]:
        steps.extend(STEP_MAP["entity"][intent.entity])

    # 触发条件
    for trigger in intent.triggers:
        if trigger in STEP_MAP["trigger"]:
            steps.extend(STEP_MAP["trigger"][trigger])

    # 行为
    for behavior in intent.behaviors:
        if behavior in STEP_MAP["behavior"]:
            steps.extend(STEP_MAP["behavior"][behavior])

    return {
        "apis": apis,
        "steps": steps
    }