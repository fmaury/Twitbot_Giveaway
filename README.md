# Twitbot_Concours
Twitbot est un programme qui permet de retweeter, aimer et suivre des postes correpondant à un hashtag ou une tendance et
followback les personnes vous ayant ajouté.

Automatisé avec crontab il permet de jouer aux jeux concours sur twitter.

## Installation

`$ pip install -r requirement.txt`

## Ajoutez vos clefs dans le fichier token.yaml :

```
CONSUMER_KEY : "Votre Consumer Key (API Key)"
CONSUMER_SECRET : "Votre Consumer Secret (API Secret)"
ACCESS_TOKEN : "Votre Access Token"
ACCESS_SECRET : "Votre Access Token Secret"
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
00 10 * * 7   cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "#pastis" 10
30 11 * * *   cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "#Concours" 50
00 12 * * 3,5 cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "#LeagueOfLegends" 20
00 15 * * *   cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "trend" 10
00 18 * * *   cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "followback"
30 22 * * *   cd /home/user/Twitbot_Concours/ && /bin/python /home/user/Twitbot_Concours/Twitbot.py "#VimOverEmacs" 20
```
