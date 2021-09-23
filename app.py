from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher.storage import FSMContext
from buttons import markup, cancel_b
from states import GetIDs
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from filters import IsJoined
import logging
from antiflood import anti_flood

logging.basicConfig(level=logging.INFO)
TOKEN='2013540624:AAErS4ZMrxK2vSgtsTfgxzGhOcIY7BqIjFw'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=5)
async def greet(message: types.Message):
    name = quote_html(message.from_user.first_name)
    await message.answer(f'Welcome, {name}!', reply_markup=markup)

@dp.message_handler(CommandHelp())
@dp.throttled(anti_flood, rate=5)
async def greet(message: types.Message):
    await message.answer("<b>Use this bot:</b>\n\n•<i>To get your info by clicking on 'My Info' button.</i>\n"
                        "•<i>To get a user's info by clicking on 'User Info' button and forwarding a message from that user to this bot.</i>\n"
                        "•<i>To get a channel info by clicking on 'Channel Info' button and forwarding a post(text, photo, audio, video, voice) from that channel to this bot.</i>\n"
                        "•<i>To get a group info by just inviting this bot to that group.</i>",parse_mode="HTML")


@dp.message_handler(text='cancel',state="*")
@dp.throttled(anti_flood, rate=2)
async def cancel(message: types.Message,state:FSMContext):
    current_state=await state.get_state()
    if not current_state:
        await message.answer('You canceled the action', reply_markup=markup)
    else:
        await state.finish()
        await message.answer("You canceled the action", reply_markup=markup)


@dp.message_handler(lambda message: message.text == 'My Info')
@dp.throttled(anti_flood, rate=2)
async def get_my_info(message: types.Message):
    name = quote_html(message.from_user.first_name)
    await message.answer(f'Your first name: <b>{name}</b>\n'
                         f'Your username: <i>@{message.from_user.username}</i>\n'
                         f'Your User ID: {message.from_user.id}',
                         reply_markup=markup, parse_mode="HTML")


@dp.message_handler(lambda message: message.text == 'User Info')
@dp.throttled(anti_flood, rate=2)
async def get_username(message: types.Message):
    await message.answer('Forward me a message(text, photo, audio, video, voice) of a user',       reply_markup=cancel_b)
    await GetIDs.user_info.set()


@dp.message_handler(lambda message: message.forward_from, content_types=types.ContentTypes.ANY, state=GetIDs.user_info)
@dp.throttled(anti_flood, rate=2)
async def get_user_info(message: types.Message, state:FSMContext):
    name = quote_html(message.forward_from.first_name)
    await message.answer(f"User's first name: <b>{name}</b>\n"
                         f"User's username: <i>@{message.forward_from.username}</i>\n"
                         f"User's User ID: {message.forward_from.id}",
                         reply_markup=markup, parse_mode='HTML')
    await state.finish()


@dp.message_handler(lambda message: message.forward_sender_name, content_types=types.ContentTypes.ANY, state=GetIDs.user_info)
@dp.throttled(anti_flood, rate=2)
async def get_user_private_info(message: types.Message, state:FSMContext):
    name = quote_html(message.forward_sender_name)
    await message.answer(f"User <b>{name}</b> decided to hide his Info", 
                         reply_markup=markup, parse_mode='HTML')
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Channel Info')
@dp.throttled(anti_flood, rate=2)
async def answer_channelInfo(message: types.Message):
    await message.answer('Forward me a post(text, photo, audio, video, voice) from that channel', reply_markup=cancel_b)
    await GetIDs.channel.set()


@dp.message_handler(lambda message: message.forward_from_chat,content_types=types.ContentTypes.ANY,state=GetIDs.channel)
@dp.throttled(anti_flood, rate=2)
async def get_channelID(message:types.Message, state:FSMContext):
    name = quote_html(message.forward_from_chat.title)
    await message.answer(f'Channel name: <b>{name}</b>\n'
                         f'Channel username: <i>@{message.forward_from_chat.username}</i>\n'
                         f'Channel ID: {message.forward_from_chat.id}',
                         reply_markup=markup, parse_mode='HTML')
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Group Info')
@dp.throttled(anti_flood, rate=2)
async def answer_groupInfo(message: types.Message):
    await message.answer(f"Invite me to a group, I'll send you the group ID", reply_markup=cancel_b)


@dp.my_chat_member_handler(IsJoined())
@dp.throttled(anti_flood, rate=2)
async def get_groupID(update: types.ChatMemberUpdated):
    title = quote_html(update.chat.title)
    await bot.send_message(update.from_user.id,f'Group name: <b>{title}</b>\n'
                                               f'Group ID: {update.chat.id}',
                                               reply_markup=markup, parse_mode='HTML')

async def setup_bot_commands(dispatcher: Dispatcher):

    bot_commands=[
        types.BotCommand(command='/start', description='Start bot'),
        types.BotCommand(command='/help', description='Show help'),
    ]
    await bot.set_my_commands(bot_commands)               


if __name__ == '__main__':
    dp.bind_filter(IsJoined)
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)