import os
import asyncio
import aiohttp
import random
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

MIX_COLORS = [
    ((255, 0, 0), (0, 0, 255)), ((255, 215, 0), (0, 0, 128)),
    ((255, 160, 122), (0, 0, 205)), ((240, 128, 128), (25, 25, 112)),
    ((255, 228, 225), (65, 105, 225)), ((240, 255, 255), (0, 0, 139)),
    ((255, 228, 181), (0, 0, 255)), ((255, 255, 0), (0, 0, 128)),
    ((0, 0, 255), (0, 255, 0))
]

def grad(text, start, end):
    res = ""
    n = len(text)
    if n <= 1: return f"\033[38;2;{start[0]};{start[1]};{start[2]}m{text}\033[0m"
    for i in range(n):
        r = int(start[0] + (end[0] - start[0]) * i / (n - 1))
        g = int(start[1] + (end[1] - start[1]) * i / (n - 1))
        b = int(start[2] + (end[2] - start[2]) * i / (n - 1))
        res += f"\033[38;2;{r};{g};{b}m{text[i]}"
    return res + "\033[0m"

def get_random_grad(text):
    start, end = random.choice(MIX_COLORS)
    return grad(text, start, end)

CHANNEL_COLORS = [Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.BLUE]
MAX_CONCURRENT_REQUESTS = 3

def print_header():
    start, end = random.choice(MIX_COLORS)
    header_text = """ââââââââââââââââââââââââââââââââââââââââââââââââââ

        âââ     ââââ   âââ
        âââ     âââââ  âââ
        âââ     ââââââ âââ
        âââ     ââââââââââ
        âââââââââââ ââââââ
        âââââââââââ  âââââ
    
 âââââââââââââââââââââââââââââââââââââââââââââââââ
                         
  TOOL SPAM DISCORD BY BO NGUYEN DEP ZAI NHAT SAN WAR 
ââââââââââââââââââââââââââââââââââââââââââââââââââââ"""
    for line in header_text.split('\n'):
        print(grad(line, start, end))

def print_author():
    start, end = random.choice(MIX_COLORS)
    author_info = f"""ââââââââââââââââââââ THÃNG TIN ADMIN  ââââââââââââââââââââ
â¦ Dev: Nguyen Long Nhat
â¦ Discord: bolalongnhat9x
âââââââââââââââââââââââââââââââââââââââââââââââââââ"""
    for line in author_info.split('\n'):
        print(grad(line, start, end))

def print_instructions():
    start, end = random.choice(MIX_COLORS)
    instructions = f"""âââââââ HÆ¯á»NG DáºªN Sá»¬ Dá»¤NG TOOL SPAM DISCORD BY BO NGUYEN  âââââââ
Chá»n má»t trong cÃ¡c chá»©c nÄng sau:
1: Bo Nguyen Log Acc Spam Discors Báº±ng tay =)) 
2: Bo Nguyen GÃµ NhÃ¢y Vá»i NÃ³ =)) 
3: Bo Nguyen Nhay And Fke Soan 
4: Bo Nguyen Reo ten 8386 ( co fke soan )
Nháº­p sá» 1, 2, 3 hoáº·c 4 Äá» chá»n chá»©c nÄng:"""
    for line in instructions.split('\n'):
        print(grad(line, start, end))

async def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200

async def load_tokens_from_file(token_file):
    if not os.path.exists(token_file):
        print(get_random_grad(f"[ERROR] File token '{token_file}' co cai buoi gi dau ?"))
        return []
    with open(token_file, 'r', encoding='utf-8') as file:
        tokens = [t.strip() for t in file.read().splitlines() if t.strip()]
    if not tokens:
        print(get_random_grad(f"[ERROR] File token '{token_file}' ÄÃ©o cÃ³ file token nÃ o ?"))
    return tokens

async def handle_response(response, channel_id, message, token):
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    try:
        if response.status == 200:
            print(get_random_grad(f"[SUCCESS] BO NGUYEN ÄÃ SPAM DISCORD THÃNH CÃNG  - Token: {token_preview}"))
            return 0
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            print(get_random_grad(f"[INFO] Token {token_preview} Bá» DISSCORD Lá»N CHO DELAY HÃY Äá»¢I 1 LÃT ANH BO NGUYEN ÄI Äáº¬P TK Táº O RA DISCORD  {retry_after}s"))
            return retry_after
        elif response.status == 401:
            print(get_random_grad(f"[ERROR] Token {token_preview} DIE TOKEN Rá»I TK NGU "))
            return 0
        else:
            print(get_random_grad(f"[ERROR] Lá»i {response.status} - Token: {token_preview}"))
            return 5
    except Exception as e:
        print(get_random_grad(f"[ERROR] Lá»i xá»­ lÃ½ pháº£n há»i: {str(e)[:50]}..."))
        return 5

