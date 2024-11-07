from aiogram.utils.keyboard import ReplyKeyboardBuilder


def gender_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(
        text="Мужчина 🧔🏻"
    )
    builder.button(
        text="Женщина 👩🏻‍🦱"
    )
    builder.adjust(2)

    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def captcha_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(
        text="Эктоморф"
    )
    builder.button(
        text="Мезоморф"
    )
    builder.button(
        text="Эндоморф"
    )

    builder.adjust(1)

    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)