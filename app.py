import streamlit as st
import json
import pandas as pd
import io
from dotenv import load_dotenv
from read_txt import to_table_html
from sound_to_txt import sound_to_txt
from return_txt import return_txt1, return_txt2, return_txt3, return_txt4
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    # 페이지 설정
    st.set_page_config(layout="wide")

    # 메인 제목
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>소리글</h1>", unsafe_allow_html=True)
    st.divider()

    # 초기 상태값 세팅
    if "transcribed" not in st.session_state:
        st.session_state["transcribed"] = False
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # -------- 사이드바 --------
    st.sidebar.header("소리글 기능 선택")
    page = st.sidebar.radio(
        "이용하실 기능을 선택하세요",
        ["대화 내용 전체 보기", "대화 내용 요약 보기", "Chat Bot"]
    )
    st.sidebar.divider()

    if st.sidebar.button("새 소리글 만들기"):
        st.session_state.clear()
        st.rerun()

    # -------- 스타일 커스터마이징 --------
    st.markdown("""
        <style>
            .upload-container {
                text-align: center;
                border: 2px dashed #cccccc;
                border-radius: 15px;
                padding: 60px;
                background-color: #fafafa;
                transition: all 0.3s ease;
                margin-top: 80px;
                margin-bottom: 50px;
            }
            .upload-container:hover {
                background-color: #f0f8ff;
                border-color: #67b7dc;
            }
            .upload-text {
                font-weight: 500;
                color: #555;
                margin-top: 15px;
            }
            .stButton button {
                background-color: #4CAF50;
                color: white;
                font-size: 1.2em;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.6em 2em;
                transition: 0.3s;
            }
            .stButton button:hover {
                background-color: #43a047;
                transform: scale(1.03);
            }
        </style>
    """, unsafe_allow_html=True)

    # -------- 변환 수행 (메인 콘텐츠 영역) --------
    if not st.session_state["transcribed"]:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        st.markdown("### 🎧 음성 파일을 업로드하고 변환을 시작하세요")
        st.markdown("<p class='upload-text'>(지원 파일 형식 : mp3, mp4, mpeg, mpga, m4a, wav)</p>", unsafe_allow_html=True)

        if st.button("변환 시작 🚀"):
            result_json = sound_to_txt()
            if not result_json:
                st.warning("⚠️ 파일 선택에 실패하거나 형식이 잘못되었습니다.")
                return
            st.session_state["transcribed"] = True
            st.session_state["result_json"] = result_json

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # -------- 변환 완료후 프롬프트 실행 --------
        data = json.loads(st.session_state["result_json"])
        segments = data.get("segments", [])

        res1 = return_txt1(data)
        res2 = return_txt2(data)
        res3 = return_txt3(res2)
        res4 = return_txt4(res3)

        # ---- 페이지 렌더링 ----
        if page == "대화 내용 전체 보기":
            st.header("🗣️ 대화 내용")

            html = to_table_html(segments)
            st.components.v1.html(html, height=500, scrolling=True)

            # 대화내용 Excel 다운로드 추가
            if segments:
                df = pd.DataFrame(segments)

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="sample")

                st.download_button(
                    label="📥 대화 내용 엑셀 다운로드",
                    data=buffer.getvalue(),
                    file_name="sample.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        elif page == "대화 내용 요약 보기":
            col1, col2 = st.columns(2)
            with col1:
                st.header("1️⃣ 대화의 주제 및 요약")
                st.write(res1)
                st.divider()

                st.header("2️⃣ 대화 내용 중 요청사항")
                st.write(res2)

            with col2:
                st.header("3️⃣ 요청사항 요약 및 미비사항")
                st.write(res3)
                st.divider()

                st.header("4️⃣ 요청사항에 대한 준비할 사항")
                st.write(res4)

        elif page == "Chat Bot":
            st.header("🤖 Chat Bot")

            for role, content in st.session_state["messages"]:
                with st.chat_message(role):
                    st.write(content)

            user_input = st.chat_input("메시지를 입력하세요.")
            if user_input:
                st.session_state["messages"].append(("user", user_input))
                with st.chat_message("user"):
                    st.write(user_input)

                system_prompt = (f"""
                    너는 친절하고 정확한 LLM 튜터이며, 사용자의 회의 음성 내용을
                    바탕으로 질문에 성실히 답변해
                    다음은 참고해야 음성 분석 내용
                    음성 대화 전체 내용: {data}
                    음성 대화 내용 요약: {res1}
                    요청사항 정리: {res2}
                    요청사항 요약 및 미비사항: {res3}
                    준비해야 할 사항: {res4}
                    반드시 이 정보를  참고하여 사용자의 질문에 답변
                """)

                # ChatGPT 응답 생성
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[
                            {"role": role, "content": content}
                            for role, content in st.session_state["messages"]
                        ],
                    ],
                )

                assistant_reply = response.choices[0].message.content
                st.session_state["messages"].append(("assistant", assistant_reply))

                with st.chat_message("assistant"):
                    st.write(assistant_reply)


if __name__ == "__main__":
    main()
