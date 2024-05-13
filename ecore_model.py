import pyecore.ecore as Ecore

def create_ecore_model(entities):
    # Tworzenie głównego pakietu modelu
    package = Ecore.EPackage('myPackage')
    eclasses = {}

    # Definiowanie klas na podstawie dostarczonych encji
    for entity in entities:
        eclass = Ecore.EClass(entity.get('name'))
        package.eClassifiers.append(eclass)
        eclasses[entity.get('name')] = eclass

    # Dodawanie atrybutów i referencji do klas
    for entity in entities:
        eclass = eclasses[entity.get('name')]
        attributes = entity.find('attributes')
        if attributes is not None:
            for attr in attributes:
                # Tworzenie typu danych na podstawie typu atrybutu
                etype = Ecore.EDataType(attr.get('type'), instanceClassName=f"ecore.{attr.get('type')}")
                if 'foreignKey' in attr.attrib:
                    # Obsługa klucza obcego jako referencji między klasami
                    referenced_class = eclasses[attr.get('references')]
                    ereference = Ecore.EReference(attr.get('name'), eType=referenced_class)
                    ereference.lowerBound = int(attr.get('min', '1'))  # Domyślna dolna granica to 1
                    ereference.upperBound = -1 if attr.get('max', '1') == '*' else int(attr.get('max'))
                    ereference.containment = False
                    eclass.eStructuralFeatures.append(ereference)
                else:
                    # Tworzenie atrybutów dla klasy
                    eattribute = Ecore.EAttribute(attr.get('name'), eType=etype)
                    eattribute.lowerBound = 0 if attr.get('optional', 'false') == 'true' else 1
                    eattribute.upperBound = 1
                    eclass.eStructuralFeatures.append(eattribute)
                    if 'primaryKey' in attr.attrib:
                        eattribute.isID = True  # Oznaczenie atrybutu jako klucz główny

    return package
