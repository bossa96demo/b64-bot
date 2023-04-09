"""
Simple Bot to transfer into base64 and back
"""

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (Application, CommandHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler)
import base64
from uuid import uuid4
# you type /decode with a reply, he will decode and send to your pm decoded message
# also he will delete message with "/decode"
async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = update.message.reply_to_message
    user_id = update.message.from_user.id
    message = reply.text
    chat_id = reply.chat.id
    msg_id  = update.message.message_id
    decoded_string = base64.b64decode(message).decode('utf-8')
    await context.bot.send_message(chat_id=user_id, text=decoded_string) 
    await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)

# inline support should be turned on
# you just type @name_of_bot test
# you press encode and you will get encoded message
async def encode(update, context):
    query = update.inline_query.query
    if query == "":
        return
    enc = base64.b64encode(query.encode('utf-8')).decode('utf-8')
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Encode",
            input_message_content=InputTextMessageContent(enc))
            ]
    await update.inline_query.answer(results)

with open('token') as f:
    TOKEN = f.read().strip()

def main():
    print("(i) Bot was started (i)")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("decode", decode))
    application.add_handler(InlineQueryHandler(encode))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
