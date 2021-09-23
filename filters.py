from aiogram.dispatcher.filters import Filter
from aiogram import types

class IsJoined(Filter):

    async def check(self, update: types.ChatMemberUpdated):
        return update.new_chat_member.status == 'member'