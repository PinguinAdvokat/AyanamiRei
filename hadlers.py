import AiApi
import config
import json
from AiApi import chat
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


ro = Router(name=__name__)


@ro.message(F.text)
async def get_message(message: Message, bot):
    if message.chat.id == config.CHAT_ID:
        if message.from_user.first_name == "Леха":
            role = "assistant"
        else:
            role = "role"
        buf = AiApi.get_context(config.context_path)
        buf.append({"role": role, "content": f'От {message.from_user.first_name}:\n{message.text}'})
        AiApi.put_context(config.context_path, buf)
        
        if message.from_user.first_name == "GG":
            aiAnswer = chat.ask(message.text)
            id = save_mess(aiAnswer)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="отпраить в чат", callback_data=str(id))]])
            await bot.send_message(chat_id=config.ADMIN_ID, text=aiAnswer, reply_markup=keyboard)
            
    
    elif message.chat.id == config.ADMIN_ID:
        if message.text == "/get_system_prompt":
            with open(config.context_path, "r", encoding="utf-8") as f:
                cont = json.load(f)[0]["content"]
            await message.answer(cont)
            
        elif message.text[:21] == "/change_system_prompt":
            with open(config.context_path, "r", encoding="utf-8") as f:
                cont = json.load(f)
            with open(config.context_path, "w", encoding="utf-8") as f:
                cont[0]["content"] = message.text[21:]
                json.dump(cont, f, ensure_ascii=False, indent=4)

        elif message.text[:4] == "/ask":
            aiAnswer = chat.ask(message.text[5:])
            id = save_mess(aiAnswer)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="отпраить в чат", callback_data=str(id))]])
            await bot.send_message(chat_id=config.ADMIN_ID, text=aiAnswer, reply_markup=keyboard)


@ro.callback_query()
async def handle_callback(query: CallbackQuery, bot):
    print(query.data)
    await bot.send_message(chat_id=config.ADMIN_ID, text=get_mess(int(query.data)))


def save_mess(mess: str):
    with open("saved_messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
        messages.append(mess)
    with open("saved_messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False)
    return len(messages) - 1
        
def get_mess(id: int):
    with open("saved_messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
    return messages[id]