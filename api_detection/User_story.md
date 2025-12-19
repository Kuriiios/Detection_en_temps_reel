# User Story — Traitement et détection d’images

## Description

En tant qu’utilisateur ayant téléversé une image via l’interface,
Je souhaite que mon image soit analysée par un modèle de détection d’objets,
Afin de recevoir une copie de l’image originale annotée avec des boîtes englobantes autour des objets détectés.

1. Fonctionnalité de traitement

Le système doit permettre :
- Le chargement du modèle de détection d’objets YOLO11 côté backend
- La réception et la validation de l’image envoyée par l’utilisateur
- L’analyse de l’image à l’aide du modèle de détection
- La génération d’une nouvelle image contenant les boîtes de détection
- La conversion de cette image annotée en Base64, compatible avec un retour via API
- L’envoi du résultat de l’analyse à l’utilisateur via l’API
- Le retour et l’affichage de l’image analysée dans l’interface utilisateur (Streamlit)

2. Gestion des états
   
- Cas nominal
   - L’image est analysée avec succès
   - L’image annotée est retournée à l’utilisateur
   - Un message de succès est affiché dans l’interface

- Cas d’erreur
  - Impossible de générer l’image annotée
  - Problème serveur lors du traitement ou de l’encodage de l’image
  - Fichier invalide ou type de fichier non supporté
  - Modèle non chargé ou indisponible

3. Notifications et messages système
   
Succès:

    - “The model is loaded”
    - “New image with boxes are generated”

Erreurs:

    - “Cannot generate new image with boxes”
    - “Invalid file”
    - “Invalid file type”
    - “The model isn’t loaded”

4. Détails techniques
   
Backend

Endpoint API :  POST /api/image/detection

- Paramètre d’entrée :
    - file: UploadFile = File(...)

- Validation des données côté serveur
    - Gestion des erreurs HTTP standards (400, 422, 500)
    - 
- Encodage de l’image résultat en Base64 avant retour JSON

5. Scénarios de test
   
- Tests fonctionnels (API_detection)
    - Envoi d’une image valide à l’endpoint
    - Réception d’une image analysée encodée en Base64
    - Code de réponse HTTP 200 OK
    - Présence du champ image_base64 dans la réponse

- Tests unitaires

    - Vérification du format de l’image retournée
    - Vérification de la taille de l’image générée
    - Validation du contenu Base64 (décodage possible)
    - Comparaison structurelle entre image d’entrée et image générée (présence des boîtes)

6, Critères d’acceptation

- L’utilisateur envoie une image valide
- L’API analyse l’image avec le modèle de détection

Cas 1 — Objets détectés:

- Une image avec des boîtes est retournée
- L’image est affichée dans le front end
- Un message de succès est affiché

Cas 2 — Aucun objet détecté:

- Une image sans boîtes est retournée
- Un message d’avertissement indique qu’aucun objet n’a été trouvé

Cas 3 — Erreur serveur:

- L’image d’origine est retournée
- Un message d’erreur est affiché

6. Definition of Done (DoD)

- La user story est considérée comme terminée lorsque :

    - Les routes API nécessaires sont implémentées et fonctionnelles
    - Le front end permet l’envoi d’images et l’affichage des résultats
    - L’API REST est documentée (endpoints, paramètres, réponses)
    - La couverture de tests unitaires est supérieure à 90 %
    - La fonctionnalité est validée par le Product Owner
    - La documentation utilisateur est mise à jour
    - Une revue de code a été réalisée et approuvée

7. Estimation

Estimation : 3 points