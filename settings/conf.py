from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

def get_env_key(key: str):
    with open('.env', 'r', encoding='utf-8') as f_tore:
        lines = f_tore.readlines()
        for line in lines:
            if key in line and '#' not in line:
                return str(line.split('=')[-1]).strip()



async def edit_env(key:str, val:str):
    with open('.env', 'r', encoding='utf-8') as f_tore:
        lines = f_tore.readlines()
        for line in lines:
            if key in line:
                lines[lines.index(line)] = f"{key}={val}\n"
                break

        with open('.env', 'w', encoding='utf-8') as f_towr:
            f_towr.writelines(lines)





bot = Bot(get_env_key('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()