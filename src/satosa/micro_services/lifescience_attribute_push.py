import re

from .base import ResponseMicroService


class LifeScienceAttributePush(ResponseMicroService):
    """
    LifeScience attributes pusher.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_attributes = config["static_attributes"]

    def process(self, context, data):
        data.attributes.update(self.static_attributes)
        return super().process(context, data)
