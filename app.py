import streamlit as st

# ---------------------- 全局样式：还原苹果备忘录图标与布局 ----------------------
st.markdown("""
<style>
/* 整体页面 */
.main {
    background-color: #ffffff;
    padding: 10px;
}
/* 顶部导航栏 */
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    margin-bottom: 10px;
}
/* 单个图标按钮通用样式（圆形/圆角，浅灰背景） */
.icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #f5f5f5;
    border-radius: 50%;
    border: none;
    width: 44px;
    height: 44px;
    font-size: 20px;
    color: #111;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.icon-btn-group {
    display: inline-flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 22px;
    padding: 8px 12px;
    gap: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.icon-btn-group span {
    font-size: 20px;
}
/* 底部工具栏 */
.bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    margin-top: 10px;
}
/* 底部左侧图标组 */
.bottom-icons {
    display: inline-flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 22px;
    padding: 10px 20px;
    gap: 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.bottom-icons span {
    font-size: 22px;
}
/* 编辑区样式 */
.stTextArea textarea {
    border: none !important;
    box-shadow: none !important;
    font-size: 17px;
    padding: 10px;
    min-height: 600px;
    width: 100%;
    background-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 1. 顶部导航栏 ----------------------
# 左侧返回按钮
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class="nav-bar">
        <div class="icon-btn">
            ←
        </div>
    </div>
    """, unsafe_allow_html=True)

# 右侧分享+更多按钮组
with col2:
    st.markdown("""
    <div class="nav-bar" style="justify-content: flex-end;">
        <div class="icon-btn-group">
            <span>⤴</span>
            <span>⋯</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- 2. 中间文本编辑区 ----------------------
memo_content = st.text_area(
    label="",
    placeholder="开始输入你的备忘录内容...",
    key="memo_text"
)

# ---------------------- 3. 底部工具栏 ----------------------
st.markdown("""
<div class="bottom-bar">
    <div class="bottom-icons">
        <span>☑️—○—</span>
        <span>📎</span>
        <span>🧭</span>
    </div>
    <div class="icon-btn">
        ✏️
    </div>
</div>
""", unsafe_allow_html=True)
