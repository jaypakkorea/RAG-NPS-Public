from pathlib import Path
import streamlit as st

# 업로드 경로 생성 함수
def save_uploaded_file(uploaded_file):
    upload_dir = Path("./uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / uploaded_file.name
    file_path.write_bytes(uploaded_file.getbuffer())
    return str(file_path)

# 사이드바
def render_sidebar():
    with st.sidebar:
        uploaded_files = st.file_uploader(
            "파일 업로드",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            st.session_state.uploaded_files_meta = [
                {"name": file.name, "size": file.size} for file in uploaded_files
            ]
        else:
            st.session_state.uploaded_files_meta = []

        st.subheader("업로드된 파일")
        if st.session_state.uploaded_files_meta:
            for item in st.session_state.uploaded_files_meta:
                size_kb = item["size"] / 1024
                st.write(f"- {item['name']} ({size_kb:.1f} KB)")
        else:
            st.caption("아직 업로드된 파일이 없습니다.")

        if st.button("대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# 채팅 내역
def render_chat():
    st.title("NPS X RAG")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    query = st.chat_input("질문을 입력해 주세요.")
    if not query:
        return

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": "안녕하세요."})
    st.rerun()


st.set_page_config(page_title="기초 챗봇 UI", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files_meta" not in st.session_state:
    st.session_state.uploaded_files_meta = []

render_sidebar()
render_chat()
