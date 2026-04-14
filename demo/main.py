import json
from parser.parser import parse
from parser.recommender import recommend   # ✅ 新增

def main():
    print("🎮 Mod Assistant Demo")
    print("输入你的玩法想法（输入 exit 退出）")

    while True:
        text = input("\n👉 ")

        if text == "exit":
            break

        intent = parse(text)
        result = recommend(intent)

        print("\n🧠 玩法解析：")
        print(json.dumps(intent.to_dict(), indent=2, ensure_ascii=False))

        print("\n🔧 推荐API：")
        for api in result["apis"]:
            print("-", api)

        print("\n📌 实现步骤：")
        for i, step in enumerate(result["steps"], 1):
            print(f"{i}. {step}")


if __name__ == "__main__":
    main()