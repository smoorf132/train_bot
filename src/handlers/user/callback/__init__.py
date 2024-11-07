from aiogram import Router


def setup_callback_handlers():
    router = Router()

    from src.handlers.user.callback import choose_plan

    router.include_routers(choose_plan.router)

    return router