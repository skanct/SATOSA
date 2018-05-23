import xml.etree.ElementTree
from satosa.micro_services.inject_attribute_for_rs_idps import InjectAttributeForRSIdPs
from satosa.internal_data import InternalResponse, AuthenticationInformation

class TestInjectAttributeForRSIdPs:

    #Provide a fakeXML, just to test it
    xmltext = "<?xml version='1.0' encoding='UTF-8'?><md:EntityDescriptor xmlns:md=\"urn:oasis:names:tc:SAML:2.0:metadata\" xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\" xmlns:mdattr=\"urn:oasis:names:tc:SAML:metadata:attribute\" xmlns:mdrpi=\"urn:oasis:names:tc:SAML:metadata:rpi\" xmlns:mdui=\"urn:oasis:names:tc:SAML:metadata:ui\" xmlns:pyff=\"http://pyff.io/NS\" xmlns:saml=\"urn:oasis:names:tc:SAML:2.0:assertion\" xmlns:shibmd=\"urn:mace:shibboleth:metadata:1.0\" xmlns:xrd=\"http://docs.oasis-open.org/ns/xri/xrd-1.0\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" entityID=\"https://idp.admin.skanct.com:8443/saml2/idp/metadata.php\" ID=\"_20180523T102622Z\" validUntil=\"2018-05-30T10:26:22Z\" cacheDuration=\"PT5H\"><md:Extensions><mdattr:EntityAttributes><saml:Attribute Name=\"http://macedir.org/entity-category-support\" NameFormat=\"urn:oasis:names:tc:SAML:2.0:attrname-format:uri\"><saml:AttributeValue xsi:type=\"xs:string\">http://refeds.org/category/research-and-scholarship</saml:AttributeValue></saml:Attribute><saml:Attribute Name=\"urn:oasis:names:tc:SAML:attribute:assurance-certification\" NameFormat=\"urn:oasis:names:tc:SAML:2.0:attrname-format:uri\"><saml:AttributeValue xsi:type=\"xs:string\">https://refeds.org/sirtfi</saml:AttributeValue></saml:Attribute></mdattr:EntityAttributes></md:Extensions></md:EntityDescriptor>"

    def create_inject_service(self, mdq_url, static_attributes, whitelist_idp, attribute_value_to_search):
        inject_service = InjectAttributeForRSIdPs(config=dict(mdq_url=mdq_url,static_attributes=static_attributes,whitelist_idp=whitelist_idp,attribute_value_to_search=attribute_value_to_search), 
        name="test_filter",
        base_url="https://satosa.example.com")
        inject_service.next = lambda ctx, data: data
        return inject_service

    def test_inject_check_xml_with_attributes(self, context):
        resp = InternalResponse(AuthenticationInformation(None, None, "https://idp.example.com/idp"))
        resp.attributes = {
            "mail": ["test@example.org"]
        }
        avts = {"https://refeds.org/sirtfi"}
        inject_service = self.create_inject_service("https://example.com/public",dict(epa="urn:example:org"),"",avts)
        link = self.xmltext
        e = xml.etree.ElementTree.fromstring(link)
        assert inject_service._check_xml(e,resp,context)

    def test_inject_check_xml_with_fail_attributes_search(self, context):
        resp = InternalResponse(AuthenticationInformation(None, None, "https://idp.example.com/idp"))
        resp.attributes = {
            "mail": ["test@example.org"]
        }
        avts = {"https://wrong_url.org/sirtfi"}
        inject_service = self.create_inject_service("https://example.com/public",dict(epa="urn:example:org"),"",avts)
        link = self.xmltext
        e = xml.etree.ElementTree.fromstring(link)
        assert not inject_service._check_xml(e,resp,context)

    def test_inject_with_empty_whitelist_and_attribute_to_search(self,context):
        resp = InternalResponse(AuthenticationInformation(None, None, "https://idp.example.com/idp"))
        resp.attributes = {
            "mail": ["test@example.org"]
        }
        inject_service = self.create_inject_service("https://example.com/public",dict(epa="urn:example:org"),"","")        
        inject = inject_service.process(context, resp)
        print(inject.attributes)
        assert "epa" not in inject.attributes
        

    def test_inject_with_whitelist_IdP(self,context):
        resp = InternalResponse(AuthenticationInformation(None, None, "https://idp.example.com/idp"))
        resp.attributes = {
            "mail": ["test@example.org"]
        }
        inject_service = self.create_inject_service("https://example.com/public",dict(epa="urn:example:org"),"https://idp.example.com/idp","")        
        inject = inject_service.process(context, resp)
        assert "epa" in inject.attributes
        assert "urn:example:org" in inject.attributes['epa']
    
    def test_inject_with_all_condition_failed(self,context):
        resp = InternalResponse(AuthenticationInformation(None, None, "https://idp.example.com/idp"))
        resp.attributes = {
            "mail": ["test@example.org"]
        }
        inject_service = self.create_inject_service("https://example.com/public",dict(epa="urn:example:org"),"http://idp2.example.org","")        
        inject = inject_service.process(context, resp)
        print(inject.attributes)
        assert "epa" not in inject.attributes
