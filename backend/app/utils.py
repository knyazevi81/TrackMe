import jwt
from datetime import datetime
import os
import dotenv
import requests
from requests.exceptions import JSONDecodeError

from config import Settings, dotenv_path



def is_expire(token: str):
    """
    Функция для проверки access_token на подлинность
    """
    token_data = jwt.decode(token, options={"verify_signature": False})
    exp = datetime.utcfromtimestamp(token_data["exp"])
    now = datetime.utcnow()
    return now >= exp


def save_tokens(access_token: str, refresh_token: str):
    """
    функция для перезаписи access и refresh токена
    """
    os.environ["AMOCRM_ACCESS_TOKEN"] = access_token
    os.environ["AMOCRM_REFRESH_TOKEN"] = refresh_token
    dotenv.set_key(dotenv_path, "AMOCRM_ACCESS_TOKEN", os.environ["AMOCRM_ACCESS_TOKEN"])
    dotenv.set_key(dotenv_path, "AMOCRM_REFRESH_TOKEN", os.environ["AMOCRM_REFRESH_TOKEN"])


def get_new_tokens():
    """
    Функция для получения новой пары токенов при истечении срока действия access_token
    """
    
    data = {
            "client_id": Settings.client_id,
            "client_secret": Settings.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": get_refresh_token(),
            "redirect_uri": Settings.redirect_uri
    }
    response = requests.post(f"https://{Settings.subdomain}.amocrm.ru/oauth2/access_token", json=data).json()
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]

    save_tokens(access_token, refresh_token)


def get_refresh_token():
    return os.getenv("AMOCRM_REFRESH_TOKEN")


def get_access_token():
    return os.getenv("AMOCRM_ACCESS_TOKEN")


class AmoCRMWrapper:
    def init_oauth2(self):
        data = {
            "client_id": Settings.client_id,
            "client_secret": Settings.client_secret,
            "code": Settings.secret_code,
            "grant_type": "authorization_code",
            "redirect_uri": Settings.redirect_uri
        }

        response = requests.post(f"https://{Settings.subdomain}.amocrm.ru/oauth2/access_token", json=data)
        
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]

            save_tokens(access_token, refresh_token)
        else:
            pass
            #print(response.json())
    
    def _base_request(self, **kwargs):
        if is_expire(get_access_token()):
            get_new_tokens()

        access_token = "Bearer " + get_access_token()

        headers = {"Authorization": access_token}
        req_type = kwargs.get("type")

        if req_type == "get":
            try:
                response = requests.get("https://{}.amocrm.ru{}".format(
                    Settings.subdomain, kwargs.get("endpoint")), headers=headers).json()
            except JSONDecodeError as e:
                print(e)

        elif req_type == "get_param":
            url = "https://{}.amocrm.ru{}?{}".format(
                Settings.subdomain,
                kwargs.get("endpoint"), kwargs.get("parameters"))
            response = requests.get(str(url), headers=headers).json()

        elif req_type == "post":
            response = requests.post("https://{}.amocrm.ru{}".format(
                Settings.subdomain,
                kwargs.get("endpoint")), headers=headers, json=kwargs.get("data")).json()
        
        return response

    #def get_lead_by_id(self, lead_id):
    #    url = "/api/v4/leads/" + str(lead_id)
    #    return self._base_request(endpoint=url, type="get")
    
    def get_tasks(self):
        url = "/api/v4/tasks"
        data = self._base_request(endpoint=url, type="get")#["_embedded"]["tasks"]
        return data


if __name__== "__main__":
    amocrm_wrapper_1 = AmoCRMWrapper() 
    amocrm_wrapper_1.init_oauth2()
    print(amocrm_wrapper_1.get_tasks())
    