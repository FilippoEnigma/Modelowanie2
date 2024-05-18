import pyecore.ecore as Ecore


def generate_pseudocode(ecore_package):
    """
    Generuje reprezentację pseudokodu dla podanego pakietu Ecore.

    Args:
        ecore_package (Ecore.EPackage): Pakiet Ecore, z którego generowany jest pseudokod.

    Returns:
        str: Ciąg znaków zawierający reprezentację pseudokodu pakietu Ecore.
    """
    code = ""

    # Iteracja przez wszystkie klasyfikatory (klasy) w pakiecie Ecore
    for eclass in ecore_package.eClassifiers:
        # Dodanie definicji klasy z nazwą
        code += f"class {eclass.name}:\n"

        # Sprawdzenie, czy klasa posiada jakiekolwiek atrybuty lub referencje
        if not eclass.eStructuralFeatures:
            code += "    pass\n"  # Dodanie 'pass' jeśli klasa jest pusta
        else:
            # Iteracja przez cechy strukturalne klasy (atrybuty i referencje)
            for feature in eclass.eStructuralFeatures:
                # Formatowanie atrybutów i referencji z typami i ograniczeniami
                multiplicity = f"{feature.lowerBound}..{'n' if feature.upperBound == -1 else feature.upperBound}"
                feature_type = "Attribute" if isinstance(feature, Ecore.EAttribute) else "Reference"
                code += f"    {feature.name}: {feature.eType.name} ({feature_type}, {multiplicity})\n"

        code += "\n"

    return code
