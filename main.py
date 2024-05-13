from xml_parser import parse_xml
from ecore_model import create_ecore_model
from uml_diagram import generate_uml_diagram
from pseudocode_generator import generate_pseudocode

def main():
    root = parse_xml('metamodel.xml')
    entities = root.findall('.//entity')
    ecore_package = create_ecore_model(entities)
    diagram = generate_uml_diagram(ecore_package)
    diagram.render('uml_diagram', view=True)
    pseudocode = generate_pseudocode(ecore_package)
    with open('output_pseudocode.txt', 'w') as f:
        f.write(pseudocode)

if __name__ == "__main__":
    main()
