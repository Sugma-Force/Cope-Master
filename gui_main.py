from fuckers import *
# CopeMaster GUI cuz why not? 

class gui():
    def make_menu(*options):
        for num, option in enumerate(options, start=1):
            label = pystyle.Center.XCenter(f"{Fore.MAGENTA}[{Fore.BLUE}{num}{Fore.MAGENTA}] {Fore.MAGENTA}{option}")
            print(label)

    def get_tokens():
        with open("tokens.txt", "r") as f:
            tokens = f.read().strip().splitlines()
        tokens = [token for token in tokens if token not in [" ", "", "\n"]]
        return tokens
    
    def get_proxies():
        with open("proxies.txt", "r") as f:
            proxies = f.read().strip().splitlines()
        proxies = [proxy for proxy in proxies if proxy not in [" ", "", "\n"]]
        return proxies

    def joiner_menu():
        gui.main_title(show=False)
        invite = str(input(pystyle.Center.XCenter("Invite: ", 30)))
        print()
        gui.make_menu("Normal Joiner", "Capsolver Joiner")
        choice = str(input(pystyle.Center.XCenter("Choice: ", 30)))
        if choice == "1":
            token_joiner(invite)
        else:
            captcha_joiner(invite)
        gui.main_menu()
    
    def spammer_menu():
        gui.main_title(show=False)
        guild_id = str(input(pystyle.Center.XCenter("Guild ID: ", 30)))
        channel_id = str(input(pystyle.Center.XCenter("Channel ID: ", 30)))
        message = str(input(pystyle.Center.XCenter("Message: ", 30)))
        amount = int(input(pystyle.Center.XCenter("Amount Of Pings (0 For None): ", 30)))
        channel_spammer(guild_id, channel_id, message, amount)
    
    def raider():
        gui.main_title(show=False)
        invite = str(input(pystyle.Center.XCenter("Invite: ", 30)))
        token_joiner(invite)
        os.system("cls")
        gui.main_title(show=False)
        req = requests.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
        if req.status_code == 200:
            res = req.json()
            guild_id = res['guild']['id']
        else:
            guild_id = str(input(pystyle.Center.XCenter("Guild ID: ", 30)))
        channel_id = str(input(pystyle.Center.XCenter("Channel ID: ", 30)))
        message = str(input(pystyle.Center.XCenter("Message: ", 30)))
        amount = int(input(pystyle.Center.XCenter("Amount Of Pings (0 For None): ", 30)))
        channel_spammer(guild_id, channel_id, message, amount)

    def main_title(show=True):
        os.system("cls")
        
        options = f"[1] Server Joiner | [2] Channel Spammer | [3] Full Raider\n\n\n"
        counter = f"Tokens: {len(gui.get_tokens())} | Proxies: {len(gui.get_proxies())}\n\n\n"
        
        ascii = f"""
  _____              __  ___         __         
 / ___/__  ___  ___ /  |/  /__ ____ / /____ ____
/ /__/ _ \/ _ \/ -_) /|_/ / _ `(_-</ __/ -_) __/
\___/\___/ .__/\__/_/  /_/\_,_/___/\__/\__/_/   
        /_/                                         
"""
        ascii = pystyle.Center.XCenter(ascii)
        ascii = pystyle.Colorate.Horizontal(pystyle.Colors.red_to_blue, ascii)

        options = pystyle.Center.XCenter(options)
        options = pystyle.Colorate.Horizontal(pystyle.Colors.red_to_blue, options)
        counter = pystyle.Center.XCenter(counter)
        counter = pystyle.Colorate.Horizontal(pystyle.Colors.red_to_blue, counter)
        if show == True:
            print(ascii + "\n\n" + counter + "\n\n" + options)
        else:
            print(ascii + "\n\n" + counter)

    def main_menu():
        os.system("cls")
        os.system("title Cope Master")
        gui.main_title()
        choice = str(input(pystyle.Center.XCenter("Choice: ", 30))).lstrip("0")
        choice = choice.upper()

        try:
            options = {
                '1': gui.joiner_menu,
                '2': gui.spammer_menu,
                '3': gui.raider
            }
            choosen = options.get(choice)
            if choosen:
                choosen()
                time.sleep(1)
            else:
                Output("bad").log("Invalid choice, please try again!")
                time.sleep(1)

        except Exception as e:
            Output("bad").log(f"{e}")
            input()

        gui.main_menu()

if __name__ == "__main__":
    os.system('cls')
    extract_token()
    gui.main_menu()
