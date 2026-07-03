from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    SEND_MEDIA_TO_USERS = State()
    SEND_TO_USERS = State()
    SEND_POST_TO_GROUP = State()
    SEND_MEDIA_TO_GROUP = State()
    SEND_POST_TO_GROUPS = State()
    SEND_MEDIA_TO_GROUPS = State()
    СANCEL_CONSULTATION = State()
    DELETE_USER_DATAS = State()
    SEND_PATIENT_WARN = State()
