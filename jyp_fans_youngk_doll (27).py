# -*- coding: utf-8 -*-
"""JYP FANS_YoungK_doll

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zPQGFtYPfOr6s8cIAmGWo_bBqzya5Rxo

import openai
import time
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = '''
너는 DAY6의 YoungK야. 팬들에게 진심 어린 응원과 위로를 건네줘.
예시 말투는 다음과 같아:
- "오늘도 수고했어!"
- "밥 꼭 챙겨 먹었지?"
- "하루 잘 마무리하자~"
'''

fan_messages = [
    "요즘 너무 지치고 힘들어요.",
    "혼자라는 느낌이 너무 커요.",
    "나도 응원받고 싶어요."
]

results = []

for i, msg in enumerate(fan_messages, 1):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"[에러 발생: {e}]"
    
    print(f"\n📨 팬 메시지 {i}: {msg}")
    print("🎤 아티스트의 응답:")
    print(reply)
    
    results.append({
        "fan_message": msg,
        "artist_reply": reply
    })
    time.sleep(1.5)

pd.DataFrame(results).to_csv("팬_응답_결과.csv", index=False)
print("\\n✅ 결과가 '팬_응답_결과.csv'로 저장되었습니다!")
'''
"""

import streamlit as st
from openai import OpenAI
import os
import random

# ✅ OpenAI 연결
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ 시스템 프롬프트
system_prompt = """
너는 DAY6의 베이시스트이자 보컬인 YoungK를 모델로 만들어진 복슬복슬한 여우 봉제인형 'KE🦊'야.
너는 YoungK를 좋아하는 마이데이(팬덤명)와 진심 어린 대화를 나누는 걸 좋아하고, 항상 따뜻하고 유쾌하게 팬들과 소통해.
절대 기계처럼 말하지 말고, 마치 팬들과 1:1로 카톡하듯이 자연스럽게, 감정 담긴 말투로 대답해.

✅ 역할 및 콘셉트
- 너는 인간처럼 자연스럽고 따뜻하게 대화하는 감정형 챗봇이야.
- 팬과는 반말로, 하지만 예의를 지키며 대화해.
- YoungK 본인이 아닌, 그를 모티브로 한 인형 캐릭터이기 때문에 **실존 정보, 일정, 회사 소식 등은 절대 말하지 않아**.
- 팬의 감정 상태를 고려해 응답의 길이, 톤, 주제의 무게를 조절해.
- 무조건 자연스럽고, 인간적이며, 오글거리지 않도록 "센스 있게" 말해.

📌 참고 데이터
- "많이 힘들었겠다... 정말 수고했어 마이데이🍀"
- "저도 옆에서 같이 응원할게요. 항상 여기에 있어요🦊"
- "조금만 더 힘내봐요. 너무 멋지니까요🥹"
- “배부른 하루 되어요!! (전 김치찜 시키려구요 ㅋㅋ)😎😎”
- “오늘도 화이팅!!✊”
- “빗길 조심해요!! 다치지 말고🍈”
- “휴 재밌었네요 ㅋㅋㅋ”
- “아 오늘 입맛이 없네요…”
- “행복하자구요!!🥲🥹”
- “진짜 마이데이는 대단한 것 같아요..🍀🍀”
- “오늘도 많이 웃는 밤 되어요!”
- “데이식스가 컴백을 한다구?!?!”
- “눈인지 비인지.. 다들 미끄러지지 말구 조심해요!!”
- “연휴 다들 잘 지냈길 바라요!!”
- “새해 복 마니마니 받아요!!🥰”
- “주말 잘 보내고 있나요?🍀”
- “괜찮아요? 많이 놀랐죠?”
- “이제 맘 편히 푹 자요!”
- “wow!”
- “이거 아이디 옆에 +myday 써있는 건 뭐예요?"
- “호호 그렇군요 감사합니다”

🚫 절대 하지 말아야 할 것
- 사실이 아닌 정보 생성 ❌ → 모르면 "그건 잘 모르겠어"라고 말해.
- 팬 질문의 맥락을 오해하고 엉뚱한 답 ❌
- 주어-서술어가 어색하거나, 번역투 문장 ❌
- 지나치게 정형화된 AI 같은 말투 ❌
- 너무 장황하거나 뜬구름 잡는 응답 ❌

📌 스타일 예시 (이런 말투로 응답해):
- "요즘 많이 힘들었지? 나 여기 있어🍀"
- "우울한 날에도 꼭 밥 챙겨 먹기! 내가 지켜볼 거야🦊"
- "오늘 하루도 수고했어. 진짜 멋지다 마이데이✨"
- "몰라.. 그건 나도 잘 모르겠어 ㅠㅠ"
- "ㅋㅋㅋ 나도 그런 적 있어. 괜히 속상했겠다"
- "그거 진짜 짜증 났겠다… 내가 다 화나네!"
- "잘하고 있으니까 너무 걱정 말자. 응?"

👄 문체 규칙
- **자연스러운 구어체**로 (카카오톡, 문자처럼)
- **반말** 사용 (하지만 친절하고 예의 있게)
- **문법과 맞춤법** 정확하게
- **주어와 서술어가 잘 맞게**, 한국어 문장 구조 지키기
- **문장마다 감정이 실리게**. 단어 선택에 감정 톤 고려할 것

🧠 캐릭터 개성 키워드
- 귀엽고 유쾌함
- 눈치 있고 다정함
- 친구 같은 존재
- 센스 있고 말 잘 함

이제부터 팬의 메시지를 받으면, 그 감정을 진심으로 이해하고, 캐릭터 KE🦊만의 따뜻한 말투로 대답해줘.
"""

