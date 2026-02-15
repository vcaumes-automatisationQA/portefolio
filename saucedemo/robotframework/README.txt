===========================================
PROJET D'AUTOMATISATION - ROBOTFRAMEWORK
===========================================

------------------------------------------------------------
Description du projet
------------------------------------------------------------
Ce projet contient des tests UI automatisés développés avec :
- Python
- RobotFramework
- RobotFramework Reporting (logs, reports)
- Allure Reporting (optionnel)

Les tests sont exécutés sur le site SauceDemo :
https://www.saucedemo.com/

------------------------------------------------------------
Structure du projet
------------------------------------------------------------
/robotframework
    /tests
        test_login.robot
        test_logout.robot
        test_inventory.robot
        test_cart.robot
        test_checkout.robot
    /resources
        login.resource
        inventory.resource
        cart.resource
        checkout.resource

/README.txt (ce fichier)

/requirements.txt (liste des exigences minimum)

/requirements-freeze.txt (liste détaillée des exigences)

------------------------------------------------------------
1) Prérequis
------------------------------------------------------------
- Windows 10/11
- Python 3.12 recommandé (vérifier avec : python --version)
- Google Chrome installé
- pip installé (fourni avec Python)
- RobotFramework installé
- (Optionnel) Allure CLI pour reporting avancé

Se placer dans le répertoire racine du projet avant d’exécuter les commandes.

------------------------------------------------------------
2) Créer un environnement virtuel (recommandé)
------------------------------------------------------------
Dans le dossier du projet :

    python -m venv venv

Activer l'environnement :
-------------------------

Windows :
    venv\Scripts\activate

Mac / Linux :
    source venv/bin/activate

Pour désactiver l'environnement (en fin de test ou avant de charger un autre environnement) :
-------------------------------------------------------------------------------------------
    deactivate

------------------------------------------------------------
3) Installer les dépendances
------------------------------------------------------------
Installer les dépendances depuis le fichier requirements.txt :

    pip install -r requirements.txt

------------------------------------------------------------
4) Lancer les tests RobotFramework
------------------------------------------------------------
Se placer dans le répertoire 'robotframework/tests'

Exemple pour exécuter tous les tests :

    robot .

Exemple pour exécuter un test précis :

    robot test_login.robot

------------------------------------------------------------
5) Générer les rapports RobotFramework
------------------------------------------------------------
- Les logs et rapports HTML sont générés automatiquement dans le dossier `log.html` et `report.html` après chaque exécution.
- Pour générer un rapport Allure (si allure-pytest est installé et configuré) :

    robot --listener allure_robotframework:./allure-results .

- Pour visualister les résultats après les tests

	allure serve allure-results
	 
⚠️ Allure CLI doit être installé séparément (voir section suivante)

------------------------------------------------------------
6) Installer Allure CLI sur Windows
------------------------------------------------------------
Important : "allure-robotframework" est une librairie Python.
Elle **n’installe pas** la commande `allure`.
Il faut installer Allure Commandline (CLI) séparément.

Option A (recommandée) : Installer Allure avec Scoop
------------------------------------------------------------
Ouvrir PowerShell (de préférence en administrateur) et exécuter :

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    irm get.scoop.sh | iex
    scoop install allure

Vérifier l'installation :

    allure --version

Option B : Installer Allure avec Chocolatey
------------------------------------------------------------
Si Chocolatey est installé :

    choco install allure
    allure --version

Option C : Installation manuelle
------------------------------------------------------------
1) Télécharger Allure Commandline (zip) depuis :
   https://github.com/allure-framework/allure2/releases

2) Extraire le dossier (ex : C:\allure)

3) Ajouter le chemin suivant dans votre PATH Windows :
   C:\allure\bin

4) Redémarrer PowerShell

5) Vérifier :

   allure --version

------------------------------------------------------------
7) Optionnel : Générer un rapport HTML simple
------------------------------------------------------------
Vous pouvez également générer un simple rapport HTML avec le listener RobotFramework HTML (built-in) :

Après chaque exécution, les fichiers `log.html`, `report.html` et `output.xml` sont créés dans le dossier courant.

Exemple pour un test unique :

    robot test_logout.robot

