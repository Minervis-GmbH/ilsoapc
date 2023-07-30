from ilsoapc import soap_client as soap_client
import pandas as pd
import xml.etree.ElementTree as ET


def build_user_from_file(filename, writer=ET):

    ##TODO: read the excel file
    obj = pd.read_excel('')
    # TODO: do some stuff with the data and save the data in a list
    users = []
    # Start building an xml object for the data
    root = ET.Element('Users')
    # TODO: use the data read from excel and build and xml string.
    return ET.tostring(root, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    installation_url = "http://127.0.0.1:9075"
    client = "some_client"
    username = "some_user"
    password = "some_pass_word"
    soap_url = f"{installation_url}/webservice/soap/server.php"

    filename = ''  # Location of the provided Excel file

    test_run = True

    soap = soap_client.SoapClient(soap_url, client)
    soap.request_token(username, password)
    if not test_run:
        #users = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE Users PUBLIC "-//ILIAS//DTD UserImport//EN" "https://maclocal.ilias.minervis:9070/xml/ilias_user_5_1.dtd"><Users><UDFDefinitions></UDFDefinitions><User Language="de" Action="Insert"><Login>soap.user-005</Login><Role Id="il_0_role_5" Type="Global">Guest</Role><Firstname>arerere</Firstname><Lastname>fgfgfgfgfg</Lastname><Gender>m</Gender><Email>some_email@email.com</Email><Active>true</Active><AuthMode type="default"/><Look Skin="default" Style="delos"/></User><User Language="de" Action="Insert"><Login>soap.user-006</Login><Role Id="il_0_role_5" Type="Global">Guest</Role><Firstname>some user</Firstname><Lastname>someother name</Lastname><Gender>m</Gender><Email>some_email@email.com</Email><Active>true</Active><AuthMode type="default"/><Look Skin="default" Style="delos"/></User></Users>'
        users = build_user_from_file(filename)
        soap.import_users(users)
