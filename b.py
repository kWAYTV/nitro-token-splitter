# Imports
import httpx, toml, os, time, colorama, pystyle, paramiko
from colorama import Fore, init, Style
from pystyle import *

# Clear the console
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")
uploadCount = -1
tokenCount = 0
filled = 0
empty = 0
error = 0
scriptDir = os.getcwd()

# Vanity Generator Logo
logo = """
████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗  ░██████╗██████╗░██╗░░░░░██╗████████╗████████╗███████╗██████╗░
╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║  ██╔════╝██╔══██╗██║░░░░░██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║  ╚█████╗░██████╔╝██║░░░░░██║░░░██║░░░░░░██║░░░█████╗░░██████╔╝
░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║  ░╚═══██╗██╔═══╝░██║░░░░░██║░░░██║░░░░░░██║░░░██╔══╝░░██╔══██╗
░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║  ██████╔╝██║░░░░░███████╗██║░░░██║░░░░░░██║░░░███████╗██║░░██║
░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝"""

# Prints the logo
def printLogo():
    print(Center.XCenter(Colorate.Horizontal(Colors.white_to_red, logo, 1)))

# Shit for the cookies
def get_dcf_sdc(cookie):
    sep = cookie.split(";")
    sx = sep[0]
    sx2 = sx.split("=")
    dcf = sx2[1]

    split = sep[6]
    split2 = split.split(",")
    split3 = split2[1]
    split4 = split3.split("=")
    sdc = split4[1]

    return dcf, sdc

# Headers
def http_headers(token):
    cookie = httpx.get("https://discord.com/register").headers['set-cookie']
    dcf, sdc = get_dcf_sdc(cookie)
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.263 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
        "Referer": "https://discord.com/register",
        "Authorization": token,
        "X-Super-Properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMC4xNDsgcnY6ODguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC84OC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiODguMCIsIm9zX3ZlcnNpb24iOiIxMC4xNCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5MTczNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
        "X-Fingerprint": '873691818078920745.AdL-Gi4qePqVs4lEO8acceJAgxc',
        "Cookie": f"__dcfduid={dcf}; __sdcfduid={sdc}; OptanonConsent=isIABGlobal=false&datestamp=Mon+Aug+09+2021+04%3A31%3A04+GMT%2B0300+(Arabian+Standard+Time)&version=6.17.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2Floggin&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _gcl_au=1.1.62729347.1628472664; _ga=GA1.2.1942394829.1628472665; _gid=GA1.2.2001024037.1628472665",
        "DNT": "1",
        "Connection": "keep-alive"
    }

# Getting guilds
def getGuilds(tokens):
    global tokenCount, filled, empty, error
    with open(f'input/tokens.txt', 'a') as f:
        for token in tokens:
            tokenCount += 1
            headers = http_headers(token)
            while True:
                try:
                    e = httpx.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
                    break
                except:
                    pass
            if e.status_code == 200:
                json_response = e.json()
                if len(e.json()) >= amount:
                    print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET}Token {tokenCount} has {len(e.json())} guilds")
                    filled += 1
                    with open(f'output/filled.txt', 'a') as f:
                            try:
                                f.write(token + "\n")
                            except:
                                pass
                else:
                    print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}Token {tokenCount} has {len(e.json())} guilds")
                    empty += 1
                    with open(f'output/empty.txt', 'a') as f:
                        try:
                            f.write(token + "\n")
                        except:
                            pass
            else:
                print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}Token {tokenCount} is invalid! Skipping...")
                error += 1
                with open(f'output/error.txt', 'a') as f:
                    try:
                        f.write(token + "\n")
                    except:
                        pass
            os.system(f"title Token Splitter - Status: {tokenCount}/{len(tokens)} - Checked: {tokenCount} - Filled: {filled} - Empty: {empty} - Error: {error}")

