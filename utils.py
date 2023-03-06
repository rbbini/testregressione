"""
Questo file contiene tutte le funzioni necessarie per fare predizioni
sui dati inseriti nel form.
"""
import pandas as pd
import numpy as np
import statistics
import pickle
import os
import joblib
from pyearth import Earth
from operator import itemgetter


dbPathR = os.path.abspath("data/db_anca.xls")
db = pd.read_excel(dbPathR)

dbPathC = os.path.abspath("data/classif_data.xlsx")
dbC = pd.read_excel(dbPathC)

ageDB = db["Anni ricovero"].to_numpy()
ageDB = ageDB.astype(int)
ageDB = ageDB.tolist()

DB_preOp_m = db["SF12 MentalScore PreOp"].tolist()
DB_preOp_p = db["SF12 PhysicalScore PreOp"].tolist()
DB_6months_m = db["SF12 MentalScore 6months"].tolist()
DB_6months_p = db["SF12 PhysicalScore 6months"].tolist()

DB_preOp_c = dbC["preOp"].tolist()
DB_6months_c = dbC["6months"].tolist()

medianP = statistics.median(DB_6months_p)
medianM = statistics.median(DB_6months_m)


# funzione per creare i dummies del campo nome_operazione
def check_nomeoperazione(data_preop: pd.DataFrame) -> pd.DataFrame:
    if 'Artrodesi cervicale' not in data_preop.columns:
        data_preop['Artrodesi cervicale'] = 0
    if 'Artrodesi lombare' not in data_preop.columns:
        data_preop['Artrodesi lombare'] = 0
    if 'Cifoplastiche' not in data_preop.columns:
        data_preop['Cifoplastiche'] = 0
    if 'Decompressione lombare' not in data_preop.columns:
        data_preop['Decompressione lombare'] = 0
    if 'Deformita degenerativa' not in data_preop.columns:
        data_preop['Deformita degenerativa'] = 0
    if 'Deformita idiopatica' not in data_preop.columns:
        data_preop['Deformita idiopatica'] = 0
    if 'Ernia cervicale' not in data_preop.columns:
        data_preop['Ernia cervicale'] = 0
    if 'Ernia lombare' not in data_preop.columns:
        data_preop['Ernia lombare'] = 0
    if 'Tumore vertebrale' not in data_preop.columns:
        data_preop['Tumore vertebrale'] = 0
    return data_preop


# sesso = m -> 0
# sesso = f -> 1
def check_gender(x: str) -> int:
    if x.lower() == "m":
        gender = 0
    elif x.lower() == "f":
        gender = 1
    else:
        gender = np.nan
    return gender


# funzione per trovare i 5 pazienti piu' simili a quello in input
# e' una funzione provvisoria che restituisce valori fantoccio, ne va
# implementata una "vera"
def most_similar_scores(all_scores: list, ages: list, input_score: list, input_age: int) -> list:
    to_sort = []
    sorted_scores = []

    for i in range(len(all_scores)):
        to_sort.append(
            (
                all_scores[i],
                abs(input_score[0] - all_scores[i]),
                ages[i],
                abs(input_age - ages[i]),
            )
        )

    to_sort.sort(key=itemgetter(1, 3))

    for x in range(0, 5):
        sorted_scores.append((to_sort[x][0], to_sort[x][2]))

    return sorted_scores


# preprocessing nel caso della spina dorsale.
# richiama check_nomeoperazione per creare i dummies per il campo
#  nome_operazione
def preprocessSpine(data_preop: pd.DataFrame) -> pd.DataFrame:
    data_preprocessed = pd.concat(
        [data_preop.drop(['nome_operazione'], axis=1), pd.get_dummies(data_preop['nome_operazione'])],
        axis=1)

    data_preprocessed = check_nomeoperazione(data_preprocessed)

    return data_preprocessed


