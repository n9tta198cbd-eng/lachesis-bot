from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.texts import AWAITING, BUTTON_DRAW, HELP, WELCOME

router = Router()


def _draw_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_DRAW, callback_data="draw")]]
    )


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME)
    await message.answer(AWAITING, reply_markup=_draw_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP)
