# MeteoSMS

Pour l'exemple, les informations météorologique récupérée sont celles de la ville de Metz.

## Configuration et utilisation
- Le script nécessite une *connection internet* et l'*activation du service "notification par sms"* de free (gratuit).
- La variable `PageFile` contient l'adresse d'une ville, mais elle peut être remplacée par une autre.
- Il faut rentrer son nom d'utilisateur et son mot de passe dans les variables `user` (l.65) et `password` (l.66)
- Pour un affichage directement dans l'environnement, décommenter la ligne 58.

## Fonctionnement
1. La page du site de météo France est récupéré dans une string 
2. On convertit la string en objet BeautifulSoup. 
3. On récupère par la suite les horaires, puis la température et enfin l'état du ciel.
4. On formatte tout cela à la fin de la fonction `parsing` pour avoir un joli message.
5. On ouvre l'URL contenant le nom d'utilisateur, le mot de passe et le message.

