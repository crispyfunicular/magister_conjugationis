# MAGISTER CONJUGATIONIS : Entraînement à la conjugaison latine
Lien vers le site internet : https://crispyfunicular.github.io/magister_conjugationis/  
Ce site permet de s'entraîner aux conjugaisons latines en proposant des exercices personnalisables par temps, personne, voix, mode ou encore groupe de verbes. *Amo*, *capiebantur*, *deleuissetis*... l'apprentissage de la conjugaison latine devient un vrai jeu d'enfant !  

![Aperçu du site Magister Conjugationis](magister_img.png "Aperçu du site Magister Conjugationis")

## Description
Ce programme permet de faire pratiquer les conjugaisons latines à l'utilisateurice de la façon suivante :
- Le programme peut afficher un verbe conjugué (ou forme fléchie) en latin, l'utilisateurice doit donner successivement les informations suivantes : personne, temps, voix, mode, traduction de l'infinitif. Exemple :
```
  Nouveau verbe à trouver : narrabamus
  Indiquer la personne (de 1 à 6) : 4
  Temps possibles : présent, imparfait, futur, parfait, plus-que-parfait ou futur antérieur : imparfait
  Indiquer la voix (actif, passif ou déponent) : actif
  Indiquer le mode (indicatif, subjonctif ou impératif) : indicatif
  Indiquer la traduction en français (à l'infinitif) : raconter
  Bravo !
```
- Le programme peut afficher les informations suivantes : personne, temps, voix, mode... et demander à l'utilisateur de fournir la forme fléchie correspondante en latin.
```
Indiquer la forme fléchie pour le(s) verbe(s) 'commencer', à la 3e personne du singulier, imparfait, passif, indicatif
incipiebatur
```

Si la réponse proposée n'est pas celle attendue, l'utilisateurice a la possibilité :
1. de tenter à nouveau sa chance ;
2. de voir les temps primitifs du verbe en question ; ou
3. de voir la réponse (auquel cas iel ne marquera aucun point pour la question).
```
Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ?
```

## Rappel concernant les conjugaisons latines
Le lemme de chaque verbe latin indique ses "**temps primitifs**", qui fournissent un certain nombre d'informations cruciales à son sujet, notamment le groupe verbal auquel il appartient. Ainsi, "o, as, are, aui, atum" indique de façon univoque qu'il s'agit d'un verbe du premier groupe.  
Les verbes latins sont en effet classés en groupes. Le programme utilise la classification suivante :
- (1) "o, as, are"
- (2) "eo, es, ere"
- (3) "o, is, ere"
- (4) "io, is, ere"
- (5) "io, is ire"
- (0) Pour les besoin du programme, la catégorie 0 correspond au verbe "esse" et à ses dérivés.

Les lettres "u" et "v" sont interchangeables, ainsi que "i" et "j" (le "v" et le "j" correspondant tous deux à une graphie tardive). Par conséquent, "amavi" est aussi valide qu'"amaui" et "jussi" est aussi valide que "iussi".  

Le latin comporte également des verbes déponents. Ces verbes ont la particularité de présenter une morphologie passive (ex: "sequor", "miraris"...) mais un sens actif. Bien qu'ils se conjuguent comme le passif de leur groupe respectif, ils se traduisent par une voix active (ex: miror = "je m'étonne"). Nous les avons marqués avec l'étiquette `VX=dep`.

Les formes verbales latines ne portant aucune marque de genre, "amat" peut aussi bien être traduit par "il aime" que par "elle aime". En revanche, "on aime" n'est pas pris en compte par le programme.  

Lorsqu'un verbe latin admet plusieurs traductions en français, n'importe laquelle de celles-ci est admise par le programme (p. ex. : "legere" = lire, cueillir, choisir).


## NooJ : génération des formes fléchies
La richesse morphologique du latin est gérée grâce à NooJ, un outil de traitement automatique du langage naturel. Le cœur du système repose sur la séparation stricte entre le lexique (les racines) et la grammaire (les règles de flexion).

