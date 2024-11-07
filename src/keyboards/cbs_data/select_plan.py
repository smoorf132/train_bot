from aiogram.filters.callback_data import CallbackData


class SelectTypeCallback(CallbackData, prefix="type"):
    type: str


class SelectPlanCallback(CallbackData, prefix="plan"):
    level: str | None = None