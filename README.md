# PROJET PYTHON : GESTION DES  LIVRES D'UNE BIBLIOTHEQUE

## Commençons

### Installation des dépendances

#### Python 3.10.2


Cliquer sur ce lien pour télécharger la dernière version de l'interpréteur python [python docs](https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe)

## Invite de commande

Nous vous recommandons de travailler dans l'invite de commande  chaque fois que vous utilisez Python pour des projets. Cela permet de garder vos dépendances pour chaque projet séparées et organisées. Les instructions pour configurer un invite de commande pour votre plate-forme peuvent être trouvées dans les [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Si vous êtes dans un envirnnement windows nous vous recommandons d'installer gitbash pour faciliter les tests,pour cela veuillez cliquer sur ce 

. (https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-32-bit.exe)  si vous utilisez une architecture 32 bits

.(https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe)si vous utilisez une architecture 64 bits
### Dépendances PIP

Une fois que vous avez configuré et exécuté votre invite de commande, installez les dépendances en accédant au répertoire `/projetPython` et exécuté:

```bash
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

Cela installera tous les packages requis que nous avons sélectionnés dans le fichier `requirements.txt`.

##### Dépendances clés

- [Flask](http://flask.pocoo.org/)  est un framework léger de microservices backend. Flask est nécessaire pour gérer les demandes et les réponses.

- [SQLAlchemy](https://www.sqlalchemy.org/)est la boîte à outils Python SQL et l'ORM que nous utiliserons pour gérer la base de données sqlite légère. Vous travaillerez principalement dans gestionLivre.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) est l'extension que nous utiliserons pour gérer les demandes d'origine croisée de notre serveur frontal.


## Exécution du serveur

Assurer que l'invite de commande soit ouvert dans le dossier `projetPython` pour pouvoir faire les tests 

Pour exécuter le serveur sous Linux ou Mac, exécutez :

```bash
export FLASK_APP=gestion_livre.py
export FLASK_ENV=development
flask run
```
Pour exécuter le serveur sur windows, exécutez :

```bash
set FLASK_APP=gestion_livre.py
set FLASK_ENV=development
flask run
```

Définir la variable `FLASK_ENV` sur `development` détectera les modifications de fichiers et redémarrera le serveur automatiquement.

Définir la variable `FLASK_APP` sur `gestion_livre` indique à flask d'utiliser le fichier `gestion_livre.py`pour trouver l'application.

## DOCUMENTATION DE L'API

Démarrage

URL de base : à l'heure actuelle, cette application ne peut être exécutée que localement et n'est pas hébergée en tant qu'URL de base. L'application principale est hébergée par défaut, http://localhost:5000 ; qui est défini comme proxy dans la configuration frontale.

## Error Handling
Les erreurs sont renvoyées sous forme d'objets JSON au format suivant :

{

    "Etat":"Echec",

    "Type d'erreur":404,

    "Cause":"Elément non trouvé"
}


L'API renvoie trois types d'erreurs en cas d'échec des requêtes :

. 400: Bad request 

. 500: Internal server error

. 404: Not found

## Les routes
### Les routes concernat les catégories
 #### GET/categories

    GENERAL:
    Cette route permet d'avoir la liste de toutes les catégories ainsi que le nombre total de catégorie. 
    
        
    EXTRAIT: curl http://localhost:5000/categories
```  
{
    "Etat": "Succès",
    "Liste des categories": [
        {
            "Identifiant": 3,
            "Libellé": "Comédie"
        },
        {
            "Identifiant": 4,
            "Libellé": "Drame"
        },
        {
            "Identifiant": 5,
            "Libellé": "Négritude"
        },
        {
            "Identifiant": 6,
            "Libellé": "Science-fiction"
        }
    ],
    "Nombre de catégories": 4
}
```

#### GET/categories/id

    GENERAL:
        Cette route permet de  retrouver une catégorie grâce à son id, si l'id n'existe pas une erreur 404 est renvoyé au cas contraire la catégorie trouvée est affichée 
    
        
    EXTRAIT: curl http://localhost:5000/categories/5
```  
{
    "Catégorie recherchée": {
        "Identifiant": 5,
        "Libellé": "Négritude"
    },
    "Etat de la recherche": "succès"
}
```

#### DELETE/categories/id

    GENERAL:
         Cette route permet de supprimer une catégorie grâce à son id;
         si l'id n'existe pas une erreur 404 est renvoyé, au cas contraire elle affiche après suppression la catégorie supprimé,les catégories restantes et leurs nombres. 
```
        EXTRAIT: curl -X DELETE http://localhost:5000/categories/3

