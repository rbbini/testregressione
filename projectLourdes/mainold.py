from flask import Flask, flash, request, render_template, jsonify, abort
from werkzeug.utils import secure_filename
import os
import pandas as pd
from utilsST import preprocessing, predictions_hip_6months

app = Flask(__name__)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static')

# CREAZIONE CARTELLA static SE NON ESISTE
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


# funzione per controllare che l'estensione del file sia accettabile
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')


@app.route('/data/analysis', methods=['POST'])
def output():
    # data_folder = os.path.join(path, '..', 'data')
    # dataset = pd.read_excel(os.path.join(data_folder, 'data_reg_anca.xls'))
    # data_preprocessed = preprocessing(dataset)

    if "dataSource" in request.form and request.form.get("dataSource") == "manually":
        file = request.files['file']
        if file.filename == '':
            flash("you have to select a file!")
            return 'File inserito correttamente'
        if not allowed_file(file.filename):
            flash('only xlsx or xls files are accepted')
            return 'File inserito non valido'

        # SALVO DATASET NELLA CARTELLA static E LO LEGGO
        #filename = secure_filename(file.filename)
        #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file.save(filepath)
        
        dataset = pd.read_excel(file)
        data_preprocessed = preprocessing(dataset)
        predictions = predictions_hip_6months(data_preprocessed, "dataset")
        results = jsonify(predictions)
        other_data = jsonify(other)
        
        return results
    
    elif "dataSource" in request.form and request.form.get("dataSource") == 'patientEpisode':
        form = request.form
        input_data = {
            "Uid": form['uid'],  # .id_paziente.data
            "Sesso": form['sesso'],  # .sesso.data
            "Anni ricovero": form['anni_ricovero'],
            "Data operazione": form['data_operazione'],
            "Data dimissione": form['data_dimissione'],
            "Nome evento": form['nome_evento'],
            "Nome equipe": form['nome_equipe'],
            "Procedura intervento": form['procedura_intervento'],
            "HHS Function PreOp": form['HHS_FpreOp'],
            "HHS Total PreOp": form['HHS_TpreOp'],
            "VAS PAIN risp PreOp": form['VAS_PAIN_PreOp'],
            "SF12 PhysicalScore PreOp": form['physicalScore'],
            "SF12 MentalScore PreOp": form['mentalScore'],
            "HOOSPS Total PreOp": form['HOOSPS'],
            "BMI altezza risp PreOp": form['bmi_altezza_preOp'],
            "BMI peso risp PreOp": form['bmi_peso_preOp'],
            "BMI Total PreOp": form['bmi_total_preOp']
            }

        input_data = pd.DataFrame.from_dict(input_data, orient='index').T
        data_preprocessed = preprocessing(input_data)
        predictions = predictions_hip_6months(data_preprocessed, "single_patient")
        results = jsonify(predictions)
        return results
    else:
        abort(400)



if __name__ == "__main__":
    app.run(debug=True)
