import requests


class ADAuthentication:
    def __init__(self, auth_url):
        self.auth_url = auth_url

    def authenticate(self, email, password):
        payload = {'username': email, 'password': password}
        authenticated = False
        try:
            res = requests.get(self.auth_url,
                               params=payload, timeout=30)
            if res.status_code == 200:
                res_text = res.text.upper()
                authenticated = (res_text == 'TRUE')
            return authenticated
        except Exception:
            return authenticated