def get_valid_input(prompt, valid_func, error_message="Input khÃ´ng há»£p lá», vui lÃ²ng thá»­ láº¡i."):
    while True:
        user_input = input(get_random_grad(prompt))
        if valid_func(user_input):
            return user_input
        print(get_random_grad(error_message))

def is_valid_delay(input_str):
    try:
        delay = float(input_str)
        return delay > 0
    except ValueError:
        return False

def is_valid_channel_id(input_str):
    return input_str.isdigit()

async def check_file_exists(file_path):
    exists = os.path.exists(file_path)
    if not exists:
        print(get_random_grad(f"[ERROR] File '{file_path}' khÃ´ng tá»n táº¡i!"))
    return exists

async def spam_message(token, channel_id, message, delay, use_random_delay, min_delay, max_delay, color, semaphore, bold_text):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    message = message[:2000]
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with semaphore:
                    message_to_send = f"# {message}" if bold_text else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except Exception as e:
                print(get_random_grad(f"[ERROR] Token {token_preview}: {str(e)[:50]}..."))
                await asyncio.sleep(1)

async def spam_message_nhay(token, channel_id, messages, delay, use_random_delay, min_delay, max_delay, color, mention_user, user_ids, semaphore, bold_text):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    async with aiohttp.ClientSession() as session:
        while True:
            message = random.choice(messages).strip() if messages else ""
            try:
                async with semaphore:
                    message_to_send = f"# {mention_string} {message}" if bold_text and mention_user else f"# {message}" if bold_text else f"{mention_string} {message}" if mention_user else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except Exception as e:
                print(get_random_grad(f"[ERROR] Token {token_preview}: {str(e)[:50]}..."))
                await asyncio.sleep(1)

async def fake_typing_and_send_message(token, channel_id, messages, delay, use_random_delay, min_delay, max_delay, color, mention_user, user_ids, semaphore, bold_text, name_to_call=None):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    async with aiohttp.ClientSession() as session:
        while True:
            message = random.choice(messages).strip() if messages else ""
            if name_to_call: message = message.replace("{name}", name_to_call)
            try:
                async with session.post(typing_url, headers=headers):
                    await asyncio.sleep(0.05)
                async with semaphore:
                    message_to_send = f"# {mention_string} {message}" if bold_text and mention_user else f"# {message}" if bold_text else f"{mention_string} {message}" if mention_user else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after: await asyncio.sleep(retry_after)
                await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except Exception as e:
                print(get_random_grad(f"[ERROR] Token {token_preview}: {str(e)[:50]}..."))
                await asyncio.sleep(1)