def pred_counterfact(data_to_pred, counterfact_values, counterfact_fields, model_nameR, model_nameC):
    """
    genera le predizioni per il controfattuale

    Parametri
    ---------
    data_to_pred : dataFrame
        dataFrame contenente i dati del paziente di cui fare le predizioni
    counterfact_values : list
        contiene tutti i valori alternativi dei campi del paziente su cui
        fare le nuove predizioni (e' una lista di liste)
    counterfact_fields : list
        contiene il nome dei campi con i valori modificati
    model_nameR : str
        nome del modello per le predizioni del task regressivo
    model_nameC : str
        nome del modello per le predizioni del task classificatorio

    Returns
    -------
    list
        lista contenente una serie di dict.
        Ogni dict contiene i valori dei campi del controfattuale e le 
        predizioni (di task sia regressivo che mentale) fatte usando i 
        valori dei campi del controfattuale.
    """
    with open(model_nameR, "rb") as file:
        loaded_modelR = joblib.load(file)
    with open(model_nameC, "rb") as file:
        loaded_modelC = joblib.load(file)

    pred = []

    field1 = counterfact_fields[0]
    field2 = counterfact_fields[1]
    field3 = counterfact_fields[2]
    field4 = counterfact_fields[3]
    field5 = counterfact_fields[4]

    # cerco un oggetto contenente la predizione per ogni combinazione
    # di valori presenti nei campi del controfattuale. 
    # Questo oggetto viene appeso alla lista da ritornare
    for i in counterfact_values[0]:
        for i2 in counterfact_values[1]:
            for i3 in counterfact_values[2]:
                for i4 in counterfact_values[3]:
                    # commentato perche' con 5 campi i tempi erano
                    # troppo elevati
                    # for i5 in counterfact_values[4]:
                    data_to_pred[field1] = i
                    data_to_pred[field2] = i2
                    data_to_pred[field3] = i3
                    data_to_pred[field4] = i4
                    # commentato perche' con 5 campi i tempi erano
                    # troppo elevati
                    # data_to_pred[field5] = i5

                    if 'MORBIDITY' in data_to_pred:
                        predictionR = loaded_modelR.predict(data_to_pred.loc[:, data_to_pred.columns != "MORBIDITY"]).tolist()
                    else:
                        predictionR = loaded_modelR.predict(data_to_pred).tolist()

                    predictionC = loaded_modelC.predict_proba(data_to_pred)[:, 1].tolist()

                    estimation = {
                        field1: i,
                        field2: i2,
                        field3: i3,
                        field4: i4,
                        # commentato perche' con 5 campi i tempi erano
                        # troppo elevati
                        # field5: i5,
                        "predictionR": predictionR,
                        "predictionC": predictionC
                    }
                    pred.append(estimation)

    return pred




