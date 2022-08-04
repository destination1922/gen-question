import logging
from config import *
from random import shuffle
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    main_btn = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [types.KeyboardButton(text=DISTRIBUTION)],
            [types.KeyboardButton(text=ADD)]
        ]
    )
    await message.answer(text=START_TEXT, reply_markup=main_btn)

@dp.callback_query_handler()
async def biletlar(query: types.CallbackQuery):
    telegram_id = query.from_user.id
    data = query.data
    bilet_number, msg_count = map(int, data.split())

    with open('nums.txt') as rfile:
        line = rfile.readline()
        got_array = list(map(int, line.split()))
    questions = generate_numbers(got_array, msg_count)
    bilet = questions[bilet_number]

    with open('questions.txt') as file:
        lines = file.readlines()

    text_question = ""
    for i, q in enumerate(bilet):
        text_question += f"{i+1}.  {lines[q-1]}\n"

    await bot.send_message(chat_id=telegram_id, text=f"<i>{bilet_number + 1} - bilet</i>\n\n{text_question}"
                           , parse_mode='HTML')

@dp.message_handler()
async def divider(message: types.Message):
    msg = message.text

    if msg == DISTRIBUTION:
        await message.answer("Savollarni nechtadan bo'lmoqchisiz?")

    elif msg == ADD:
        await message.answer("Savolingizni yuboring...\n"
                             "Savolni - belgisi bilan boshlang"
                             "\nMasalan:\n"
                             "-Maxfiy harflar qaysilar?😉")

    elif msg.isdigit():
        msg_count = int(msg)
        with open('questions.txt') as file:
            lines = file.readlines()
            q_array = list(range(1, len(lines) + 1))
            shuffle(q_array)
        with open('nums.txt', 'w') as wfile:
            for i in q_array:
                wfile.write(f"{i} ")
        if msg_count > 10:
            await message.answer("10 tadan ko'p bo'lishi mumkin emas!")
        elif msg_count < 1:
            await message.answer("1 dan kichik kiritish mumkin emas!")
        else:
            with open('nums.txt') as rfile:
                line = rfile.readline()
                got_array = list(map(int, line.split()))
            questions = generate_numbers(got_array, msg_count)
            Bs = []
            for i, ar in enumerate(questions):
                text = f"{i+1}-bilet"
                c_data = f"{i} {msg_count}"
                l = []
                l.append(text)
                l.append(c_data)
                Bs.append(l)
            bilets = types.InlineKeyboardMarkup(row_width=3)
            btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in Bs)
            bilets.add(*btns)
            await message.answer("Biletlar", reply_markup=bilets)

    elif msg[0] == '-':
        msg = msg[1:]
        question = ""
        for i in msg.split('\n'):
            question += i
        with open('questions.txt', 'a') as file:
            file.write(f"\n{question}")
        await message.answer("Savolingiz muvaffaqqiyatli qo'shildi!")
    else:
        await message.answer("Ortiqcha xabar yubormang! Muammo kerak emas 😉")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)