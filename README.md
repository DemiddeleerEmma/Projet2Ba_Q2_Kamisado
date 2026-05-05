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

## Principe de la stratégie

Pour la prise de décision de l’IA, nous utilisons l’algorithme Negamax couplé à l’élagage alpha‑beta, une optimisation du Minimax permettant d’explorer efficacement l’arbre des coups tout en réduisant drastiquement le nombre d’états évalués. L’évaluation d’un coup repose sur plusieurs critères positionnels et stratégiques, détaillés ci‑dessous : 

* **Détection immédiate de victoire :** priorité absolue si une pièce atteint la ligne d’arrivée.

* **Avancement des pièces :** bonus croissant selon la progression vers la zone adverse.

* **Contrôle du centre :** bonus supplémentaire pour les pièces situées dans les colonnes centrales.

* **Liberté d’avancement :** points pour chaque case libre devant une pièce dans sa direction de déplacement.

* **Mobilité globale :** avantage proportionnel à la différence de coups légaux entre dark et light.

## Arborescence du dépôt
```
.
├── requirement.txt
├── .gitignore
├── serveur.py
├── stratégie.py
├── test_stratégie
├── main.py              # Fichier principal : IA + serveur TCP
└── README.md            # Documentation du projet
```

## bibliothèques utilisées

* socket : communication réseau
* threading : gestion du serveur
* struct : encodage des messages
* json : échanges de données
* time : gestion du temps
* sys : arguments en ligne de commande
* random : messages aléatoires

## Dépendances 
L'IA a été développée et testée sous Pyhton 3.11.4.

Pour installer les éventuelles dépendances :

```
python -m pip install -r requirement.txt
```

## Auteurs
**Noms:** Demiddeleer Emma; Gailly Aurélie

**Matricules:** 24374 et 24164

## organigramme algorithmique de l'IA

<img width="439" height="1600" alt="stratégie" src="https://github.com/user-attachments/assets/42163669-c3a9-4fe7-b558-e15c8b4f6126" />

> Ce projet est développé dans le cadre du cours "Advanced Python 2BA", à l’ECAM

