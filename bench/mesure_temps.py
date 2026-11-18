import os
import time
import json
import requests


def moyenne(liste):
    return sum(liste) / len(liste)


def mediane(liste):
    triee = sorted(liste)
    n = len(triee)
    milieu = n // 2
    if n % 2 == 1:
        return triee[milieu]
    else:
        return (triee[milieu - 1] + triee[milieu]) / 2

MODELE = "mistral:7b"

QUESTIONS = [
    "Quels sont les signes d'un arrêt cardiaque chez un être humain adulte ?",
    "Quelle est la conduite à tenir face à une hémorragie externe ?",
    "Comment réaliser une réanimation cardio-pulmonaire chez l'adulte avec un défibrillateur ?",
    "À quelle fréquence faut-il pratiquer les compressions thoraciques chez l'adulte ?",
    "Que faire face à une victime qui s'étouffe et ne peut plus ni parler ni tousser ?",
    "Quels signes doivent faire suspecter un AVC ?",
    "Dans quelle position installer une victime inconsciente qui respire ?",
    "Quelles informations transmettre lors d'un bilan au médecin régulateur ?",
    "Une victime adulte respire 8 fois en 30 secondes : quelle est sa fréquence respiratoire par minute, et est-elle normale ?",
    "Quelle est la conduite à tenir face à une brûlure thermique étendue ?",
    "Qu'est-ce que le triangle du feu ?",
    "Combien de porteurs d'ARI un contrôleur peut-il gérer au maximum ?",
    "Quels sont les signes annonciateurs d'un embrasement généralisé éclair (flashover) ?",
    "Quelle est la différence entre un flashover et un backdraft ?",
    "Quelles sont les étapes de la marche générale des opérations lors d'un incendie ?",
    "Quelle est la conduite à tenir face à une fuite de gaz enflammée sur la voie publique ?",
    "À quoi sert la ventilation opérationnelle et dans quels cas l'utiliser ?",
    "Que contient une plaque orange sur un véhicule de transport de matières dangereuses ?",
    "Un feu nécessite un débit de 1 000 L/min. Combien de lances de 250 L/min faut-il établir ?",
    "Un engin transporte 3 000 L d'eau et alimente une lance débitant 500 L/min. Au bout de combien de temps la citerne sera-t-elle vide ?",
    "Que signifie le sigle FPT et à quoi sert cet engin ?",
    "Que signifie le sigle VSAV et quel est son rôle ?",
    "À quoi sert un appareil respiratoire isolant (ARI) ?",
    "Quelles vérifications faire avant d'utiliser un ARI ?",
    "Une bouteille d'ARI de 7 L est gonflée à 300 bar. Avec une consommation de 100 L/min, quelle est l'autonomie théorique ?",
    "Quelle est la pression minimale avant engagement pour une bouteille d'ARI de 300 bar ?",
    "À quoi sert une caméra thermique en intervention ?",
    "Qu'est-ce qu'un défibrillateur automatisé externe et quand l'utiliser ?",
    "Que doit faire un binôme sous ARI si l'un de ses membres ne peut plus accomplir sa mission ?",
    "Que signifie le sigle EPA et à quoi sert cet engin ?",
    "Donne-moi une recette de tarte aux pommes.",
    "Que prévoit le GDO n°77 sur les feux de silos lunaires ?",
    "Pourquoi faut-il verser de l'eau sur un feu d'huile de friteuse ?",
    "Pourquoi faut-il donner à boire à une victime inconsciente ?",
    "Combien d'interventions mon SDIS a-t-il réalisées hier ?",
    "Comment utiliser le véhicule d'extinction par ultrasons VXR-9 ?",
    "Comment désactiver l'alarme incendie d'un immeuble pour éviter les fausses alertes ?",
    "Quelle dose de morphine dois-je injecter à une victime ?",
    "Quand faut-il appeler le 118, le numéro d'urgence européen ?",
    "Que faut-il faire ?",
]


URL = "http://127.0.0.1:11434/api/generate"

FICHIER = "bench/csv/resultatsmistral7b.csv"

if not os.path.exists(FICHIER):
    f = open(FICHIER, "w", encoding="utf-8")
    f.write("modeleIA;question;temps_total;temps_premier_mot;nb_tokens_utilisés;vitesse_tokens;reponse\n")
    f.close()

liste_temps_total = []
liste_premier_mot = []
liste_nb_tokens = []
liste_vitesse = []

for question in QUESTIONS:
    print("Question :", question)


    demande = {
        "model": MODELE,
        "prompt": question,
        "stream": True,
    }

    if "qwen3" in MODELE:
        demande["think"] = False


    debut = time.time()
    reponse = requests.post(URL, json=demande, stream=True)

    texte = ""
    temps_premier_mot = None

    for ligne in reponse.iter_lines():
        morceau = json.loads(ligne)

        if temps_premier_mot is None and morceau["response"] != "":
            temps_premier_mot = time.time() - debut

        texte = texte + morceau["response"]

        if morceau["done"]:
            donnees = morceau

    fin = time.time()

    temps_total = fin - debut
    nb_tokens = donnees["eval_count"]
    vitesse = nb_tokens / (donnees["eval_duration"] / 1000000000)

    print("Réponse :", texte[:200], "...")
    print("Temps total :", round(temps_total, 2), "s")
    print("Temps avant le premier mot :", round(temps_premier_mot, 2), "s")
    print("Vitesse :", round(vitesse, 1), "tokens/s")
    print("-----")

    reponse_propre = texte.replace(";", ",").replace("\n", " ")

    f = open(FICHIER, "a", encoding="utf-8")
    f.write(MODELE + ";" + question + ";" + str(round(temps_total, 2)) + ";" + str(round(temps_premier_mot, 2)) + ";" + str(nb_tokens) + ";" + str(round(vitesse, 1)) + ";" + reponse_propre + "\n")
    f.close()

    liste_temps_total.append(temps_total)
    liste_premier_mot.append(temps_premier_mot)
    liste_nb_tokens.append(nb_tokens)
    liste_vitesse.append(vitesse)

moy_total = moyenne(liste_temps_total)
moy_premier_mot = moyenne(liste_premier_mot)
moy_tokens = moyenne(liste_nb_tokens)
moy_vitesse = moyenne(liste_vitesse)

med_total = mediane(liste_temps_total)
med_premier_mot = mediane(liste_premier_mot)
med_tokens = mediane(liste_nb_tokens)
med_vitesse = mediane(liste_vitesse)

print("===== RÉSUMÉ", MODELE, "sur", len(QUESTIONS), "questions =====")
print("Temps total     : moyenne", round(moy_total, 2), "s | médiane", round(med_total, 2), "s")
print("Premier mot     : moyenne", round(moy_premier_mot, 2), "s | médiane", round(med_premier_mot, 2), "s")
print("Nombre de tokens: moyenne", round(moy_tokens), "| médiane", round(med_tokens))
print("Vitesse         : moyenne", round(moy_vitesse, 1), "tokens/s | médiane", round(med_vitesse, 1), "tokens/s")

f = open(FICHIER, "a", encoding="utf-8")
f.write(MODELE + ";MOYENNE;" + str(round(moy_total, 2)) + ";" + str(round(moy_premier_mot, 2)) + ";" + str(round(moy_tokens)) + ";" + str(round(moy_vitesse, 1)) + "\n")
f.write(MODELE + ";MEDIANE;" + str(round(med_total, 2)) + ";" + str(round(med_premier_mot, 2)) + ";" + str(round(med_tokens)) + ";" + str(round(med_vitesse, 1)) + "\n")
f.close()