async def main():
    print_header()
    print_author()
    print_instructions()
    choice = get_valid_input("Chá»n chá»©c nÄng (1-4): ", lambda x: x in ["1", "2", "3", "4"], "m chá»n cÃ¡i ÄÃ©o gÃ¬ váº­y tháº±ng ngu ? ")
    mention_user = False
    name_to_call = None
    if choice in ["2", "3", "4"]:
        mention_user = input(get_random_grad("m cÃ³ muá»n tag tháº±ng máº·t lá»n ÄÃ³ khÃ´ng ? (y/n): ")).strip().lower() == 'y'
    if mention_user:
        user_ids = input(get_random_grad("Nháº­p ID tháº±ng vÃ´ danh vÃ o ÄÃ¢y Äá» Äáº¡i ca bo nguyen rÃ©o cho (cÃ¡ch nhau bá»i dáº¥u pháº©y): ")).split(',')
        user_ids = [uid.strip() for uid in user_ids if uid.strip()]
    else: user_ids = []
    if choice == "4":
        name_to_call = input(get_random_grad("Nháº­p tÃªn cáº§n rÃ©o: ")).strip()
    channel_ids = []
    while True:
        channel_id = input(get_random_grad("NHAP ID KENH SEVER GHE DO VO DAY  (gÃµ 'done' Äá» káº¿t thÃºc): ")).strip().lower()
        if channel_id == "done": break
        if is_valid_channel_id(channel_id): channel_ids.append(channel_id)
        else: print(get_random_grad("ID kÃªnh sai kÃ¬a tháº±ng ngu Æ¡i ? "))
    tokens_map = {}
    for idx, channel_id in enumerate(channel_ids):
        token_file = input(get_random_grad(f"Nháº­p file token vÃ´ ÄÃ¢y , token pháº£i khoáº» nha tháº±ng ngu  {channel_id}: "))
        if not await check_file_exists(token_file): continue
        tokens = await load_tokens_from_file(token_file)
        valid_tokens = [t for t in tokens if await validate_token(t)]
        if not valid_tokens:
            print(get_random_grad(f"[ERROR] TOKEN DIE ROI TK CAC OI  {token_file}!"))
            continue
        tokens_map[channel_id] = valid_tokens
    if not tokens_map: return
    use_multiple_files = False
    if choice in ["2", "3", "4"]:
        use_multiple_files = input(get_random_grad("m cÃ³ muá»n cháº¡y Äa file ngÃ´n k ?  (nhiá»u file tin nháº¯n)? (y/n): ")).strip().lower() == 'y'
    files_content = []
    if use_multiple_files:
        txt_files = [f for f in os.listdir() if f.endswith('.txt')]
        if not txt_files: return
        print(get_random_grad("âââââââ FILE TIN NHAN CUA BO NGUYEN DZAI MOI ANH LUA CHON  âââââââ"))
        for idx, file in enumerate(txt_files, 1):
            print(get_random_grad(f"{idx}: {file}"))
        file_indexes = input(get_random_grad("Chá»n file tin nháº¯n (sá» thá»© tá»±, cÃ¡ch nhau bá»i dáº¥u pháº©y): "))
        file_indexes = [int(i) - 1 for i in file_indexes.split(',') if i.strip()]
        for file_index in file_indexes:
            with open(txt_files[file_index], 'r', encoding='utf-8') as file:
                files_content.extend([line.strip() for line in file.read().splitlines() if line.strip()])
    else:
        if choice == "1":
            txt_files = [f for f in os.listdir() if f.endswith('.txt')]
            for idx, file in enumerate(txt_files, 1): print(get_random_grad(f"{idx}: {file}"))
            file_index = int(input(get_random_grad("Chá»n file tin nháº¯n (sá» thá»© tá»±): "))) - 1
            with open(txt_files[file_index], 'r', encoding='utf-8') as file:
                files_content = [file.read().strip()]
        else:
            with open("nhaychet.txt", 'r', encoding='utf-8') as file:
                files_content = [line.strip() for line in file.read().splitlines() if line.strip()]
    bold_text = input(get_random_grad("Báº¡n muá»n chá»¯ in Äáº­m? (y/n): ")).strip().lower() == 'y'
    print(get_random_grad("âââââââ BO NGUYEN  Báº®T Äáº¦U SPAM âââââââ"))
    tasks = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    for idx, (channel_id, tokens) in enumerate(tokens_map.items()):
        for i, token in enumerate(tokens):
            delay = float(input(get_random_grad(f"Nháº­p delay cho token thá»© {i+1} (kÃªnh {channel_id}): ")))
            use_random_delay = input(get_random_grad("Báº¡n muá»n delay ngáº«u nhiÃªn? (y/n): ")).strip().lower() == 'y'
            min_delay = delay; max_delay = delay
            if use_random_delay:
                min_delay = float(input(get_random_grad("Nháº­p delay tháº¥p nháº¥t: ")))
                max_delay = float(input(get_random_grad("Nháº­p delay cao nháº¥t: ")))
            if choice == "1": tasks.append(spam_message(token, channel_id, files_content[i % len(files_content)], delay, use_random_delay, min_delay, max_delay, None, semaphore, bold_text))
            elif choice == "2": tasks.append(spam_message_nhay(token, channel_id, files_content, delay, use_random_delay, min_delay, max_delay, None, mention_user, user_ids, semaphore, bold_text))
            elif choice in ["3", "4"]: tasks.append(fake_typing_and_send_message(token, channel_id, files_content, delay, use_random_delay, min_delay, max_delay, None, mention_user, user_ids, semaphore, bold_text, name_to_call))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
