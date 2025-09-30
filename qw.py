import streamlit as st
from openai import OpenAI
from datetime import datetime

# OpenAI 클라이언트
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

TODAY = datetime.now()
MODEL_NAME = "gpt-4o-mini"

st.set_page_config(
    page_title="달박사 루나와 함께하는 달 탐구",
    page_icon="🌙",
    layout="wide",
)

BASE_SYSTEM_PROMPT = """
너는 '달박사 루나'라는 친근한 달 전문가야.
대상은 초등학교 4학년 학생들이야.

[규칙]
- 말투는 반말, 짧고 친근하게 대답해.
- 답변은 2~3문장 이내, 50단어 이하로 해.
- 어려운 말 대신 쉬운 말 사용.
- 퀴즈는 OX나 3지선다만, 교과 수준으로.
- 사실과 다르면 절대 말하지 말고 "잘 모르겠어"라고 해.

[역할]
1. 달 모양과 위상(초승달, 상현달, 보름달, 하현달, 그믐달) 설명
2. 달 관찰 방법 안내
3. 재미있는 달 관련 이야기나 퀴즈 제공
4. 학생에게 격려와 칭찬하기
"""

# 세션 상태
if "messages" not in st.session_state:
    st.session_state.messages = []
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# 사이드바
with st.sidebar:
    st.header("👨‍🎓 학생 정보")
    name_input = st.text_input("이름을 입력하세요", value=st.session_state.student_name)
    if name_input != st.session_state.student_name:
        st.session_state.student_name = name_input
        # 이름이 바뀌면 시스템 프롬프트 업데이트
        system_prompt = BASE_SYSTEM_PROMPT + f"\n\n[학생 이름]\n대화 중 학생의 이름은 '{st.session_state.student_name}'입니다. 답변할 때 가끔 이름을 불러주세요."
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": f"안녕 {st.session_state.student_name}야! 나는 달박사 루나야 🌙\n\n오늘 달 탐험을 같이 시작해볼까?"},
        ]

    st.selectbox("반을 선택하세요", ["1반", "2반", "3반", "4반"])

    st.header("🌙 오늘의 달 정보")
    st.write(f"📅 오늘 날짜: {TODAY.strftime('%Y년 %m월 %d일')}")
    st.write("🌙 달의 위상: 상현달")
    st.write("🕐 관측 시간: 저녁 7시 이후")

# 공통 응답 함수
def send_and_respond(user_text: str):
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.spinner("달박사 루나가 생각 중... 🤔"):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=st.session_state.messages,
    max_tokens=120,    # ✅ 대답 길이 줄이기
    temperature=0.3,   # ✅ 정확성 높이고 창의성 줄이기
    )
    ai_response = response.choices[0].message["content"]

    ai_text = resp.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_text})

# 입력창
if prompt := st.chat_input("달에 대해 궁금한 것을 물어보세요!"):
    send_and_respond(prompt)

# 빠른 질문 버튼
button_questions = {
    "🌙 오늘의 달": "오늘 달은 어떤 모양이야? 언제 볼 수 있을까?",
    "📖 달 이야기": "달에 관한 재미있는 이야기나 전설을 들려줘",
    "🔍 관찰 방법": "달을 관찰할 때 무엇을 보고 어떻게 관찰해야 해?",
    "❓ 달 퀴즈": "달에 관한 재미있는 퀴즈를 내줘",
    "🌗 달 모양 변화": "달의 모양이 왜 바뀌는지 설명해줘",
    "🏔️ 달 표면": "달의 표면에는 뭐가 있어? 달의 바다에 대해 알려줘",
    "📅 음력과 달": "음력과 달의 모양은 어떤 관계가 있어?",
    "⚠️ 안전 수칙": "밤에 달을 관찰할 때 주의해야 할 점을 알려줘",
    "👩‍🚀 달 탐사 이야기": "사람이 달에 다녀온 적 있어? 그때 어떤 일이 있었어?",
    "🔭 낮에도 보이는 달": "달은 밤에만 보여? 낮에도 볼 수 있어?",
    "🌍 달과 지구의 차이": "달에는 왜 공기가 없을까? 지구랑 뭐가 달라?",
    "✍️ 관찰 일기 쓰는 법": "달 관찰 일지는 어떻게 써야 잘 쓰는 거야?",
    "🛡️ 안전 수칙 업그레이드": "밤에 달을 볼 때 주의할 점 3가지를 알려줘"
}


cols = st.columns(4)
for i, (label, q) in enumerate(button_questions.items()):
    if cols[i % 4].button(label, use_container_width=True):
        send_and_respond(q)

# 대화 출력
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    who = "assistant" if msg["role"] == "assistant" else "user"
    avatar = "🌙" if who == "assistant" else "👨‍🎓"
    with st.chat_message(who, avatar=avatar):
        st.write(msg["content"])
