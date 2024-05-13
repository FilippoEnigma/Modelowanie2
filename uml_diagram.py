from graphviz import Digraph
import pyecore.ecore as Ecore

def generate_uml_diagram(ecore_package):
    dot = Digraph(comment='UML Diagram', format='png')
    # Definiowanie stylów wierzchołków i krawędzi
    dot.attr('node', shape='record', style='filled', fillcolor='gray90')
    dot.attr('edge', fontsize='10', fontcolor='blue')

    for eclass in ecore_package.eClassifiers:
        # Generowanie opisu atrybutów dla każdej klasy
        attribute_details = '\\l'.join([f"{feature.name}: {feature.eType.name}\\l" for feature in eclass.eStructuralFeatures if isinstance(feature, Ecore.EAttribute)])
        # Dodawanie wierzchołka dla klasy
        dot.node(eclass.name, f'{eclass.name}|{attribute_details}')

        # Przetwarzanie powiązań (referencji) między klasami
        for feature in eclass.eStructuralFeatures:
            if isinstance(feature, Ecore.EReference):
                # Określenie typu strzałki na podstawie górnej granicy krotności
                arrowhead = 'vee' if feature.upperBound == 1 else 'crow' if feature.upperBound > 1 else 'obox' if feature.upperBound == 0 else 'diamond'
                # Etykieta dla krawędzi uwzględniająca krotność
                label = f"{feature.name} ({feature.lowerBound}..{('n' if feature.upperBound == -1 else feature.upperBound)})"
                dot.edge(eclass.name, feature.eType.name, label=label, arrowhead=arrowhead)

    return dot
