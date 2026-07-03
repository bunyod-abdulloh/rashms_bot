from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAnketa(StatesGroup):
    add_fullname = State()
    add_phone = State()
    GET_GENDER = State()
    GET_AGE = State()
    FULL_NAME = State()
    MARITAL_STATUS = State()
    ABSENCE_CHILDREN = State()
    WORK = State()
    EEG = State()
    PHONE = State()
    PAYMENT = State()


class UserEditDatas(StatesGroup):
    EDIT_FULLNAME = State()
    EDIT_GENDER = State()
    EDIT_AGE = State()
    EDIT_MARITAL_STATUS = State()
    EDIT_ABSENCE_CHILDREN = State()
    EDIT_WORK = State()
    EDIT_EEG = State()
    EDIT_PHONE = State()


class Patient(StatesGroup):
    WARN = State()
