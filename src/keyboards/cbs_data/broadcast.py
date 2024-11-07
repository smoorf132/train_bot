from aiogram.filters.callback_data import CallbackData


class ConfirmingCallback(CallbackData, prefix="sending"):
    action: str