# Split and upload them to the vps'set
def vpsUpload():
    global uploadCount
    # You can add/remove as many as you want keeping the format.
    vps_list = [
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},]

    tokens = open("output/filled.txt", "r").read().splitlines()

    length = len(tokens)
    split = int(length / vps_count)
    for i in range(vps_count):
        with open("vps/vps" + str(i) + ".txt", "w") as f:
            for j in range(split):
                f.write(tokens[i * split + j] + "\n")

    for vps in vps_list:
        uploadCount += 1
        try:
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, f"Starting upload of vps {uploadCount} tokens...", 1)))
            ip = vps["ip"]
            username = vps["username"]
            password = vps["password"]
            vps = paramiko.SSHClient()
            vps.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            vpsTransport = paramiko.Transport((ip, 22))
            vpsTransport.connect(username=username, password=password)
            vpsSFTP = paramiko.SFTPClient.from_transport(vpsTransport)
            vpsSFTP.put(f'{scriptDir}/vps/vps{uploadCount}.txt', f'/root/tokens.txt')
            vpsSFTP.close()
            vpsTransport.close()
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, f"Upload of vps {uploadCount} tokens completed!", 1)))
        except Exception as e:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: " + str(e))
            input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
            exit()

# Checking for folders, files existing and file integrity
try:
    clear()
    printLogo()
    print(f"{Fore.MAGENTA}[{Fore.RESET}INFO{Fore.MAGENTA}]{Fore.RESET} Checking files...")
    try:
        config = toml.load("config.toml")
    except:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}Could not load the config.toml file.")
        input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
        exit()
    try:
        amount = config["amount"]
    except:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}Missing value for amount")
        input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
        exit()
    try:
        vps_count = config["vps_count"]
    except:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}Missing value for vps_count")
        input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
        exit()

    if not os.path.exists("input"):
        os.mkdir("input")
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Input folder already exists.")

    if not os.path.exists("output"):
        os.mkdir("output")
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Output folder already exists.")

    if not os.path.exists("vps"):
        os.mkdir("vps")
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} VPS folder already exists.")

    if not os.path.exists("input/tokens.txt"):
        with open("input/tokens.txt", "w") as f:
            f.write("")
            f.close()
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} input/tokens.txt already exists.")

    if not os.path.exists("output/filled.txt"):
        with open("output/filled.txt", "w") as f:
            f.write("")
            f.close()
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} output/filled.txt already exists.")

    if not os.path.exists("output/empty.txt"):
        with open("output/empty.txt", "w") as f:
            f.write("")
            f.close()
    else:
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} output/empty.txt already exists.")
    
    with open("input/tokens.txt", "r") as f:
        try:
            lines = f.read().splitlines()
            lines = len(lines)
            lines = int(lines)
            if lines < 1 or lines == "":
                print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} No tokens found in input/tokens.txt")
                input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
                exit()
        except Exception as e:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: " + str(e))
            input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
            exit()
    # Load the tokens
    try:
        tokens = []
        with open('input/tokens.txt', 'r') as f:
            for i in f:
                tokens.append(i.split(' | ')[0].strip())
        tokens = list(set(tokens))
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: " + str(e))
        input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
        exit()
    clear()
    printLogo()
    print(f"\n{Fore.MAGENTA}[{Fore.RESET}INFO{Fore.MAGENTA}]{Fore.RESET} Getting token guilds!\n")
    getGuilds(tokens)
    print(f"\n{Fore.MAGENTA}[{Fore.RESET}INFO{Fore.MAGENTA}]{Fore.RESET} Done getting guilds!")
    time.sleep(1)
    # Split the tokens into text files for each vps to save time
    print(f"{Fore.MAGENTA}[{Fore.RESET}INFO{Fore.MAGENTA}]{Fore.RESET} Splitting tokens for each vps and uploading them to the vps!")
    try:
        vpsUpload()
    except Exception as e:
        print("Something went wrong. Please try again. Error: " + str(e))
        input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
        exit()
    print(f"{Fore.MAGENTA}[{Fore.RESET}INFO{Fore.MAGENTA}]{Fore.RESET} Done splitting tokens and uploading! Finished.")
    input(f"\n{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
    exit()
# Catch errors and exit
except Exception as e:
    print("Something went wrong. Please try again. Error: " + str(e))
    input(f"{Fore.YELLOW}[{Fore.RESET}-{Fore.YELLOW}]{Fore.RESET} Press any key to exit...")
    exit()