### Dictionnaire (.dic)
Chaque verbe est entré dans le dictionnaire avec deux racines distinctes, correspondant aux deux thèmes fondamentaux du système verbal latin :

- `Theme=INF` (**infectum**) : utilisé pour les temps suivants : présent, imparfait et futur actifs et passifs.
- `Theme=PER` (**perfectum**) : utilisé pour les temps suivants : parfait, plus-que-parfait et futur antérieur *actifs*.
- `Theme=SUP` (**supinum**) : utilisé pour les temps suivants : parfait, plus-que-parfait et futur antérieur *passifs*.

Exemple pour le verbe "amare" (aimer) :

```
am,amare,V+GP=1+Theme=INF+FLX=GP1_INF   # Racine "am-" pour l'infectum (INF)
amau,amare,V+GP=1+Theme=PER+FLX=GP1_PER # Racine "amau-" pour le perfectum (PER)
amat,amare,V+GP=1+Theme=SUP+FLX=GP1_SUP # Racine "amat-" pour le supinum (SUP)
```

### Grammaire flexionnelle (.nof)
Les formes conjuguées sont générées par des grammaires graphiques qui assemblent dynamiquement :
- Le thème verbal fourni par le dictionnaire.
- La voyelle thématique propre au groupe verbal (ex : "a" pour le 1er groupe, "e" pour le 2e...).
- Le suffixe temporel (ex: "ba" pour l'imparfait, "bi" pour le futur des 1er et 2e groupes...).
- La désinence personnelle (ex: "o" ou "m", "s", "t", "mus", "tis", "nt" pour les temps de l'actif).

Exemple de règle pour l'imparfait actif du 1er groupe : thème de l'infectum (**am**) + voyelle thématique (**a**) + suffixe temporel (**ba**) + désinence personnelle (**m**) -> **amabam**

### Les verbes déponents
Une gestion spécifique a été implémentée pour les verbes déponents (verbes ayant une forme passive mais un sens actif, comme *sequor* ou *miror*). Ils sont identifiés par l'étiquette `VX=dep`.

Ces verbes ne possédant pas de forme active, et dans la mesure où le thème du *perfectum* ne sert à former que des temps de la forme active, les verbes déponents ne disposent pas de thème perfectum dans le dictionnaire, mais uniquement des deux thèmes suivants :
- `Theme=INF` : utilise les désinences passives pour former les temps de l'infectum (ex: "sequeris").
- `Theme=SUP` : utilise les formes composées (participe + "esse") pour former les temps du perfectum (ex: "secutus sum").

### Nettoyage des faux positifs
Par souci d'efficacité et de simplicité, la grammaire NooJ gère les formes régulières et "régulièrement irrégulières" et génère occasionnellement de "faux positifs" pour les formes "irrégulièrement irrégulières" (p. ex. *"loquiris" vs "loqueris"). Ces formes incorrectes sont filtrées *a posteriori* en Python via le script `pynooj.py`.

## Installation de l'environnement
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation du programme
Attention, les scripts sont conçus pour être lancés depuis la racine comme suit : `python scripts/magister.py`

```bash
$ python scripts/magister.py --help
usage: magister.py [-h] [-d {latin,français}] [-g {0,1,2,3,4,5}] [-p {0,1,2,3,4,5,6}] [-t {futur,futur antérieur,imparfait,parfait,plus-que-parfait,présent}] [-v {actif,passif}] [-m {indicatif,subjonctif}] [--debug]

Interroge l'utilisateur sur les verbes latins

options:
  -h, --help            show this help message and exit
  -d {latin,français}, --direction {latin,français}
                        latin : latin -> français ; français : français -> latin
  -g {0,1,2,3,4,5}, --groupe {0,1,2,3,4,5}
                        Le groupe verbal (ex: 1) que vous souhaitez réviser (0 correspond à "esse" et ses dérivés)
  -p {0,1,2,3,4,5,6}, --personne {0,1,2,3,4,5,6}
                        La personne (comprise entre 1 et 6) que vous souhaitez pratiquer
  -t {futur,futur antérieur,imparfait,parfait,plus-que-parfait,présent}, --temps {futur,futur antérieur,imparfait,parfait,plus-que-parfait,présent}
                        Le temps (ex: "présent") que vous souhaitez pratiquer
  -v {actif,passif,déponent}, --voix {actif,passif,déponent}
                        La voix (actif ou passif) que vous souhaitez pratiquer
  -m {indicatif,subjonctif,impératif}, --mode {indicatif,subjonctif,impératif}
                        Le mode (indicatif ou subjonctif) que vous souhaitez pratiquer
  --debug               activer le mode debug

Bonam fortunam!
```

```
$ python magister.py
Combien de verbes voulez-vous pratiquer (entre 1 et 10) ? 3
Nouveau verbe à trouver : aberas
Indiquer la personne (de 1 à 6) : 2
Bravo !
Temps possibles : présent, imparfait, futur, parfait, plus-que-parfait ou futur antérieur
Réponse : imparfait
Bravo !
Indiquer la voix (actif, passif ou déponent) : actif
Bravo !
Indiquer le mode (indicatif, subjonctif ou impératif) : indicatif
Bravo !
Indiquer la traduction en français (à l'infinitif) : être absent
Bravo !
Indiquer la forme fléchie pour le(s) verbe(s) 'rester', à la 1e personne du pluriel, parfait, passif, indicatif : ?
Mauvaise réponse ! Errare humanum est...
Essayer à nouveau cette question (1), voir les temps primitifs (2), voir le lemme (3) ou voir la réponse (4) ? 2
Voici les temps primitifs : eo, es, ere, mansi, mansum
Indiquer la forme fléchie pour le(s) verbe(s) 'rester', à la 1e personne du pluriel, parfait, passif, indicatif : mansi sumus
Bravo !
Nouveau verbe à trouver : mittentur
Indiquer la personne (de 1 à 6) : 6
Bravo !
Temps possibles : présent, imparfait, futur, parfait, plus-que-parfait ou futur antérieur
Réponse : présent
Mauvaise réponse ! Errare humanum est...
Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ? 3
futur
Indiquer la voix (actif, passif ou déponent) : passif
Bravo !
Indiquer le mode (indicatif, subjonctif ou impératif) : indicatif
Bravo !
Indiquer la traduction en français (à l'infinitif) : ?
Mauvaise réponse ! Errare humanum est...
Essayer à nouveau cette question (1) ou voir la réponse (2) ? 2
envoyer
Score total : 2.6/3
Prêt-e pour une nouvelle partie ?
```

## Remerciements
### NooJ
L'idée de cette migration vers NooJ m'a été aimablement soufflée par <a href="https://nooj.univ-fcomte.fr/the-author.html">M. Max Silberztein</a> à l'issue de la semaine de formation intensive NooJ à l'Inalco du 5 au 9 janvier 2026. Je l'en remercie vivement, tant pour ses conseils que pour la formation.
### DUCLA
Ce projet repose sur la liste de verbes latin fournie dans le cadre du <a href="https://dep-lettresclassiques.parisnanterre.fr/diplomes-universitaires/diplome-universitaire-de-competences-en-langues-anciennes-ducla">Diplôme universitaire de compétences en langues anciennes (DUCLA)</a>, latin, de l'Université Paris Nanterre, et dont Mme Véronique Merlier-Espenel est l'enseignante responsable. Je tiens à la remercier pour le plaisir que je prends à suivre ses cours et à mémoriser mes conjugaisons latines !
### Morphologie
Pour les cours de morphologie, en particulier ceux portant sur les langues fusionnelles, je tiens également à remercier <a href="https://modyco.fr/membre/florence-villoing/">Mme Florence Villoing</a>, de l'Université Paris Nanterre (laboratoire MoDyCo).
### Python
Un énorme merci à ```@camathieu``` pour son aide inestimable sur toute la partie informatique, en particulier pour le code Python.

*Projet développé par Morgane Bona-Pellissier entre 2025 et 2026*