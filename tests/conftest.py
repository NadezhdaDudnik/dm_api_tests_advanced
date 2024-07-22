from collections import namedtuple
from datetime import datetime
from pathlib import Path
from vyper import v

import pytest
from faker import Faker

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.utilities import allure_attach
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog
import json
import re

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4, ensure_ascii=True
            # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.password'
)

def mask_string(string, keys_to_mask):
    for key in keys_to_mask:
        string = re.sub(rf'({key}=)([^&]+)', rf'\1*****', string)
    return string

def mask_user_data(user):
    keys_to_mask = ['login', 'password', 'email', 'change_email', 'change_password']
    return namedtuple(
        "User", ["login", "password", "email", "change_email", "change_password"]
    )(
        login=mask_string(user.login, keys_to_mask),
        password=mask_string(user.password, keys_to_mask),
        email=mask_string(user.email, keys_to_mask),
        change_email=mask_string(user.change_email, keys_to_mask),
        change_password=mask_string(user.change_password, keys_to_mask)
    )

@pytest.fixture(scope='session', autouse=True)
def set_config(
        request
        ):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


def pytest_addoption(
        parser
        ):
    parser.addoption("--env", action="store", default='stg', help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"))
    mailhog_client = MailHogApi(mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    return account

@pytest.fixture(scope="function")
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
    password = v.get("user.password")
    change_password = '2355227413'
    email = f'{login}@mail.ru'
    change_email = f'{login}7@mail.ru'

    User = namedtuple("User", ["login", "password", "email", "change_email", "change_password"])
    user = User(login=login, password=password, email=email, change_email=change_email, change_password=change_password)
    return mask_user_data(user)


@pytest.fixture(scope="function")
def auth_account_helper(
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    return account_helper
