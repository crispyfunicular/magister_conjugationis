# Magister Conjugationis : Modélisation NooJ
Ce projet vise à modéliser la morphologie flexionnelle du verbe latin à l'aide du moteur linguistique <a href="https://nooj.univ-fcomte.fr/">NooJ</a>.

L'objectif est de générer dynamiquement l'ensemble des formes fléchies (conjugaisons) en décrivant les règles morphosyntaxiques sous forme de graphes, plutôt que de les lister de manière exhaustive. Cette approche remplace l'ancienne méthode statique (fichiers CSV) utilisée dans le projet <a href="https://github.com/crispyfunicular/magister_conjugationis">Magister conjugationis</a>.

Les dictionnaires et grammaires produits ici ont vocation à être exploités en Python via la librairie pynooj (voir ci-dessous), conçue spécifiquement pour faire le pont entre NooJ et le code Python.

## Librairie pynooj
Pour intégrer les ressources NooJ dans l'écosystème Python, j'ai développé une librairie capable de parser les fichiers ```.dic``` et ```.nod```. Elle est open source et disponible sur PyPI (<a href="https://pypi.org/project/pynooj/">pynooj</a>).

## Lexique des abréviations
```bash
# TP = temps (pres/impf/fut/pft/pqp/fta)
# MOD = mode (ind/sub)
# VX = voix (act/pas)
# P = personne (1/2/3)
# NB = nombre (sg/pl)
# inf = infinitif
# pres = présent (amo)
# impf = imparfait (ex. amabam)
# fut = futur (ex. amabo)
# pft = parfait (ex. amaui)
# pqp = plus-que-parfait (ex. amaueram)
# fta = futur antérieur (ex. amauero)
```

## Arborescence du projet
### 1. Lexical Analysis (analyse lexicale)
Ce dossier contient toutes les ressources nécessaires pour que NooJ reconnaisse les verbes et sache comment ils se transforment (la morphologie).

