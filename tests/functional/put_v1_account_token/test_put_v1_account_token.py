from json import loads

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

from faker import Faker


def test_put_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    mailhog = MailHogApi(mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    fake = Faker("en_US")
    login = fake.first_name_female() + '12345'
    password = '123456789'
    email = f'{login}@mail.ru'
    account_helper.register_new_user(login=login, password=password, email=email)