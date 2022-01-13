from flask import Flask, flash, request, render_template, jsonify
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


ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS



# funzione per controllare che l'estensione del file sia accettabile
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def input():
    return render_template('index.html')


@app.route('/data/analysis', methods=['POST'])
def output():

    # data_folder = os.path.join(path, '..', 'data')
    # dataset = pd.read_excel(os.path.join(data_folder, 'data_reg_anca.xls'))
    # data_preprocessed = preprocessing(dataset)
    if request.method == 'POST':
        if request.form.get("submit_a"):
            file = request.files['file']
            if file.filename == '':
                flash("you have to select a file!")
                return render_template('index.html')
            if not allowed_file(file.filename):
                flash('only xlsx or xls files are accepted')
                return render_template('index.html')

            # SALVO DATASET NELLA CARTELLA static E LO LEGGO
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            dataset = pd.read_excel(filepath)
            data_preprocessed = preprocessing(dataset)
            results = jsonify(predictions_hip_6months(data_preprocessed))
            return results
        elif request.form.get("submit_b"):
            form = request.form
            input_data = {
                "Uid": form,#.id_paziente.data
                "Sesso": form, #.sesso.data
                "Anni ricovero": form,
                "Data operazione": form,
                "Data dimissione": form,
                "Nome evento": form,
                "Nome equipe": form,
                "Procedura intervento": form,
                "HHS Function PreOp": form,
                "HHS Total PreOp": form,
                "VAS PAIN risp PreOp": form,
                "SF12 PhysicalScore PreOp": form,
                "SF12 MentalScore PreOp": form,
                "HOOSPS Total PreOp": form,
                "BMI altezza risp PreOp": form,
                "BMI peso risp PreOp": form,
                "BMI Total PreOp": form,
                }
            input_data = pd.DataFrame.from_dict(input_data).T
            data_preprocessed = preprocessing(input_data)
            results = jsonify(predictions_hip_6months(data_preprocessed))
            return results

        return render_template('index.html')


if __name__ =="__main__":  
    app.run(debug = True)  