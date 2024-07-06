from array import array
from datetime import datetime
from assertpy import (
    assert_that,
    soft_assertions,
)

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

from dm_api_account.models.user_details_envelope import UserRole


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
    ):
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
        # with soft_assertions():
        #     today = datetime.now().strftime('%Y-%m-%d')
        #     assert_that(str(response.resource.registration).startswith(today))
        #     assert_that(str(response.resource.online).startswith(today))
