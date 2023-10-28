from fuckers import *

def captcha_joiner(invite=None):
    args = []
    tokens = TokenManager.get_tokens()

    def runJoiner(token, invite):
        retry, rqdata, rqtoken = join(token, invite, "","")
        if retry:
            proxy = "http://" + ProxyManager.clean_proxy(ProxyManager.random_proxy())
            solver = Captcha(proxy=proxy, siteKey="b2b02ab5-7dae-4d6f-830e-7b55634c888b", siteUrl="https://discord.com/", rqdata=rqdata)
            Output("cap").log(f'Solving Captcha...')
            capkey = solver.solveCaptcha()
            if capkey is not None:
                Output("cap").log(f"Solved Captcha -> {Fore.LIGHTBLACK_EX} {capkey[:70]}")
            else: 
                Output("bad").log(f"Failed To Solve Captcha -> {Fore.LIGHTBLACK_EX} {capkey}")
            join(token, invite, capkey, rqtoken)

    def join(token, invite, capkey, rqtoken):
        session = tls_session()
        session.headers = headers
        session.headers.update({"Authorization":token})

        if capkey != "":
            session.headers.update({"x-captcha-key":capkey})
            session.headers.update({"x-captcha-rqtoken":rqtoken})
            
        if capkey != "":
            data = {
                "captcha_key": capkey,
                "captcha_rqtoken": rqtoken,
                "session_id": utility.rand_str(32),
            }  
        else:
            data = {"session_id": utility.rand_str(32),}


        result = session.post(f"https://discord.com/api/v9/invites/{invite}", json=data)

        if result.text.startswith('{"captcha_key"'):
            Output("bad").log(f"Error -> {token[:60]} {Fore.LIGHTBLACK_EX}({result.status_code}) {Fore.RED}(Captcha)")
            return True, result.json()["captcha_rqdata"], result.json()["captcha_rqtoken"]
        else:
            utility.logger(token, result.text, result.status_code)
            return False, None, None 

        return False
        
    def thread_complete(future):
        try:
            result = future.result()
        except Exception as e:
            if "failed to do request" in str(e):
                message = f"Proxy Error -> {str(e)[:80]}..."
            else:
                message = f"Error -> {e}"
            Output("bad").log(message)

    if tokens is None:
        return

    invite = invite.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "").replace("https://discord.com/invite/", "")
    max_threads = 15

    req = requests.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
    if req.status_code == 200:
        res = req.json()
        Output("info").log(f"Joining {Fore.MAGENTA}{res['guild']['name']}")
    else:
        pass

    if tokens:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            for token in tokens:
                try:
                    token = TokenManager.OnlyToken(token)
                    args = [token, invite]
                    future = executor.submit(runJoiner, *args)
                    future.add_done_callback(thread_complete)
                    time.sleep(0.1)
                except Exception as e:
                    Output("bad").log(f"{e}")
    else:
        return
