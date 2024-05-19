import os
from xml_parser import parse_xml
from ecore_model import create_ecore_model, save_ecore_model_to_xmi
from uml_diagram import generate_uml_diagram
from pseudocode_generator import generate_pseudocode

def main():
    """
    Główna funkcja programu. Parsuje plik XML z metamodelu, tworzy model Ecore,
    generuje diagram UML i pseudokod, a następnie zapisuje wyniki do plików.
    """
    xml_file = 'metamodel.xml'
    diagram_file = 'uml_diagram'
    pseudocode_file = 'output_pseudocode.txt'
    xmi_file = 'model.xmi'

    try:
        # Parsowanie pliku XML
        root = parse_xml(xml_file)
        if root is None:
            raise ValueError("Root element not found in the XML file.")

        # Znajdowanie encji w pliku XML
        entities = root.findall('.//entity')
        if not entities:
            raise ValueError("No entities found in the XML file.")

        # Tworzenie modelu Ecore
        ecore_package = create_ecore_model(entities)

        # Zapisywanie modelu Ecore do pliku XMI
        save_ecore_model_to_xmi(ecore_package, xmi_file)

        # Generowanie diagramu UML
        diagram = generate_uml_diagram(ecore_package)
        diagram_path = os.path.join(os.getcwd(), diagram_file)
        diagram.render(diagram_path, view=True)

        # Generowanie pseudokodu
        pseudocode = generate_pseudocode(ecore_package)
        pseudocode_path = os.path.join(os.getcwd(), pseudocode_file)
        with open(pseudocode_path, 'w') as f:
            f.write(pseudocode)

        print(f"UML diagram saved to {diagram_path}.")
        print(f"Pseudocode saved to {pseudocode_path}.")
        print(f"XMI model saved to {xmi_file}.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
