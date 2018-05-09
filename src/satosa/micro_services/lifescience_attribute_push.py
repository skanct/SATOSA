import re
import logging

from .base import ResponseMicroService
from ..exception import SATOSAAuthenticationError
from ..util import get_dict_defaults
from ..logging_util import satosa_logging

logger = logging.getLogger(__name__)

class LifeScienceAttributePush(ResponseMicroService):
    """
    LifeScience attributes pusher.
    A work in progress story
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_attributes = config["static_attributes"]
        self.whitelist_idp = config["whitelist_idp"]

    def process(self, context, data):
        if data.attributes in self.whitelist_idp:
            satosa_logging(logger, logging.DEBUG, "Pushing attributes for mail %s" % data.attributes.get("mail")[0], context.state)
            data.attributes.update(self.static_attributes)
            return super().process(context, data)
        satosa_logging(logger, logging.DEBUG, "Attribute not pushed for user %s" % data.attributes.get("mail")[0],, context.state)
        return super().process(context, data)
