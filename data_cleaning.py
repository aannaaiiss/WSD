# path to adapt
gold_path = "C:/Users/Utilisateur/Projet_TAL_M1/FSE-1.1-191210/wiktionary-190418.gold.key.txt"

gold_file = open(gold_path, "r",encoding="utf-8")

# homogeneize the name of the keys
for key in gold_file:
    given_key = key.split()[1].split("__")[2]
    if given_key == "onom":
        given_key = given_key.replace("onom", "onomatopée")
    if given_key == "prép":
        given_key = given_key.replace("prép", "préposition")
    
