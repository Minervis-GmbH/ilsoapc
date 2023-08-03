from ilsoapc import soap_client as soap_client
import pandas as pd
import xml.etree.ElementTree as ET

def build_user_from_file(filename, writer=ET):
    obj = pd.read_excel(filename)

    users = []

    for index, row in obj.iterrows():
        user = {
            "Login": row["Login"],
            "firstname": row["Firstname"],
            "lastname": row["Lastname"],
            "email": row["Email"],
            "institution": row["Institution"],
            "active": 1,
            "auth_mode": "default",
            "skin": "default",
            "style": "delos"
        }
        users.append(user)

    root = ET.Element('Users')
    

    for user in users:
        user_element = ET.SubElement(root, 'User', Language='de', Action='Insert')
        
        ET.SubElement(user_element, 'Login').text = user['Login']
        role_element = ET.SubElement(user_element, 'Role', Id='il_0_role_5', Type='Global')
        role_element.text = "Guest"
    
        
        ET.SubElement(user_element, 'Firstname').text = user['firstname']
        ET.SubElement(user_element, 'Lastname').text = user['lastname']
        ET.SubElement(user_element, 'Gender').text = 'm'  #we set a default value
        
        ET.SubElement(user_element, 'Email').text = user['email']
        ET.SubElement(user_element, 'Active').text = "true" 
        ET.SubElement(user_element, 'AuthMode', type='default')
        
        look_element = ET.SubElement(user_element, 'Look', Skin='default', Style='delos')

    return ET.tostring(root, encoding='UTF-8', xml_declaration=True).decode('utf-8')

if __name__ == '__main__':
    installation_url = "http://127.0.0.1:80"
    client = "default"
    username = "root"
    password = "homer123"
    soap_url = f"{installation_url}/webservice/soap/server.php"

    filename = 'users.xlsx'  # Location of the provided Excel file-it's in the same directory-

    test_run = True

    soap = soap_client.SoapClient(soap_url, client)
    soap.request_token(username, password)

    if test_run:
        users = build_user_from_file(filename)
        print(users)
        soap.import_users(users)
