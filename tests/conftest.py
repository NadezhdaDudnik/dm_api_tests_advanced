from collections import namedtuple
from datetime import datetime

import pytest
from faker import Faker

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4, ensure_ascii=True
            # sort_keys=True
        )
    ]
)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    return account




@pytest.fixture(scope="session")
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    fake = Faker("en_US")
    login = fake.first_name_female() + f'{data}'
    password = '123456789'
    change_password = '2355227413'
    email = f'{login}@mail.ru'
    change_email = f'{login}7@mail.ru'

    User = namedtuple("User", ["login", "password", "email", "change_email", "change_password"])
    user = User(login=login, password=password, email=email, change_email=change_email, change_password=change_password)
    return user

@pytest.fixture(scope="session")
def auth_account_helper(
        mailhog_api
        ):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    #account_helper.auth_client(
     #   login=prepare_user.us,
      #  password=prepare_user.password
   # )
    return account_helper
