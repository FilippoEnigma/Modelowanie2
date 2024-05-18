import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """
    Parsuje plik XML i zwraca korzeń drzewa XML.

    Args:
        file_path (str): Ścieżka do pliku XML.

    Returns:
        xml.etree.ElementTree.Element: Korzeń drzewa XML, jeśli parsowanie się powiedzie, w przeciwnym razie None.
    """
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            tree = ET.parse(file)
            return tree.getroot()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except ET.ParseError:
        print(f"Error: Failed to parse XML from '{file_path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
