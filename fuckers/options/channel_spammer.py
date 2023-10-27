from fuckers import *
def send(token, message, channel_id, amount=None):
    try:
        session = tls_session()
        while True:
            try:
                content = f"{message} {utility.get_random_id(int(amount))} {utility.rand_str(9)}"

                data = {'session_id': utility.rand_str(32), "content": content}
                session.headers = headers
                session.headers.update({"Authorization":token})
                result = session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=data)
                utility.logger(token, result.text, result.status_code)
            except Exception as e:
                print(f"{e}")
    except Exception as e:
        print(f"{e}")

def channel_spammer(guild_id, channel_id, message, amount):
    args = []
    tokens = TokenManager.get_tokens()

    if tokens is None:
        return

    id_scraper(guild_id, channel_id)

    max_threads = 13

    while True:
        if tokens:
            def thread_send(token):
                try:
                    token = TokenManager.OnlyToken(token)
                    args = [token, message, channel_id, amount]
                    send(*args)
                except Exception as e:
                    print(f"{e}")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=thread_send, args=(token,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        else:
            return