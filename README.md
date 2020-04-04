# Twitbot_Concours
Twitbot est un programme qui permet de retweeter, aimer et suivre des postes correpondant à un hashtag ou une tendance, 
followback les personnes vous ayant ajouté ou tweeter sur le top tendance.

Automatisé avec cron il permet de jouer aux jeux concours sur twitter.

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
python Twitbot.py --help
```

## Pourquoi l'utiliser 
En utilisant le #Concours comme premier argument, il ne va jouer qu'aux concours ayant deja 500 retweet, modifiable dans le fichier config.yaml, pour éviter de jouer a des concours peu interessants (on veut des lots stylé).

Pour les autres hashtag, il les retweetera que si ils ont deja 5RT, modifiable dans le fichier config.yaml, pour eviter de retweeter n'importe quoi (spam, d'autres bot...).

Il faut eviter de jouer uniquement aux jeux concours avec votre compte au cas ou une des personnes l'organisant verifie votre compte.

```
