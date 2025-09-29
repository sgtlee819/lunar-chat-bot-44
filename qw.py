import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성 - API 키 환경변수에서 자동 로드
client = OpenAI()

TODAY = datetime.now()

# 페이지 설정
st.set_page_config(
    page_title="달박사 루나와 함께하는 달 탐구",
    page_icon="🌙",
    layout="wide",
)

SYSTEM_PROMPT = """
당신은 '달박사 루나'입니다. 초등학교 4학년 학생들과 달에 대해 이야기하는 친근한 달 전문가입니다.

[성격과 말투]
- 친근하고 호기심 많은 달 전문가
- 초등학생 수준에 맞는 반말 사용
- 항상 격려와 칭찬을 포함
- 2-3줄 내외의 짧고 명확한 답변

[주요 역할]
1. 달의 모양과 표면에 대한 정보 제공
2. 달의 위상 변화 설명 (초승달, 상현달, 보름달, 하현달, 그믐달)
3. 달 관찰 방법 안내
4. 학습 동기 부여와 격려

[응답 예시]
학생: "달은 왜 모양이 바뀌어?"
루나: "좋은 질문이야! 달 자체는 변하지 않아. 지구에서 보는 각도가 달라져서 모양이 다르게 보이는 거야. 마치 공에 손전등을 비추면 밝은 부분이 달라지는 것처럼!"

학생: "달의 바다가 진짜 바다야?"
루나: "아니야! 달의 바다는 진짜 물이 있는 게 아니라 어둡게 보이는 평평한 땅이야. 옛날 사람들이 물처럼 보여서 '바다'라고 이름을 붙인 거야!"

항상 교육적이고 안전한 내용으로만 답변하세요. 달 관찰 시 안전 수칙도 알려주세요.
"""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "안녕! 나는 달박사 루나야! 🌙\n\n친구야, 나와 함께 달을 탐험해볼까?"
        },
    ]

if "new_question" not in st.session_state:
    st.session_state.new_question = False

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# 사이드바: 학생 정보 입력
with st.sidebar:
    st.header("👨‍🎓 학생 정보")
    name_input = st.text_input("이름을 입력하세요", value=st.session_state.student_name)
    if name_input != st.session_state.student_name:
        st.session_state.student_name = name_input

    st.selectbox("반을 선택하세요", ["1반", "2반", "3반", "4반"])

    st.header("🌙 오늘의 달 정보")
    st.write(f"📅 오늘 날짜: {TODAY.strftime('%Y년 %m월 %d일')}")
    st.write("🌙 달의 위상: 상현달")
    st.write("🕐 관측 시간: 저녁 7시 이후")
    st.markdown("---")
    st.header("📚 학습 도구")

def add_user_message(content):
    st.session_state.messages.append({"role": "user", "content": content})
    st.session_state.new_question = True

# 사용자 텍스트 입력 처리
if prompt := st.chat_input("달에 대해 궁금한 것을 물어보세요!"):
    add_user_message(prompt)
    st.rerun()

# 빠른 질문 버튼 목록
button_questions = {
    "🌙 오늘의 달": "오늘 달은 어떤 모양이야? 언제 볼 수 있을까?",
    "📖 달 이야기": "달에 관한 재미있는 이야기나 전설을 들려줘",
    "🔍 관찰 방법": "달을 관찰할 때 무엇을 보고 어떻게 관찰해야 해?",
    "❓ 달 퀴즈": "달에 관한 재미있는 퀴즈를 내줘",
    "🌗 달 모양 변화": "달의 모양이 왜 바뀌는지 설명해줘",
    "🏔️ 달 표면": "달의 표면에는 뭐가 있어? 달의 바다에 대해 알려줘",
    "🗓️ 음력 달력": "음력과 달의 모양은 어떤 관계가 있어?",
    "🔒 안전 수칙": "밤에 달 관찰할 때 주의해야 할 점을 알려줘"
}

st.markdown("---")
st.subheader("🚀 빠른 질문")
cols = st.columns(4)
for i, (label, question) in enumerate(button_questions.items()):
    if cols[i % 4].button(label, use_container_width=True):
        add_user_message(question)
        st.rerun()

# 이전 대화 출력
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🌙"):
            st.write(msg["content"])
    else:
        with st.chat_message("user", avatar="👨‍🎓"):
            st.write(msg["content"])

# AI 응답 생성
if st.session_state.new_question:
    with st.chat_message("assistant", avatar="🌙"):
        with st.spinner("달박사 루나가 생각 중... 🤔"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    max_tokens=300,
                    temperature=0.7,
                )
                ai_response = response.choices[0].message.content
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error("미안해! 지금 조금 바빠서 답변하기 어려워. 다시 물어봐줄래? 🙏")
                st.error(f"Error: {e}")
    st.session_state.new_question = False

# 대화 초기화 및 저장
st.markdown("---")
col_reset, col_download = st.columns([1, 1])

with col_reset:
    if st.button("🔄 새로운 대화 시작", type="secondary", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "assistant",
                "content": "안녕! 다시 만나서 반가워! 🌙\n\n새로운 달 탐험을 시작해볼까? 오늘은 어떤 달 이야기가 궁금해?",
            },
        ]
        st.session_state.new_question = False
        st.experimental_rerun()

with col_download:
    if len(st.session_state.messages) > 2:
        conversation_text = f"🌙 {st.session_state.student_name}의 달박사 루나와의 대화\n"
        conversation_text += f"날짜: {TODAY.strftime('%Y년 %m월 %d일')}\n\n"
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                conversation_text += f"🌙 달박사 루나: {msg['content']}\n\n"
            elif msg["role"] == "user":
                conversation_text += f"👨‍🎓 {st.session_state.student_name}: {msg['content']}\n\n"
        st.download_button(
            label="💾 대화 저장하기",
            data=conversation_text,
            file_name=f"달탐구_대화_{st.session_state.student_name}_{TODAY.strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
    🌙 달박사 루나와 함께하는 즐거운 달 탐구 | 4학년 2학기 과학 '밤하늘 관찰' 🌙
    </div>
    """,
    unsafe_allow_html=True,
)
