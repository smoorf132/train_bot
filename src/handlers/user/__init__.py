from aiogram import Router


def setup_handlers():
    from src.handlers.user.commands import setup_commands_router
    from src.handlers.user.callback import setup_callback_handlers
    from src.handlers.user.my_chat_member import setup_my_chat_member_handlers
    from src.handlers.user.join_requests import setup_join_requests_handlers
    

    router = Router()

    router.include_routers(setup_commands_router(), setup_callback_handlers(), setup_my_chat_member_handlers(), setup_join_requests_handlers())

    return router