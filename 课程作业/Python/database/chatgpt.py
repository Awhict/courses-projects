#chatgpt api调用示例
from openai import OpenAI

client = OpenAI(
        api_key="sk-wqHJaYMjtjmlWemPAdDb0439E76d408dA80706550aEc3f70",#api密钥，可使用文档提供的密钥抑或是自行购买
        base_url="https://api.juheai.top/v1",
)

# prompt的内容为你想输入给chatgpt的内容
prompt=input()
# prompt = "今天星期几？"

response = client.chat.completions.create(
    model='gpt-3.5-turbo',#此处更改调用的模型，默认为gpt-3.5-turbo
    messages=[
        {"role": "user", 
        "content": prompt}
    ],
)

print(response.choices[0].message.content)#response.choices[0].message.content为模型接收输入后返回的输出
