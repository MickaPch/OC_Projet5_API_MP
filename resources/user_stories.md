# Utilisez les données publiques de l'Open Food Facts


## Définition des acteurs


* Utilisateur de l'application (*yakaUser*)
    * Simple visiteur (*yakaVisitor*)
    * Utilisateur authentifié (*registeredUser*)

## User stories & fonctionnalités


* En tant que **visiteur**, je veux **créer un compte utilisateur** pour **enregistrer mes recherches**. ***--> MUST HAVE***
    * Formulaire de connexion /inscription
        * Au menu principal
        * Lors de l'accès à l'historique des recherches


* En tant qu'**utilisateur de l'application**, je veux **accéder à la liste des catégories** pour **afficher les aliments**. ***--> MUST HAVE***
    * Sélection de la catégorie
        * Affichage de la liste
        * Sélection par choix numéroté (*input* + *vérification validité du choix utilisateur*)
        * Arborescence des catégories et sous catégories
    * Affichage de la liste complète des produits appartenant à la catégorie (choix 0)


* En tant qu'**utilisateur de l'application**, je veux **accéder aux informations Open Food Facts** d'un aliment pour **connaître ses qualités nutritives**. ***--> MUST HAVE***
    * Sélection d'un aliment
        * Affichage de la liste des aliments de la catégorie
        * Sélection par choix numéroté (*input* + *vérification validité du choix utilisateur*)
    * Affichage des informations principales sur l'aliment sélectionné


* En tant qu'**utilisateur de l'application**, je veux **voir les produits alternatifs** à celui sélectionné dans le but de **trouver un aliment plus sain**. ***--> MUST HAVE***
    * Affichage de la liste des aliments
        * Recherche des aliments alternatifs
        * Liste des aliments ordonnée par pertinence et/ou choix plus sain
    * Affichage de la note nutriscore des aliments alternatifs


* En tant qu'**utilisateur authentifié**, je veux **enregistrer l'aliment sélectionné** pour le **retrouver** ultérieurement. ***--> MUST HAVE***
    * Intégrer l'option dans la page de l'aliment
    * Authentification nécessaire


* En tant qu'**utilisateur authentifié**, je veux **accéder à l'historique des produits enregistrés** pour **retrouver les requêtes de recherche de produits alternatifs**. ***--> MUST HAVE***
    * Accéder à l'historique des recherches liées à l'utilisateur depuis le menu
        * Historique des produits cherchés
    * Type de recherche ? (catégorie / date / liste complète) ***--> COULD HAVE***


* En tant qu'**utilisateur de l'application**, je veux **voir le détail des informations de l'un des aliments alternatifs** pour le **comparer à l'aliment sélectionné**. ***--> SHOULD HAVE***
    * Dans la liste des aliments alternatifs, option comparaison avec le produit sélectionné pour comparer les informations essentielles des 2 aliments
    * Possibilité d'enregistrer l'aliment alternatif comparé


* En tant qu'**utilisateur de l'application**, je veux **savoir où le produit sélectionné** et les produits alternatifs sont vendus pour **l'acheter**. ***--> SHOULD HAVE***
    * Choix de la localisation dans une liste
    * Affichage de la disponibilité du produit sélectionné et des produits alternatifs dans le lieu sélectionné


* En tant qu'**utilisateur de l'application**, je veux **voir les détails supplémentaires sur l'aliment sélectionné** pour **m'informer de ses apports nutritifs**. ***--> COULD HAVE***
    * Ouverture d'une page d'informations complémentaires (ingrédients, apports nutritionnels, ... )


* En tant qu'**utilisateur de l'application**, je veux **chercher un produit par une recherche textuelle** pour **accéder à ses informations**. ***--> WON'T HAVE***
    * Possibilité de rechercher un produit grâce à son nom

