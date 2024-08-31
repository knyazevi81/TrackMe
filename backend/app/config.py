from dotenv import load_dotenv
import os
import datetime
#from pydantic_settings import BaseSettings
from dataclasses import dataclass

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


load_dotenv(dotenv_path)

@dataclass
class Settings:
    # amo integration
    subdomain: str = os.getenv("AMOCRM_SUBDOMAIN")
    client_id: str = os.getenv("AMOCRM_CLIENT_ID")
    client_secret: str = os.getenv("AMOCRM_CLIENT_SECRET")
    redirect_uri: str = os.getenv("AMOCRM_REDIRECT_URL")
    secret_code: str = "def50200a4578daa28031a5713e96c4488878802929aebcac4cc1544b05ed4430bbe2ef9d5867b030cb881179f5daef29837461e505067214597d0dc614eb2b59c59515f33301e7508c6301e41363c523921968591f7a075c363fd7339c42f15943f8effff1de000e7649993755621bef7a2485adcf83fd6bc3070f65db95103f40d694e00803e09eb7c8ec0ae62c33b1220ae687523f6520df8e44231f958f66a956b669b5ecdc4c76b9137142b1f800660ea50da03d7a319b985c6cd30ac4fadd590c73f4a47c6244ca0b7aca16ad0840ea34eba45b3c4050c292bd00838df5c32198be2c1ed91d2efe0a39449d85b8c7465d41d99de8b2c92ad6eaa9009b000b4c8c5945363d243b5bfaba8fac6a0e642774e56a2adf6890cb3078b98e920455af1e02be346d90cb96bbd8fea0015d840a1d616159943bb8918789183b8800e57fccc470ddfe140637b597212981da6bcdad21bc6e0f692dc6a5af3805de264f50afb2416d6dc3ba7ca28f10d4fa16f832fa322dc8a4d6577b474c38eddb8d3105cd111c384511ec908e40e8f51d5272b584edef9fb40d6ab40790248872448f4bc48a133a15125df60d2a10d7409da378c733ebbd93e31a97dadf1937b871ce2caee3f5efce1e649d34ae14d2a7990f1c730b2b30f519f07da7f940f"
    # project
    secret_token: str = os.getenv("SECRET_AUTH_TOKEN")
    token_expire_minutes = 30
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
