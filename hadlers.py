import AiApi
import config
import json
from AiApi import chat
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, Message


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
            await bot.send_message(chat_id=config.ADMIN_ID, text=aiAnswer)
    
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