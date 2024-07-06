from datetime import datetime

from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
    only_contains,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    account_helper.auth_client(
        login=login,
        password=password
    )
    with check_status_code_http():
        response = account_helper.dm_account_api.account_api.get_v1_account()
        assert_that(
            response, all_of(
                has_property(
                    'resource', has_properties(
                        {
                            'settings': has_properties(
                                {
                                    "colorSchema": starts_with("Modern"),
                                    'paging': has_properties(
                                        {
                                            "postsPerPage": equal_to(10),
                                            "commentsPerPage": equal_to(10),
                                            "topicsPerPage": equal_to(10),
                                            "messagesPerPage": equal_to(10),
                                            "entitiesPerPage": equal_to(10)
                                        }
                                    )
                                }
                            ),
                            'login': login,
                            'roles': all_of(
                                only_contains(
                                    UserRole.GUEST,
                                    UserRole.PLAYER,
                                )
                            ),
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            ),
                            'online': instance_of(datetime),
                            'registration': instance_of(datetime),
                        }
                    )
                )
            )
        )


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
