from aiogram import Router


def setup_commands_router():
    from src.handlers.user.commands import start, send, quiz

    router = Router()

    router.include_routers(quiz.router, send.router, start.router)
    
    return router