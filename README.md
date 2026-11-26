# Electric City

**Electric City** est un jeu de gestion de réseau électrique écrit en Python avec Pygame. Explore une carte sans limite, installe des moyens de production, stocke l'énergie, alimente des clients et développe tes technologies grâce à la recherche.

## Sommaire

- [Installation et lancement](#installation-et-lancement)
- [Première partie](#première-partie)
- [Commandes](#commandes)
- [La carte et le personnage](#la-carte-et-le-personnage)
- [Construire son réseau](#construire-son-réseau)
- [Recherche et progression](#recherche-et-progression)
- [Économie et énergie](#économie-et-énergie)
- [Graphiques](#graphiques)
- [Sauvegardes](#sauvegardes)
- [Dépannage](#dépannage)
- [À propos du prototype](#à-propos-du-prototype)

## Installation et lancement

1. Installe Python 3 si nécessaire.
2. Ouvre un terminal dans le dossier `ElectricCitySim`.
3. Installe Pygame Community Edition :

   ```powershell
   py -m pip install pygame-ce
   ```

4. Lance le jeu :

   ```powershell
   py electric_city.py
   ```

Si la commande `py` n'existe pas sur ton ordinateur, essaie `python` à la place. Depuis le dossier parent du projet, tu peux aussi lancer le jeu avec :

```powershell
py .\ElectricCitySim\electric_city.py
```

## Première partie

Depuis le menu principal, choisis **Nouvelle partie** pour créer une ville. Tu commences avec un budget, une petite réserve d'énergie et une parcelle libre autour de ton personnage.

Pour construire :

1. Choisis une catégorie dans le panneau **Construire**.
2. Fais défiler le catalogue avec la molette si tu veux voir d'autres équipements.
3. Clique sur l'équipement désiré.
4. Clique sur une parcelle libre de la carte.

Le coût est retiré du budget au moment de la construction. Tu ne peux pas construire sur une parcelle occupée ni sur la case où se trouve le personnage. Les bâtiments bloquent son passage.

## Commandes

| Action | Commande |
| --- | --- |
| Marcher vers le haut | **Z** |
| Marcher vers la gauche | **Q** |
| Marcher vers le bas | **S** |
| Marcher vers la droite | **D** |
| Afficher/masquer les graphiques | **G** |
| Ouvrir/fermer l'arbre de recherche | **R** |
| Mettre en pause/reprendre | **Espace** ou bouton **Pause** |
| Modifier la vitesse | Boutons **x1**, **x2**, **x4** |
| Revenir au menu principal | **Échap** ou bouton **Menu** |
| Ouvrir les outils de test | **F3** |

Les touches **ZQSD** correspondent à un clavier français AZERTY. Le personnage reste au centre de l'écran pendant que la carte défile autour de lui.

## La carte et le personnage

La carte est générée au fur et à mesure de l'exploration : tu peux continuer à marcher et à construire dans toutes les directions. Le personnage sert de repère pour parcourir la ville. Si un bâtiment se trouve devant lui, il faudra contourner l'obstacle.

L'heure du jeu apparaît dans l'interface et dans la bulle du personnage. Le décor change entre le jour et la nuit. La production solaire augmente pendant la journée et diminue la nuit.

## Construire son réseau

Le catalogue contient **plus de 50 équipements de production et de stockage**, ainsi que des installations pour créer de la demande. Les modèles avancés coûtent davantage et nécessitent des recherches.

| Catégorie | Exemples | Fonction |
| --- | --- | --- |
| Solaire | Panneaux de toiture, bifaciaux, fermes solaires | Produit de l'électricité surtout le jour |
| Éolien | Micro-éoliennes, modèles terrestres et offshore | Produit selon la force du vent |
| Hydro | Roues hydrauliques, turbines, barrages | Produit une puissance régulière |
| Autres | Biomasse, géothermie, hydrogène, centrales thermiques | Ajoute différentes sources de production |
| Stockage | Batteries, supercondensateurs, hydrogène, stockage gravitaire | Augmente la capacité de la réserve |
| Clients | Bornes téléphone, bornes voiture, quartiers | Crée une demande et rapporte de l'argent lorsque l'énergie est fournie |

Les illustrations des équipements sont dessinées dans le jeu. Les formes et les détails changent selon leur technologie : panneaux, pales, turbines, réservoirs, batteries, bâtiments et bornes.

## Recherche et progression

Appuie sur **R** ou clique sur **Recherche** pour afficher l'arbre. Il comporte des branches pour le solaire, l'éolien, l'hydraulique, les autres productions et le stockage.

Les recherches se font dans l'ordre, niveau par niveau. Les équipements avancés restent visibles dans le catalogue, mais leur niveau technologique doit être débloqué avant de pouvoir les construire. Les ventes d'énergie rapportent des points de recherche.

## Économie et énergie

Les sources alimentent les clients. Quand la production dépasse la demande, l'énergie excédentaire recharge les batteries. Quand elle ne suffit pas, le réseau utilise la réserve. Si la production et la réserve sont trop faibles, certains clients ne sont pas servis.

Les ventes rapportent de l'argent. Développe les installations de production avant d'ajouter trop de clients, et construis du stockage pour mieux gérer les variations de production, en particulier la nuit.

Le vent varie au cours de la partie. Le panneau supérieur affiche l'heure, le budget, la production, le stock de batterie et les coupures.

## Graphiques

Appuie sur **G** ou clique sur **Graphiques** pour voir l'évolution récente de la production et de la consommation, ainsi que le niveau de charge des batteries. Les courbes affichent les 60 derniers relevés et adaptent leur échelle aux valeurs de la partie.

## Sauvegardes

Le menu principal propose trois emplacements. Tu peux charger ou sauvegarder une partie depuis ce menu. Dans la ville, le bouton **Sauvegarder** écrit dans l'emplacement 1. Une sauvegarde automatique de l'emplacement 1 est également faite au passage d'un nouveau jour et à la fermeture du jeu.

Les données sont stockées dans `saves.json`, à côté de `electric_city.py`. Les anciennes sauvegardes de la première carte sont converties lors du chargement.

## Dépannage

### La fenêtre du jeu reste noire

Ferme la fenêtre, puis relance `electric_city.py` depuis le terminal. Vérifie que tu exécutes le fichier présent dans le dossier `ElectricCitySim` et que Pygame est installé avec `py -m pip install pygame-ce`.

### Pygame n'est pas trouvé

Dans le même terminal que celui utilisé pour lancer le jeu, exécute :

```powershell
py -m pip install pygame-ce
```

Puis relance le jeu avec `py electric_city.py`.

## À propos du prototype

Electric City est un prototype en cours de développement. Les calculs de production, de demande, de stockage et de revenus sont simplifiés pour rendre la simulation facile à prendre en main. Les sauvegardes sont locales à ce dossier.
