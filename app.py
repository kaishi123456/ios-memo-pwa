import streamlit as st
import re

# ---------------------- 全局样式：1:1还原苹果备忘录+iMessage界面 ----------------------
st.markdown("""
<style>
/* 全局重置 */
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
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
/* 圆形图标按钮（返回/编辑） */
.icon-btn-circle {
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
/* 顶部右侧按钮组（分享+更多） */
.icon-btn-group {
    display: inline-flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 22px;
    padding: 8px 16px;
    gap: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.icon-btn-group span {
    font-size: 20px;
    color: #111;
}

/* 备忘录文本编辑区 */
.stTextArea textarea {
    border: none !important;
    box-shadow: none !important;
    font-size: 17px;
    padding: 10px;
    min-height: 600px;
    width: 100%;
    background-color: transparent;
}

/* 底部工具栏 */
.bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    margin-top: 10px;
}
/* 底部左侧功能图标组 */
.bottom-icons {
    display: inline-flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 22px;
    padding: 10px 24px;
    gap: 32px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.bottom-icons span {
    font-size: 22px;
    color: #111;
}

/* 仿iOS手机号操作菜单 */
.phone-menu-container {
    background-color: #f8f8f8;
    border-radius: 16px;
    padding: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    max-width: 300px;
}
.phone-header {
    display: flex;
    align-items: center;
    padding: 8px;
    margin-bottom: 8px;
}
.phone-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #ccc;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #fff;
    margin-right: 12px;
}
.phone-menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 8px;
    border-bottom: 1px solid #e0e0e0;
    cursor: pointer;
}
.phone-menu-item:last-child {
    border-bottom: none;
}
.phone-menu-item span {
    font-size: 16px;
}

/* 仿iMessage短信界面 */
.sms-container {
    background-color: #fff;
    border-radius: 16px 16px 0 0;
    padding: 20px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
}
.sms-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.sms-header h3 {
    margin: 0;
    font-weight: 500;
}
.sms-header .cancel-btn {
    color: #007aff;
    font-size: 16px;
    cursor: pointer;
}
.recipient-box {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;
}
.recipient-label {
    color: #888;
    font-size: 14px;
    margin-bottom: 4px;
}
.recipient-number {
    font-size: 16px;
    color: #007aff;
}
.sender-select {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 30px;
}
.message-input {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 20px;
    margin-top: 20px;
}
.message-input input {
    flex: 1;
    border: none;
    background-color: transparent;
    font-size: 16px;
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 会话状态初始化 ----------------------
if "page_state" not in st.session_state:
    st.session_state.page_state = "memo"  # 状态：memo/menu/sms
if "selected_phone" not in st.session_state:
    st.session_state.selected_phone = None
if "sms_content" not in st.session_state:
    st.session_state.sms_content = ""

# ---------------------- 1. 备忘录主界面 ----------------------
if st.session_state.page_state == "memo":
    # 顶部导航栏
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="nav-bar">
            <div class="icon-btn-circle">←</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="nav-bar" style="justify-content: flex-end;">
            <div class="icon-btn-group">
                <span>⤴</span>
                <span>⋯</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 备忘录文本编辑区
    memo_text = st.text_area(
        label="",
        placeholder="在这里输入内容，比如：\n联系电话：18125434594",
        key="memo_input"
    )

    # 识别文本中的手机号
    phone_pattern = r"1[3-9]\d{9}"
    phones_found = re.findall(phone_pattern, memo_text)

    if phones_found:
        st.info(f"识别到手机号：{', '.join(phones_found)}")
        # 生成手机号操作按钮
        for phone in phones_found:
            if st.button(f"📞 操作号码：{phone}"):
                st.session_state.selected_phone = phone
                st.session_state.page_state = "menu"
                st.rerun()

    st.divider()

    # 底部工具栏
    st.markdown("""
    <div class="bottom-bar">
        <div class="bottom-icons">
            <span>☑</span>
            <span>📎</span>
            <span>🧭</span>
        </div>
        <div class="icon-btn-circle">✏️</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- 2. 仿iOS手机号操作菜单 ----------------------
elif st.session_state.page_state == "menu":
    st.markdown(f"""
    <div class="phone-menu-container">
        <div class="phone-header">
            <div class="phone-avatar">👤</div>
            <div style="font-size: 20px; font-weight: 500;">{st.session_state.selected_phone}</div>
        </div>
        <div class="phone-menu-item">
            <span>呼叫 {st.session_state.selected_phone}</span>
            <span>📞</span>
        </div>
        <div class="phone-menu-item">
            <span>发送信息</span>
            <span>💬</span>
        </div>
        <div class="phone-menu-item">
            <span>FaceTime 通话</span>
            <span>📹</span>
        </div>
        <div class="phone-menu-item">
            <span>添加到通讯录</span>
            <span>➕</span>
        </div>
        <div class="phone-menu-item">
            <span>拷贝</span>
            <span>📋</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 返回备忘录"):
            st.session_state.page_state = "memo"
            st.session_state.selected_phone = None
            st.rerun()
    with col2:
        if st.button("发送信息"):
            st.session_state.page_state = "sms"
            st.rerun()

# ---------------------- 3. 仿iMessage短信发送界面 ----------------------
elif st.session_state.page_state == "sms":
    st.markdown(f"""
    <div class="sms-container">
        <div class="sms-header">
            <h3>新iMessage信息</h3>
            <div class="cancel-btn">取消</div>
        </div>
        <div class="recipient-box">
            <div class="recipient-label">收件人：</div>
            <div class="recipient-number">+86 {st.session_state.selected_phone}</div>
        </div>
        <div class="sender-select">
            <div class="recipient-label">发件人：</div>
            <div style="display: flex; gap: 12px;">
                <span style="background-color: #007aff; color: #fff; padding: 4px 8px; border-radius: 4px;">副号1</span>
                <span>副号</span>
            </div>
        </div>
        <div class="message-input">
            <span>📷</span>
            <span>🅰️</span>
            <input type="text" placeholder="iMessage信息" id="sms_input">
            <span>🎤</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 发送/返回按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 返回菜单"):
            st.session_state.page_state = "menu"
            st.rerun()
    with col2:
        if st.button("发送短信"):
            st.success(f"已向 {st.session_state.selected_phone} 发送短信！")
            st.session_state.page_state = "memo"
            st.session_state.selected_phone = None
            st.rerun()
