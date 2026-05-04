# Les Infernales – IA de jeu

Cette intelligence artificielle a été développée pour jouer à Kamisado.
Elle repose sur une stratégie combinant recherche algorithmique (Negamax), heuristiques d’évaluation, et gestion du temps pour prendre des décisions efficaces en temps limité.

## Fonctionnalités principales
* Génération de coups légaux : prise en compte des contraintes du jeu.
* Détection de victoire immédiate : l’IA reconnaît les situations gagnantes et les exploite directement.
* Évaluation heuristique : l'IA score les mouvements possible selon la progression des pièces sur le plateau, le contrôle du centre et la mobilité.
* Algorithme Negamax avec élagage alpha-bêta : exploration optimisée de l’arbre de jeu.
* Deepening progressif : amélioration continue du coup tant que le temps le permet.
* Gestion du temps : limite de calcul (~2.5 secondes) avec arrêt sécurisé.

## Arborescence du dépôt
```
.
├── requirements.txt
├── .gitignore
├── serveur.py
├── stratégie.py
├── test_stratégie
├── main.py              # Fichier principal : IA + serveur TCP
└── README.md            # Documentation du projet
```

## Principe de la stratégie
```

![Description](asserts/stratégie.jpeg)

```

## bibliothèques utilisées

* socket : communication réseau
* threading : gestion du serveur
* struct : encodage des messages
* json : échanges de données
* random : messages aléatoires
* time : gestion du temps
* sys : arguments en ligne de commande

## Auteurs
**Noms:** Demiddeleer Emma; Gailly Aurélie

**Matricules:** 24374 et 24164
