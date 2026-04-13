import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# --- 頁面設定 ---
st.set_page_config(page_title="民眾用藥習慣調查", page_icon="💊", layout="centered")

# --- 自定義 CSS (讓介面更像 Netlify 範例) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3em;
        font-size: 1.2rem;
        transition: all 0.3s;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .question-text {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #2E4053;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 問卷題目邏輯 ---
questions = [
    {"q": "您的年齡層是？", "options": ["20歲以下", "20-40歲", "41-60歲", "61歲以上"]},
    {"q": "您目前是否有長期服用慢性病藥物？", "options": ["是", "否"]},
    {"q": "藥瓶內的棉花和乾燥劑，開瓶後應該...", "options": ["繼續留在瓶子裡", "立刻丟掉"]},
    {"q": "忘記吃藥時，下次吃藥可以吃兩倍劑量嗎？", "options": ["可以", "不可以"]},
    {"q": "過期的感冒藥水，可以直接沖入馬桶嗎？", "options": ["可以", "不可以"]},
    {"q": "當症狀好轉，您會自行停藥嗎？", "options": ["從不", "偶爾", "經常", "總是"]},
    {"q": "對於家中不需要的藥，您通常怎麼處理？", "options": ["直接丟垃圾桶", "送回藥局", "藥物回收六步驟"]},
]

# --- 初始化 Session State (紀錄進度) ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# --- 介面呈現 ---
num_questions = len(questions)
progress = st.session_state.step / num_questions

if st.session_state.step < num_questions:
    # 顯示進度條
    st.progress(progress)
    st.write(f"問題 {st.session_state.step + 1} / {num_questions}")
    
    current_q = questions[st.session_state.step]
    
    # 顯示問題標題
    st.markdown(f"<p class='question-text'>{current_q['q']}</p>", unsafe_allow_html=True)
    
    # 使用按鈕選擇答案 (點擊即跳下一題)
    for option in current_q['options']:
        if st.button(option):
            st.session_state.answers.append(option)
            st.session_state.step += 1
            st.rerun()

else:
    # --- 填寫完成畫面 ---
    st.balloons()
    st.success("🎉 感謝您的填寫！您的回覆已成功記錄。")
    st.markdown("### 您的用藥認知小回饋：")
    
    # 這裡可以根據回答顯示衛教資訊
    if st.session_state.answers[2] == "繼續留在瓶子裡":
        st.warning("💡 小提醒：乾燥劑開瓶後會吸濕，建議丟掉以免滋生細菌喔！")
    else:
        st.info("✅ 專業！開瓶後丟棄棉花與乾燥劑是正確的。")

    if st.button("重新填寫"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
