import pyecore.ecore as Ecore

def generate_pseudocode(ecore_package):
    code = ""
    # Iteracja przez wszystkie klasyfikatory (klasy) w pakiecie Ecore
    for eclass in ecore_package.eClassifiers:
        # Dodanie definicji klasy z nazwą
        code += f"class {eclass.name}:\n"
        # Sprawdzenie, czy klasa posiada jakiekolwiek atrybuty lub referencje
        if not eclass.eStructuralFeatures:
            code += "    pass\n"  # Dodanie 'pass' jeśli klasa jest pusta
        # Iteracja przez cechy strukturalne klasy (atrybuty i referencje)
        for feature in eclass.eStructuralFeatures:
            # Formatowanie atrybutów i referencji z typami i ograniczeniami
            multiplicity = f"{feature.lowerBound}..{('n' if feature.upperBound == -1 else feature.upperBound)}"
            code += f"    {feature.name}: {feature.eType.name} ({multiplicity})\n"
    return code
