import chat
import config
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated, Message


ro = Router(name=__name__)


@ro.message(F.text)
async def get_message(message: Message):
    buf = chat.get_context(config.context_path)
    buf.append({"role": "user", "content": f'От {message.from_user.first_name}:\n{message.text}'})
    chat.put_context(config.context_path, buf)