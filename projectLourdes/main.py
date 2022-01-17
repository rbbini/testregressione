from flask import Flask, flash, request, render_template, jsonify, abort
from werkzeug.utils import secure_filename
import os
import pandas as pd
from utils import preprocessing, predictions_hip_6months

app = Flask(__name__)


path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static')

# CREAZIONE CARTELLA static SE NON ESISTE
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


SECRET_KEY = 'b\xfeT\x93\x1b\xe5\x9b\xe9\x9c\x1c@\xf6\xef\xbe\x81b\xc2\xd5(\xe9E\xab\xe8\xfe'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['SECRET_KEY'] = SECRET_KEY


# funzione per controllare che l'estensione del file sia accettabile
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/data/analysis', methods=['POST'])
def output():
    if "dataSource" in request.form and request.form.get("dataSource") == "manually":
        file = request.files['file']
        if file.filename == '':
            flash("you have to select a file!")
            return render_template('index.html')
        if not allowed_file(file.filename):
            flash('only xlsx or xls files are accepted')
            return render_template('index.html')
        
        # SALVO DATASET NELLA CARTELLA static E LO LEGGO
        #filename = secure_filename(file.filename)
        #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file.save(filepath)
        
        dataset = pd.read_excel(file)
        data_preprocessed = preprocessing(dataset)
        predictions, other = predictions_hip_6months(data_preprocessed)
        results = jsonify(predictions)
        other_data = jsonify(other)
        
        return results, other_data
    
    elif "dataSource" in request.form and request.form.get("dataSource") == 'patientEpisode':
        form = request.form
        input_data = {
            "Uid": form['uid'],
            "Sesso": form['sesso'],
            "Anni ricovero": form['anni_ricovero'],
            "Data operazione": form['data_operazione'],
            "Data dimissione": form['data_dimissione'],
            "Nome evento": form['nome_evento'],
            "Nome equipe": form['nome_equipe'],
            "Procedura intervento": form['procedura_intervento'],
            "HHS Function PreOp": form['anni_ricovero'],
            "HHS Total PreOp": form['anni_ricovero'],
            "VAS PAIN risp PreOp": form['anni_ricovero'],
            "SF12 PhysicalScore PreOp": form['anni_ricovero'],
            "SF12 MentalScore PreOp": form['anni_ricovero'],
            "HOOSPS Total PreOp": form['anni_ricovero'],
            "BMI altezza risp PreOp": form['anni_ricovero'],
            "BMI peso risp PreOp": form['anni_ricovero'],
            "BMI Total PreOp": form['anni_ricovero']
            }
        
        input_data = pd.DataFrame.from_dict(input_data, orient = 'index').T
        data_preprocessed = preprocessing(input_data)
        predictions, other = predictions_hip_6months(data_preprocessed)
        results = jsonify(predictions)
        other_data = jsonify(other)
        return results, other_data
    else:    
        abort(400)



if __name__ =="__main__":  
    app.run(debug = True)  