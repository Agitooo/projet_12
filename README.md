# **Projet 12 python openclassrooms**

Application CLI EpicEvents réalisée avec Django, click, rich

La version de **Python** à utiliser : _**3.10.5**_

# **ENVIRONNEMENT VIRTUEL**

Création de l'environnement virtuel :


Pour créer l'environnement virtuel il faut exécuter la commande suivante à la racine du projet :

    python -m venv env


Puis la commande suivante pour démarrer l'environnement :

-   sous Linux

    
    source env/bin/activate

-   sous Windows


    env/Scripts/activate.bat


Pour installer les packages spécifiés dans le fichier requirements.txt il faut exécuter la commande suivante :

    pip install -r requirements.txt


# **SCRIPT**

Il faut dans un premier temps, se connecter sinon il ne sera pas possible d'effectuer des actions pour cela il faut 
exécuter la commande suivante :

    python manage.py login

Une fois connecté, il sera possible d'utiliser les fonctions suivantes en fonction du profil de l'utilisateur connecté :

Concernant les employés :

    python manage.py get_employees
    python manage.py add_employee
    python manage.py logout

Concernant les clients :

    python manage.py get_customers
    python manage.py search_customer
    python manage.py add_customer
    python manage.py add_customer_contact

Concernant les contrats :

    python manage.py get_contracts
    python manage.py update_contract
    python manage.py add_contract

Concernant les événements :

    python manage.py get_events
    python manage.py update_event
    python manage.py add_event


### Avec le fichier db.sqlite fournis


Comptes utilisateurs :

| *Identifiant* | *Mot de passe* |
|---------------|----------------|
| gestion       | Tata123!       |
| commercial    | Tata123!       |
| support       | Tata123!       |
| com1          | Tata123!       |
| com2          | Tata123!       |
| com3          | Tata123!       |

Les utilisateurs font partit d'un département (gestion, commercial, support) qui ont des droits spécifiques.
Cette configuration est définie dans le groupe de l'utilisateur lorsque celui-ci a un département attribué.

GESTION :

    ● Créer, mettre à jour et supprimer des collaborateurs dans le système CRM.
    ● Créer et modifier tous les contrats.
    ● Filtrer l’affichage des événements, par exemple : afficher tous les événements qui n’ont pas de «support» associé.
    ● Modifier des événements (pour associer un collaborateur support à l’événement)

COMMERCIAL :

    ● Créer des clients (le client leur sera automatiquement associé).
    ● Mettre à jour les clients dont ils sont responsables.
    ● Modifier/mettre à jour les contrats des clients dont ils sont responsables.
    ● Filtrer l’affichage des contrats, par exemple : afficher tous les contrats qui ne sont pas encore signés, 
    ou qui ne sont pas encore entièrement payés.
    ● Créer un événement pour un de leurs clients qui a signé un contrat.

SUPPORT :

    ● Filtrer l’affichage des événements, par exemple : afficher uniquement les événements qui leur sont attribués.
    ● Mettre à jour les événements dont ils sont responsables.

## Fonctionnalités de l'application CLI

 - Se connecter / Se déconnecter
 - Récupérer la liste des employés / créer un employé
 - Récupérer la liste des clients / rechercher un client / créer un client / ajouter un contact au client
 - Récupérer la liste des contrats / mettre à jour un contrat / créer un contrat
 - Récupérer la liste des événements / mettre à jour un événement / créer un événement