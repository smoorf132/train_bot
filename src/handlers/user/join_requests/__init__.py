from aiogram import Router


def setup_join_requests_handlers():
    router = Router()

    from src.handlers.user.join_requests import approve_requests

    router.include_routers(approve_requests.router)

    return router