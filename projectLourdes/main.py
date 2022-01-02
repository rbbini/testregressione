from flask import Flask, flash, request, secure_filename, render_template
import os
import pandas as pd

app = Flask(__name__)


path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static')

# CREAZIONE CARTELLA static SE NON ESISTE
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS



# funzione per controllare che l'estensione del file sia accettabile
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash("you have to select a file!")
            return render_template('inserire il nome della pagina html')
        if not allowed_file(file.filename):
            flash('only xlsx files are accepted')
            return render_template('inserire il nome della pagina html')
        
        # SALVO DATASET NELLA CARTELLA static E LO LEGGO
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        dataset = pd.read_excel(filepath)
        return render_template('inserire il nome della pagina html')
    return True


@app.route('/output')
def output():
    
    return True






if __name__ =="__main__":  
    app.run(debug = True)  