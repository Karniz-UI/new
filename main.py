from telethon import TelegramClient, events
import logging
import os
import importlib.util
import sys
from datetime import datetime
import asyncio

logging.basicConfig(
    format="%(message)s",
    datefmt="%H:%M:%S %d-%m-%Y",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

API_ID = "28275928"
API_HASH = "a0828d5f1a36532b58290ea652960864"
BOT_NAME = "H1llBot Release"
VERSION = "2.3 Release"
PREFIX = "-"
MODULES_DIR = "modules"
YOUR_USER_ID = 1540613583

if not os.path.exists(MODULES_DIR):
    os.makedirs(MODULES_DIR)

loaded_modules = {}
main_client = TelegramClient("H1llBotV2_session", API_ID, API_HASH, connection_retries=5)

def print_banner():
    print(f"{BOT_NAME} v{VERSION} by xyecoc hekcoh starting...")
    print("Bot Ready..")

def load_module(module_name, client):
    try:
        module_path = f"{MODULES_DIR}/{module_name}.py"
        if not os.path.exists(module_path):
            logger.error(f"Модуль {module_name} не найден: {module_path}")
            return f"Модуль {module_name} не найден."
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        module.register(client)
        loaded_modules[module_name] = client
        logger.info(f"{module_name} успешно загружен.")
        return f"{module_name} загружен."
    except Exception as e:
        logger.error(f"Ошибка загрузки {module_name}: {e}")
        return f"Ошибка загрузки {module_name}: {e}"

def unload_module(module_name, client):
    try:
        if module_name not in loaded_modules:
            return f"Модуль {module_name} не загружен!"
        for handler in loaded_modules[module_name].__dict__.values():
            if isinstance(handler, events.EventHandler):
                client.remove_event_handler(handler)
        del sys.modules[module_name]
        del loaded_modules[module_name]
        return f"Модуль {module_name} выгружен!"
    except Exception as e:
        logger.error(f"Ошибка выгрузки {module_name}: {e}")
        return f"Ошибка выгрузки {module_name}: {e}"

def delete_module(module_name):
    try:
        module_path = f"{MODULES_DIR}/{module_name}.py"
        if not os.path.exists(module_path):
            return f"Модуль {module_name} не найден!"
        os.remove(module_path)
        if module_name in loaded_modules:
            unload_module(module_name, main_client)
        return f"Модуль {module_name} удалён!"
    except Exception as e:
        logger.error(f"Ошибка удаления {module_name}: {e}")
        return f"Ошибка удаления {module_name}: {e}"

def refresh_module(module_name, client):
    try:
        if module_name not in loaded_modules:
            return f"Модуль {module_name} не загружен!"
        unload_module(module_name, client)
        result = load_module(module_name, client)
        return f"Модуль {module_name} обновлён!\n{result}"
    except Exception as e:
        logger.error(f"Ошибка обновления {module_name}: {e}")
        return f"Ошибка обновления {module_name}: {e}"

async def is_owner(event):
    sender = await event.get_sender()
    return sender.id == YOUR_USER_ID

@main_client.on(events.NewMessage(pattern=f"{PREFIX}start"))
async def start(event):
    if not await is_owner(event):
        return
    sender = await event.get_sender()
    try:
        await event.message.edit(
            f"Привет {sender.first_name}.\n"
            f"Я юзербот — хиллбот v{VERSION}\n"
            f"`Желаю удачи..)`\n"
            f"__Спасибо за покупку.__",
            parse_mode='markdown'
        )
    except Exception as e:
        logger.error(f"Ошибка редактирования start: {e}")
        await event.reply("Не могу отредактировать сообщение!")
    logger.info(f"[-] Команда {PREFIX}start от {sender.username or sender.id}")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}help"))
async def help(event):
    if not await is_owner(event):
        return
    help_text = (
        f"Команды {BOT_NAME}\n\n"
        f"Price — $5\n"
        f"`{PREFIX}help` — Список команд\n"
        f"`{PREFIX}info` — Инфа о боте\n"
        f"`{PREFIX}time` — Текущее время\n"
        f"`{PREFIX}addmod` — Добавить модуль (только .py)\n"
        f"`{PREFIX}delmod <имя>` — Удалить модуль\n"
        f"`{PREFIX}refreshmod <имя>` — обновить модуль\n"
        f"`{PREFIX}modules` — Список модулей\n"
        f"`?..`"
    )
    try:
        await event.message.edit(help_text, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Ошибка редактирования help: {e}")
        await event.reply("Не могу отредактировать сообщение.")
    logger.info("[-] Команда -help")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}info"))
