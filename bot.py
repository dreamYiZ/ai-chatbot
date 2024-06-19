from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import json
import os

def say(user_message, model="llama3"):
    prompt = f'你是一个高级心理学咨询师，{user_message}。请用中文回答。'
    data = {
        "model": model,
        "prompt": prompt,
    }

    url = "http://localhost:11434/api/generate"

    # 发送POST请求
    response = requests.post(url, data=json.dumps(data))

    response_texts = response.text.split("\n")

    # 解析每个JSON对象
    response_jsons = [
        json.loads(response_text) for response_text in response_texts if response_text
    ]

    output_str = ""
    # 打印返回的数据
    for response_json in response_jsons:
        output_str += response_json["response"]

    return output_str

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = say(user_message)
    await update.message.reply_text(response)

# 从环境变量中读取 Telegram 机器人的 token
token = os.getenv("TELEGRAM_BOT_TOKEN")

app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.run_polling()
