from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class IsBotAdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        admin_ids_int = [int(id) for id in ADMINS]
        return int(message.from_user.id) in admin_ids_int
