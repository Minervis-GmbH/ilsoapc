from ilsoapc import soap_client as soap_client
import pandas as pd
import xml.etree.ElementTree as ET


def build_user_from_file(filename, writer=ET):

    #1. we use pandas to read the excel file
    obj = pd.read_excel(filename)

    #2. we initialize some empty list to store the user dictionaries
    users = []

    #3. we iterate through each row of the DataFrame object obtained from
    # reading the file in step 1, and then create user dictionaries

    for index, row in obj.iterrows():
        user = {
            "Login": row["Login"],
            "First Name": row["Firstname"],
            "Last Name": row["Lastname"],
            "global_role": row["Rolle#global"],
            "email": row["Email"],
            "password": row["Password"],
            "institiution": row["Institution"]
            
        }

        # we append the user dictionary to the list of users dictionaries
        users.append(user)
        
    

    # Start building an xml object for the data
    root = ET.Element('Users')


    #we create an XML reperesentation of the user data using ElmentTree
    for user in users:
        user_element = ET.SubElement(root, 'User', Language='de', Action='Insert')
        for key, value in user.items():
            ET.SubElement(user_element, key).text = str(value)
    
    #return the converted XML element into a string
    return ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    

if __name__ == '__main__':
    installation_url = "http://127.0.0.1:80"
    client = "default"
    username = "root"
    password = "homer123"
    soap_url = f"{installation_url}/webservice/soap/server.php"

    filename = 'users.xlsx'  # Location of the provided Excel file

    test_run = True

    soap = soap_client.SoapClient(soap_url, client)
    soap.request_token(username, password)
    if not test_run:
        #users = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE Users PUBLIC "-//ILIAS//DTD UserImport//EN" "https://maclocal.ilias.minervis:9070/xml/ilias_user_5_1.dtd"><Users><UDFDefinitions></UDFDefinitions><User Language="de" Action="Insert"><Login>soap.user-005</Login><Role Id="il_0_role_5" Type="Global">Guest</Role><Firstname>arerere</Firstname><Lastname>fgfgfgfgfg</Lastname><Gender>m</Gender><Email>some_email@email.com</Email><Active>true</Active><AuthMode type="default"/><Look Skin="default" Style="delos"/></User><User Language="de" Action="Insert"><Login>soap.user-006</Login><Role Id="il_0_role_5" Type="Global">Guest</Role><Firstname>some user</Firstname><Lastname>someother name</Lastname><Gender>m</Gender><Email>some_email@email.com</Email><Active>true</Active><AuthMode type="default"/><Look Skin="default" Style="delos"/></User></Users>'
        users = build_user_from_file(filename)
        soap.import_users(users)

build_user_from_file(filename)
