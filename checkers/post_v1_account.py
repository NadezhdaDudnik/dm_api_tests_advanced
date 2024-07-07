from datetime import datetime

import allure
from assertpy import assert_that

from hamcrest import (
    has_property,
    all_of,
    instance_of,
    has_properties,
    equal_to,
    assert_that,
)


class PostV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
    ):
        with allure.step("Проверка ответа"):
            today = datetime.now().strftime('%Y-%m-%d')
            # assert_that(str(response.resource.registration).startswith(today))
            assert_that(
                response, all_of(
                    has_property('resource', has_property('registration', instance_of(datetime))),
                    has_property(
                        'resource', has_properties(
                            {
                                'rating': has_properties(
                                    {
                                        "enabled": equal_to(True),
                                        "quality": equal_to(0),
                                        "quantity": equal_to(0)
                                    }
                                )
                            }
                        )
                    )
                )
            )
