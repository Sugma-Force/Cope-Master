from colorama import Fore
import concurrent.futures
import random
import string
from dataclasses import dataclass
from datetime import datetime
import pystyle
import os
import tls_client
import re
import time
import json
import requests

# static headers :skull: since this project wont be maintained...
headers = {
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'en-US',
    'x-discord-timezone': 'Europe/Stockholm',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
}
class Output:
    def __init__(this, level):
        this.level = level
        this.color_map = {
            "info": (Fore.BLUE, "[*]"),
            "bad": (Fore.RED, "[-]"),
            "good": (Fore.GREEN, "[+]")
        }

    def log(this, *args, **kwargs):
        color, text = this.color_map.get(this.level, (Fore.LIGHTWHITE_EX, this.level))
        time_now = datetime.now().strftime("%H:%M:%S")

        base = f"{Fore.MAGENTA}│{Fore.BLUE}{time_now}{Fore.MAGENTA}│ {color}{text.upper()}"
        for arg in args:
            base += f" {arg}"

        if kwargs:
            for key, value in kwargs.items():
                base += f" {key}={value}"
        print(base)

class ProxyManager:
    def get_proxies():
        with open("proxies.txt", "r") as f:
            proxies = f.read().strip().splitlines()
        proxies = [proxy for proxy in proxies if proxy not in [" ", "", "\n"]]
        return proxies
        
    def random_proxy():
        try:
            return random.choice(ProxyManager.get_proxies())
        except:
            return {}

    def clean_proxy(proxy):
        if isinstance(proxy, str):
            parts = proxy.split(':')
            if '@' in proxy or len(parts) == 2:
                return proxy
            elif len(parts) == 4:
                return f'{parts[2:]}@{parts[:2]}'
            elif '.' in parts[0]:
                return f'{parts[2:]}@{parts[:2]}'
            else:
                return f'{parts[:2]}@{parts[2:]}'
        elif isinstance(proxy, dict):
            http_proxy = proxy.get("http") or proxy.get("https")
            https_proxy = proxy.get("https") or proxy.get("http")
            if http_proxy or https_proxy:
                return {
                    "http://": http_proxy,
                    "https://": https_proxy
                }
            elif proxy in [dict(), {}]:
                return {}
        return proxy
    
    def client_proxy():
        proxy = ProxyManager.clean_proxy(ProxyManager.random_proxy())
        if isinstance(proxy, str):
            proxy_dict = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        elif isinstance(proxy, dict):
            proxy_dict = proxy

        return proxy_dict

class TokenManager:
    @classmethod
    def get_tokens(cls):
        with open("tokens.txt", "r") as f:
            tokens = f.read().strip().splitlines()
        tokens = [token for token in tokens if token not in [" ", "", "\n"]]
        return tokens

    @staticmethod
    def OnlyToken(tokenn):
        r = re.compile(r"(.+):(.+):(.+)")
        if r.match(tokenn):
            return tokenn.split(":")[2]
        else:
            token = tokenn
        return token
    
    @classmethod
    def get_random_token(cls):
        tokens = cls.get_tokens()
        if tokens:
            return random.choice(tokens)
        else:
            return None

def extract_token():
    with open("tokens.txt", 'r') as file:
        lines = file.readlines()

    new_tokens = [TokenManager.OnlyToken(line.strip()) for line in lines]

    with open("tokens.txt", 'w') as file:
        for token in new_tokens:
            file.write(token + '\n')
extract_token()
def tls_session() -> tls_client.Session:
    client = tls_client.Session(
        client_identifier=f"chrome_{random.randint(110, 116)}",
        random_tls_extension_order=True
    )

    proxy = ProxyManager.clean_proxy(ProxyManager.random_proxy())
    if isinstance(proxy, str):
        proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    elif isinstance(proxy, dict):
        proxy_dict = proxy
    client.proxies = proxy_dict
    
    return client

class utility:
    def logger(token, res_text, res_status_code):
        # Fire code!!!!
        if res_status_code == 200:
            Output("good").log(f"Success -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code})")
        elif res_status_code == 429:
            passDecimal
        elif res_text.startswith('{"captcha_key"'):
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(Captcha)")
        elif res_text.startswith('{"message": "401: Unauthorized'):
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(Unauthorized)")
        elif "Cloudflare" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(CloudFlare Blocked)")
        elif "\"code\": 40007" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(Token Banned)")
        elif "\"code\": 40002" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(Locked Token)")
        elif "\"code\": 10006" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}(Invalid Invite)")
        elif "\"code\": 50001:" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX } {res_status_code}) {Fore.RED}(No Access)")
        elif "\"code\": 50013:" in res_text:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX } {res_status_code}) {Fore.RED}(No Access)")
        else:
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({res_status_code}) {Fore.RED}({res_text})")
    
    def rand_str(length:int) -> str:
        return ''.join(random.sample(string.ascii_lowercase+string.digits, length))
    
    def get_random_id(id):
        with open("scraped.txt", "r", encoding="utf8") as f:
            users = [line.strip() for line in f.readlines()]
        randomid = random.sample(users, id)
        return "<@" + "> <@".join(randomid) + ">"
    
    def get_ids():
        with open("scraped.txt", "r") as f:
            ids = f.read().strip().splitlines()
        ids = [idd for idd in ids if idd not in [" ", "", "\n"]]
        return ids