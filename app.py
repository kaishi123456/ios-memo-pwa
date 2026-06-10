import streamlit as st

# -------------------------- 页面基础设置 --------------------------
st.set_page_config(
    page_title="快捷工具",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 侧边栏：功能选择 --------------------------
with st.sidebar:
    st.title("📋 功能选择")
    page = st.radio(
        "请选择功能",
        ["短信快捷入口", "备忘录"],
        index=0
    )

# -------------------------- 页面1：短信快捷入口 --------------------------
if page == "短信快捷入口":
    st.title("📱 短信快捷入口")
    st.markdown("""
    1.  把手机号粘贴到下方文本框，**一行一个**
    2.  粘贴后会自动生成可点击链接
    3.  点击号码，iPhone 会直接唤起短信界面
    """)
    
    # 手机号输入框
    phone_text = st.text_area(
        "粘贴手机号（一行一个）",
        placeholder="例如：\n18125434594\n18276415554\n18744721968",
        height=300
    )
    
    st.divider()
    
    # 处理手机号并生成链接
    if phone_text:
        phone_list = [line.strip() for line in phone_text.splitlines() if line.strip()]
        st.subheader("点击号码发送短信")
        
        for num in phone_list:
            # 使用 sms: 协议，点击后直接跳转到短信界面
            st.markdown(
                f'''
                <a href=" " style="
                    color:#007AFF;
                    font-size:18px;
                    text-decoration:none;
                    display:block;
                    padding:12px 16px;
                    border-bottom:1px solid #eee;
                    background-color:#f8f9fa;
                    border-radius:8px;
                    margin:8px 0;
                ">{num}</a >
                ''',
                unsafe_allow_html=True
            )

# -------------------------- 页面2：备忘录 --------------------------
elif page == "备忘录":
    st.title("📝 备忘录")
    
    # 简单的备忘录功能（你原来的功能）
    note_title = st.text_input("笔记标题", placeholder="给笔记起个名字...")
    note_content = st.text_area("笔记内容", placeholder="在这里写你的笔记...", height=300)
    
    if st.button("保存笔记", use_container_width=True):
        if note_title and note_content:
            st.success(f"✅ 笔记「{note_title}」已保存！")
        else:
            st.warning("⚠️ 请填写标题和内容再保存")