{
    "Catégorie suprimée": {
        "Identifiant": 3,
        "Libellé": "Comédie"
    },
    "Catégories restantes": [
        {
            "Identifiant": 4,
            "Libellé": "Drame"
        },
        {
            "Identifiant": 5,
            "Libellé": "Négritude"
        },
        {
            "Identifiant": 6,
            "Libellé": "Science-fiction"
        }
    ],
    "Etat de suppression": "succès",
    "Nombre restant": 3
}
```
#### PATCH/categories/id
  ``` 
  GENERAL:

  Cette route permet de modifier le libellé d'une catégorie grâce à son id;
  si l'id n'est pas trouvé une erreur 404 est renvoyé,au cas où l'id est trouvé mais les données fournies en json ne sont pas conformes une erreur 400 est renvoyée.Au cas contraire  la catégorie 
  est renvoyée avec les modifications effectuées
  ``` 
  ``` 
  EXTRAIT.....Pour la modification

  curl -X PATCH http://localhost:5000/categories/6 -H "Content-Type:application/json" -d '{"libelle":"Aventure"}'
  
{
         "Categorie modifiee": {
         "Identifiant": 6,
           "Libelle": "Aventure"
         },
      "Etat de la modification": "succes"
}

  ``` 
#### POST/categories
  ``` 
    GENERAL:    
    Cette route est utilisée pour créer des catégories en envoyant les données en format json si les données envoyées ne sont pas conformes une erreur 400 est renvoyée au cas contraire la catégorie créer est renvoyée avec le nombre total de catégories
  ``` 

    EXTRAIT.....Pour l'ajout

    curl -X POST http://localhost:5000/categories -H "Content-Type:application/json" -d '{"libelle":"Horreur"}'

    {
    "Etat ajout": "success",
    "Total des categories": 4,
    "categorie ajoutee": {
    "Identifiant": 7,
    "Libelle": "Horreur"
    }
    }
   
### Les routes concernat les livres
  
#### GET/livres
 ```
    GENERAL:
        Cette route permet d'avoir la liste de tous les livres ainsi que le nombre total de livre. 
  ```
         
    EXTRAIT: curl http://localhost:5000/livres
  
    {
    "Etat": "Succes",
    "Liste des livres": [
    {
      "Auteur": "Ferdinand OYONO",
      "Code ISBN": "VIBO",
      "Date de la publication ": "Tue, 05 Dec 2000 00:00:00 GMT",
      "Editeur": "kbbueb",
      "Identifant Categorie": 4,
      "Identifiant": 40,
      "Titre": "Une vie de boy"
    },
    {
      "Auteur": "Bernard DADIE",
      "Code ISBN": "CLIB",
      "Date de la publication ": "Sun, 02 Mar 1952 00:00:00 GMT",
      "Editeur": "li",
      "Identifant Categorie": 5,
      "Identifiant": 44,
      "Titre": "Climbi\u00e9"
    }
    ],
    "Nombre de livres": 2
    }



#### GET/livres/id

    GENERAL:
        Cette route permet de  retrouver un livre grâce à son id, si l'id n'existe pas une erreur 404 est renvoyé au cas contraire le livre trouvé est affiché 
    
  ```    
    EXTRAIT: curl http://localhost:5000/livres/44

{
  "Etat de la recherche": "succes",
  "Livre recherche": {
    "Auteur": "Bernard DADIE",
    "Code ISBN": "CLIB",
    "Date de la publication ": "Sun, 02 Mar 1952 00:00:00 GMT",
    "Editeur": "li",
    "Identifant Categorie": 5,
    "Identifiant": 44,
    "Titre": "Climbi\u00e9"
  }
}
```

#### GET/livres/id_cat/categories

    GENERAL:
        Cette route permet de  retrouver les livres d'une catégorie grâce à l'id de ce dernier,si l'id n'est pas trouvé une erreur 404 est renvoyée, au cas contraire la liste des livres ainsi que le nombre de livre de la catégorie est renvoyé.
    
 ```       
    EXTRAIT: curl http://localhost:5000/livres/6/categories
  