- ```lat_verbes.dic``` (dictionnaire source) : fichier texte éditable contenant la liste des thèmes verbaux (deux par lemme pour l'instant) et leurs propriétés.

```bash
# GP1 (AMARE)
# amare
am,amare,V+GP=1+Theme=INF+TRAD=aimer+FLX=GP1_INF
amau,amare,V+GP=1+Theme=PER+TRAD=aimer+FLX=GP1_PER

# cogitare
cogit,cogitare,V+GP=1+Theme=INF+TRAD=penser+FLX=GP1_INF
cogitau,cogitare,V+GP=1+Theme=PER+TRAD=penser+FLX=GP1_PER
```

- ```lat_verbes.nod``` (dictionnaire compilé) : version binaire du dictionnaire, générée par NooJ lors de la compilation. C'est ce fichier que le logiciel lit pour analyser le texte. Le ```.dic``` doit être recompilé après chaque modification pour mettre à jour le ```.nod```.

- ```latin_verbs.nof``` (grammaire morphologique) : fichier contenant la grammaire définissant les règles morphosyntaxiques de construction des conjugaisons pour chaque groupe verbal.

```bash
# GP1 (AMARE)
## INFECTUM (am-)

GP1_INF =
	:P1_O/GP=1+TP=pres+MOD=ind | :GP :P_ACT/TP=pres+MOD=ind | :GP :P3_ACT/TP=pres+MOD=ind |
	:GP :IMPF_IND :P1_M/ | :GP :IMPF_IND :P_ACT/ | :GP :IMPF_IND :P3_ACT/ |
	:GP :FUT_1-2 <B> :P1_O/ | :GP :FUT_1-2 :P_ACT/ | :GP :FUT_1-2 <B>u :P3_ACT/ |

	:P1_OR/GP=1+TP=pres+MOD=ind | :GP :P_PAS/TP=pres+MOD=ind |
	:GP :IMPF_IND r/VX=pas+P=1+NB=sg | :GP :IMPF_IND :P_PAS/ | :GP :IMPF_IND :P3_PAS/ |
	:GP :FUT_1-2 <B> :P1_OR/ | :GP :FUT_1-2 <B>eris/P=2+NB=sg | :GP :FUT_1-2 :P_PAS/ | :GP :FUT_1-2 <B>u :P3_PAS/ |

	:GP_SUB :P1_M/TP=pres | :GP_SUB :P_ACT/TP=pres | :GP_SUB :P3_ACT/TP=pres |
	:GP :IMPF_SUB :P1_M/ | :GP :IMPF_SUB :P_ACT/ | :GP :IMPF_SUB :P3_ACT/ |

	:GP_SUB :P1_OR <L><B>/TP=pres | :GP_SUB :P_PAS/TP=pres | :GP_SUB :P3_PAS/TP=pres ;
```

- ```lat_verbes-flx.dic``` : fichier contenant le résultat de l'application de la grammaire sur le dictionnaire, c'est-à-dire la liste complète des formes fléchies générées.

```bash
amo,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+VX=act+P=1+NB=sg+GP=1+TP=pres+MOD=ind
amor,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+VX=pas+P=1+NB=sg+GP=1+TP=pres+MOD=ind
amem,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=1+NB=sg+TP=pres
ames,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=2+NB=sg+TP=pres
amet,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=3+NB=sg+TP=pres
amemus,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=1+NB=pl+TP=pres
ametis,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=2+NB=pl+TP=pres
ament,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=act+P=3+NB=pl+TP=pres
ameris,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=2+NB=sg+TP=pres
ametur,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=3+NB=sg+TP=pres
amemur,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=1+NB=pl+TP=pres
amemini,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=2+NB=pl+TP=pres
amentur,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=3+NB=pl+TP=pres
amer,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+MOD=sub+VX=pas+P=1+NB=sg+TP=pres
amas,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+VX=act+P=2+NB=sg+TP=pres+MOD=ind
amat,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+VX=act+P=3+NB=sg+TP=pres+MOD=ind
amamus,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+VX=act+P=1+NB=pl+TP=pres+MOD=ind
amatis,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+VX=act+P=2+NB=pl+TP=pres+MOD=ind
amant,amare,V+Theme=INF+TRAD=aimer+FLX=GP1_INF+GP=1+VX=act+P=3+NB=pl+TP=pres+MOD=ind
```

- ```Conjugaisons latines.pdf``` : Tableau de conjugaison des cinq groupes de verbes latins pour l'indicatif (manque le subjonctif).

### 2. Projects (projets & corpus)
Il contient les textes bruts sur lesquels lancer les analyses, en l'occurrence une liste ```.txt``` de toutes les formes fléchies des verbes. 

## Etat du projet
### Fonctionnalités implémentées
Le projet couvre déjà tous les groupes verbaux, pour les temps et modes suivants :
```bash
# INFECTUM (am-)
## INDICATIF (ind)
#### > ACTIF (act) : présent (pres) | imparfait (impf) | futur (fut)
#### > PASSIF (pas) : présent (pres) | imparfait (impf) | futur (fut)
## SUBJONCTIF (sub)
#### > ACTIF (act) : présent (pres) | imparfait (impf)
#### > PASSIF (pas) : présent (pres) | imparfait (impf)

# PERFECTUM (amau-)
## INDICATIF (ind)
#### > ACTIF (act) : parfait (pft) | plus-que-parfait (pqp) | futur antérieur(fta)
## SUBJONCTIF (sub)
#### > ACTIF (act) : parfait (pft) | plus-que-parfait (pqp)

# SUPINUM (amat-)
## INDICATIF (ind)
#### > PASSIF (pas) : parfait (pft) | plus-que-parfait (pqp) | futur antérieur(fta)
## SUBJONCTIF (sub)
#### > PASSIF (pas) : parfait (pft) | plus-que-parfait (pqp)
```
