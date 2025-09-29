import streamlit as st
from openai import OpenAI
from datetime import datetime

# OpenAI 클라이언트 초기화 (Secrets에서 API 키 가져오기)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
"""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "안녕! 나는 달박사 루나야! 🌙\n\n친구야, 나와 함께 달을 탐험해볼까?"},
    ]

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# 사이드바: 학생 정보
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

# 사용자 입력 처리
if prompt := st.chat_input("달에 대해 궁금한 것을 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

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
                st.error("미안해! 지금 답변하기 힘들어. 다시 시도해줄래?")
                st.error(f"Error: {e}")

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

# 대화 초기화
st.markdown("---")
if st.button("🔄 새로운 대화 시작", type="secondary", use_container_width=True):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "안녕! 다시 만나서 반가워! 🌙\n\n새로운 달 탐험을 시작해볼까? 오늘은 어떤 달 이야기가 궁금해?"},
    ]
    st.experimental_rerun()
