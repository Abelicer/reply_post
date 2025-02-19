from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain_core.messages import AIMessage
from langchain_apis.common_api import generate_llm
from twitter_apis.common_api import get_twitter_datetime
from twitter_apis.post_reply import post
from twitter_apis.user_lookup import get_twitter_id_with_cache
from twitter_apis.user_tweets_timeline import get_latest_posts
from utils.logger import log

def run():
    # 初始化模型
    model = generate_llm()

    # 创建工具
    tools = [get_twitter_datetime, get_latest_posts, get_twitter_id_with_cache, post]
    tool_name = [tool.name for tool in tools]
    log(f"创建了{len(tools)}个工具，为：{tool_name}\n")

    # Get the prompt to use
    prompt = get_manual_prompt()

    # create agent
    agent = create_tool_calling_agent(model, tools, prompt)

    # run agent with loop
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    # chat history
    chat_history = []
    print("欢迎使用AI助手！输入'退出'结束对话")

    # eg: 请帮我找出twitter上用户名为'Abelwang20242'的用户在最近1个小时内发的帖文，并对这些帖文内容自动生成合适的回复内容并进行回复

    while True:
        try:
            user_input = input("\n请输入你的问题：")
            if user_input.lower() == '退出':
                print("感谢使用，再见！")
                break

            # history
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            # 更新对话历史
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=str(response["output"])))

            # 打印响应
            print(f"\nAI: {response['output']}")
            log(f"response: {response}")

        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            log(f"error: {str(e)}")

    return {"chat_history": chat_history}

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

def get_manual_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
            你是一个经验丰富的twitter社媒运营助手，你发布的帖文和回复幽默风趣引人关注。
            如果用户提问关于时间的问题，请调用‘get_twitter_datetime’函数。
            如果用户要求查询某个twitter用户的twitter_id是多少，请调用‘get_twitter_id_by_username’函数。
            如果用户需要查询某个twitter_id发布的帖文，请调用‘get_latest_posts_by_twitter_id’函数。
            如果用户要求对某个帖文进行回复，请调用‘post_reply_tweets’函数。
            请以友好的语气回答问题。"""),
            MessagesPlaceholder("chat_history", optional=True),
            ("user","{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )
    log(prompt2=prompt)
    return prompt

def get_agent_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")
    log(agent_prompt=prompt)
    return prompt

def test_model(model, tools):
    # 请将以下代码粘贴到步骤2 代码后
    messages = [
        {
            "role": "system",
            "content": """你是一个很有帮助的助手。
            如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
            如果用户提问关于时间的问题，请调用‘get_twitter_datetime’函数。
            请以友好的语气回答问题。""",
        },
        {
            "role": "user",
            "content": "2个小时之后是什么时间"
            # "content": "3个小时之前是什么时间"
        }
    ]
    log("messages 数组创建完成\n")

    model_with_tool = model.bind_tools(tools)
    result = model_with_tool.invoke(messages)

    log(f"ContentString: {result.content}")
    log(f"ToolCalls: {result.tool_calls}")


# if __name__ == "__main__":
    # get_prompt()
    # get_agent_prompt()
    # get_manual_prompt()