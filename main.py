import asyncio
import logging

from question_api import *
import config
import lang_utils

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram import html
from aiogram.filters.command import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

TOKEN = config.TOKEN
password = config.password

bot = Bot(token=TOKEN)

disp = Dispatcher()


@disp.message(Command("start"))
async def start(message: Message):
    kb = [
        [
            KeyboardButton(text="🍎 Geschlecht von Substantiven")
        ],
        [
            KeyboardButton(text="🚶‍♂️ Verben"),
            KeyboardButton(text="📝 Pluralformen")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True,
                                   input_field_placeholder="Что мы сегодня практикуем??")
    await message.reply("👋 Hallo...\nДавайте учить deutsch Sprache вместе... \nLasst uns gemeinsam Deutsch lernen!", reply_markup=keyboard)

@disp.message(F.text == "📝 Pluralformen")
async def plural(message: Message, variables: dict):
    # Проверка пользователя и режима
    if message.chat not in variables:
        variables[message.chat] = {}

    variables[message.chat]["mode"] = 1
    # - Конец проверки

    q = get_random_noun_with_answer()
    que = q[0]
    variables[message.chat]["correct_answer"] = q[1]
    await message.answer(f"Okay, sehr gut!\nЯ называю тебе существительное на немецком, а ты мне говоришь его множественное число с частицой",
                        reply_markup=ReplyKeyboardRemove())

    await message.answer(f"Слово: {html.italic(que)}", parse_mode=ParseMode.HTML)

@disp.message(F.text == "🍎 Geschlecht von Substantiven")
async def genders(message: Message, variables: dict):
    # Проверка пользователя и режима
    if message.chat not in variables:
        variables[message.chat] = {}

    variables[message.chat]["mode"] = 1
    # - Конец проверки

    q = get_random_gender_with_answer()
    que = q[0]
    variables[message.chat]["correct_answer"] = q[1]
    await message.answer(f"Okay, sehr gut!\nIch nenne dir ein Nomen und du nennst mir sein Geschlecht\nm - männlich; w - weiblich; s - sächlich",
                        reply_markup=ReplyKeyboardRemove())

    await message.answer(f"Nomen: {html.italic(que)}", parse_mode=ParseMode.HTML)

@disp.message(F.text == "🚶‍♂️ Verben")
async def verbs(message: Message, variables: dict):
    # Проверка пользователя и режима
    if message.chat not in variables:
        variables[message.chat] = {}

    variables[message.chat]["mode"] = 1
    # - Конец проверки

    q = get_random_verb_with_answer()
    que = q[0]
    variables[message.chat]["correct_answer"] = q[1]
    pronoun = q[2]
    await message.answer(f"Okay, sehr gut!\nЯ говорю тебе глагол и местоимение, а ты мне правильное спряжение этого глагола с этим местоимением...",
                        reply_markup=ReplyKeyboardRemove())

    await message.answer(f"Глагол: {html.italic(que)}\nМестоимение: {html.italic(pronoun)}", parse_mode=ParseMode.HTML)

@disp.message(Command(f"add_question_{password}"))
async def add_question(message: Message):
    split_message_text = message.text.replace(",", "").split()
    adding_changed_to = split_message_text[1]

    old_to_add = split_message_text[2::]

    to_add = [lang_utils.umlauts_and_eszett(a) for a in old_to_add]

    if adding_changed_to == "verb":
        Editor.add_verb(to_add)

    elif adding_changed_to == "genders":
        Editor.add_gender(to_add)

    elif adding_changed_to == "plurals":
        to_add = [i.replace("_", " ") for i in to_add]
        if not Editor.add_noun(to_add):
            await message.reply("Error occurred when trying to add to \"noun_plurals\". Try again or check for the mistakes.")
            return

    else:
        await message.reply("Incorret argument used. Use verb/genders/plurals.")
        return

    await message.reply(f"Successfully added {to_add} to \"{adding_changed_to}\"")



@disp.message(F.text)
async def general_message_getter(message: Message, variables: dict):
    if message.chat not in variables or variables[message.chat]["mode"] == 0:
        await message.answer(f"Oh, es tut mir leid. Я не знаю такой команды 😔")

    else:
        # Ставим режим снова в "сон"
        variables[message.chat]["mode"] = 0

        # Получаем правильный ответ
        corr = variables[message.chat]["correct_answer"]

        kb = [
            [
                KeyboardButton(text="🍎 Geschlecht von Substantiven")
            ],
            [
                KeyboardButton(text="🚶‍♂️ Verben"),
                KeyboardButton(text="📝 Pluralformen")
            ]
        ]

        keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                       resize_keyboard=True,
                                       input_field_placeholder="Что мы сегодня практикуем??")

        if lang_utils.umlauts_and_eszett(message.text) == corr:
            await message.reply(f"Sehr gut! Richtig!", reply_markup=keyboard)
        else:
            await message.reply(f"Oh! Nein... Правильно было {html.italic(corr)}... Passiert:)", reply_markup=keyboard, parse_mode=ParseMode.HTML)



async def main():
    await disp.start_polling(bot, variables={"correct_answer": "",})



if __name__ == "__main__":
    print(f"Current password: {password}")
    asyncio.run(main())

