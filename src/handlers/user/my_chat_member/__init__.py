from aiogram import Router


def setup_my_chat_member_handlers():
    router = Router()

    from src.handlers.user.my_chat_member import private_status

    router.include_routers(private_status.router)

    return router