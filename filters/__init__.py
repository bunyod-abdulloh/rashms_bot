from loader import dp
from .admins import IsBotAdminFilter

if __name__ == "filters":
    dp.filters_factory.bind(IsBotAdminFilter)
