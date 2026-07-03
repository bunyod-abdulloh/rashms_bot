import asyncio

from aiogram import types
from aiogram.utils.exceptions import (
    BotBlocked,
    UserDeactivated,
    ChatNotFound,
    RetryAfter
)

from loader import bot, udb


async def send_message_to_users(message: types.Message):
    success_count = 0
    failed_count = 0

    limit = 1000
    offset = 0

    while True:

        users = await udb.get_users(
            limit=limit,
            offset=offset
        )

        if not users:
            break

        for index, user in enumerate(users, start=1):

            telegram_id = user["telegram_id"]

            try:

                await message.copy_to(
                    chat_id=telegram_id
                )

                success_count += 1

                # Telegram flood limit uchun
                await asyncio.sleep(0.06)

            except RetryAfter as e:

                print(f"Flood limit! Sleep: {e.timeout} sec")

                await asyncio.sleep(e.timeout)

                try:
                    await message.copy_to(
                        chat_id=telegram_id
                    )
                    success_count += 1

                except Exception as err:
                    failed_count += 1


            except (
                    BotBlocked,
                    UserDeactivated,
                    ChatNotFound
            ):

                failed_count += 1

                await udb.delete_user(
                    telegram_id
                )

            except Exception as err:

                failed_count += 1

            # Har 2000 userdan keyin qisqa dam
            if index % 2000 == 0:
                await asyncio.sleep(10)

        offset += limit

        # Batchlar orasida kichik pause
        await asyncio.sleep(2)

    return success_count, failed_count


async def send_media_group_to_users(
        media_group: list[types.InputMedia]
):
    success_count = 0
    failed_count = 0

    limit = 500
    offset = 0

    while True:

        users = await udb.get_users(
            limit=limit,
            offset=offset
        )

        if not users:
            break

        for index, user in enumerate(users, start=1):

            telegram_id = user["telegram_id"]

            try:

                await bot.send_media_group(
                    chat_id=telegram_id,
                    media=media_group
                )

                success_count += 1

                # Media group uchun sekinroq throttle
                await asyncio.sleep(0.15)

            except RetryAfter as e:

                print(
                    f"Flood control! "
                    f"Sleep {e.timeout} sec"
                )

                await asyncio.sleep(
                    e.timeout
                )

                try:

                    await bot.send_media_group(
                        chat_id=telegram_id,
                        media=media_group
                    )

                    success_count += 1

                    await asyncio.sleep(0.15)

                except (
                        BotBlocked,
                        UserDeactivated,
                        ChatNotFound
                ):

                    failed_count += 1

                    await udb.delete_user(
                        telegram_id
                    )

                except Exception as err:

                    failed_count += 1

            except (
                    BotBlocked,
                    UserDeactivated,
                    ChatNotFound
            ):

                failed_count += 1

                await udb.delete_user(
                    telegram_id
                )

            except Exception as err:

                failed_count += 1

            # Har 1000 userdan keyin pause
            if index % 1000 == 0:
                await asyncio.sleep(15)

        offset += limit

        # Batchlar orasida pause
        await asyncio.sleep(3)

    return success_count, failed_count
