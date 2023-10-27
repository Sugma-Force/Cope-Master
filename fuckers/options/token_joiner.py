from fuckers import *

@dataclass
class JoinerData:
    pass

@dataclass
class Instance(JoinerData):
    client: tls_client.sessions
    token: str
    invite: str
    headers: dict

class Joiner:
    def __init__(self, data:Instance) -> None:
        self.session = data.client
        self.session.headers = data.headers
        self.get_cookies()
        self.instance = data

    def get_cookies(self) -> None:
        site = self.session.get("https://discord.com")
        self.session.cookies = site.cookies

    def join(self) -> None:
        self.session.headers.update({"Authorization":self.instance.token})
        result = self.session.post(f"https://discord.com/api/v9/invites/{self.instance.invite}",json={
            'session_id': utility.rand_str(32),
        })
        utility.logger(self.instance.token, result.text, result.status_code)

class intilize:
    def start(i):
        Joiner(i).join()

def token_joiner(invite=None):
    tokens = TokenManager.get_tokens()

    if not tokens:
        Output("bad").log(f"No Tokens")
        time.sleep(2)
        return

    instances = []
    max_threads=10
    invite = invite.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "").replace("https://discord.com/invite/", "")
    # Fire code i know

    req = requests.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
    if req.status_code == 200:
        res = req.json()
        Output("info").log(f"Joining {Fore.RED}{res['guild']['name']}")
    else:
        pass

    for i in range(len(tokens)):
        header = headers
        instances.append(Instance(
            client=tls_client.Session(
            client_identifier=f"chrome_{random.randint(110,116)}",
            random_tls_extension_order=True
        ),
            token=tokens[i],
            headers=header,
            invite=invite
        ))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i in instances:
            executor.submit(intilize.start, i)