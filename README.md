# Quoridor

## Documentation utilisateur

### Installation et exécution

Pour exécuter le jeu Quoridor, suivez les étapes ci-dessous

1. Assurez-vous d'avoir **Python 3.11** installé sur votre système.
1. Installez les dépendances requises en **exécutant la commande** suivante dans votre **terminal**
   > **pip install socket pickle threading random time**
1. executez également cette commande afin d'installer une version de pygame fonctionnelle
   > **pip install pygame --pre**
1. Naviguez vers le répertoire contenant le code source téléchargé.
1. Exécutez le jeu en utilisant cette commande
   > **python -m main**
1. Le jeu **Quoridor** devrait se lancer avec une interface graphique.
1. Si ce n'est pas le cas essayez de lancer le jeu en utilisant un IDE tel que **Visual Studio Code** ou **Pycharm**

### Utilisation des menus

#### Menu principal

Au lancement du jeu, vous êtes accueillie par le menu principal, il vous offre 3 options

<div class=bulletContainer>

- "Play" pour lancer une partie
- "Rules" pour lire les règles du jeu
- "Quit" pour quitter le jeu

![Lobby](assets/pictures/manual/lobby.png)

</div>

#### Bouton Retour

Un bouton retour est présent dans le coin haut gauche de chaque menu. Il permet de revenir au menu précédent.
![Bouton retour](assets/pictures/manual/boutonBack.png)

#### Régles

La page de régles contient tout ce qu'il y à a savoir sur le déroulement de la partie. vous pouvez naviguer dans en utilisant le défilement de la molette de la souris.

![Régles 1](assets/pictures/Rule.png)![Régles 2](assets/pictures/imageRules.jpg)

#### Jouer une partie en solo

<div class=bulletContainer>

Deux options se présentent a vous

- "Solo" permet de jouer sur un ordinateur
- "Multi" permet de jouer en multijoueur sans fil-local

choisisez donc le mode solo
![Modes de jeux](assets/pictures/manual/choiceMode.png)

</div>

Indiquez maintenant le nombre de joueurs que vous souhaitez avoir dans votre partie.
![Nombre de joueurs](assets/pictures/manual/players.png)

Faites de même avec le nombre de bots
![Nombre de bots](assets/pictures/manual/bots.png)

Indiquez maintenant la taille de la grille de jeu
![Taille de grille](assets/pictures/manual/grid.png)

Finalement choisisez le nombre de barières que vous souhaitez avoir par joueurs

les fleches correspondent a des boutons permettant d'augmenter ou de diminuer le nombre de barières

une fois que vous serez satisfaits de votre choix, cliquez sur le bouton "Done" afin de lancer la partie
![Nombre de barrières](assets/pictures/manual/barrier.png)

<div class=bulletContainer>

La partie démarre, vous pouvez maintenant jouer !

- Le premier joueur est tiré **aléatoirement**.
- Le joueur qui doit jouer est désigné par une pastille blanche sur le plateau, son encard a droite est également plus grand que les autres.
- Les cases roses sont les cases où vous pouvez vous déplacer.

![Plateau de jeu](assets/pictures/manual/game.png)

</div>

Félicitation ! Vous avez désormais toute les connaissances nécessaires pour démarer la partie !

#### Créer une partie multijoueur sans fil-local

Après avoir appuyé sur "Play"
Choisissez le bouton "Multi"

![Modes de jeux](assets/pictures/manual/choiceMode.png)

On souhaite créer un serveur, il faut donc appuyer sur le bouton "Host"

![créer ou rejoindre un serveur](assets/pictures/manual/choiceModeMulti.png)

On choisi le nombre de joueurs (Humains).
A savoir que si vous choisissez 3 joueurs la partie sera comblée avec un bot. le jeu ne pouvant pas être joué par un nombre impaire de joueurs
![Nombre de joueurs](assets/pictures/manual/playersMulti.png)

Indiquez maintenant la taille de la grille de jeu
![Taille de grille](assets/pictures/manual/grid.png)

Choisisez le nombre de barières que vous souhaitez avoir par joueurs
![Nombre de barrières](assets/pictures/manual/barrier.png)

Finalement nommez votre serveur pour que les autres joueurs puissent s'y connecter.
![Nom du serveur](assets/pictures/manual/NameServer.png)

Vous n'avez plus qu'a attendre que vos amis vous rejoignent dans la salle d'attente.
Quand tout le monde est prêt, cliquez sur le bouton "Start" pour lancer la partie.
![Salle d'attente](assets/pictures/manual/waitingRoom.png)

Félicitation ! Vous n'avez plus qu'a jouer !
![Plateau de jeu](assets/pictures/manual/game.png)

#### Rejoindre une partie multijoueur sans fil-local

Après avoir appuyer sur le bouton Play
Choisissez le bouton "Multi".
![Modes de jeux](assets/pictures/manual/choiceMode.png)

On souhaite rejoindre un serveur, il faut donc appuyer sur le bouton "Join"
![créer ou rejoindre un serveur](assets/pictures/manual/choiceModeMulti.png)

Après quelques secondes, un nouveau menu apparait, il peut y avoir deux cas:

<div class="twoPicturesContainer">

<div>

Aucun serveur n'est trouvé. Vous pouvez appuyer sur le bouton "Refresh" pour actualiser la liste des serveurs.
![Aucun serveur trouvé](/assets/pictures/manual/findServerError.png)

</div>

<div>

un serveur est trouvé, cliquez dessus pour le rejoindre.
![Serveur trouvé](assets/pictures/manual/findServerSuccess.png)

</div>

</div>

Vous avez rejoint la salle d'attente, plus qu'a patienter que l'host lance la partie.
![Salle d'attente](assets/pictures/manual/waitingRoomClient.png)
