import requests
import xml.etree.ElementTree as ET
from lxml import etree, objectify


def token(username='', password='', client=''):
    url = "http://192.168.64.2:9075/webservice/soap/server.php"
    payload = (f"<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope "
               "xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"> <soap:Body> <login>     "
               f"<client>{client}</client><username>{username}</username>"
               f"<password>{password}</password> </login> </soap:Body></soap:Envelope>")
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': 'urn:ilUserAdministration#login'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    tree = objectify.fromstring(preprocess_response(response.text))
    if response.status_code >= 400:
        return False
    if tree.Body.find('Fault') and tree.Body.Fault and tree.Body.Fault.faultstring:
        return False
    print("Successfully retrieved the token from the server ...")
    return tree.Body.loginResponse.sid.text


def preprocess_response(response=''):
    response = response.replace('SOAP-ENV:', '')
    response = response.replace('ns1:', '')
    return response.encode('utf-8')
