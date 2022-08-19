from flask import Flask, flash, request, render_template, jsonify, abort
import os
import pandas as pd
from utilsindent import (
    preprocessSpine,
    check_gender,
    predictions_hipAndKneeR,
    predictions_hipAndKneeC,
    predictions_SpineR,
    predictions_SpineC
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

    if "dataSource" in request.form and request.form.get("dataSource") == "manually":
        file = request.files["file"]
        if file.filename == "":
            flash("you have to select a file!")
            return "File inserito correttamente"
        if not allowed_file(file.filename):
            flash("only xlsx or xls files are accepted")
            return "File inserito non valido"

        dataset = pd.read_excel(file)

        # predizioni:
        #   zona_operazione ==  0 o 1 -> anca/ginocchio
        #   zona_operazione ==  2 -> colonna spinale
        if request.form.get("zona_operazione") == 0 or request.form.get("zona_operazione") == 1:
            # predizioni sia del physical che del mental score
            predictionsR = predictions_hipAndKneeR(dataset, "dataset")
            predictionsC = predictions_hipAndKneeC(dataset, "dataset")
            results = {
                "predictionsR": predictionsR,
                "predictionsC": predictionsC
            }
        elif request.form.get("zona_operazione") == 2:
            if request.form.get("score") == "Phisycal":
                predictionsR = predictions_SpineR(dataset, "dataset")
                predictionsC = predictions_SpineC(dataset, "dataset")

                results = {
                    "predictionsR": predictionsR,
                    "predictionsC": predictionsC,
                }

        json_results = jsonify(results)
        return json_results


    elif "dataSource" in request.form and request.form.get("dataSource") == "patientEpisode":
        form = request.form

        # knee/hip
        if request.form.get("zona_operazione") == '0' or request.form.get("zona_operazione") == '1':

            input_data = {
                "sesso": form["sesso"],
                "anni_ricovero": form["anni_ricovero"],
                "classe_asa": form["classe_asa"],
                "VAS_Total_PreOp": form["VAS_Total_PreOp"],
                "SF12_PhysicalScore_PreOp": form["physicalScore"],
                "SF12_MentalScore_PreOp": form["mentalScore"],
                "BMI_altezza_PreOp": form["bmi_altezza_preOp"],
                "BMI_peso_PreOp": form["bmi_peso_preOp"],
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
            input_data['sesso'] = input_data['sesso'].apply(check_gender)
            predictionsR = predictions_hipAndKneeR(input_data, "single_patient")
            predictionsC = predictions_hipAndKneeC(input_data, "single_patient")

            results = {
                "predictionsR": predictionsR,
                "predictionsC": predictionsC
            }
            json_results = jsonify(results)

            return json_results

    #Spine
        elif request.form.get("zona_operazione") == '2':

            form = request.form

            input_data = {
                "nome_operazione": form["nome_operazione"],
                "sesso": form["sesso"],
                "anni ricovero": form["anni_ricovero"],
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
                "nome_operazione": form["nome_operazione"],
                "sesso": form["sesso"],
                "anni ricovero": form["anni_ricovero"],
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
            input_data = preprocessSpine(input_data)
            input_data['sesso'] = input_data['sesso'].apply(check_gender)

            input_dataC = pd.DataFrame.from_dict(input_dataC, orient="index").T
            input_dataC = preprocessSpine(input_data)
            input_dataC['sesso'] = input_dataC['sesso'].apply(check_gender)

            predictionsR = predictions_SpineR(input_data, "single_patient")
            predictionsC = predictions_SpineC(input_dataC, "single_patient")

            results = {
                "predictionsR": predictionsR,
                "predictionsC": predictionsC
            }
            json_results = jsonify(results)

            return json_results


    else:
        abort(400)




if __name__ == "__main__":
    app.run(debug=True)




