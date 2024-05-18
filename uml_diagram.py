from graphviz import Digraph
import pyecore.ecore as Ecore


def generate_uml_diagram(ecore_package):
    """
    Generuje diagram UML dla podanego pakietu Ecore.

    Args:
        ecore_package (Ecore.EPackage): Pakiet Ecore, z którego generowany jest diagram UML.

    Returns:
        Digraph: Obiekt Digraph reprezentujący diagram UML.
    """
    dot = Digraph(comment='UML Diagram', format='png')

    # Definiowanie stylów wierzchołków i krawędzi
    dot.attr('node', shape='record', style='filled', fillcolor='gray90')
    dot.attr('edge', fontsize='10', fontcolor='blue')

    for eclass in ecore_package.eClassifiers:
        # Generowanie opisu atrybutów dla każdej klasy
        attribute_details = '\\l'.join(
            [f"{feature.name}: {feature.eType.name}\\l" for feature in eclass.eStructuralFeatures if
             isinstance(feature, Ecore.EAttribute)]
        )
        # Dodawanie wierzchołka dla klasy
        dot.node(eclass.name, f'{eclass.name}|{attribute_details}')

        # Przetwarzanie powiązań (referencji) między klasami
        for feature in eclass.eStructuralFeatures:
            if isinstance(feature, Ecore.EReference):
                # Określenie typu strzałki na podstawie górnej granicy krotności
                arrowhead = determine_arrowhead(feature)
                # Etykieta dla krawędzi uwzględniająca krotność
                label = f"{feature.name} ({feature.lowerBound}..{'n' if feature.upperBound == -1 else feature.upperBound})"
                dot.edge(eclass.name, feature.eType.name, label=label, arrowhead=arrowhead)

    return dot


def determine_arrowhead(feature):
    """
    Określa typ strzałki na podstawie górnej granicy krotności referencji.

    Args:
        feature (Ecore.EReference): Referencja Ecore.

    Returns:
        str: Typ strzałki dla referencji.
    """
    if feature.upperBound == 1:
        return 'vee'
    elif feature.upperBound > 1:
        return 'crow'
    elif feature.upperBound == 0:
        return 'obox'
    else:
        return 'diamond'
