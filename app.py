import streamlit as st
import json
import os
from datetime import datetime

# 页面配置（必须放在最前面）
st.set_page_config(
    page_title="备忘录",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态数据
def load_memos():
    if "memos" not in st.session_state:
        st.session_state["memos"] = []
    return st.session_state["memos"]

def save_memos(memos):
    st.session_state["memos"] = memos

memos = load_memos()

# 仿苹果备忘录CSS样式
st.markdown("""
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background-color: #F2F2F7;
}
.stButton>button {
    background-color: #007AFF;
    color: white;
    border-radius: 8px;
}
.delete-btn>button {
    background-color: #FF3B30;
}
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("# 📝 备忘录")
    st.divider()
    if st.button("➕ 新建笔记", use_container_width=True):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        memos.append({"title": "新笔记", "content": "", "time": now})
        save_memos(memos)
        st.rerun()
    st.divider()
    if memos:
        selected_idx = st.radio("笔记列表", range(len(memos)), format_func=lambda i: memos[i]["title"])
    else:
        st.info("暂无笔记")
        selected_idx = None

# 主编辑区
if memos and selected_idx is not None:
    current = memos[selected_idx]
    title = st.text_input("标题", value=current["title"], label_visibility="collapsed")
    content = st.text_area("内容", value=current["content"], height=500, label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 保存", use_container_width=True):
            memos[selected_idx]["title"] = title
            memos[selected_idx]["content"] = content
            memos[selected_idx]["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_memos(memos)
            st.success("已保存！")
    with col2:
        if st.button("🗑️ 删除", use_container_width=True, key="del"):
            memos.pop(selected_idx)
            save_memos(memos)
            st.rerun()
else:
    st.info("👈 点击左侧「新建笔记」开始使用")