from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


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
    response = account_helper.dm_account_api.account_api.get_v1_account()
    resource = response.resource

    assert_that(
        resource,
        has_properties(
            {
                "info": equal_to(""),
                "settings": has_properties(
                    {
                        "color_schema": starts_with("Modern"),
                        'paging': has_properties(
                            {
                                "posts_per_page": equal_to(10),
                                "comments_per_page": equal_to(10),
                                "topics_per_page": equal_to(10),
                                "messages_per_page": equal_to(10),
                                "entities_per_page": equal_to(10)
                            }
                        )
                    }
                ),
                "roles": equal_to(["Guest", "Player"]),
                "rating": has_properties(
                    {
                        "enabled": equal_to(True),
                        "quality": equal_to(0),
                        "quantity": equal_to(0)
                    }
                ),
                "online": instance_of(datetime),
                "registration": instance_of(datetime)
            }
        )
    )

    assert_that(resource, has_property('info'))
    assert_that(resource, has_property('settings'))
    assert_that(resource, has_property('roles'))
    assert_that(resource, has_property('rating'))
    assert_that(resource, has_property('online'))
    assert_that(resource, has_property('registration'))


    # assert_that(
    #     response, all_of(
    #         has_property(
    #             'resource', has_properties(
    #                 {
    #                     'settings': has_properties(
    #                         {
    #                             "colorSchema": starts_with("Modern"),
    #                             'paging': has_properties(
    #                                 {
    #                                     "postsPerPage": equal_to(10),
    #                                     "commentsPerPage": equal_to(10),
    #                                     "topicsPerPage": equal_to(10),
    #                                     "messagesPerPage": equal_to(10),
    #                                     "entitiesPerPage": equal_to(10)
    #                                 }
    #                             )
    #                         }
    #                     ),
    #                     'login': login,
    #                     'roles': all_of(
    #                         only_contains(
    #                             UserRole.GUEST,
    #                             UserRole.PLAYER,
    #                         )
    #                     ),
    #                     'rating': has_properties(
    #                         {
    #                             "enabled": equal_to(True),
    #                             "quality": equal_to(0),
    #                             "quantity": equal_to(0)
    #                         }
    #                     ),
    #                     'online': instance_of(datetime),
    #                     'registration': instance_of(datetime),
    #                 }
    #             )
    #         )
    #     )
    # )

    with check_status_code_http():
        response = account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values(response)



def test_get_v1_account_no_auth(
        auth_account_helper
):

    with check_status_code_http(401, 'User must be authenticated'):
        auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
