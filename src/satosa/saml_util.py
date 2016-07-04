from saml2 import BINDING_HTTP_REDIRECT

from satosa.response import SeeOther, Response


def make_saml_response(binding, http_args):
    """
    Creates a SAML response.
    :param binding: SAML response binding
    :param http_args: http arguments
    :return: saml2.httputil.Response
    """
    if binding == BINDING_HTTP_REDIRECT:
        headers = dict(http_args["headers"])
        return SeeOther(str(headers["Location"]))

    return Response(http_args["data"], headers=http_args["headers"])