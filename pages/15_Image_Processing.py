
import streamlit as st
import anthropic
import ollama as ol
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import datetime
import json

def log_interaction(action, data):
    timestamp = datetime.datetime.now().isoformat()
    log = {"timestamp": timestamp, "action": action, "data": data}
    with open("user_interactions_log.json", "a") as logfile:
        logfile.write(json.dumps(log) + "\n")

def print_txt(text):
    if any("\u0600" <= c <= "\u06FF" for c in text):  # check if text contains Arabic characters
        text = f"<p style='direction: rtl; text-align: right;'>{text}</p>"
    st.markdown(text, unsafe_allow_html=True)

def print_chat_message(message):
    text = message["content"]
    if message["role"] == "user":
        with st.chat_message("user", avatar="🎙️"):
            print_txt(text)
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🦙"):
            print_txt(text)

def get_chat_history(key):
    return st.session_state.chat_history[key]

def init_chat_history(key, system_prompt):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if key not in st.session_state.chat_history:
        st.session_state.chat_history[key] = [{"role": "system", "content": system_prompt}]

def system_prompt_input(default_prompt):
    return st.sidebar.text_area("System Prompt", value=default_prompt, height=100)

def llm_selector():
    ollama_models = [m['name'] for m in ol.list()['models']]
    with st.sidebar:
        return st.selectbox("LLM", ollama_models)




# 设置页面标题和图标
st.set_page_config(page_title="图像处理", page_icon="🖼️")

st.title("🖼️ 图像处理")
uploaded_file = st.file_uploader("上传图像", type=("png"))

model = llm_selector()
chat_key = f"对话_chat_history_{model}"  # Unique key for each mode and model
default_prompt = ("我现在将要给你传送一张图片，你需要识别图像中的文字然后给我发送处理后的文本（关键词、短语等）。")

system_prompt = system_prompt_input(default_prompt)
init_chat_history(chat_key, system_prompt)
chat_history = get_chat_history(chat_key)

debug_mode = st.sidebar.checkbox("Debug Mode", value=True)

# 创建两列布局，左边显示用户输入，右边显示模型输出
user_input_col, model_output_col = st.columns(2)

# 用户输入列
with user_input_col:
    question = st.text_area("用户输入")
    if st.button("提交"):
        log_interaction("User input", {"mode": "对话", "question": question})

        if question:
            user_message = {"role": "user", "content": question}
            print_chat_message(user_message)
            chat_history.append(user_message)

            if uploaded_file:
                article = uploaded_file.read().decode('utf-8', 'ignore')
                chat_history.append({"role": "user", "content": article})

            response = ol.chat(model=model, messages=chat_history)
            answer = response['message']['content']

            # 模型输出列
            with model_output_col:
                ai_message = {"role": "assistant", "content": answer}
                print_chat_message(ai_message)
                chat_history.append(ai_message)

                debug_info = {"messages": chat_history, "response": response}

                if debug_mode:
                    st.write("Debug Info: Complete Prompt Interaction")
                    st.json(debug_info)

                if len(chat_history) > 20:
                    chat_history = chat_history[-20:]


                st.session_state.chat_history[chat_key] = chat_history
