import re

from .base import ResponseMicroService
from ..exception import SATOSAAuthenticationError
from ..util import get_dict_defaults


class LifeScienceAttributePush(ResponseMicroService):
    """
    LifeScience attributes pusher.
    A work in progress story
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_attributes = config["static_attributes"]
        self.attribute_allow = config.get("attribute_allow", {})

    def process(self, context, data):
        for attribute_name, attribute_filters in get_dict_defaults(self.attribute_allow, data.requester, data.auth_info.issuer).items():
            if attribute_name in data.attributes:
                if any([any(filter(re.compile(af).search, data.attributes[attribute_name])) for af in attribute_filters]):
		    data.attributes.update(self.static_attributes)
                    return super().process(context, data)
        return super().process(context, data)

