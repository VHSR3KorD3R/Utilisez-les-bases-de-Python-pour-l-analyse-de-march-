# Utilisez les bases de Python pour l'analyse de marché

##Outil de scraping du site http://books.toscrape.com/

Cet outil récupère toutes les informations disponible des livres sur le site.
Ensuite ces données seront stockés sous la forme d'un fichier csv. Chaque catégorie de livre aura son fichier csv.
De plus chaque l'outil télécharge les couvertures de chaque livre.
Voici la liste des données récupéré par le script:

 - product_page_url : l'url du livre
 - universal_product_code (upc) : le code du livre
 - title : le titre
 - price_including_tax : le prix avec taxe
 - price_excluding_tax : le prix hors taxe
 - number_available: le nombre de livres disponible
 - product_description: un résumé du livre
 - category: la catégorie du livre
 - review_rating: la note des personnes qui ont acheté le livre
 - image_url: l'url de la couverture du livre


##Utilisation de l'outil de scraping

1 - Installer Python 3 et git

2 - Placez-vous dans le répertoire souhaité et entrez les commandes suivantes
```bash
mkdir scraping
cd scraping
git clone https://github.com/VHSR3KorD3R/Utilisez-les-bases-de-Python-pour-l-analyse-de-march-.git
```

3 - Créez l'environnement virtuel et activez-le
```bash
    python -m venv env
    source env/bin/activate
```

4 - Installez les modules requis
```bash
    pip install -r requirements.txt
```

5 - Lancez l'application 
```bash
    python main.py
```