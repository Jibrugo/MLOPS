# Vers du DevOps (Code Engineering)

**Attention : ces TD font office de contrôle continu pour le module MLOps. Une note individuelle sera attribuée.**

## Partie I : 

### Contexte Général

Les deux séances de TD seront consacrées au déploiement (ingénierie logicielle). L'objectif est d'aborder des notions essentielles à travers un projet pratique. Ces notions seront intégrées dans l'ordre suivant :

1. Gérer la communication entre des microservices (API) avec Docker Compose, via des Domain Unix Sockets.
2. Ajouter une base de données dans l'écosystème.
--- Réponse 2 ---
L'ajout de la base de données s'effectue via une base postgre que je rends accessible de 2 manières différentes en admin et en utilisateur.


3. Introduire les GitHub Actions (.github/workflows/ci_cd.yml).
--- Réponse 3 ---
Pour ce qui est des GitHub Actions j'ai choisis d'en avoir 3 différentes :
    - Ci_Cd : Le processus d'intégration et déploiement continu qui est là pour tester et construire et déployer mon application.
    - Docker-image : Pour vérifier que tout ce qui concerne la construction d'images Docker, leur publication et les tests.
    - db-Update : Pour la mise à jour des bases de données dès qu'il y en a une


4. L'utilisation de Nginx est-elle nécessaire ? (Questions)
--- Réponse 4 ---

Dans notre cas Nginx n'est pas forcément nécessaire, dans le cas où l'on souhaite une redirection du trafic sur des ports spécifiques et configurer plus simplement le réseau entre nos services. Dans notre cas on restera sur Docker Compose qui fait déjà très bien le travail désirer


5. Migrer de Docker Compose vers Kubernetes (Minikube) ? 
--- Réponse 5 ---

Dans notre cas , n'est clairement pas nécessaire car il est principalement adapté pour des grands projets qui ont besoin de grande scalabilité. Pour nous cela constituerai à terme un potentiel surcoût inutile pour la complexité du projet. Utiliser Kubernetes est une perspectives dans le cas où on voudrait gérer plusieurs environnement pour le développement si il se fait à grande échelle. 


### Lien vers la base commune

Une base commune vous a été fournie sous le lien suivant : [https://github.com/AghilasSini/build_api_ml.git](https://github.com/AghilasSini/build_api_ml.git). Vous devrez décider si vous souhaitez intégrer ou non les éléments mentionnés dans la liste ci-dessus. Chaque choix devra être justifié.

---

## Instructions Générales : 

Une base commune vous a été fournie. À vous de décider si vous souhaitez intégrer ou non les éléments évoqués dans la liste ci-dessus. Chaque choix devra être justifié.

---

## Partie II – Un portail web adapté 

Il s'agit de concevoir une solution prenant en compte les éléments mentionnés ci-dessus et répondant au cahier des charges illustré par la figure ci-dessous (analogie avec Umtice).

![Projet](./un_portail_pour_les_gouverner_tous.png)
---

## Partie III – Un portail web pour tous les gouvernés (conception et architecture de système pour du ML)

Il s'agit de concevoir une plateforme d'annotation automatique de données brutes. Cette plateforme devra héberger des outils de traitement automatique des langues.
--- Partie 3 Explication ---

Sujet choisis :
Notre objectif est de réaliser une plateforme d'annotation automatique. le but est de pouvoir avoir en entrée de l'audio qui sera enregistrer puis transcrit à l'écrit ou bien du texte brut directement écrit par l'utilisateur. Le but plus précis derrière est d'identifier le registre dans lequel le contenu a été écrit. Ici on se concentrera sur un contenu qui sera dit soutenu (textes avec du respect de la langue et entre les personnes), neutre (qui sera notre marqueur d'hésitation du système) et enfin familier (l'emploi de gimique de langage, patois, formulation vulgaire qui seront pénalisés et mènera à cette annotation).

1. Données disponibles et défis : 

Dans le cadre du projet MLOPS ayant pour but d'exploiter des outils issus du traitement automatique des langues. On sait que l'on va avoir à gérer diverses types de données en entrées. Dans notre cas on souhaite pouvoir recueillir en entrée des données textuelles et vocales. Nous allons donc avoir à gérer des fichiers d'entrée potentiellement volumineux. 

Dans un premier temps pour les données vocales on les transcris vers du texte.
Bien que un bruit n'est pas à négliger une correction de cette transcription sera possible car proposée à l'utilisateur.

Notre priorité sera également de veiller à la balance des classes entre elles lorsque l'on aura entrainé notre système derrière de sorte à bien avoir une annotation qui ne soit pas toujours la même. 

Par soucis d'éthique, nous ne conserverons pas les données vocales des utilisateurs. Une des limites du système est dans le cas où des personnes sont citées de manière directes ou indirectes.

2. Processus et approches :

Dans un premier temps il y aura pour le système une phase de préparation de la base de données qui sera exploitée en ammont. On aura comme dit précedemment un prétraitement des textes qui sera nécessaire pour possiblement les annonymisés, les lemmatisés ou plus simplement avoir le même format de typographie.

Notre modèle on partira d'un système qui a déjà fait ses preuves dans la tâche comme un BERT que l'on va entrainé à le spécialisé. 

On prendra soin d'au préalable décider de métriques d'évaluation de celui-ci pour se justifier via le précision, rappel ou encore f1-score.


Pour ce qui est du côté technologique, un stockage cloud sera privilégier au vu de la quantité de données qui sera enmagasinée. On prendra soin de containeriser justement via Kubernetes comme notre plateforme sera un projet à grande échelle.

L'utilisation d'une grande variété de tests automatisés pour s'assurer du bon fonctionnement de l'application et du modèle sans encombre. 

L'ensemble sera donc une application web qui sera connecter à une API RESTful qui emploiera le modèle dans le but annoter automatiquement le contenu.

Côté développement on se permettra de suivre en temps réel les performances et retours du modèle afin de l'ajuster et le mettre à jour en cas d'erreurs de performance à l'utilisation. On mettra à disposition un système de retour utilisateur en plus pour nous simplifier la remontée de cas spécifiques d'erreurs.


3. Objectifs et résultats attendus

Etant donner que notre tâche est assez simple, il est attendu d'avoir une précision du modèle élevée. D'autre part l'utilisation de kuberneties et l'optimisation de l'application de manière générale vise à avoir une latence extrêmement faible de toute part, à la fois du modèle mais aussi de la réponse API pour ne pas entâcher l'expérience utilisateur. 
Là où il faudra être vigilant c'est sur la robustesse du modèle afin qu'il n'y ait peu ou pas de bavures problématiques de sa part.

Conclusion : 
L'architecture globale du projet vise à être efficace et de pouvoir identifier rapidement à travers les remontées d'erreurs ce qu'il faut faire pour l'améliorer.
Bien que plutôt basique comme annotation elle ne reste néanmoins potentiellement utile pour juger la qualité de son propre discours si l'on veut un exemple de son utilisation dans la vie courante.


---

 