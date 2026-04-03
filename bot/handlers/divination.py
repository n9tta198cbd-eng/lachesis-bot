import logging

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.quantum import RandomProvider
from bot.texts import ANSWER_NO, ANSWER_YES, AWAITING, BUTTON_AGAIN, BUTTON_DRAW, ORACLE_UNAVAILABLE

logger = logging.getLogger(__name__)
router = Router()


def _again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_AGAIN, callback_data="draw")]]
    )


@router.callback_query(lambda c: c.data == "draw")
async def cb_draw(callback: CallbackQuery, quantum: RandomProvider) -> None:
    await callback.answer()

    try:
        bit = await quantum.get_bit()
    except Exception as exc:
        logger.error("QRNG failure: %s", exc)
        await callback.message.answer(ORACLE_UNAVAILABLE)
        return

    answer = ANSWER_YES if bit else ANSWER_NO
    await callback.message.answer(answer, reply_markup=_again_keyboard())
