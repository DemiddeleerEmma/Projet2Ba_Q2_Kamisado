# Les Infernales – IA de jeu

Cette intelligence artificielle a été développée pour jouer à Kamisado.
Elle repose sur une stratégie combinant recherche algorithmique (Negamax), heuristiques d’évaluation, et gestion du temps pour prendre des décisions efficaces en temps limité.

#Fonctionnalités principales
Détection de victoire immédiate : l’IA reconnaît les situations gagnantes et les exploite directement.
Algorithme Negamax avec élagage alpha-bêta : exploration optimisée de l’arbre de jeu.
Deepening progressif : amélioration continue du coup tant que le temps le permet.
Gestion du temps : limite de calcul (~2.5 secondes) avec arrêt sécurisé.
Génération de coups légaux : prise en compte des contraintes du jeu (couleur imposée).
Évaluation heuristique : l'IA score les mouvements possible selon la progression des pièces sur le plateau, le contrôle du centre et la mobilité.
