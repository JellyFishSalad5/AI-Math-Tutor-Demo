import streamlit as st
from dotenv import load_dotenv
import os
from zai import ZhipuAiClient

# Load .env file 加载环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Get API Key and initialize client 获取 API Key 并初始化客户端
api_key = os.getenv("ZAI_API_KEY")
client = ZhipuAiClient(api_key=api_key)

# Debug: check if API key is loaded 调试：确认 API Key 是否读取
st.write("DEBUG: ZAI API Key =", "已读取" if api_key else "未读取")

# Streamlit page setup Streamlit 页面设置
st.title("AI 数学助教 Demo (GLM-4.5-Flash)")
mode = st.radio("选择模式:", ["模式 A: 直接解答", "模式 B: 解答 + 总结"])
user_question = st.text_area("输入你的数学题或问题:")

# Function to call ZhipuAiClient 调用 ZhipuAiClient 的函数
def ask_zhipu(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="glm-4.5-flash",
        messages=messages,
        thinking={"type": "enabled"},  # Enable deep thinking mode 启用深度思考模式
        stream=True,                   # Enable streaming output 流式输出
        max_tokens=4096,
        temperature=0.7
    )
    output_text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            output_text += chunk.choices[0].delta.content
    return output_text

# Submit button logic 提交按钮逻辑
if st.button("提交"):
    if not user_question.strip():
        st.warning("请输入题目！")
    else:
        prompt = f"请直接解答以下数学问题：\n{user_question}" if mode == "模式 A: 直接解答" else f"请解答以下数学问题，并给出最终总结说明：\n{user_question}"
        try:
            answer = ask_zhipu(prompt)
            st.success("回答生成成功：")
            st.write(answer)
        except Exception as e:
            st.error(f"请求失败: {e}")
