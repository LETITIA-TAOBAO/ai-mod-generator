import streamlit as st
import json

from llm.qwen_client import design_with_llm, explore_with_llm
from bridge.intent_builder import build_intent_from_design
from parser.recommender import recommend

from core.agent_flow import explore_step, generate_step

from ui.theme import inject_theme
from ui.components import (
    render_banner,
    render_boss_card,
    render_mechanics,
    render_chat
)

from generator.image_generator import generate_boss_image
from generator.packer import build_full_mod


# =========================
# 🎨 页面基础设置
# =========================
st.set_page_config(
    page_title="AI Mod Generator",
    layout="wide"
)

# 注入主题（非常关键）
st.markdown(inject_theme(), unsafe_allow_html=True)


# =========================
# 🧠 Session State 初始化
# =========================
if "mode" not in st.session_state:
    st.session_state.mode = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# 🌙 顶部UI
# =========================
render_banner()


# =========================
# 🎮 模式选择
# =========================
st.markdown("## 🎮 选择你的创作模式")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 快速生成模式"):
        st.session_state.mode = "fast"

with col2:
    if st.button("🧠 探索设计模式"):
        st.session_state.mode = "explore"


# =========================
# 🧠 探索模式（多轮对话）
# =========================
if st.session_state.mode == "explore":

    st.markdown("## 🧠 世界观构建中...")

    user_input = st.chat_input("描述你的Boss/怪物/物品想法...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        reply = explore_step(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    # 渲染聊天
    render_chat(st.session_state.messages)

    # 进入生成
    if st.button("🌙 生成Boss实体"):
        st.session_state.mode = "generate"


# =========================
# ⚙️ 生成模式（核心）
# =========================
if st.session_state.mode == "generate":

    st.markdown("## ⚙️ 正在构建你的月之造物...")

    with st.spinner("AI正在塑造世界结构..."):

        # ===== 1. 生成设计 =====
        design, result = generate_step(st.session_state.messages)

        # ===== 2. 图片生成 =====
        image_url = generate_boss_image(design.get("entity", "boss"))

    # =========================
    # 🎮 展示 Boss
    # =========================
    render_boss_card(design, image_url)

    # =========================
    # ⚔️ 机制展示
    # =========================
    render_mechanics(design.get("mechanics", []))

    # =========================
    # 🔧 API & 代码
    # =========================
    st.markdown("## 🔧 生成代码")

    code = result.get("code", "-- no code generated")

    st.code(code, language="lua")

    # =========================
    # 📦 下载 Mod
    # =========================
    zip_data = build_full_mod(code)

    st.download_button(
        "📦 下载你的月之Mod",
        data=zip_data,
        file_name="moon_boss_mod.zip"
    )


# =========================
# 🧪 Debug模式（可选）
# =========================
if st.sidebar.checkbox("Debug模式"):

    st.sidebar.write("Mode:", st.session_state.mode)
    st.sidebar.write("Messages:")
    st.sidebar.json(st.session_state.messages)