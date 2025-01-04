from aiogram import Router


def setup_commands_router():
    from src.handlers.user.commands import start, send, quiz

    router = Router()

    router.include_routers(send.router, quiz.router, start.router)
    
    return router