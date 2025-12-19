# Projet 1 : Détection en temps réel avec webcam et image to text

### Énoncé :
Développez une application de détection en temps réel qui utilise la webcam pour identifier des
objets dans l'environnement. L'application doit permettre :
- La visualisation du flux vidéo de la webcam avec les objets détectés en temps réel.
- La prise de photos à partir du flux vidéo.
- Le chargement d'images depuis le système de fichiers.
- Pour chaque image (prise par la webcam ou chargée), l'application doit :
* Identifier les objets présents dans l'image.
* Générer une description textuelle de l'image en utilisant un modèle "image to text".
* Afficher la description textuelle à l'utilisateur.

### Détails :
- Utilisez OpenCV pour la capture vidéo et le traitement d'images.
- Utilisez un modèle de détection d'objets pré-entraîné de Hugging Face (ex:
facebook/detr-resnet-50). Explorez Yolo V11
- Utilisez un modèle "image to text" pré-entraîné de Hugging Face (ex:
nlpconnect/vit-gpt2-image-captioning).

#### Description détaillée :
L'application permettra à l'utilisateur de visualiser le flux vidéo de sa webcam avec les objets
détectés en temps réel. Il pourra prendre des photos à partir du flux vidéo ou charger des
images depuis son ordinateur. Pour chaque image, l'application identifiera les objets
présents et générera une description textuelle en utilisant un modèle "image to text"
pré-entraîné. La description sera affichée à l'utilisateur dans l'interface Gradio.

### Bibliothèques :
- opencv-python
- transformers
- torch

### Architecture Fichiers

``` 

```

### Methode Merise
**MCD**
**MLD**
**MPD**

### Répartition US:
**Hanna :** US 7 (5 points), US 6 (3 points)
**Djanamali :** US 1 (2 points), US 2 (3 points), US 5 (3 points)
**Cyril :** US 3 (5 points), US 4 (5 points)

### Liens Internes:
* [Excalidraw](https://excalidraw.com/#room=dc221f1a8d9507c1e77d,XtKv-aLhHVwFvLK4v--Q_Q) 
* [Story mapping sheets](https://docs.google.com/spreadsheets/d/1aZ3k_PSkeQrGVGQ7HDYPhYgNXTsV9dMSDWWDFndWSDg/edit?gid=0#gid=0)
* [Story mapping Miro](https://miro.com/app/board/uXjVGbXlrEQ=/)
* [Logiciel Gestion Taiga](https://tree.taiga.io/project/cyril07-projet-1-detection-en-temps-reel-avec-webcam-et-image-to-text/backlog)
* [docs](https://docs.google.com/document/d/1z-2EQtrSnGrUCZtEnxD7ydTiCBjTCLG9PlurV5bL-g8/edit?tab=t.0)

### Sources:

* [OpenCV Capture Video from Camera](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
* [modèle de détection d'objets](https://huggingface.co/facebook/detr-resnet-50)
* [modèle de détection d'objets YOLO](https://docs.ultralytics.com/fr/modes/predict/#why-use-ultralytics-yolo-for-inference)
* [liste modeles open cv](https://huggingface.co/opencv)
* [modèle "image to text"](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)
* [modele “image to text2”](https://huggingface.co/Salesforce/blip-image-captioning-large)