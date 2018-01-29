# Twitbot_Concours
Twitbot est un programme qui permet de retweeter, aimer et suivre des postes correpondant à un hashtag ou une tendance et
followback les personnes vous ayant ajouté.

Automatisé avec crontab il permet de jouer aux jeux concours sur twitter.

## Installation

`$ pip install -r requirement.txt`

## Exportez vos clef dans des variables d'environnement :

```
export CONSUMER_KEY="Consumer Key"
export CONSUMER_SECRET="Consumer Secret"
export ACCESS_TOKEN="Access Token"
export ACCESS_SECRET="Access Token Secret"
```
## Usage
```
python Twitbot.py [argument] [nb of tweet]
```
Le premier argument doit etre un hashtag ou un mot clef.

Mots clef :
* trend : récupère le hashtag en tendance France.

* followback : va suivre toutes les personne qui ont suivit votre compte.

Le deuxieme argument doit etre un int, il correspond au nombre de hashtag à récupérer, un tri se fera par la suite pour supprimer les tweet inutiles. Il n'est pas utilisé avec l'argument "followback".

## Pourquoi l'utiliser 
En utilisant le #Concours comme premier argument, il ne va jouer qu'aux concours ayant deja 1k retweet pour éviter de jouer a des concours peu interessants (on veut des lots stylé).

Pour les autres hashtag, il les retweetera que si ils ont deja 5RT, pour eviter de retweeter n'importe quoi (spam, d'autres bot...).

Il faut eviter de jouer uniquement aux jeux concours avec votre compte au cas ou une des personnes l'organisant verifie votre compte.

## Automatiser
Il ne vous reste plus qu'a l'automatiser.

#### Exemple de mon crontab :

```
00 10 * * 7   python Twitbot.py "#melanchon" 10
30 11 * * *   python Twitbot.py "#Concours" 50
00 12 * * 3,5 python Twitbot.py "#LeagueOfLegends" 20
00 15 * * *   Twitbot.py "trend" 10
00 18 * * *   Twitbot.py "followback"
30 22 * * *   Twitbot.py "#PSG" 20
```
