import requests
import xml.etree.ElementTree as ET
from lxml import etree, objectify


class SoapClient:
    def __init__(self, url, client=''):
        self.url = url
        self.token = ''
        self.authenticated = False
        self.client = client
        self.writer = ET

    def send(self, payload, headers=None, method='POST'):
        if headers is None:
            headers = {
                'Content-Type': 'text/xml; charset=utf-8'
            }
        response = requests.request("POST", self.url, headers=headers, data=payload, verify=False)
        tree = objectify.fromstring(self.__preprocess_response(response.text))
        if response.status_code >= 400 or tree.Body.find('Fault') and tree.Body.Fault and tree.Body.Fault.faultstring:
            print(f'request has failed with status: {response.status_code}')
            print(response.text)
            return False
        else:
            return tree

    def request_token(self, username, password):
        if self.authenticated:
            print('already authenticated ...')
            return True
        payload = self.login(username, password)
        response = self.send(payload)
        if response:
            self.token = response.Body.loginResponse.sid.text
            self.authenticated = True
            print('authenticated ...')
        else:
            self.authenticated = False
            print('soap authentication failed')

    def build_xml(self):
        raise NotImplementedError

    def __add_request_stub(self, function_name, sid=''):
        self.envelope = self.writer.Element('soap:Envelope')
        self.envelope.set('xmlns:soap', "http://schemas.xmlsoap.org/soap/envelope/")
        body = self.writer.SubElement(self.envelope, 'soap:Body')
        function = self.writer.SubElement(body, function_name)
        if sid:
            self.writer.SubElement(function, 'sid').text = sid
        return function

    def build_request_xml(self):
        pass

    def parse_response_xml(self):
        pass

    def import_users(self, user_xml_str=''):

        body = self.__add_request_stub('importUsers', self.token)
        self.writer.SubElement(body, 'usr_xml').text = user_xml_str
        payload = self.__request_to_string()
        #print(payload)
        if len(user_xml_str) == 0:
            raise NotImplementedError
        self.send(payload)

    def export_members(self):
        raise NotImplementedError

    def login(self, username, password):
        body = self.__add_request_stub('login')
        self.writer.SubElement(body, 'client').text = self.client
        self.writer.SubElement(body, 'username').text = username
        self.writer.SubElement(body, 'password').text = password
        return self.__request_to_string()

    def __request_to_string(self):
        return self.writer.tostring(self.envelope, encoding='UTF-8', xml_declaration=True)

    def __preprocess_response(self, response):
        #print(response)
        response = response.replace('SOAP-ENV:', '')
        response = response.replace('ns1:', '')
        return response.encode('utf-8')