async def info(event):
    if not await is_owner(event):
        return
    info_text = (
        f"{BOT_NAME} v{VERSION}\n\n"
        f"Создатель: HEKCOH\n"
        f"Тип: Userbot\n"
        f"Статус: Активен..\n"
        f"Модулей: {len(loaded_modules)}"
    )
    try:
        await event.message.edit(info_text, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Ошибка редактирования info: {e}")
        await event.reply("Не могу отредактировать сообщение!")
    logger.info("[-] Команда -info")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}time"))
async def time(event):
    if not await is_owner(event):
        return
    current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    try:
        await event.message.edit(f"Время: {current_time}", parse_mode='markdown')
    except Exception as e:
        logger.error(f"Ошибка редактирования time: {e}")
        await event.reply("Не могу отредактировать сообщение!")
    logger.info("[-] Команда -time")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}addmod"))
async def add_module(event):
    if not await is_owner(event):
        return
    if not event.message.file or not event.message.file.name.endswith(".py"):
        try:
            await event.message.edit("Ошибка: Прикрепите .py файл!", parse_mode='markdown')
        except Exception as e:
            logger.error(f"Ошибка редактирования addmod: {e}")
            await event.reply("Не могу отредактировать сообщение!")
        return
    try:
        module_name = os.path.splitext(event.message.file.name)[0]
        module_path = f"{MODULES_DIR}/{module_name}.py"
        await event.message.download_media(file=module_path)
        logger.info(f"[-] Загружен модуль: {module_path}")
        result = load_module(module_name, main_client)
        try:
            await event.message.edit(result, parse_mode='markdown')
        except Exception as e:
            logger.error(f"Ошибка редактирования addmod: {e}")
            await event.reply("Не могу отредактировать сообщение!")
        logger.info(f"[-] Загрузка {module_name}: {result}")
    except Exception as e:
        try:
            await event.message.edit(f"Ошибка: {e}", parse_mode='markdown')
        except Exception as edit_error:
            logger.error(f"Ошибка редактирования addmod: {edit_error}")
            await event.reply("Не могу отредактировать сообщение!")
        logger.error(f"[-] Ошибка загрузки модуля: {e}")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}delmod (.+)"))
async def delete_module_cmd(event):
    if not await is_owner(event):
        return
    module_name = event.pattern_match.group(1).strip()
    result = delete_module(module_name)
    try:
        await event.message.edit(result, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Ошибка редактирования delmod: {e}")
        await event.reply("Не могу отредактировать сообщение!")
    logger.info(f"[-] Удаление {module_name}: {result}")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}refreshmod (.+)"))
async def refresh_module_cmd(event):
    if not await is_owner(event):
        return
    module_name = event.pattern_match.group(1).strip()
    result = refresh_module(module_name, main_client)
    try:
        await event.message.edit(result, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Ошибка редактирования refreshmod: {e}")
        await event.reply("Не могу отредактировать сообщение!")
    logger.info(f"[-] Обновление {module_name}: {result}")

@main_client.on(events.NewMessage(pattern=f"{PREFIX}modules"))
async def list_modules(event):
    if not await is_owner(event):
        return
    if loaded_modules:
        modules_text = "\n".join([f"{mod}" for mod in loaded_modules])
        try:
            await event.message.edit(f"Список модулей:\n{modules_text}", parse_mode='markdown')
        except Exception as e:
            logger.error(f"Ошибка редактирования modules: {e}")
            await event.reply("Не могу отредактировать сообщение!")
    else:
        try:
            await event.message.edit("Модули отсутствуют!", parse_mode='markdown')
        except Exception as e:
            logger.error(f"Ошибка редактирования modules: {e}")
            await event.reply("Не могу отредактировать сообщение!")
    logger.info("[-] Команда -modules")

async def main():
    print_banner()
    logger.info(f"[-] {BOT_NAME} запускается...")
    
    if os.path.exists(MODULES_DIR):
        for file in os.listdir(MODULES_DIR):
            if file.endswith(".py"):
                module_name = file[:-3]
                logger.info(f"[-] Загрузка модуля {module_name}")
                result = load_module(module_name, main_client)
                logger.info(f"[-] {result}")
    else:
        logger.error(f"Папка модулей {MODULES_DIR} не найдена!")

    try:
        await main_client.start()
        logger.info(f"{BOT_NAME} онлайн!")
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")

    await main_client.run_until_disconnected()

if __name__ == "__main__":
    try:
        main_client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info(f"{BOT_NAME} завершает работу...")
        main_client.disconnect()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
