import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.quantum import RandomProvider
from bot.texts import ANSWER_NO, ANSWER_YES, BUTTON_AGAIN, ORACLE_UNAVAILABLE

logger = logging.getLogger(__name__)
router = Router()


def _again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_AGAIN, callback_data="draw")]]
    )


@router.callback_query(lambda c: c.data == "draw")
async def cb_draw(callback: CallbackQuery, quantum: RandomProvider) -> None:
    try:
        await callback.answer()
    except TelegramBadRequest:
        # Запрос протух (> 60 сек) — просто игнорируем, всё равно отправим ответ
        pass

    try:
        bit = await quantum.get_bit()
    except Exception as exc:
        logger.error("QRNG failure: %s", exc)
        await callback.message.answer(ORACLE_UNAVAILABLE)
        return

    answer = ANSWER_YES if bit else ANSWER_NO
    await callback.message.answer(answer, reply_markup=_again_keyboard())
