import asyncio
import os

from utils.core import create_sessions, logger
from utils.telegram import Accounts
from utils.cryptorank import CryptoRank
from data.config import hello, USE_PROXY

async def gather_tasks(accounts, proxy_dict=None):
    tasks = []
    for thread, account in enumerate(accounts):
        proxy = proxy_dict.get(account) if proxy_dict else None
        tasks.append(asyncio.create_task(CryptoRank(account=account, thread=thread, proxy=proxy).main()))
    await asyncio.gather(*tasks)

def load_proxies():
    proxy_dict = {}
    try:
        with open('proxy.txt', 'r', encoding='utf-8') as file:
            for line in file:
                prox, name = line.strip().split()
                proxy_dict[name] = prox
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    return proxy_dict

async def main():
    print(hello)
    action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n>'))
    
    if not os.path.exists('sessions'):
        os.mkdir('sessions')
    
    if action == 2:
        await create_sessions()

    elif action == 1:
        accounts = await Accounts().get_accounts()
        proxy_dict = load_proxies() if USE_PROXY else None
        await gather_tasks(accounts, proxy_dict)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
