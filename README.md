# Patrimoine en jeu backend

### *fr*

Ceci est une application avec le but de faire revivre le **Patrimoine Alsacien**.

Ici, vous trouvez la configuration pour le **backend.**
Pour la configuration du frontend, vous pouvez la trouver en cliquant sur [ce lien](https://github.com/DragosNH/projet_patrimoine-front).

## 1. Preparer la connexion

- Allez dans les paramètres de votre ordinateur.
- Activez le Mobile Hotspot (Point d’accès mobile).
- Sur votre téléphone, connectez-vous au réseau Wi-Fi partagé par l’ordinateur.

## 2. Trouvez l'adresse IP

- Ouvrez la console Windows :

    - Tapez `cmd` dans la barre de recherche,
    - ou appuyez sur ***Windows + R*** puis écrivez `cmd`.

- Dans la console, tapez :
>ipconfig

- Cherchez la section suivante (votre adresse IP peut être différente) :
>Wireless LAN adapter Local Area Connection* 2:

>IPv4 Adress . . . . . . . . . . . : 192.168.158.6

**Remarque** : C’est l’adresse IP de l’ordinateur qu’il faut récupérer, car c’est lui qui héberge le backend.

## 3. Accéder au dossier backend

Le backend fonctionne avec **Django.**
Naviguez dans le terminal jusqu’au dossier :
>C:\\*ton fichier*\Alsace app\AppCode\backend

## 4. Lancer le serveur Django

Danse ce dossier, lancez le serverur avec la commande suivante:
>python manage.py runserver 0.0.0.0:80

Remplacez `0.0.0.0` par l’adresse IP de votre PC trouvée à l’étape 2, par exemple :

> python manage.py runserver 192.168.158.6:80

## 5. Tester la connexion depuis le téléphone
- Ouvrez un navigateur sur votre téléphone.
- Entrez l’adresse IP (celle du PC) dans la barre d’adresse.

Exemple:
>http://192.168.158.6

## 6. Et Maintenant?
Vous pouvez passer à la documentation pour la [partie frontend.](https://github.com/DragosNH/projet_patrimoine-front)

### *en*

This is a mobile app created to bring the **Heritage from Alsace** back to life.

This is the configuration for the **backend**. To access the configuration for the frontend, you can[click here.](https://github.com/DragosNH/projet_patrimoine-front)

## 1. Getting started
- Go to **settings** on your computer.
- Activate **Mobile hotspot**.
- On your mobile phone, connect to the **Wi-Fi signal shared by your computer.**

## 2. Find the IP address
- Open **Command promt**:
    - Type `cmd` inside the searchbar *(on windows)*
    -   or press ***Windows + R*** and type `cmd`
- Inside the console, type:
>ipconfig
- Look for the following section:
> Wireless LAN adapter Local Area Connection* 2:

>IPv4 Adress . . . . . . . . . . . : 192.168.158.6

**Note**: This is the computer's IP adress that you should recover since that's the one that is hosting the backend.

## 3. Access to the backend file
The backend is in **Django.**
Navigate inside the terminal till you get to the following file:
>C:\\*your folder*\Alsace app\AppCode\backend

## 4. Run the Django server

Once inside the file, run the *Django* server wit the following command:
>python manage.py runserver 0.0.0.0:80

Replace `0.0.0.0` with your IP adress, exemple:
>python manage.py runserver 192.168.158.6:80

## 5. Test the connexion from your phone
- Open a browser from your phone.
- Insert the IP adress inside the URL bar.

Exemple:
> http://192.168.158.6
- If you see a blank page with a small "**Hello world!**" message,  it means the connection was successful.

## 6. And now what?

You can go to the frontend documentation by [clicking here.](https://github.com/DragosNH/projet_patrimoine-front)