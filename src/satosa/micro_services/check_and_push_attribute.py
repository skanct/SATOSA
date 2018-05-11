import re
import logging
import urllib.parse
from urllib.request import urlopen
import xml.etree.ElementTree
from .base import ResponseMicroService
from ..exception import SATOSAAuthenticationError
from ..util import get_dict_defaults
from ..logging_util import satosa_logging

logger = logging.getLogger(__name__)

class CheckAndPushAttribute(ResponseMicroService):
    """
    LifeScience attributes pusher.
    A work in progress story
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_attributes = config["static_attributes"]
        self.whitelist_idp = config["whitelist_idp"]
        self.cp_webname = config["cp_webname"]
        self.attribute_value_to_search = config["attribute_value_to_search"]

    def process(self, context, data):
        #Check if issuer is inside whitelist
        if self.whitelist_idp:
            if data.auth_info.issuer in self.whitelist_idp:
                satosa_logging(logger, logging.DEBUG, "IdP in whitelist. Pushing attributes for %s" % data.attributes.get("mail")[0], context.state)
                data.attributes.update(self.static_attributes)
                return super().process(context, data)

        #Check if Issuer have desider value
        mdq_url = self.cp_webname + "/entities/" + urllib.parse.quote(data.auth_info.issuer, safe='')
        e = xml.etree.ElementTree.parse(urlopen(mdq_url)).getroot()
        iterator = e.getiterator()
        for key in iterator:
            if key.text in self.attribute_value_to_search:
                satosa_logging(logger, logging.DEBUG, "Founded attribute value. Pushing attributes for %s" % data.attributes.get("mail")[0], context.state)
                data.attributes.update(self.static_attributes)
                return super().process(context, data)

        satosa_logging(logger, logging.DEBUG, "Attribute not pushed for user %s" % data.attributes.get("mail")[0], context.state)
        return super().process(context, data)
