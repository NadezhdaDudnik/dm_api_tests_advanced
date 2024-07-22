from datetime import datetime

from hamcrest import (
    assert_that,
    has_properties,
    has_key,
    starts_with,
    equal_to,
    instance_of,
    has_property,
)


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
    ):
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
        # with soft_assertions():
        #     today = datetime.now().strftime('%Y-%m-%d')
        #     assert_that(str(response.resource.registration).startswith(today))
        #     assert_that(str(response.resource.online).startswith(today))
