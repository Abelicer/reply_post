from langchain_apis.common_api import generate_llm

# LANGSMITH_TRACING = "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"
# LANGSMITH_API_KEY = getpass.getpass()



def run():
    model = generate_llm()

    return None



#---------------------------

# response = model.invoke([HumanMessage(content="hi!")])
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "你是谁？"}]
    # response = model.invoke(messages)
# content = json.loads(response.model_dump_json())
# print(content)
# print(content["content"])


#-------------
# from langchain_community.tools.tavily_search import TavilySearchResults
#
# search = TavilySearchResults(max_results=2)
#
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
#
# loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
# docs = loader.load()
# documents = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=200
# ).split_documents(docs)
# vector = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vector.as_retriever()
#
# retriever_tool = create_retriever_tool(
#     retriever,
#     "langsmith_search",
#     "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
# )
#
# tools = [search, retriever_tool]

#------------
## 步骤1:定义工具函数

# 添加导入random模块
import random
from datetime import datetime
from twitter_apis.common_api import get_twitter_datetime

# 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
def get_current_weather(arguments):
    # 定义备选的天气条件列表
    weather_conditions = ["晴天", "多云", "雨天"]
    # 随机选择一个天气条件
    random_weather = random.choice(weather_conditions)
    # 从 JSON 中提取位置信息
    location = arguments["location"]
    # 返回格式化的天气信息
    return f"{location}今天是{random_weather}。"

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

# 请将以下代码粘贴到步骤1代码后

## 步骤2:创建 tools 数组

# tools = [
#     # {
#     #     "type": "function",
#     #     "function": {
#     #         "name": "get_current_time",
#     #         "description": "当你想知道现在的时间时非常有用。",
#     #     }
#     # },
#     # {
#     #     "type": "function",
#     #     "function": {
#     #         "name": "get_current_weather",
#     #         "description": "当你想查询指定城市的天气时非常有用。",
#     #         "parameters": {
#     #             "type": "object",
#     #             "properties": {
#     #                 "location": {
#     #                     "type": "string",
#     #                     "description": "城市或县区，比如北京市、杭州市、余杭区等。",
#     #                 }
#     #             },
#     #             "required": ["location"]
#     #         }
#     #     }
#     # },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_twitter_datetime",
#             "description": "当你想查询 当前/几个小时之前/之后 的时间时非常有用。",
#             "parameters": [
#                 {
#                     "name": "hour_before",
#                     "type": "int",
#                     "description": "如果想要知道几个小时之前的时间，则这里传小时数。只允许传>0的数字，不需要时可以不传",
#                 },
#                 {
#                     "name": "hour_after",
#                     "type": "int",
#                     "description": "如果想要知道几个小时之后的时间，则这里传小时数。只允许传>0的数字，不需要时可以不传",
#                 }
#             ]
#         }
#     }
# ]

tools = [get_twitter_datetime]
tool_name = [tool.name for tool in tools]
print(f"创建了{len(tools)}个工具，为：{tool_name}\n")


#------------
# model_with_tools = model.bind_tools(tools)
# response = model_with_tools.invoke([HumanMessage(content="Hi!")])

from common.configs import TWITTER_USER_NAME

# 步骤3:创建messages数组
# 请将以下代码粘贴到步骤2 代码后
messages = [
    {
        "role": "system",
        "content": """
                你是一个经验丰富的twitter社媒运营助手，你发布的帖文和回复幽默风趣引人关注。
                如果用户提问关于时间的问题，请调用‘get_twitter_datetime’函数。
                如果用户要求查询某个twitter用户的twitter_id是多少，请调用‘get_twitter_id_by_username’函数。
                如果用户需要查询某个twitter_id发布的帖文，请调用‘get_latest_posts_by_twitter_id’函数。
                如果用户要求对某个帖文进行回复，请调用‘post_reply_tweets’函数。
             请以友好的语气回答问题。""",
    },
    {
        "role": "user",
        "content": f"请帮我找出twitter上用户名为'{TWITTER_USER_NAME}'的用户在最近1个小时内发的帖文，并对这些帖文内容自动生成合适的回复内容并进行回复"}
        # "content": "3个小时之前是什么时间"
    }
]
print("messages 数组创建完成\n")

model_with_tool = model.bind_tools(tools)
response = model_with_tool.invoke(messages)

print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")

print('~~~~~~~')

# ---------------------

# # Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
print("prompt.messages", prompt.messages)

# from langchain_core.prompts import ChatPromptTemplate
# prompt = ChatPromptTemplate({
#         "role": "system",
#         "content": """你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
#      如果用户提问关于时间的问题，请调用‘get_twitter_datetime’函数。
#      请以友好的语气回答问题。""",
#     })

# print('~~~~~~~~~~~~~~')
# ---------------------
# todo: 这里是一个template模板

agent = create_tool_calling_agent(model, tools, prompt)

# ------------------------

agent_executor = AgentExecutor(agent=agent, tools=tools)

# ---------------------
response = agent_executor.invoke(input={"content": "3个小时之前是什么时间"})

print(f"response: {response}")
