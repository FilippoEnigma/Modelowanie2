import xml.etree.ElementTree as ET

def parse_xml(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        return ET.parse(file).getroot()
