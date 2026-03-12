# ID3 (Iterative Dichotomiser 3) - decision tree learning algorithm 
# P.S. Pentru testare s-a folosit setul de date:
# https://www.kaggle.com/datasets/krishnagiri/id3csv/data

import pandas as pd
import numpy as np

# calculeaza entropia unui set de date
def entropy(target_col):
    # extragem valorile unice si numarul lor
    elements, counts = np.unique(target_col, return_counts=True)

    entropy_value = -np.sum([
        (counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts))
        for i in range(len(elements))
    ])

    return entropy_value

# calculeaza gain-ul pentru un feature
def information_gain(data, feature, target="Class"):
    # entropia intregului set de date
    total_entropy = entropy(data[target])
    # extragem valorile unice ale feature-ului si numarul lor
    values, counts = np.unique(data[feature], return_counts=True)

    # entropia sub-seturilor
    weighted_entropy = np.sum([
        (counts[i] / np.sum(counts)) *
        entropy(data[data[feature] == values[i]][target])
        for i in range(len(values))
    ])

    # gain-ul este diferenta intre entropia intregului set de date si entropia sub-seturilor
    return total_entropy - weighted_entropy

def id3(data, original_data, features, target="Class", parent_node_class=None):
    # pentru cazul în care setul de date este gol
    if len(data) == 0:
        return parent_node_class

    # pentru cazul în care toate valorile sunt egale
    if len(np.unique(data[target])) == 1:
        return np.unique(data[target])[0]

    # pentru cazul în care nu sunt mai multe feature-uri
    if len(features) == 0:
        return parent_node_class

    # extragem clasa majoritară
    parent_node_class = np.unique(data[target])[np.argmax(
    np.unique(data[target], return_counts=True)[1])]

    # calulul gain-ului pentru fiecare feature
    gains = [information_gain(data, feature, target) for feature in features]
    # extragem feature-ul cu cea mai mare valoare de gain
    best_feature = features[np.argmax(gains)]

    # cream arborele care va fi sub forma unui dictionar de forma
    # {feature1: {value1: subtree1}, feature2: {value2: subtree2}, ...}
    tree = {best_feature: {}}

    # eliminam feature-ul folosit pentru a-l folosi in urmatoarea iteratie
    # si a ramane doar feature-urile care nu sunt folosite
    features = [f for f in features if f != best_feature]

    # pentru fiecare valoare a feature-ului ales
    for value in np.unique(original_data[best_feature]):
        # cream subsetul care are valoarea feature-ului ales
        subset = data[data[best_feature] == value]
        # cream subarborele conform acestei valori ale feature-ului
        subtree = id3(subset, original_data, features, target, parent_node_class)
        # adaugam subarborele in arbore corespunzator valorii
        tree[best_feature][value] = subtree

    # returnam arborele obtinut in urma constructiei
    return tree

if __name__ == "__main__":
    # Citim setul de date
    df = pd.read_csv("id3.csv")
    
    # Coloana cu rezultatul pe care încercăm să-l determinăm este "Answer"
    target_column = "Answer"
    
    # Restul sunt trăsături (features)
    features_list = list(df.columns)
    features_list.remove(target_column)

    # Rulam algoritmul 
    tree = id3(df, df, features_list, target=target_column)
    
    import pprint
    print("Arborele de decizie generat din id3.csv:")
    pprint.pprint(tree)
    # print(tree)
