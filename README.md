# Noodle Classifier 

A noodle classifier with a flask web api. The classifier can distingish between six kind of noodles with an accuracy of about 80 percent. A resnet34 was used as the architecture. Improvement can most likely be achieved by using a different network architecture like resnet50 and training with a cleaner dataset.

noodle_types = ['penne', 'maccheroni', 'fusilli', 'farfalle', 'spaghetti', 'udon']

The training of the model was done in the jupyter nodebook using fastai libraries.

The web app can be launched by navigating to the api directory and lauching the web with:

> gunicorn -w 1 -b :8000 app:app

The images were downloaded from google images with javascript console.

Training dataset is not supplied to avoid copyright issues.