{
  "Categorie": "Aventure",
  "Etat de la recherche": "success",
  "Les livres trouves": [
    {
      "Auteur": "Voltaire",
      "Code ISBN": "CAVO",
      "Date de la publication ": "Wed, 02 Oct 1478 00:00:00 GMT",
      "Editeur": "kalo",
      "Identifant Categorie": 6,
      "Identifiant": 46,
      "Titre": "Candide"
    }
  ],
  "Nombre de livre": 1
}

```

#### DELETE/livres/id

    GENERAL:
         Cette route permet de supprimer un livre grâce à son id;
         si l'id n'existe pas une erreur 404 est renvoyé, au cas contraire elle affiche après suppression le livre supprimé,les livres restants et leurs nombres. 
```

        EXTRAIT: curl -X DELETE http://localhost:5000/livres/44
{
    "Catégorie suprimée": {
        "Identifiant": 3,
        "Libellé": "Comédie"
    },
    "Catégories restantes": [
        {
            "Identifiant": 4,
            "Libellé": "Drame"
        },
        {
            "Identifiant": 5,
            "Libellé": "Négritude"
        },
        {
            "Identifiant": 6,
            "Libellé": "Science-fiction"
        }
    ],
    "Etat de suppression": "succès",
    "Nombre restant": 3
}{
  "Etat de suppression": "success",
  "Livre restants": [
    {
      "Auteur": "Ferdinand OYONO",
      "Code ISBN": "VIBO",
      "Date de la publication ": "Tue, 05 Dec 2000 00:00:00 GMT",
      "Editeur": "kbbueb",
      "Identifant Categorie": 4,
      "Identifiant": 40,
      "Titre": "Une vie de boy"
    }
  ],
  "Livre suprimee": {
    "Auteur": "Bernard DADIE",
    "Code ISBN": "CLIB",
    "Date de la publication ": "Sun, 02 Mar 1952 00:00:00 GMT",
    "Editeur": "li",
    "Identifant Categorie": 5,
    "Identifiant": 44,
    "Titre": "Climbi\u00e9"
  },
  "Nombre restant": 1
}

```
#### PATCH/livres/id
```
  GENERAL:
   Cette route permet de modifier des informations  d'un livre grâce à son id;
   si l'id n'est pas trouvé une erreur 404 est renvoyé,au cas où l'id est trouvé mais  les données fournies en json ne sont pas conformes une erreur 400 est renvoyée.Au cas contraire  la livre
  est renvoyé avec les modifications effectuées
```
```

  EXTRAIT.....Pour la modification
   curl -X PATCH http://localhost:5000/livres/40 -H "Content-Type:application/json" -d '{"Editeur":"Africa","Date de la publication":"1658-05-12"}'  

{
  "Etat de la modification": "success",
  "Livre modifie": {
    "Auteur": "Ferdinand OYONO",
    "Code ISBN": "VIBO",
    "Date de la publication ": "Sun, 12 May 1658 00:00:00 GMT",
    "Editeur": "Africa",
    "Identifant Categorie": 4,
    "Identifiant": 40,
    "Titre": "Une vie de boy"
  }
}
```


#### POST/livres

    GENERAL:    
    Cette route est utilisée pour créer des livres en envoyant lles données en format json si les données envoyées ne sont pas conformes une erreur 400 est renvoyée au cas contraire le livre est enregistré est renvoyée avec le nombre total de livre
   
```

    EXTRAIT.....Pour l'ajout

    curl -X POST http://localhost:5000/livres -H "Content-Type:application/json" -d '{"Code ISBN":"CAVO","Titre":"Candide","Date de la publication":"1478-10-02","Auteur":"Voltaire","Editeur":"kalo","Identifiant Categorie":6}'

{
  "Etat de l'ajout": "success",
  "Livre ajoute": {
    "Auteur": "Voltaire",
    "Code ISBN": "CAVO",
    "Date de la publication ": "Wed, 02 Oct 1478 00:00:00 GMT",
    "Editeur": "kalo",
    "Identifant Categorie": 6,
    "Identifiant": 46,
    "Titre": "Candide"
  },
  "Total des livres": 2
}
```
