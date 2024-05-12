import xml.etree.ElementTree as ET
from graphviz import Digraph
import pyecore.ecore as Ecore

def parse_xml(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        return ET.parse(file).getroot()

def create_ecore_model(entities):
    package = Ecore.EPackage('myPackage')
    eclasses = {}

    for entity in entities:
        eclass = Ecore.EClass(entity.get('name'))
        package.eClassifiers.append(eclass)
        eclasses[entity.get('name')] = eclass

    for entity in entities:
        eclass = eclasses[entity.get('name')]
        attributes = entity.find('attributes')
        if attributes is not None:
            for attr in attributes:
                etype = Ecore.EDataType(attr.get('type'), instanceClassName=f"ecore.{attr.get('type')}")
                if 'foreignKey' in attr.attrib:
                    referenced_class = eclasses[attr.get('references')]
                    ereference = Ecore.EReference(attr.get('name'), eType=referenced_class)
                    ereference.upperBound = 1
                    ereference.lowerBound = 0 if attr.get('optional', 'false') == 'true' else 1
                    ereference.containment = False
                    eclass.eStructuralFeatures.append(ereference)
                else:
                    # Zwykłe atrybuty z ograniczeniami ilości
                    eattribute = Ecore.EAttribute(attr.get('name'), eType=etype)
                    eattribute.lowerBound = 0 if attr.get('optional', 'false') == 'true' else 1
                    eattribute.upperBound = 1
                    eclass.eStructuralFeatures.append(eattribute)
                    if 'primaryKey' in attr.attrib:
                        eattribute.isID = True

    return package

def generate_uml_diagram(ecore_package):
    dot = Digraph(comment='UML Diagram', format='png')
    for eclass in ecore_package.eClassifiers:
        attribute_details = '\\l'.join([f"{feature.name}: {feature.eType.name}\\l" for feature in eclass.eStructuralFeatures if isinstance(feature, Ecore.EAttribute)])
        dot.node(eclass.name, f'{eclass.name}|{attribute_details}', shape='record')
        for feature in eclass.eStructuralFeatures:
            if isinstance(feature, Ecore.EReference):
                dot.edge(eclass.name, feature.eType.name, label=feature.name, arrowhead='normal')
    return dot

def generate_pseudocode(ecore_package):
    code = ""
    for eclass in ecore_package.eClassifiers:
        code += f"class {eclass.name}:\n"
        for feature in eclass.eStructuralFeatures:
            code += f"    {feature.name}: {feature.eType.name}\n"
    return code

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
