=============================================
PROJET D'AUTOMATISATION - PYTEST + PLAYWRIGHT
=============================================

------------------------------------------------------------
Description du projet
------------------------------------------------------------
Ce projet contient des tests UI automatisés développés avec :
- Python
- Pytest
- Playwright
- Allure Reporting

Les tests sont exécutés sur le site SauceDemo :
https://www.saucedemo.com/

------------------------------------------------------------
Structure du projet
------------------------------------------------------------
/tests
    test_cart.py
    test_checkout.py
    test_login.py
    test_logout.py
    test_inventory.py

/pages
    cart.py
    checkout.py
    login.py      # utilisé pour login et logout, pas besoin de logout.py séparé
    inventory.py

requirements.txt (liste des exigences minimum)

requirements-freeze.txt (liste détaillée des exigences)


------------------------------------------------------------
1) Prérequis
------------------------------------------------------------
- Windows 10/11
- Python 3.12 recommandé (vérifier avec : python --version)
- Google Chrome installé
- pip installé (fourni avec Python)
- (Optionnel mais recommandé) Allure CLI pour le reporting

Se placer dans le répertoire racine du projet avant d’exécuter les commandes

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
4) Lancer les tests
------------------------------------------------------------
Se placer dans le répertoire 'saucedemo\playwright'

Lancer les tests dans le dossier tests :

    pytest -v tests\

------------------------------------------------------------
5) Générer le rapport Allure
------------------------------------------------------------
Étape 1 : Exécuter les tests et générer les résultats Allure :

    pytest -v --alluredir=allure-results

Étape 2 : Ouvrir le rapport Allure :

    allure serve allure-results

------------------------------------------------------------
6) Installer Allure CLI sur Windows
------------------------------------------------------------
Important : "allure-pytest" est une librairie Python.
Elle **n’installe pas** la commande `allure`.
Il faut installer Allure Commandline (CLI) séparément.

------------------------------------------------------------
Option A (recommandée) : Installer Allure avec Scoop
------------------------------------------------------------
Ouvrir PowerShell (de préférence en administrateur) et exécuter :

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    irm get.scoop.sh | iex

Puis installer Allure :

    scoop install allure

Vérifier l'installation :

    allure --version

------------------------------------------------------------
Option B : Installer Allure avec Chocolatey
------------------------------------------------------------
Si Chocolatey est installé :

    choco install allure

Vérifier :

    allure --version

------------------------------------------------------------
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
7) Optionnel : Générer un rapport HTML (alternative à Allure)
------------------------------------------------------------
Vous pouvez également générer un simple rapport HTML avec pytest-html :

Installer :

    pip install pytest-html

Générer le rapport :

    pytest -v --html=report.html --self-contained-html

Le rapport sera créé dans le fichier : report.html



