from openai import OpenAI

def ask_withKG(logger, query, KG_info, api_key):


    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    add_info = ';'.join(KG_info)
    prompt = f"我的问题是：{query}，关于问题的额外有效信息是：{add_info}"
    logger.info(f"prompt:{prompt}")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个严谨的医生，我将问你一些问题并同时给你一些参考信息，你需要严谨认真地回答问题，如果问题超过你的能力范畴请拒绝回答，而不是编造答案"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    logger.info(response.choices[0].message.content)