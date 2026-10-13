# Assistant pompiers mobile

> Portage sur smartphone d'un assistant conversationnel pour les sapeurs-pompiers et intégration de modèles d'IA exécutés localement.

**Projet en cours** (année 2026-2027). .

## Contexte

Projet Annuel:



Il existe déjà un chatbot destiné aux sapeurs-pompiers. Il s'appuie sur des modèles de langage **distants**, donc sur des serveurs accessibles par internet.

Sur le terrain, un agent a besoin d'un outil qui :
- tient dans la poche ;
- se lance vite et s'utilise **d'une seule main** ;
- continue, idéalement, de fonctionner quand le réseau est **mauvais ou absent**.

## Objectifs    

### 1. Portage sur smartphone
- Comprendre l'architecture du chatbot existant.
- Choisir et justifier une approche : application native, multiplateforme ou web app installable.
- Réaliser un prototype fonctionnel sur Android ou iOS.

### 2. Modèles d'IA locaux
- Identifier de petits modèles capables de tourner **sur le téléphone** ou sur un **petit serveur local**.
- Les intégrer au chatbot.
- Les comparer aux modèles distants sur des questions représentatives :

| Critère | Ce qu'on mesure |
|---|---|
| Qualité | Justesse et utilité des réponses |
| Rapidité | Temps avant la première réponse, temps total |
| Mémoire | RAM utilisée sur le téléphone |
| Batterie | Consommation pendant l'utilisation |

**But :** savoir dans quels cas un modèle local suffit et dans quels cas un modèle distant reste nécessaire.


## Pistes techniques envisagées

*Elles seront confirmées dans le cahier des charges.*

- **Application mobile :** Expo / React Native (TypeScript), avec un seul code pour Android et iOS.
- **IA sur le téléphone :** [llama.rn](https://github.com/mybigday/llama.rn), qui intègre llama.cpp dans React Native.
- **IA sur un serveur local :** [Ollama](https://ollama.com).
- **Modèles candidats :** petits modèles ouverts (1 à 4 milliards de paramètres), par exemple Qwen, Gemma, Llama ou Phi.

```
          ┌──────────────────────┐
          │   App smartphone     │
          │  (interface du chat) │
          └──────────┬───────────┘
                     │ askModel(question)
       ┌─────────────┼──────────────┐
       ▼             ▼              ▼
  Modèle distant  Serveur local  Modèle sur
   (internet)      (Ollama)      le téléphone
```

## Calendrier

| Période | Étape |
|---|---|
| Octobre à décembre 2026 | Prise en main du chatbot existant et cahier des charges définitif |
| Janvier à mars 2027 | Prototype mobile |
| Avril à juin 2027 | Modèles locaux et évaluation |
| Fin de parcours | Rapport et soutenance |

## Livrables

- [ ] Code du prototype et sa documentation
- [ ] Tableau comparatif des modèles testés
- [ ] Rapport
- [ ] Démonstration

## Structure du dépôt

*À venir.*

## Installation

*À venir, dès que le premier prototype sera disponible.*

## Auteur

Projet réalisé par **Sulio08** dans le cadre d'un projet de formation.
