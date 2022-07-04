# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 11:23:51 2022

@author: andre
"""

from flask import Flask, flash, request, render_template, jsonify, abort
from werkzeug.utils import secure_filename
import os
import pandas as pd
#from pyearth import Earth
from utilsindent import (
    preprocessing,
    predictions_hip_6months,
    predictions_hipAndKneeR,
    predictions_hipAndKneeC,
    predictions_SpineR,
    predictions_SpineC,
    predictions_SpineOdi,
    predictions_SpineCOdi
)

app = Flask(__name__)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, "static")

# CREAZIONE CARTELLA static SE NON ESISTE
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"xlsx", "xls"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS


# funzione per controllare che l'estensione del file sia accettabile
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home_page():
    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    return render_template("results.html")


@app.route("/data/analysis", methods=["POST"])
def output():
    # data_folder = os.path.join(path, '..', 'data')
    # dataset = pd.read_excel(os.path.join(data_folder, 'data_reg_anca.xls'))
    # data_preprocessed = preprocessing(dataset)

    if "dataSource" in request.form and request.form.get("dataSource") == "manually":
        file = request.files["file"]
        if file.filename == "":
            flash("you have to select a file!")
            return "File inserito correttamente"
        if not allowed_file(file.filename):
            flash("only xlsx or xls files are accepted")
            return "File inserito non valido"

        # SALVO DATASET NELLA CARTELLA static E LO LEGGO
        # filename = secure_filename(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(filepath)

        dataset = pd.read_excel(file)

        # predizioni:
        #   zona_operazione ==  0 o 1 -> anca/ginocchio
        #   zona_operazione ==  2 -> colonna spinale
        if (
            request.form.get("zona_operazione") == 0
            or request.form.get("zona_operazione") == 1
        ):
            # predizioni sia del physical che del mental score
            predictionsR = predictions_hipAndKneeR(dataset, "dataset")
            predictionsC = predictions_hipAndKneeC(dataset, "dataset")
        elif request.form.get("zona_operazione") == 2:
            ############# DA UNIRE LE PREDIZIONI DI PHYSICAL E ODI IN UNA SOLA FUNZIONE/METODO NELL'UTILS
            ############# POI TOGLIERE L'IF/ELSE request.form.get("score") == E LASCIARE SOLO UN CALCOLO DELLE PREDICTIONS
            if request.form.get("score") == "Phisycal":
                predictionsR = predictions_SpineR(dataset, "dataset")
                predictionsC = predictions_SpineC(dataset, "dataset")
                predictionsRO = predictions_SpineOdi(dataset, "dataset")
                predictionsCO = predictions_SpineCOdi(dataset, "dataset")

        # data_preprocessed = preprocessing(dataset)
        # predictions = predictions_hip_6months(data_preprocessed, "dataset")
        # results = jsonify(predictions)
        # other_data = jsonify(other)

        results = {
            "predictionsR": predictionsR,
            "predictionsC": predictionsC,
            "predictionsRO": predictionsRO,
            "predictionsCO": predictionsCO,
        }
        json_results = jsonify(results)
        return json_results

    elif (
        "dataSource" in request.form
        and request.form.get("dataSource") == "patientEpisode"
    ):
        form = request.form

        # knee-hip regressivo

        if (
            request.form.get("zona_operazione") == 0
            or request.form.get("zona_operazione") == 1
        ):

            input_data = {
                "sesso": form["sesso"],
                "anni_ricovero": form["anni_ricovero"],
                "classe_asa": form["classe_asa"],
                "VAS_Total_PreOp": form["VAS_Total_PreOp"],
                "SF12_PhysicalScore_PreOp": form["physicalScore"],
                "SF12_MentalScore_PreOp": form["mentalScore"],
                "BMI_altezza_PreOp'": form["bmi_altezza_preOp"],
                "BMI_peso_PreOp": form["BMI_peso_PreOp"],
                "SF12_autovalsalute_risp_0": form["SF12_autovalsalute_risp_0"],
                "SF12_scale_risp_0": form["SF12_scale_risp_0"],
                "SF12_ultimomeseresa_risp_0": form["SF12_ultimomeseresa_risp_0"],
                "SF12_ultimomeselimite_risp_0": form["SF12_ultimomeselimite_risp_0"],
                "SF12_ultimomeseemo_risp_0": form["SF12_ultimomeseemo_risp_0"],
                "SF12_ultimomeseostacolo_risp_0": form["SF12_ultimomeseostacolo_risp_0"],
                "SF12_ultimomesesereno_risp_0": form["SF12_ultimomesesereno_risp_0"],
                "SF12_ultimomeseenergia_risp_0": form["SF12_ultimomeseenergia_risp_0"],
                "SF12_ultimomesetriste_risp_0": form["SF12_ultimomesetriste_risp_0"],
                "SF12_ultimomesesociale_risp_0": form["SF12_ultimomesesociale_risp_0"],
                "zona_operazione": form["zona_operazione"],
            }

        input_data = pd.DataFrame.from_dict(input_data, orient="index").T
        predictionsR = predictions_hipAndKneeR(input_data, "single_patient")

        predictionsC = predictions_hipAndKneeC(input_data, "single_patient")

        results = {"predictionsR": predictionsR, "predictionsC": predictionsC}
        json_results = jsonify(results)
        return json_results

        # input_data = pd.DataFrame.from_dict(input_data, orient='index').T
        # data_preprocessed = preprocessing(input_data)
        # predictions = predictions_hip_6months(data_preprocessed, "single_patient")
        # results = jsonify(predictions)
        # return results

        # regre classi spine

    elif request.form.get("zona_operazione") == 2:

        if request.form.get("score") == "Phisycal":

            form = request.form

            #if request.form.get("nome_operazione") ==  :

            input_data = {

                "Artrodesi cervicale": "0",
                "Artrodesi lombare": "0",
                "Cifoplastiche": "0",
                "Decompressione lombare": "0",
                "Deformita degenerativa": "0",
                "Deformita idiopatica" : "0",
                "Ernia cervicale": "0",
                "Ernia lombare": "0",
                "Tumore vertebrale": "0",
                "sesso": form["sesso"],  # .sesso.data
                "anni ricovero": form["anni_ricovero"],
                # non separo i valori perché non sono sicuro quali siano di phy/odi pd
                "ODI_Total_PreOp": form["ODI_Total_PreOp"],
                "Vas_Back_PreOp": form["Vas_Back_PreOp"],
                "Vas_Leg_PreOp": form["Vas_Leg_PreOp"],
                "SF36_GeneralHealth_PreOp": form["SF36_GeneralHealth_PreOp"],
                "SF36_PhysicalFunctioning_PreOp": form["SF36_PhysicalFunctioning_PreOp"],
                "SF36_RoleLimitPhysical_PreOp": form["SF36_RoleLimitPhysical_PreOp"],
                "SF36_RoleLimitEmotional_PreOp": form["SF36_RoleLimitEmotional_PreOp"],
                "SF36_SocialFunctioning_PreOp": form["SF36_SocialFunctioning_PreOp"],
                "SF36_Pain_PreOp": form["SF36_Pain_PreOp"],
                "SF36energyfatiguepreop": form["SF36_EnergyFatigue_PreOp"],
                "SF36_EmotionalWellBeing_PreOp": form["SF36_EmotionalWellBeing_PreOp"],
                "SF36_MentalScore_PreOp": form["SF36_MentalScore_PreOp"],
                "SF36_PhysicalScore_PreOp": form["SF36_PhysicalScore_PreOp"],
                "fabqworkpreop": form["FABQ_Work_PreOp"],
                "classe_asa_1": form["classe_asa_1"],
            }

            input_dataC = {
               # "nomeoperazione": form["nome_operazione"],
                "Artrodesi cervicale": "0",
                "Artrodesi lombare": "0",
                "Cifoplastiche": "0",
                "Decompressione lombare": "0",
                "Deformita degenerativa": "0",
                "Deformita idiopatica" : "0",
                "Ernia cervicale": "0",
                "Ernia lombare": "0",
                "Tumore vertebrale": "0",
                "sesso": form["sesso"],  # .sesso.data
                "anni ricovero": form["anni_ricovero"],
                # non separo i valori perché non sono sicuro quali siano di phy/odi pd
                "ODI_Total_PreOp": form["ODI_Total_PreOp"],
                "Vas_Back_PreOp": form["Vas_Back_PreOp"],
                "Vas_Leg_PreOp": form["Vas_Leg_PreOp"],
                "SF36_GeneralHealth_PreOp": form["SF36_GeneralHealth_PreOp"],
                "SF36_PhysicalFunctioning_PreOp": form["SF36_PhysicalFunctioning_PreOp"],
                "SF36_RoleLimitPhysical_PreOp": form["SF36_RoleLimitPhysical_PreOp"],
                "SF36_RoleLimitEmotional_PreOp": form["SF36_RoleLimitEmotional_PreOp"],
                "SF36_SocialFunctioning_PreOp": form["SF36_SocialFunctioning_PreOp"],
                "SF36_Pain_PreOp": form["SF36_Pain_PreOp"],
                "SF36energyfatiguepreop": form["SF36_EnergyFatigue_PreOp"],
                "SF36_EmotionalWellBeing_PreOp": form["SF36_EmotionalWellBeing_PreOp"],
                "SF36_MentalScore_PreOp": form["SF36_MentalScore_PreOp"],
                "SF36_PhysicalScore_PreOp": form["SF36_PhysicalScore_PreOp"],
                "fabqworkpreop": form["FABQ_Work_PreOp"],
                "classe_asa_1": form["classe_asa_1"],
                "MORBIDITY": form["MORBIDITY"],
            }

        input_data = pd.DataFrame.from_dict(input_data, orient="index").T
        input_dataC = pd.DataFrame.from_dict(input_dataC, orient="index").T
        # per ora manca lo step del preprocess, dopo la modifica nel caso lo addiamo

        predictionsR = predictions_SpineR(input_data, "single_patient")
        predictionsC = predictions_SpineC(input_dataC, "single_patient")
        predictionsRO = predictions_SpineOdi(input_data, "single_patient")
        predictionsCO = predictions_SpineCOdi(input_dataC, "single_patient")

        results = {
            "predictionsR": predictionsR,
            "predictionsC": predictionsC,
            "predictionsRO": predictionsRO,
            "predictionsCO": predictionsCO,
        }

        json_results = jsonify(results)
        return json_results

    # input_data = pd.DataFrame.from_dict(input_data, orient='index').T
    # data_preprocessed = preprocessing(input_data)
    # predictions = predictions_hip_6months(data_preprocessed, "single_patient")
    # results = jsonify(predictions)
    # return results
    else:
        abort(400)




"""
input_dataC = {
                "artrodesicervicale": "0",
                "artrodesilombare": "1",
                "cifoplastiche": "0",
                "decompressionelombare": "0",
                "deformitadegenerativa": "0",
                "deformitaidiopatica" : "0",
                "erniacervicale": "0",
                "ernialombare": "0",
                "tumorevertebrale": "0",
                "Sesso": "1",  # .sesso.data
                "Anni ricovero": "4",
                # non separo i valori perché non sono sicuro quali siano di phy/odi pd
                "odi_total_preop": "3",
                "vas back preop": "3",
                "vas leg preop":"3",
                "SF36generalpreop": "3",
                "SF36physicalfunctionpreop": "3",
                "SF36rolelimitphysicalpreop": "3",
                "SF36rolelimitemotionalpreop": "3",
                "SF36socialfunctioningpreop": "3",
                "SF36painpreop": "3",
                "SF36energyfatiguepreop": "3",
                "SF36emotionalwellbeingpreop": "3",
                "SF36mentalscorepreop": "3",
                "SF36physicalscore": "3",
                "fabqworkpreop": "3",
                "classeasa1": "3",
                "morbidity": "3",
            }

input_dataC = pd.DataFrame.from_dict(input_dataC, orient="index").T
predictionsCO = predictions_SpineCOdi(input_dataC, "single_patient")
print(predictionsCO)



"""



if __name__ == "__main__":
    app.run(debug=True)




