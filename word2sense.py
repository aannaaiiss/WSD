# building of the word2sense dictionary
# It may be useful to use it during the K-means algo to determine the starting points and the number of clusters

from collections import defaultdict
import xml.etree.ElementTree as ET

# path to adapt
gold_path = "C:/Users/Utilisateur/Projet_TAL_M1/FSE-1.1-191210/wiktionary-190418.gold.key.txt"

#récupération des données .txt
gold_file = open(gold_path, "r",encoding="utf-8")

word2sense = defaultdict(set)
for line in gold_file:
    word = line.split("_")
    word2sense[word[4]].add(word[3])
print(word2sense)