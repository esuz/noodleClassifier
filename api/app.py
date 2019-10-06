import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from fastai import *
from fastai.vision import *

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    # clean up
    os.system("rm -rf ./uploads/*")
    os.system("rm -rf ./static/*")

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("Nothing done.")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('generate_result', filename=filename))
    return '''
    <!doctype html>
    <head>
    <title>NoodleClassifier</title>
    </head>
    <body>
    <h1>Noodle classifier</h1>
    <h2>Upload an image of a noodle.</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </body>
    '''

def model(image_path:str)->str:
    noodle_types = ['penne', 'maccheroni', 'fusilli', 'farfalle', 'spaghetti', 'udon']
    img = open_image(Path(image_path))
    data2 = ImageDataBunch.single_from_classes(".", noodle_types, 
                                          ds_tfms=get_transforms(),
                                          size=224).normalize(imagenet_stats)
    learn = cnn_learner(data2, models.resnet34)
    #../noodleClassifier/data/models
    learn.load('./stage_2')
    pred_class, pred_idx, outputs = learn.predict(img);
    return(pred_class)

from flask import send_from_directory
@app.route('/result/<filename>')
def generate_result(filename):
    path = (app.config['UPLOAD_FOLDER'])

    file_path = path + "/" + filename
    prediction = model(file_path)

    static_file_path = "/static/" + filename
    os.system("mv " + file_path + " ./static")

    return render_template("result.html", file_path=static_file_path,
     prediction=prediction)


    
                               