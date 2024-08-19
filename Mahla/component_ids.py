
import requests
import xml.etree.ElementTree as ET 
import json

emailAddressUsername = 'm.nasrollahi@reply.com'
username = 'BOOMI_TOKEN.' + emailAddressUsername
accountID = 'gluereply-5JLXNN'
BoomiAPIKeyPass= '50b85078-ad6c-483e-9c49-53d93f9259a5' 
compID = 'b1bb4bb6-9380-4ab4-b372-04a113f7ea04'

url = 'https://api.boomi.com/api/rest/v1/' + accountID + '/PackagedComponentManifest/' + compID




def xml_to_dict(element):
    # Recursively convert XML elements to a dictionary
    def _element_to_dict(elem):
        # Strip the namespace from the tag
        tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
        data = {tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for dc in map(_element_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            data = {tag: dd}
        if elem.attrib:
            data[tag].update(('@' + k, v) for k, v in elem.attrib.items())
        if elem.text:
            text = elem.text.strip()
            if children or elem.attrib:
                if text:
                    data[tag]['#text'] = text
            else:
                data[tag] = text
        return data
    
    return _element_to_dict(element)

def get_comp_package():
    response = requests.get(url, auth=(username, BoomiAPIKeyPass))
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        xml_dict = xml_to_dict(root)
        json_data = json.dumps(xml_dict, indent=4)
        print(json_data)
    else:
        print('Error: ', response.status_code)


def xml_to_dict(element):
    # Recursively convert XML elements to a dictionary
    def _element_to_dict(elem):
        # Strip the namespace from the tag
        tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
        data = {tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for dc in map(_element_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            data = {tag: dd}
        if elem.attrib:
            data[tag].update((k, v) for k, v in elem.attrib.items())
        if elem.text:
            text = elem.text.strip()
            if children or elem.attrib:
                if text:
                    data[tag]['#text'] = text
            else:
                data[tag] = text
        return data
    
    return _element_to_dict(element)

def get_component_package():
    response = requests.get(url, auth=(username, BoomiAPIKeyPass))
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        xml_dict = xml_to_dict(root)
        # json_data = json.dumps(xml_dict, indent=4)
        return xml_dict

    else:
        print('Error: ', response.status_code)
        return 'Error'



def get_component_IDs():
    # json_data = json.dumps(get_component_package(), indent=4)

    xml_data = get_component_package()
    comp_IDs = [component['id'] for component in xml_data["PackagedComponentManifest"]["componentInfo"]]

    return (comp_IDs)

    


if __name__ == "__main__":
    print(get_component_IDs())
    