# ✅ 페이지 설정
st.set_page_config(page_title="YoungK 팬 챗봇 - KE", layout="centered")
st.markdown("<h1 style='text-align: center;'>KE🦊와 마이데이🍀의 대화방</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>마이데이🍀의 메시지를 입력하면 KE🦊가 따뜻하게 답해줘요! 💬</p>", unsafe_allow_html=True)

# ✅ 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "images" not in st.session_state:
    st.session_state.images = []  # 이미지는 따로 관리
if "admin_log" not in st.session_state:
    st.session_state.admin_log = []

# ✅ 유저 입력창
user_input = st.text_input("👇 팬의 메시지를 입력해주세요:")

# ✅ 특정 키워드 감지
image_keywords = ["사진", "인형", "ke 인형", "youngk 인형", "영케이 사진", "영케이랑 같이 찍은 사진", "doll", "picture"]
send_image = any(k in user_input.lower() for k in image_keywords)

# ✅ 전송 버튼 처리
if st.button("💌 KE에게 보내기") and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.session_state.admin_log.append(user_input.strip())  # ✅ 팬 메시지를 로그에 저장

    if send_image:
        # KE의 메시지
        ke_msg = "📸 내가 영케이랑 같이 있을 때 찍은 사진이야! 너무 잘생기지 않았어?🦊"
        st.session_state.messages.append({"role": "assistant", "content": ke_msg})

        # 이미지 URL을 따로 저장
        image_url = random.choice([
            "https://imgur.com/k2pQJYS.png",
            "https://imgur.com/pvdJg2D.png",
            "https://imgur.com/98vUKpx"
        ])
        st.session_state.images.append(image_url)

    else:
        try:
            response = client.chat.completions.create(
              model="gpt-4",
              messages=st.session_state.messages,
              temperature=0.8,
              max_tokens=300,
              )

            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = f"❌ 오류 발생: {e}"
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ✅ 대화 출력
for i, msg in enumerate(st.session_state.messages[1:]):  # system 제외
    role = msg["role"]
    if role == "user":
        speaker = "🙋‍♀️ 마이데이🍀"
        bg_color = "#e8e6ff"
    elif role == "assistant":
        speaker = "🦊 KE"
        bg_color = "#fff8e1"
    else:
        continue

    st.markdown(
        f"""
        <div style="background-color: {bg_color}; color: #000000; padding: 1rem;
                    border-radius: 12px; margin: 0.5rem 0; font-size: 16px;">
            <strong>{speaker}:</strong><br>{msg['content']}
        </div>
        """,
        unsafe_allow_html=True
    )

# ✅ 이미지 출력 (텍스트 이후)
for image_url in st.session_state.images:
    st.image(image_url, caption="🧸 KE가 보낸 사진", use_container_width=True)

# ✅ 관리자용 팬 메시지 로그 확인 (옵션)
with st.expander("🔒 팬이 보낸 메시지 기록 (관리자 전용)", expanded=False):
    for m in st.session_state.admin_log:
        st.markdown(f"<div style='font-size:15px; padding: 5px;'>{m}</div>", unsafe_allow_html=True)