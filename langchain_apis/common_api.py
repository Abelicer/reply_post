from langchain_openai import ChatOpenAI
import os

def generate_llm():
    chat_llm = ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"
    )
    return chat_llm
