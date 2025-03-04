'''
Author: Li, Hang
Date: 2025-03-03 00:28:36
LastEditors: Li, Hang
FilePath: /blank-app/test.py
'''
# coding=utf-8

from openai import OpenAI

base_url = "https://maas-cn-southwest-2.modelarts-maas.com/deepseek-r1/v1" # API地址
api_key = "Tn2DLZwhGm1OAxMC74mOg4gR6v1N9y02h4rbKYfzY9kSVzyzVAXwdnTc3ljHjqUD08BzSfk5I_ErESGwfGrNDA" # 把yourApiKey替换成已获取的API Key

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model = "DeepSeek-R1", # 模型名称
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你好"},
    ],
    max_tokens = 1024,
    temperature = 1,
    stream = False
)

print(response.choices[0].message.content)
