import logging
from pathlib import Path

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.quantum import RandomProvider
from bot.texts import ANSWER_NO, ANSWER_YES, BUTTON_AGAIN, ORACLE_UNAVAILABLE

logger = logging.getLogger(__name__)
router = Router()

_ROOT = Path(__file__).parent.parent.parent
_IMG = {
    True:  _ROOT / "Да.png",
    False: _ROOT / "Нет.png",
}


def _again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_AGAIN, callback_data="draw")]]
    )


@router.callback_query(lambda c: c.data == "draw")
async def cb_draw(callback: CallbackQuery, quantum: RandomProvider) -> None:
    try:
        await callback.answer()
    except TelegramBadRequest:
        pass

    try:
        bit = await quantum.get_bit()
    except Exception as exc:
        logger.error("QRNG failure: %s", exc)
        await callback.message.answer(ORACLE_UNAVAILABLE)
        return

    yes = bool(bit)
    answer = ANSWER_YES if yes else ANSWER_NO
    photo = FSInputFile(_IMG[yes])
    await callback.message.answer_photo(photo, caption=answer, reply_markup=_again_keyboard())