# regressivo anca + ginocchio
def predictions_hipAndKneeR(data_to_pred, mode):
    """
    calcolo di: 
        - predizioni (sia mentali che fisiche) del task regressivo sui
          dati del paziente in input
        - dati controfattuali
        - i 5 pazienti piu' simili a quello in input
    in aggiunta si ritornano anche gli score classificatori dei pazienti
    presenti nel dataset "classif_data.xlsx"

    Parametri
    ---------
    data_to_pred : dataFrame
        dati del paziente su cui fare le predizioni (gia' preprocessati)
    mode : str
        puo' essere "dataset" o "single_patient":
            dataset = inserimento in input di un dataset (per ora questa
                parte non funziona, va implementata)
            single_patient = i valori in input sono di un singolo 
                paziente. In questo caso calcolo anche i pazienti 
                simili, la parte controfattuale e score classificatori
                dei pazienti nel dataset

    Returns
    -------
    dict
        contiene i valori del controfattuale, le predizioni fatte sul
        paziente in input, gli score classificatori degli altri 
        pazienti, i 5 pazienti piu' simili.
        Questo dict dovrà essere convertito in json e poi mandato al
        front-end (in main.py)
    """
    with open("model_regression_physical.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhyList = loaded_model.predict(data_to_pred).tolist()
    predictionsPhy = predictionsPhyList[0]
    with open("model_regression_mental.pkl", "rb") as file:
        loaded_model2 = joblib.load(file)
    predictionsMenList = loaded_model2.predict(data_to_pred).tolist()
    predictionsMen = predictionsMenList[0]

    # eta' del paziente
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age[0]
    age = int(age)

    # ---------------- OGGETTO CON LA PREDIZIONE ----------------
    estimation = {
        "SF12_PhysicalScore_6months": predictionsPhy,  # previsione score fisico 
        "SF12_MentalScore_6months": predictionsMen,  # previsione score mentale
        "age": age
    }

    # ------------------- CONTROFATTUALE -----------------------
    # campi controfattuale fisico e mentale
    counterfactPhy = ["anni_ricovero", "SF12_PhysicalScore_PreOp", "SF12_MentalScore_PreOp",
                      "BMI_altezza_PreOp", "BMI_peso_PreOp"]
    counterfactMen = ["SF12_PhysicalScore_PreOp", "SF12_MentalScore_PreOp", "BMI_altezza_PreOp",
                      "BMI_peso_PreOp", "SF12_ultimomesetriste_risp_0"]

    # calcolo dei valori del controfattuale  
    anni_ricovero = float(data_to_pred["anni_ricovero"])
    anni_ricovero_counterfact = [anni_ricovero + 4.29, anni_ricovero + 3.22, anni_ricovero + 2.14,
                                 anni_ricovero + 1.07, anni_ricovero, anni_ricovero - 1.07, anni_ricovero - 2.14,
                                 anni_ricovero - 3.22, anni_ricovero - 4.29]

    SF12_PhysicalScore_PreOp = float(data_to_pred["SF12_PhysicalScore_PreOp"])
    SF12_PhysicalScore_PreOp_counterfact = [SF12_PhysicalScore_PreOp + 3.15,
                                            SF12_PhysicalScore_PreOp + 2.36, SF12_PhysicalScore_PreOp + 1.58,
                                            SF12_PhysicalScore_PreOp + 0.788, SF12_PhysicalScore_PreOp,
                                            SF12_PhysicalScore_PreOp - 0.788, SF12_PhysicalScore_PreOp - 1.58,
                                            SF12_PhysicalScore_PreOp - 2.36, SF12_PhysicalScore_PreOp - 3.15]

    SF12_MentalScore_PreOp = float(data_to_pred["SF12_MentalScore_PreOp"])
    SF12_MentalScore_PreOp_counterfact = [SF12_MentalScore_PreOp + 4.89,
                                          SF12_MentalScore_PreOp + 3.66, SF12_MentalScore_PreOp + 2.44,
                                          SF12_MentalScore_PreOp + 1.22, SF12_MentalScore_PreOp,
                                          SF12_MentalScore_PreOp - 1.22, SF12_MentalScore_PreOp - 2.44,
                                          SF12_MentalScore_PreOp - 3.66, SF12_MentalScore_PreOp - 4.89]

    BMI_altezza_PreOp = float(data_to_pred["BMI_altezza_PreOp"])
    BMI_altezza_PreOp_counterfact = [BMI_altezza_PreOp + 3.75, BMI_altezza_PreOp + 2.81,
                                     BMI_altezza_PreOp + 1.87, BMI_altezza_PreOp + 0.94, BMI_altezza_PreOp,
                                     BMI_altezza_PreOp - 0.94, BMI_altezza_PreOp - 1.87, BMI_altezza_PreOp - 2.81,
                                     BMI_altezza_PreOp - 3.75]

    BMI_peso_PreOp = float(data_to_pred["BMI_peso_PreOp"])
    BMI_peso_PreOp_counterfact = [BMI_peso_PreOp + 6.24, BMI_peso_PreOp + 4.68,
                                  BMI_peso_PreOp + 3.12, BMI_peso_PreOp + 1.56, BMI_peso_PreOp,
                                  BMI_peso_PreOp - 1.56, BMI_peso_PreOp - 3.12, BMI_peso_PreOp - 4.68,
                                  BMI_peso_PreOp - 6.24]

    SF12_ultimomesetriste_risp_0 = float(data_to_pred["SF12_ultimomesetriste_risp_0"])
    SF12_ultimomesetriste_risp_0_counterfact = [SF12_ultimomesetriste_risp_0 + 0.53,
                                                SF12_ultimomesetriste_risp_0 + 0.4, SF12_ultimomesetriste_risp_0 + 0.27,
                                                SF12_ultimomesetriste_risp_0 + 0.13, SF12_ultimomesetriste_risp_0,
                                                SF12_ultimomesetriste_risp_0 - 0.13,
                                                SF12_ultimomesetriste_risp_0 - 0.27,
                                                SF12_ultimomesetriste_risp_0 - 0.4, SF12_ultimomesetriste_risp_0 - 0.53]

    # lista contenente tutti i valori dei campi del controfattuale
    counterfact_values = [anni_ricovero_counterfact, SF12_PhysicalScore_PreOp_counterfact,
                          SF12_MentalScore_PreOp_counterfact,
                          BMI_altezza_PreOp_counterfact, BMI_peso_PreOp_counterfact]

    # ---------------- PREDIZIONI CONTROFATTUALE ----------------
    # valori fisici del controfattuale
    estimation_counterfact_phy = pred_counterfact(data_to_pred, counterfact_values, counterfactPhy,
                                                  "model_regression_physical.pkl", "model_classification_physical.pkl")

    # valori mentali del controfattuale
    counterfact_values = [SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact,
                          BMI_altezza_PreOp_counterfact,
                          BMI_peso_PreOp_counterfact, SF12_ultimomesetriste_risp_0_counterfact]

    estimation_counterfact_men = pred_counterfact(data_to_pred, counterfact_values, counterfactMen,
                                                  "model_regression_mental.pkl", "model_classification_mental.pkl")

    # ---------------- LISTA CON TUTTE LE PREDIZIONI ----------------
    predictions = [estimation, estimation_counterfact_phy, estimation_counterfact_men]

    # ---------------- OGGETTO PER LA CREAZIONE DELLA PARTE CONTROFATTUALE IN HTML ----------------
    anni_ricovero_counterfact.insert(0, "anni_ricovero")
    SF12_PhysicalScore_PreOp_counterfact.insert(0, "SF12_PhysicalScore_PreOp")
    SF12_MentalScore_PreOp_counterfact.insert(0, "SF12_MentalScore_PreOp")
    BMI_altezza_PreOp_counterfact.insert(0, "BMI_altezza_PreOp")
    BMI_peso_PreOp_counterfact.insert(0, "BMI_peso_PreOp")
    SF12_ultimomesetriste_risp_0_counterfact.insert(0, "SF12_ultimomesetriste_risp_0")

    counterfact = {
        "physical": [anni_ricovero_counterfact, SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact, BMI_altezza_PreOp_counterfact],

        "mental": [SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact, BMI_altezza_PreOp_counterfact, BMI_peso_PreOp_counterfact]
    }

    # -------------------- ALTRI PAZIENTI --------------------
    # lista che conterra' gli score di tutti i pazienti del dataset
    others = []

    # prendo il valore in pos i nella lista dei valori preOp e lo metto 
    # in un dict che poi appendo a others. 
    # Rifaccio la stessa cosa con i valori nella lista del post operatorio
    for i in range(len(DB_preOp_c)):
        dict = {
            "period": "preOp",
            "score": DB_preOp_c[i],
        }
        others.append(dict)
        dict = {
            "period": "6months",
            "score": DB_6months_c[i]
        }
        others.append(dict)

    # -------------------- PAZIENTI SIMILI --------------------
    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(
            DB_6months_p, ageDB, predictionsPhyList, age
        )
        for x in range(len(similar_p)):
            similar_p_dict = {
                "SF12_PhysicalScore_6months": similar_p[x][0],
                "age": similar_p[x][1],
            }
            similar_scores.append(similar_p_dict)

        similar_m = most_similar_scores(
            DB_6months_m, ageDB, predictionsMenList, age
        )
        for x in range(len(similar_m)):
            similar_m_dict = {
                "SF12_MentalScore_6months": similar_m[x][0],
                "age": similar_m[x][1],
            }
            similar_scores.append(similar_m_dict)

    # -------------------- OGGETTO FINALE DA RITORNARE --------------------
    to_json = {
        "counterfactual": counterfact,
        "predictions": predictions,
        "other_patients": others,
        "similar_patients": similar_scores
    }

    return to_json


# classificatorio anca + ginocchio
def predictions_hipAndKneeC(data_to_pred, mode):
    """
    calcolo delle predizioni (mentali e fisiche) per il task 
    classificatorio sul paziente in input

    Parametri
    ---------
    data_to_pred : dataFrame
        dati su cui faccio le predizioni (gia' preprocessati)
    mode: str
        puo' essere "dataset" o "single_patient":
            dataset = inserimento in input di un dataset (per ora questa
                parte non funziona, va implementata)
            single_patient = calcolo delle predizioni per il paziente

    Returns
    -------
    dict
        contiente i valori delle predizioni del task classificatorio.
        Questo dict dovrà essere convertito in json e poi mandato al
        front-end (in main.py)
    """
    with open("model_classification_physical.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict_proba(data_to_pred)[:, 1].tolist()
    with open("model_classification_mental.pkl", "rb") as file:
        loaded_model2 = joblib.load(file)
    predictionsMen = loaded_model2.predict_proba(data_to_pred)[:, 1].tolist()

    estimation = {
        "physical_classif_score": predictionsPhy,  # previsione score fisico dopo 6 mesi
        "mental_classif_score": predictionsMen  # previsione score mentale dopo 6 mesi
    }

    return estimation


# regressivo spine
def predictions_SpineR(data_to_pred, mode):
    """
    calcolo di: 
        - predizioni (sia ODI che fisiche) del task regressivo sui
          dati del paziente in input
        - dati controfattuali
        - i 5 pazienti piu' simili a quello in input
    in aggiunta si ritornano anche gli score classificatori dei pazienti
    presenti nel dataset "classif_data.xlsx"

    Parametri
    ---------
    data_to_pred : dataFrame
        dati del paziente su cui fare le predizioni (gia' preprocessati)
    mode : str
        puo' essere "dataset" o "single_patient":
            dataset = inserimento in input di un dataset (per ora questa
                parte non funziona, va implementata)
            single_patient = i valori in input sono di un singolo 
                paziente. In questo caso calcolo anche i pazienti 
                simili, la parte controfattuale e score classificatori
                dei pazienti nel dataset

    Returns
    -------
    dict
        contiene i valori del controfattuale, le predizioni fatte sul
        paziente in input, gli score classificatori degli altri 
        pazienti, i 5 pazienti piu' simili.
        Questo dict dovrà essere convertito in json e poi mandato al
        front-end (in main.py)
    """
    with open("model_regression_physical_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhyList = loaded_model.predict(data_to_pred.loc[:, data_to_pred.columns != "MORBIDITY"]).tolist()
    predictionsPhy = predictionsPhyList[0]
    with open("model_regression_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsODIList = loaded_model.predict(data_to_pred.loc[:, data_to_pred.columns != "MORBIDITY"]).tolist()
    predictionsODI = predictionsODIList[0]

    # eta' del paziente 
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age[0]
    age = int(age)

    # ---------------- OGGETTO CON LA PREDIZIONE ----------------
    estimation = {
        "SF12_PhysicalScore_6months": predictionsPhy,  # previsione score fisico
        "SF12_MentalScore_6months": predictionsODI,  # previsione score ODI (si chiama "MentalScore" per riciclare una funzione in results.js)
        "age": age
    }

    # ------------------- CONTROFATTUALE -----------------------
    # campi controfattuale fisico e ODI
    counterfactPhy = ["SF36_PhysicalFunctioning_PreOp", "SF36_GeneralHealth_PreOp", "anni_ricovero",
                      "ODI_Total_PreOp", "classe_asa_1"]
    counterfactODI = ["ODI_Total_PreOp", "SF36_GeneralHealth_PreOp", "Vas_Back_PreOp",
                      "anni_ricovero", "sesso"]

    # calcolo dei valori del controfattuale  
    SF36_PhysicalFunctioning_PreOp = float(data_to_pred["SF36_PhysicalFunctioning_PreOp"])
    SF36_PhysicalFunctioning_PreOp_counterfact = [SF36_PhysicalFunctioning_PreOp + 10.84,
                                                  SF36_PhysicalFunctioning_PreOp + 8.13,
                                                  SF36_PhysicalFunctioning_PreOp + 5.42,
                                                  SF36_PhysicalFunctioning_PreOp + 2.71, SF36_PhysicalFunctioning_PreOp,
                                                  SF36_PhysicalFunctioning_PreOp - 2.71,
                                                  SF36_PhysicalFunctioning_PreOp - 5.42,
                                                  SF36_PhysicalFunctioning_PreOp - 8.13,
                                                  SF36_PhysicalFunctioning_PreOp - 10.84]

    SF36_GeneralHealth_PreOp = float(data_to_pred["SF36_GeneralHealth_PreOp"])
    SF36_GeneralHealth_PreOp_counterfact = [SF36_GeneralHealth_PreOp + 8.33,
                                            SF36_GeneralHealth_PreOp + 6.24, SF36_GeneralHealth_PreOp + 4.16,
                                            SF36_GeneralHealth_PreOp + 2.08, SF36_GeneralHealth_PreOp,
                                            SF36_GeneralHealth_PreOp - 2.08, SF36_GeneralHealth_PreOp - 4.16,
                                            SF36_GeneralHealth_PreOp - 6.24, SF36_GeneralHealth_PreOp - 8.33]

    anni_ricovero = float(data_to_pred["anni_ricovero"])
    anni_ricovero_counterfact = [anni_ricovero + 7.1, anni_ricovero + 5.33, anni_ricovero + 3.55,
                                 anni_ricovero + 1.78, anni_ricovero, anni_ricovero - 1.78, anni_ricovero - 3.55,
                                 anni_ricovero - 5.33, anni_ricovero - 7.1]

    ODI_Total_PreOp = float(data_to_pred["ODI_Total_PreOp"])
    ODI_Total_PreOp_counterfact = [ODI_Total_PreOp + 8, ODI_Total_PreOp + 6, ODI_Total_PreOp + 4,
                                   ODI_Total_PreOp + 2, ODI_Total_PreOp, ODI_Total_PreOp - 2, ODI_Total_PreOp - 4,
                                   ODI_Total_PreOp - 6, ODI_Total_PreOp - 8]

    classe_asa_1_counterfact = [1, 2, 3, 4]

    Vas_Back_PreOp = float(data_to_pred["Vas_Back_PreOp"])
    Vas_Back_PreOp_counterfact = [Vas_Back_PreOp + 1.21, Vas_Back_PreOp + 0.91,
                                  Vas_Back_PreOp + 0.61,
                                  Vas_Back_PreOp + 0.3, Vas_Back_PreOp, Vas_Back_PreOp - 0.3, Vas_Back_PreOp - 0.61,
                                  Vas_Back_PreOp - 0.91, Vas_Back_PreOp - 1.21]

    sesso_counterfact = [0, 1]

    counterfact_values = [SF36_PhysicalFunctioning_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact,
                          anni_ricovero_counterfact,
                          ODI_Total_PreOp_counterfact, classe_asa_1_counterfact]

    # ---------------- PREDIZIONI CONTROFATTUALE ----------------
    # valori fisici del controfattuale
    estimation_counterfact_phy = pred_counterfact(data_to_pred, counterfact_values, counterfactPhy,
                                                  "model_regression_physical_spine.pkl", "model_classification_physical_spine.pkl")

    # valori ODI del controfattuale
    counterfact_values = [ODI_Total_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact, Vas_Back_PreOp_counterfact,
                          anni_ricovero_counterfact, sesso_counterfact]

    estimation_counterfact_ODI = pred_counterfact(data_to_pred, counterfact_values, counterfactODI,
                                                  "model_regression_odi_spine.pkl", "model_classification_odi_spine.pkl")

    # ---------------- LISTA CON TUTTE LE PREDIZIONI ----------------
    predictions = [estimation, estimation_counterfact_phy, estimation_counterfact_ODI]

    # ---------------- OGGETTO PER LA CREAZIONE DELLA PARTE CONTROFATTUALE IN HTML ----------------
    SF36_PhysicalFunctioning_PreOp_counterfact.insert(0, "SF36_PhysicalFunctioning_PreOp")
    SF36_GeneralHealth_PreOp_counterfact.insert(0, "SF36_GeneralHealth_PreOp")
    anni_ricovero_counterfact.insert(0, "anni_ricovero")
    ODI_Total_PreOp_counterfact.insert(0, "ODI_Total_PreOp")
    classe_asa_1_counterfact.insert(0, "classe_asa_1")
    Vas_Back_PreOp_counterfact.insert(0, "Vas_Back_PreOp")
    sesso_counterfact.insert(0, "sesso")

    counterfact = {
        "physical": [SF36_PhysicalFunctioning_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact, anni_ricovero_counterfact, ODI_Total_PreOp_counterfact],

        "ODI": [ODI_Total_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact, Vas_Back_PreOp_counterfact, anni_ricovero_counterfact]
    }

    # -------------------- ALTRI PAZIENTI --------------------
    # lista che conterra' gli score di tutti i pazienti del dataset
    others = []

    # prendo il valore in pos i nella lista dei valori preOp e lo metto
    # in un dict che poi appendo a others.
    # Rifaccio la stessa cosa con i valori nella lista del post operatorio
    for i in range(len(DB_preOp_c)):
        dict = {
            "period": "preOp",
            "score": DB_preOp_c[i],
        }
        others.append(dict)
        dict = {
            "period": "6months",
            "score": DB_6months_c[i]
        }
        others.append(dict)

    # -------------------- PAZIENTI SIMILI --------------------
    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(
            DB_6months_p, ageDB, predictionsPhyList, age
        )
        for x in range(len(similar_p)):
            similar_p_dict = {
                "SF12_PhysicalScore_6months": similar_p[x][0], # si chiama SF12_PhysicalScore_6months per riciclare codice in results.js
                "age": similar_p[x][1],
            }
            similar_scores.append(similar_p_dict)

        similar_m = most_similar_scores(
            DB_6months_m, ageDB, predictionsODIList, age
        )
        for x in range(len(similar_m)):
            similar_m_dict = {
                "SF12_MentalScore_6months": similar_m[x][0], # SF12_MentalScore_6months per riciclare codice (sarebbe ODI score)
                "age": similar_m[x][1],
            }
            similar_scores.append(similar_m_dict)

    # -------------------- OGGETTO FINALE DA RITORNARE --------------------
    to_json = {
        "counterfactual": counterfact,
        "predictions": predictions,
        "other_patients": others,
        "similar_patients": similar_scores
    }

    return to_json


# classificatorio spine
def predictions_SpineC(data_to_pred, mode):
    """
    calcolo delle predizioni (ODI e fisiche) per il task 
    classificatorio sul paziente in input

    Parametri
    ---------
    data_to_pred : dataFrame
        dati su cui faccio le predizioni (gia' preprocessati)
    mode: str
        puo' essere "dataset" o "single_patient":
            dataset = inserimento in input di un dataset (per ora questa
                parte non funziona, va implementata)
            single_patient = calcolo delle predizioni per il paziente

    Returns
    -------
    dict
        contiente i valori delle predizioni del task classificatorio.
        Questo dict dovrà essere convertito in json e poi mandato al
        front-end (in main.py)
    """
    with open("model_classification_physical_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict_proba(data_to_pred)[:, 1].tolist()
    with open("model_classification_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsODI = loaded_model.predict_proba(data_to_pred)[:, 1].tolist()

    estimation = {
        "physical_classif_score": predictionsPhy,  # previsione score classificatorio fisico
        "mental_classif_score": predictionsODI  # previsione score classificatorio ODI (e' "mental" per poter riciclare una funzione in results.js)
    }

    return estimation






# -------------------- PER TESTING --------------------------------------------
"""
data_prepr = preprocessing(data)
e = predictions_hip_6months(data_prepr)
print(e)
"""

"""
input_data = {
     "sesso": "1",
     "anni_ricovero": "63",
     "classe_asa": "3",
     "VAS_Total_PreOp": "6",
     "SF12_PhysicalScore_PreOp": "33",
     "SF12_MentalScore_PreOp": "45",
     "BMI_altezza_PreOp": "180",
     "BMI_peso_PreOp": "84",
     "SF12_autovalsalute_risp_0": "33",
     "SF12_scale_risp_0": "35",
     "SF12_ultimomeseresa_risp_0": "37",
     "SF12_ultimomeselimite_risp_0": "43",
     "SF12_ultimomeseemo_risp_0": "34",
     "SF12_ultimomeseostacolo_risp_0": "33",
     "SF12_ultimomesesereno_risp_0": "23",
     "SF12_ultimomeseenergia_risp_0": "23",
     "SF12_ultimomesetriste_risp_0": "63",
     "SF12_ultimomesesociale_risp_0": "13",
     "zona_operazione": "0"
}

input_data = pd.DataFrame.from_dict(input_data, orient="index").T
estimation = predictions_hipAndKneeR(input_data, "single_patient")
estimation2 = predictions_hipAndKneeC(input_data, "single_patient")
print(estimation)
"""

"""
input_data = {
    "nome_operazione": "Cifoplastiche",
    "sesso": "M",
    "anni_ricovero": "77",
    "ODI_Total_PreOp": "34",
    "Vas_Back_PreOp": "34",
    "Vas_Leg_PreOp":"34",
    "SF36_GeneralHealth_PreOp": "34",
    "SF36_PhysicalFunctioning_PreOp": "34",
    "SF36_RoleLimitPhysical_PreOp": "34",
    "SF36_RoleLimitEmotional_PreOp": "34",
    "SF36_SocialFunctioning_PreOp": "34",
    "SF36_Pain_PreOp": "34",
    "SF36_EnergyFatigue_PreOp": "34",
    "SF36_EmotionalWellBeing_PreOp": "34",
    "SF36_MentalScore_PreOp": "34",
    "SF36_PhysicalScore_PreOp": "34",
    "FABQ_Work_PreOp": "34",
    "classe_asa_1": "1",
    "MORBIDITY": "1"
}

input_data = pd.DataFrame.from_dict(input_data, orient="index").T
input_data = preprocessSpine(input_data)
input_data['sesso'] = input_data['sesso'].apply(check_gender)
estimation = predictions_SpineR(input_data, "single_patient")   
predictionsC = predictions_SpineC(input_data, "single_patient")

print("R: ", estimation)
print("C: ",predictionsC)
"""
