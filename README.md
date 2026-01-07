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

### How to run the app : 
```
    python -m api_detection.main
    python -m api_description.main
    python -m api_intermediaire.main
    streamlit run app_streamlit/app.py
```

### Architecture Fichiers

``` 
    ├── 🗂️ api_description
    │   ├── 📄 __init__.py
    │   ├── 🗂️ dev
    │   │       └── 📄 dev_notebook.ipynb
    │   ├── 🗂️ tests
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 test_api_description.py
    │   ├── 📄 requirements.txt
    │   ├── 📄 main.py
    │   └── 📄 setup_model.py
    ├── 🗂️ api_detection
    │   ├── 📄 __init__.py
    │   ├── 🗂️ tests
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 test_detection.py
    │   ├── 📄 requirements.txt
    │   └── 📄 main.py
    ├── 🗂️ api_intermediaire
    │   ├── 📄 __init__.py
    │   ├── 🗂️ dev
    │   │       └── 📄 dev_notebook.ipynb
    │   ├── 🗂️ modules
    │   │       └── 📄 db_tools.py
    │   ├── 🗂️ tests
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 test_intermediaire.py
    │   ├── 📄 requirements.txt
    │   └── 📄 main.py
    ├── 🗂️ app_streamlit
    │   ├── 📄 __init__.py
    │   ├── 🗂️ pages
    │   │       ├── 📄 1_formulaire.py
    │   │       └── 📄 2_charger_images.py
    │   ├── 🗂️ modules
    │   │       └── 📄 email_valide.py
    │   ├── 🗂️ tests
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 test_app_streamlit.py
    │   ├── 📄 requirements.txt
    │   └── 📄 app.py
    ├── 🗂️ database
    │   ├── 📄 __init__.py
    │   ├── 🗂️ data
    │   │       ├── 📄 db_init.py
    │   │       └── 📄 models.py
    │   ├── 🗂️ dev
    │   │       └── 📄 dev.py
    │   ├── 🗂️ modules
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 encryption_db.py
    │   ├── 🗂️ tests
    │   │       ├── 📄 __init__.py
    │   │       └── 📄 test_orm.py
    │   ├── 📄 requirements.txt
    │   ├── 📄 main.py
    │   └── 📖 users.db
    ├── 🗂️ logs
    │   ├── 📄 log_main.log
    │   └── 📄 log_test.log
    ├── 🗂️ reference
    ├── 🗂️ tests
    │   └── 📄 test_setup.py
    │   ├── 🗂️ assets
    │       └── 📄 react.svg
    ├── 📄 .gitignore
    ├── 📄 pytest.ini
    ├── 📄 README.md
    ├── 📄 requirements.in
    └── 📄 requirements.txt
```

### Methode Merise
**MCD**
**MLD**
**MPD**

### Répartition US:
- SPRINT 1 :
    **Hanna :** US 7 (5 points), US 6 (3 points)
    **Djanamali :** US 1 (2 points), US 2 (3 points), US 5 (3 points)
    **Cyril :** US 3 (5 points), US 4 (5 points)
- SPRINT 2 :
    **Hanna :** US 10, US 11, US 14 
    **Djanamali :** US 15 , US 16, US 8, US 9, US 12
    **Cyril :** US 17, US 18, US 19, US 20

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

[![Build Status](https://github.com/PSEUDO/DEPOT/actions/workflows/build_tests.yml/badge.svg)](https://github.com/PSEUDO/DEPOT/actions)