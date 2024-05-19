import pyecore.ecore as Ecore
from pyecore.resources import ResourceSet, URI

def create_ecore_model(entities):
    # Tworzenie głównego pakietu modelu
    package = Ecore.EPackage('myPackage')
    eclasses = {}
    data_types = {}

    # Definiowanie klas na podstawie dostarczonych encji
    for entity in entities:
        entity_name = entity.get('name')
        if not entity_name:
            raise ValueError("Entity must have a name attribute.")

        eclass = Ecore.EClass(entity_name)
        package.eClassifiers.append(eclass)
        eclasses[entity_name] = eclass

    # Dodawanie atrybutów i referencji do klas
    for entity in entities:
        eclass = eclasses[entity.get('name')]
        attributes = entity.find('attributes')

        if attributes is not None:
            for attr in attributes:
                attr_name = attr.get('name')
                attr_type = attr.get('type')

                if not attr_name or not attr_type:
                    raise ValueError("Attribute must have a name and type.")

                # Tworzenie typu danych na podstawie typu atrybutu
                if attr_type not in data_types:
                    data_types[attr_type] = Ecore.EDataType(attr_type, instanceClassName=f"ecore.{attr_type}")
                etype = data_types[attr_type]

                if 'foreignKey' in attr.attrib:
                    # Obsługa klucza obcego jako referencji między klasami
                    referenced_class_name = attr.get('references')
                    if referenced_class_name not in eclasses:
                        raise ValueError(f"Referenced class '{referenced_class_name}' not found.")

                    referenced_class = eclasses[referenced_class_name]
                    ereference = Ecore.EReference(attr_name, eType=referenced_class)
                    ereference.lowerBound = int(attr.get('min', '1'))  # Domyślna dolna granica to 1
                    ereference.upperBound = -1 if attr.get('max', '1') == '*' else int(attr.get('max'))
                    ereference.containment = False
                    eclass.eStructuralFeatures.append(ereference)
                else:
                    # Tworzenie atrybutów dla klasy
                    eattribute = Ecore.EAttribute(attr_name, eType=etype)
                    eattribute.lowerBound = 0 if attr.get('optional', 'false') == 'true' else 1
                    eattribute.upperBound = 1
                    eclass.eStructuralFeatures.append(eattribute)
                    if 'primaryKey' in attr.attrib:
                        eattribute.isID = True  # Oznaczenie atrybutu jako klucz główny

    return package

def save_ecore_model_to_xmi(package, file_path):
    resource_set = ResourceSet()
    resource = resource_set.create_resource(URI(file_path))
    resource.append(package)
    resource.save()
