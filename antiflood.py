async def anti_flood(*args, **kwargs):
    message = args[0]   
    await message.answer('Too many requests!')