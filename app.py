import streamlit as st
import re

# ---------------------- 全局样式：仿iOS备忘录风格 ----------------------
st.markdown("""
<style>
/* 整体页面 */
.main {
    background-color: #ffffff;
}
/* 文本编辑区：无边框，大高度 */
.stTextArea textarea {
    border: none !important;
    box-shadow: none !important;
    font-size: 17px;
    padding: 10px;
    min-height: 500px;
    width: 100%;
}
/* 按钮样式：圆角浅灰，仿iOS */
.stButton > button {
    border-radius: 20px !important;
    background-color: #f5f5f5 !important;
    border: none !important;
    color: #111111 !important;
    padding: 5px 12px !important;
    margin: 2px;
}
.stButton > button:hover {
    background-color: #e8e8e8 !important;
}
/* 菜单弹窗样式 */
.menu-container {
    background-color: #f8f8f8;
    border-radius: 12px;
    padding: 10px;
    margin: 10px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.menu-item {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}
.menu-item:last-child {
    border-bottom: none;
}
/* 短信界面样式 */
.sms-box {
    background-color: #f0f0f0;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 初始化会话状态 ----------------------
if "selected_phone" not in st.session_state:
    st.session_state.selected_phone = None
if "show_sms" not in st.session_state:
    st.session_state.show_sms = False
if "sms_content" not in st.session_state:
    st.session_state.sms_content = ""

# ---------------------- 1. 顶部导航栏 ----------------------
col1, col_spacer, col2, col3 = st.columns([1, 6, 1, 1])
with col1:
    if st.button("← 返回"):
        st.session_state.selected_phone = None
        st.session_state.show_sms = False
with col2:
    st.button("⤴ 分享")
with col3:
    st.button("⋯ 更多")

st.divider()

# ---------------------- 2. 备忘录文本编辑区 ----------------------
memo_text = st.text_area(
    label="",
    placeholder="在这里输入内容，比如：\n我的电话是18125434594，有事联系我",
    key="memo_input"
)

# 自动识别文本中的手机号
phone_pattern = r"1[3-9]\d{9}"
phones_found = re.findall(phone_pattern, memo_text)

if phones_found:
    st.info(f"识别到手机号：{', '.join(phones_found)}")
    # 生成可点击的按钮，点击后弹出操作菜单
    for phone in phones_found:
        if st.button(f"📞 操作号码：{phone}"):
            st.session_state.selected_phone = phone
            st.session_state.show_sms = False

# ---------------------- 3. 仿iOS操作菜单 ----------------------
if st.session_state.selected_phone and not st.session_state.show_sms:
    st.markdown(f"""
    <div class="menu-container">
        <div class="menu-item">{st.session_state.selected_phone}</div>
        <div class="menu-item">📞 呼叫 {st.session_state.selected_phone}</div>
        <div class="menu-item">💬 发送信息</div>
        <div class="menu-item">➕ 添加到通讯录</div>
        <div class="menu-item">📋 拷贝</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 点击“发送信息”的按钮
    if st.button("点击这里发送信息"):
        st.session_state.show_sms = True

# ---------------------- 4. 仿iMessage短信发送界面 ----------------------
if st.session_state.show_sms and st.session_state.selected_phone:
    st.markdown(f"### 新iMessage信息")
    st.markdown(f"**收件人：** +86 {st.session_state.selected_phone}")
    st.divider()
    
    # 短信内容输入框
    sms_text = st.text_input(
        label="",
        placeholder="iMessage信息",
        key="sms_input"
    )
    
    # 发送按钮（Streamlit里模拟发送，也可以改成实际调用短信接口）
    if st.button("发送"):
        st.success(f"已向 {st.session_state.selected_phone} 发送短信：{sms_text}")
        # 发送后返回备忘录界面
        st.session_state.show_sms = False
        st.session_state.selected_phone = None

# ---------------------- 底部工具栏 ----------------------
st.divider()
c1, c2, c3, c_space, c_edit = st.columns([1, 1, 1, 5, 1])
with c1:
    st.button("☰ 格式")
with c2:
    st.button("📎 附件")
with c3:
    st.button("📍 定位")
with c_edit:
    st.button("✏️ 编辑")
