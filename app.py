import streamlit as st
import json

from llm.qwen_client import design_with_llm
from bridge.intent_builder import build_intent_from_design
from parser.recommender import recommend


st.title("🎮 AI 饥荒 Mod 生成器")

user_input = st.text_input("输入你的想法（例如：月亮Boss）")

if st.button("生成"):
    
    # ===== 1. LLM设计 =====
    design_str = design_with_llm(user_input)

    try:
        design = json.loads(design_str)
    except:
        st.error("LLM返回不是JSON")
        st.text(design_str)
        st.stop()

    st.subheader("🧠 设计概念")
    st.write(design.get("concept"))

    st.subheader("❓ 建议补充")
    for q in design.get("questions", []):
        st.write("•", q)

    # ===== 2. intent =====
    intent = build_intent_from_design(design)

    # ===== 3. recommend =====
    result = recommend(intent)

    st.subheader("🔧 推荐API")
    st.write(result.get("apis", []))

    st.subheader("📌 实现步骤")
    for i, step in enumerate(result.get("steps", []), 1):
        st.write(f"{i}. {step}")

    st.subheader("💻 Lua代码")
    st.code(result.get("code", "-- no code"))