import streamlit as st
import re
import os
import json
from datetime import datetime

# ===================== 全局配置 & 样式（1:1 iOS 备忘录风格）=====================
st.set_page_config(page_title="仿苹果备忘录", layout="wide")

# 数据目录初始化
DATA_DIR = "memo_data"
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
MEMO_FILE = os.path.join(DATA_DIR, "memos.json")

# 初始化数据
def init_data():
    if not os.path.exists(MEMO_FILE):
        with open(MEMO_FILE, "w", encoding="utf-8") as f:
            json.dump({"folders": ["默认文件夹"], "memos": []}, f, ensure_ascii=False, indent=2)

def load_data():
    with open(MEMO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

init_data()
data = load_data()

# 会话状态初始化
if "curr_folder" not in st.session_state:
    st.session_state.curr_folder = "默认文件夹"
if "curr_memo_id" not in st.session_state:
    st.session_state.curr_memo_id = None
if "page" not in st.session_state:
    st.session_state.page = "list"  # list / edit / menu

# ===================== iOS 原生样式 CSS =====================
st.markdown("""
<style>
* {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;}
.main {background: #ffffff;}
.sidebar .block-container {background: #f7f7f9;}

/* 圆形图标按钮 */
.ios-icon-btn {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    width:44px;
    height:44px;
    border-radius:50%;
    background:#f2f2f7;
    font-size:20px;
    color:#007aff;
    cursor:pointer;
}
.ios-icon-group {
    display:inline-flex;
    gap:20px;
    background:#f2f2f7;
    border-radius:22px;
    padding:8px 16px;
    font-size:20px;
    color:#007aff;
}

/* 文本编辑区 无边框 */
.stTextArea textarea {
    border:none !important;
    box-shadow:none !important;
    font-size:17px;
    min-height:600px;
    background:transparent !important;
}

/* 底部工具栏 */
.bottom-tool {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 0;
}
.tool-group {
    display:inline-flex;
    gap:30px;
    background:#f2f2f7;
    border-radius:22px;
    padding:10px 24px;
    font-size:22px;
    color:#007aff;
}

/* iOS 弹出菜单 */
.ios-menu {
    background:#f2f2f7;
    border-radius:16px;
    padding:12px;
    box-shadow:0 4px 20px rgba(0,0,0,0.15);
    max-width:320px;
}
.menu-item {
    padding:12px 8px;
    border-bottom:1px solid #e5e5ea;
    font-size:16px;
    cursor:pointer;
}
.menu-item:last-child {border:none;}

/* 笔记列表项 */
.memo-item {
    padding:12px;
    border-bottom:1px solid #e5e5ea;
    cursor:pointer;
}
.memo-item:hover {background:#f2f2f7;}
</style>
""", unsafe_allow_html=True)

# ===================== 工具函数：手机号识别 =====================
PHONE_REG = re.compile(r"1[3-9]\d{9}")

# ===================== 页面1：笔记列表页 =====================
if st.session_state.page == "list":
    # 顶部导航
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="ios-icon-btn">←</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align:right" class="ios-icon-group">⤴ ⋯</div>', unsafe_allow_html=True)

    st.divider()

    # 新建笔记按钮
    if st.button("➕ 新建备忘录", use_container_width=True):
        new_id = str(datetime.now().timestamp())
        data["memos"].append({
            "id": new_id,
            "folder": st.session_state.curr_folder,
            "title": "",
            "content": "",
            "create_time": str(datetime.now()),
            "update_time": str(datetime.now())
        })
        save_data(data)
        st.session_state.curr_memo_id = new_id
        st.session_state.page = "edit"
        st.rerun()

    st.subheader(f"📁 {st.session_state.curr_folder}")

    # 展示当前文件夹笔记
    memo_list = [m for m in data["memos"] if m["folder"] == st.session_state.curr_folder]
    if not memo_list:
        st.info("暂无备忘录，点击上方按钮新建")
    else:
        for memo in reversed(memo_list):
            title = memo["title"] if memo["title"] else "无标题备忘录"
            preview = memo["content"][:30] + "..." if len(memo["content"]) > 30 else memo["content"]
            st.markdown(f"""
            <div class="memo-item" onclick="parent.document.querySelector('[data-testid=stButton]').click()">
                <b>{title}</b><br>
                <span style="color:#666;font-size:14px">{preview}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"打开_{memo['id']}", key=f"open_{memo['id']}", visible=False):
                st.session_state.curr_memo_id = memo["id"]
                st.session_state.page = "edit"
                st.rerun()

# ===================== 页面2：笔记编辑页（核心编辑界面） =====================
elif st.session_state.page == "edit":
    # 查找当前笔记
    curr_memo = None
    for m in data["memos"]:
        if m["id"] == st.session_state.curr_memo_id:
            curr_memo = m
            break

    if not curr_memo:
        st.session_state.page = "list"
        st.rerun()

    # 顶部导航
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← 返回列表"):
            # 自动保存
            save_data(data)
            st.session_state.page = "list"
            st.rerun()
    with col2:
        st.markdown('<div style="text-align:right" class="ios-icon-group">⤴ ⋯</div>', unsafe_allow_html=True)

    st.divider()

    # 标题输入
    note_title = st.text_input("标题", value=curr_memo["title"], label_visibility="collapsed")
    # 正文编辑
    note_content = st.text_area("", value=curr_memo["content"], placeholder="开始输入备忘录内容...")

    # 识别手机号
    phones = PHONE_REG.findall(note_content)
    if phones:
        st.success(f"识别到号码：{', '.join(phones)}")
        for p in phones:
            if st.button(f"操作号码 {p}", key=f"phone_{p}"):
                st.session_state["selected_phone"] = p
                st.session_state.page = "menu"
                st.rerun()

    # 附件上传
    st.file_uploader("添加附件/图片", accept_multiple_files=True)

    # 实时保存
    curr_memo["title"] = note_title
    curr_memo["content"] = note_content
    curr_memo["update_time"] = str(datetime.now())
    save_data(data)

    st.divider()

    # 底部工具栏（苹果原生图标）
    st.markdown("""
    <div class="bottom-tool">
        <div class="tool-group">☑ 📎 📍</div>
        <div class="ios-icon-btn">✏️</div>
    </div>
    """, unsafe_allow_html=True)

# ===================== 页面3：手机号操作菜单（仿iOS弹窗） =====================
elif st.session_state.page == "menu":
    phone = st.session_state.get("selected_phone", "")
    st.markdown(f"""
    <div class="ios-menu">
        <div style="padding:12px;font-size:18px;font-weight:bold">{phone}</div>
        <div class="menu-item">📞 呼叫 {phone}</div>
        <div class="menu-item">💬 发送信息</div>
        <div class="menu-item">📹 FaceTime 通话</div>
        <div class="menu-item">➕ 添加到通讯录</div>
        <div class="menu-item">📋 拷贝号码</div>
    </div>
    """, unsafe_allow_html=True)

    # 功能按钮
    if st.button("📲 打开系统短信"):
        # 唤起手机原生短信（sms协议，手机浏览器生效）
        st.markdown(f'<a href=" " target="_blank">跳转短信</a >', unsafe_allow_html=True)
    if st.button("返回笔记"):
        st.session_state.page = "edit"
        st.rerun()
