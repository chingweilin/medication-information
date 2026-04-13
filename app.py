import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="一般民眾用藥習慣調查", page_icon="💊")

# --- 2. 建立連線 (直接指定網址，確保路徑正確) ---
# 這是你剛才提供的試算表網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1MkdJGPHdAJC9fK5ufExy3UJlj-yvsZeXYEjcjXqWjVQ/edit"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. 初始化問卷狀態 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 問卷題目內容
questions = [
    {"q": "您的年齡層是？", "opts": ["20歲以下", "20-40歲", "41-60歲", "61歲以上"]},
    {"q": "您目前是否有長期服用慢性病藥物？", "opts": ["是", "否"]},
    {"q": "藥瓶內的棉花和乾燥劑，開瓶後應該...", "opts": ["繼續留在瓶子裡", "立刻丟掉"]},
    {"q": "忘記吃藥時，下次吃藥可以吃兩倍劑量嗎？", "opts": ["可以", "不可以"]},
    {"q": "過期的感冒藥水，可以直接沖入馬桶嗎？", "opts": ["可以", "不可以"]},
    {"q": "當症狀好轉，您會自行停藥嗎？", "opts": ["從不", "偶爾", "經常", "總是"]},
    {"q": "您會定期檢查家中藥櫃並清理過期藥嗎？", "opts": ["從不", "偶爾", "經常", "總是"]}
]

# --- 4. 問卷介面邏輯 ---
if st.session_state.step < len(questions):
    # 顯示進度
    progress_value = st.session_state.step / len(questions)
    st.progress(progress_value)
    st.write(f"進度：{st.session_state.step + 1} / {len(questions)}")
    
    current_q = questions[st.session_state.step]
    st.markdown(f"### {current_q['q']}")
    
    # 選項按鈕
    for opt in current_q['opts']:
        if st.button(opt, use_container_width=True):
            st.session_state.answers.append(opt)
            st.session_state.step += 1
            st.rerun()

# --- 5. 填寫完成與資料寫入 ---
else:
    st.balloons()
    st.success("🎉 感謝填寫！資料正在同步至雲端試算表...")
    
    try:
        # 讀取現有資料 (明確指定網址)
        existing_data = conn.read(spreadsheet=SHEET_URL)
        
        # 準備標題與新資料
        columns = ["年齡", "慢性病", "乾燥劑", "兩倍劑量", "回收認知", "自行停藥", "清理頻率"]
        new_row = pd.DataFrame([st.session_state.answers], columns=columns)
        
        # 合併資料
        if existing_data.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # 寫回 Google Sheets
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        st.info("✅ 雲端同步完成！")
        
    except Exception as e:
        st.error(f"儲存時發生錯誤：{e}")
        st.warning("請確認您已在 Secrets 填寫連線設定，並將 s-connection@streamlit.io 設為編輯者。")

    if st.button("重新填寫問卷"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
