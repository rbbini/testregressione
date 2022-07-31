import pandas as pd
import numpy as np
import statistics
import os
import joblib
from pyearth import Earth
from operator import itemgetter

#dataz = pd.read_excel(r'E:\Stage\nuovo env\projectLourdes\testinonino.xls')


# dati che saranno ritornati in un json
dbPath = os.path.abspath("data/db_anca.xls")
db = pd.read_excel(dbPath)

ageDB = db["Anni ricovero"].to_numpy()
ageDB = ageDB.astype(int)
ageDB = ageDB.tolist()

DB_6months_p = db["SF12 MentalScore 6months"].tolist()
DB_6months_m = db["SF12 PhysicalScore 6months"].tolist()

medianP = statistics.median(DB_6months_p)
medianM = statistics.median(DB_6months_m)



def check_nomeoperazione(data_preop):
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


# per applicare il check del gender usare la seguente riga
# data_preop["Sesso"] = data_preop["Sesso"].apply(check_gender)
def check_gender(x):
    if x.lower() == "m":
        gender = 0
    elif x.lower() == "f":
        gender = 1
    else:
        gender = np.nan
    return gender


def most_similar_scores(all_scores, ages, input_score, input_age):
    to_sort = []
    sorted_scores = []

    for i in range(len(all_scores)):
        to_sort.append(
            (
                all_scores[i],
                abs(input_score[0] - all_scores[i]),
                ages[i],
                abs(input_age[0] - ages[i]),
            )
        )

    to_sort.sort(key=itemgetter(1, 3))

    for x in range(0, 5):
        sorted_scores.append((to_sort[x][0], to_sort[x][2]))

    return sorted_scores



def preprocessSpine(data_preop):
    data_preprocessed = pd.concat([data_preop.drop(['nome_operazione'], axis=1), pd.get_dummies(data_preop['nome_operazione'])],
                           axis=1)

    data_preprocessed = check_nomeoperazione(data_preprocessed)
    
    return data_preprocessed


# funzione per la predizione dei valori del controfattuale
def pred_counterfact(data_to_pred, counterfact_values, counterfact_fields, model_name):
    with open(model_name, "rb") as file:
        loaded_model = joblib.load(file)
    
    pred = []
    
    field1 = counterfact_fields[0]
    field2 = counterfact_fields[1]
    field3 = counterfact_fields[2]
    field4 = counterfact_fields[3]
    field5 = counterfact_fields[4]
    
    # vado a creare un oggetto contenente la predizione per ogni combinazione di valori presenti 
    # nei campi del controfattuale. Questo oggetto viene appeso all'array che verra' poi ritornato
    for i in counterfact_values[0]:
        for i2 in counterfact_values[1]:
            # commentato per test
            #for i3 in counterfact_values[2]:
                #for i4 in counterfact_values[3]:
                    #for i5 in counterfact_values[4]:
            data_to_pred[field1] = i
            data_to_pred[field2] = i2
            # commentato per test
            #data_to_pred[field3] = i3
            #data_to_pred[field4] = i4
            #data_to_pred[field5] = i5

            prediction = loaded_model.predict(data_to_pred).tolist()

            estimation = {
				field1: i,
				field2: i2,
                # commentato per test
                #field3: i3,
                #field4: i4,
                #field5: i5,
				"prediction": prediction
			}
            pred.append(estimation)

    return pred



# tenere come esempio per gli "altri pazienti"
"""
def predictions_hip_6months(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_6months_phy.pkl", "rb") as file:
        loaded_model = pickle.load(file)
    predictionsP = loaded_model.predict(data_to_pred).tolist()
    with open("model_6months_men.pkl", "rb") as file:
        loaded_model2 = pickle.load(file)
    predictionsM = loaded_model2.predict(data_to_pred).tolist()

    age = data_to_pred["Anni ricovero"].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {
        "SF12_PhysicalScore_6months": predictionsP,  # previsione score fisico dopo 6 mesi
        "SF12_MentalScore_6months": predictionsM,  # previsione score mentale dopo 6 mesi
        "age": age,  # eta'
    }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene)
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i],
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM, "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(
            DB_6months_p, ageDB, predictionsP, data_to_pred["Anni ricovero"]
        )
        for x in range(len(similar_p)):
            similar_p_dict = {
                "SF12_PhysicalScore_6months": similar_p[x][0],
                "age": similar_p[x][1],
            }
            similar_scores.append(similar_p_dict)

        similar_m = most_similar_scores(
            DB_6months_m, ageDB, predictionsM, data_to_pred["Anni ricovero"]
        )
        for x in range(len(similar_m)):
            similar_m_dict = {
                "SF12_MentalScore_6months": similar_m[x][0],
                "age": similar_m[x][1],
            }
            similar_scores.append(similar_m_dict)

        to_json.append(similar_scores)

    return to_json
"""

# regressivo anca + ginocchio
def predictions_hipAndKneeR(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_regression_physical.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict(data_to_pred).tolist()
    with open("model_regression_mental.pkl", "rb") as file:
        loaded_model2 = joblib.load(file)
    predictionsMen = loaded_model2.predict(data_to_pred).tolist()
    
    # age della persona 
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # ---------------- OGGETTO CON LA PREDIZIONE ----------------
    estimation = {
        "SF12_PhysicalScore_6months": predictionsPhy,  # previsione score fisico dopo 6 mesi  
        "SF12_MentalScore_6months": predictionsMen,  # previsione score mentale dopo 6 mesi
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
    anni_ricovero_counterfact = [anni_ricovero + 5.36, anni_ricovero + 4.29, anni_ricovero + 3.22, anni_ricovero + 2.14, 
                                 anni_ricovero + 1.07, anni_ricovero, anni_ricovero - 1.07, anni_ricovero - 2.14, 
                                 anni_ricovero - 3.22, anni_ricovero - 4.29, anni_ricovero - 5.36]
    
    SF12_PhysicalScore_PreOp = float(data_to_pred["SF12_PhysicalScore_PreOp"])
    SF12_PhysicalScore_PreOp_counterfact = [SF12_PhysicalScore_PreOp + 3.94, SF12_PhysicalScore_PreOp + 3.15, 
                                            SF12_PhysicalScore_PreOp + 2.36, SF12_PhysicalScore_PreOp + 1.58, 
                                            SF12_PhysicalScore_PreOp + 0.788, SF12_PhysicalScore_PreOp, 
                                            SF12_PhysicalScore_PreOp - 0.788, SF12_PhysicalScore_PreOp - 1.58, 
                                            SF12_PhysicalScore_PreOp - 2.36, SF12_PhysicalScore_PreOp - 3.15, 
                                            SF12_PhysicalScore_PreOp - 3.94]
    
    SF12_MentalScore_PreOp = float(data_to_pred["SF12_MentalScore_PreOp"])
    SF12_MentalScore_PreOp_counterfact = [SF12_MentalScore_PreOp + 6.11, SF12_MentalScore_PreOp + 4.89,
                                          SF12_MentalScore_PreOp + 3.66, SF12_MentalScore_PreOp + 2.44,
                                          SF12_MentalScore_PreOp + 1.22, SF12_MentalScore_PreOp,
                                          SF12_MentalScore_PreOp - 1.22, SF12_MentalScore_PreOp - 2.44,
                                          SF12_MentalScore_PreOp - 3.66, SF12_MentalScore_PreOp - 4.89,
                                          SF12_MentalScore_PreOp - 6.11]

    BMI_altezza_PreOp = float(data_to_pred["BMI_altezza_PreOp"])
    BMI_altezza_PreOp_counterfact = [BMI_altezza_PreOp + 4.68, BMI_altezza_PreOp + 3.75, BMI_altezza_PreOp + 2.81,
                                     BMI_altezza_PreOp + 1.87, BMI_altezza_PreOp + 0.94, BMI_altezza_PreOp,
                                     BMI_altezza_PreOp - 0.94, BMI_altezza_PreOp - 1.87, BMI_altezza_PreOp - 2.81,
                                     BMI_altezza_PreOp - 3.75, BMI_altezza_PreOp - 4.68]

    BMI_peso_PreOp = float(data_to_pred["BMI_peso_PreOp"])
    BMI_peso_PreOp_counterfact = [BMI_peso_PreOp + 7.80, BMI_peso_PreOp + 6.24, BMI_peso_PreOp + 4.68, 
                                     BMI_peso_PreOp + 3.12, BMI_peso_PreOp + 1.56, BMI_peso_PreOp, 
                                     BMI_peso_PreOp - 1.56, BMI_peso_PreOp - 3.12, BMI_peso_PreOp - 4.68,
                                     BMI_peso_PreOp - 6.24, BMI_peso_PreOp - 7.80]

    SF12_ultimomesetriste_risp_0 = float(data_to_pred["SF12_ultimomesetriste_risp_0"])
    SF12_ultimomesetriste_risp_0_counterfact = [SF12_ultimomesetriste_risp_0 + 0.66, SF12_ultimomesetriste_risp_0 + 0.53,
                                                SF12_ultimomesetriste_risp_0 + 0.4, SF12_ultimomesetriste_risp_0 + 0.27,
                                                SF12_ultimomesetriste_risp_0 + 0.13, SF12_ultimomesetriste_risp_0,
                                                SF12_ultimomesetriste_risp_0 - 0.13, SF12_ultimomesetriste_risp_0 - 0.27,
                                                SF12_ultimomesetriste_risp_0 - 0.4, SF12_ultimomesetriste_risp_0 - 0.53,
                                                SF12_ultimomesetriste_risp_0 - 0.66]
    
    counterfact_values = [anni_ricovero_counterfact, SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact, 
                          BMI_altezza_PreOp_counterfact, BMI_peso_PreOp_counterfact]
    # ---------------- PREDIZIONI CONTROFATTUALE ----------------
    # inserimento nell'array dei valori fisici del controfattuale
    estimation_counterfact_phy = pred_counterfact(data_to_pred, counterfact_values, counterfactPhy, "model_regression_physical.pkl")
    
    # valori mentali del controfattuale
    counterfact_values = [SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact, BMI_altezza_PreOp_counterfact, 
                          BMI_altezza_PreOp_counterfact, SF12_ultimomesetriste_risp_0_counterfact]
    estimation_counterfact_men = pred_counterfact(data_to_pred, counterfact_values, counterfactMen, "model_regression_mental.pkl")
      
    
    # ---------------- ARRAY CON TUTTE LE PREDIZIONI ----------------
    predictions = [estimation, estimation_counterfact_phy, estimation_counterfact_men]


    # ---------------- OGGETTO PER LA CREAZIONE DELLA PARTE CONTROFATTUALE IN HTML ----------------
    anni_ricovero_counterfact.insert(0, "anni_ricovero")
    SF12_PhysicalScore_PreOp_counterfact.insert(0, "SF12_PhysicalScore_PreOp")
    SF12_MentalScore_PreOp_counterfact.insert(0, "SF12_MentalScore_PreOp")
    BMI_altezza_PreOp_counterfact.insert(0, "BMI_altezza_PreOp")
    BMI_peso_PreOp_counterfact.insert(0, "BMI_peso_PreOp")
    SF12_ultimomesetriste_risp_0_counterfact.insert(0, "SF12_ultimomesetriste_risp_0")

    counterfact = {
        "physical": [anni_ricovero_counterfact, SF12_PhysicalScore_PreOp_counterfact],
        
        "mental": [SF12_PhysicalScore_PreOp_counterfact, SF12_MentalScore_PreOp_counterfact]
    }

    
    # -------------------- OGGETTO FINALE DA RITORNARE --------------------
    to_json = {
        "counterfactual": counterfact, 
        "predictions": predictions
    }

    return to_json



# classificatorio anca + ginocchio
def predictions_hipAndKneeC(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_classification_physical.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict(data_to_pred).tolist()
    with open("model_classification_mental.pkl", "rb") as file:
        loaded_model2 = joblib.load(file)
    predictionsMen = loaded_model2.predict(data_to_pred.values).tolist()

    estimation = {
        "physical_classif_score": predictionsPhy,  # previsione score fisico dopo 6 mesi
        "mental_classif_score": predictionsMen  # previsione score mentale dopo 6 mesi
    }
    
    return estimation

    

# regressivo spine
def predictions_SpineR(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    # data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_regression_physical_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict(data_to_pred.values).tolist()
    with open("model_regression_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsODI = loaded_model.predict(data_to_pred.values).tolist()

    # age della persona 
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # ---------------- OGGETTO CON LA PREDIZIONE ----------------
    estimation = {
        "Physical_score": predictionsPhy,  # previsione score fisico
        "ODI_score": predictionsODI,  # previsione score ODI
        "age": age
    }


    # ------------------- CONTROFATTUALE -----------------------
    # campi controfattuale fisico e mentale
    counterfactPhy = ["SF36_PhysicalFunctioning_PreOp", "SF36_GeneralHealth_PreOp", "anni_ricovero", 
                      "ODI_Total_PreOp", "classe_asa_1"]
    counterfactODI = ["ODI_Total_PreOp", "SF36_GeneralHealth_PreOp", "Vas_Back_PreOp", 
                      "anni_ricovero", "sesso"]
    
    # calcolo dei valori del controfattuale  
    SF36_PhysicalFunctioning_PreOp = float(data_to_pred["SF36_PhysicalFunctioning_PreOp"])
    SF36_PhysicalFunctioning_PreOp_counterfact = [SF36_PhysicalFunctioning_PreOp + 13.56, SF36_PhysicalFunctioning_PreOp + 10.84, 
                                                  SF36_PhysicalFunctioning_PreOp + 8.13, SF36_PhysicalFunctioning_PreOp + 5.42, 
                                                  SF36_PhysicalFunctioning_PreOp + 2.71, SF36_PhysicalFunctioning_PreOp, 
                                                  SF36_PhysicalFunctioning_PreOp - 2.71, SF36_PhysicalFunctioning_PreOp - 5.42,
                                                  SF36_PhysicalFunctioning_PreOp - 8.13, SF36_PhysicalFunctioning_PreOp - 10.84,
                                                  SF36_PhysicalFunctioning_PreOp - 13.56]

    SF36_GeneralHealth_PreOp = float(data_to_pred["SF36_GeneralHealth_PreOp"])
    SF36_GeneralHealth_PreOp_counterfact = [SF36_GeneralHealth_PreOp + 10.41, SF36_GeneralHealth_PreOp + 8.33,
                                            SF36_GeneralHealth_PreOp + 6.24, SF36_GeneralHealth_PreOp + 4.16,
                                            SF36_GeneralHealth_PreOp + 2.08, SF36_GeneralHealth_PreOp,
                                            SF36_GeneralHealth_PreOp - 2.08, SF36_GeneralHealth_PreOp - 4.16,
                                            SF36_GeneralHealth_PreOp - 6.24, SF36_GeneralHealth_PreOp - 8.33,
                                            SF36_GeneralHealth_PreOp - 10.41]

    anni_ricovero = float(data_to_pred["anni_ricovero"])
    anni_ricovero_counterfact = [anni_ricovero + 8.89, anni_ricovero + 7.1, anni_ricovero + 5.33, anni_ricovero + 3.55, 
                                 anni_ricovero + 1.78, anni_ricovero, anni_ricovero - 1.78, anni_ricovero - 3.55, 
                                 anni_ricovero - 5.33, anni_ricovero - 7.1, anni_ricovero - 8.89]

    ODI_Total_PreOp = float(data_to_pred["ODI_Total_PreOp"])
    ODI_Total_PreOp_counterfact = [ODI_Total_PreOp + 10, ODI_Total_PreOp + 8, ODI_Total_PreOp + 6, ODI_Total_PreOp + 4,
                                   ODI_Total_PreOp + 2, ODI_Total_PreOp, ODI_Total_PreOp - 2, ODI_Total_PreOp - 4,
                                   ODI_Total_PreOp - 6, ODI_Total_PreOp - 8, ODI_Total_PreOp - 10]

    classe_asa_1_counterfact = [1, 2, 3, 4]

    Vas_Back_PreOp = float(data_to_pred["Vas_Back_PreOp"])
    Vas_Back_PreOp_counterfact = [Vas_Back_PreOp + 1.52, Vas_Back_PreOp + 1.21, Vas_Back_PreOp + 0.91, Vas_Back_PreOp + 0.61,
                                  Vas_Back_PreOp + 0.3, Vas_Back_PreOp, Vas_Back_PreOp - 0.3, Vas_Back_PreOp - 0.61,
                                  Vas_Back_PreOp - 0.91, Vas_Back_PreOp - 1.21, Vas_Back_PreOp - 1.52]
    
    sesso_counterfact = [0, 1]

    counterfact_values = [SF36_PhysicalFunctioning_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact, anni_ricovero_counterfact,
                          ODI_Total_PreOp_counterfact, classe_asa_1_counterfact]
    # ---------------- PREDIZIONI CONTROFATTUALE ----------------
    # inserimento nell'array dei valori fisici del controfattuale
    estimation_counterfact_phy = pred_counterfact(data_to_pred, counterfact_values, counterfactPhy, "model_regression_physical_spine.pkl")

    counterfact_values = [ODI_Total_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact, Vas_Back_PreOp_counterfact, 
                          anni_ricovero_counterfact, sesso_counterfact]
    estimation_counterfact_ODI = pred_counterfact(data_to_pred, counterfact_values, counterfactODI, "model_regression_odi_spine.pkl")


    # ---------------- ARRAY CON TUTTE LE PREDIZIONI ----------------
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
        "physical": [SF36_PhysicalFunctioning_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact],
        
        "ODI": [ODI_Total_PreOp_counterfact, SF36_GeneralHealth_PreOp_counterfact]
    }


    # -------------------- OGGETTO FINALE DA RITORNARE --------------------
    to_json = {
        "counterfactual": counterfact, 
        "predictions": predictions
    }

    return to_json



"""
def predictions_SpineOdi(data_to_pred):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_regression_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPineOdiR = loaded_model.predict(data_to_pred.values).tolist()
    
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age.astype(int)
    age = age.tolist()
    
    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)
    
    estimation = {
        "ODI_score": predictionsPineOdiR,  # previsione score ODI
        "age": age,  # eta'
    }
    
    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []
    
    ###da controllare con rob!?!
    return to_json
"""
    

# classificatorio spine
def predictions_SpineC(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_classification_physical_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPhy = loaded_model.predict(data_to_pred).tolist()
    with open("model_classification_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsODI = loaded_model.predict(data_to_pred).tolist()

    estimation = {
        "physical_classif_score": predictionsPhy,  # previsione score classificatorio fisico
        "ODI_classif_score": predictionsODI  # previsione score classificatorio ODI
    }
  
    
    return estimation

"""
def predictions_SpineCOdi(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop("Uid", axis=1, inplace=True)

    with open("model_classification_odi_spine.pkl", "rb") as file:
        loaded_model = joblib.load(file)
    predictionsPineCodi = loaded_model.predict(data_to_pred).tolist()
    
    age = data_to_pred["anni_ricovero"].to_numpy()
    age = age.astype(int)
    age = age.tolist()
    
    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)
    
    estimation = {
        "spine_ODI_classif_score": predictionsPineCodi,  # previsione score classificatorio ODI
        "age": age,  # eta'
    }
    
    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []
    
    
    return to_json
"""




# -------------------- PER TESTING --------------------------------------------
"""
data_prepr = preprocessing(data)
e = predictions_hip_6months(data_prepr)
print(e)
"""

"""
input_data = {
                "sesso": "1",
                "anni_ricovero": "3",
                "classe_asa": "3",
                "VAS_Total_PreOp": "3",
                "SF12_PhysicalScore_PreOp": "3",
                "SF12_MentalScore_PreOp": "3",
                "BMI_altezza_PreOp": "180",
                "BMI_peso_PreOp": "3",
                "SF12_autovalsalute_risp_0": "3",
                "SF12_scale_risp_0": "3",
                "SF12_ultimomeseresa_risp_0": "3",
                "SF12_ultimomeselimite_risp_0": "3",
                "SF12_ultimomeseemo_risp_0": "3",
                "SF12_ultimomeseostacolo_risp_0": "3",
                "SF12_ultimomesesereno_risp_0": "3",
                "SF12_ultimomeseenergia_risp_0": "3",
                "SF12_ultimomesetriste_risp_0": "3",
                "SF12_ultimomesesociale_risp_0": "3",
                "zona_operazione": "0"
            }


input_data = pd.DataFrame.from_dict(input_data, orient="index").T
estimation = predictions_hipAndKneeR(input_data, "single_patient")
print(estimation)
"""

"""
input_data = {
                "nome_operazione": "Cifoplastiche",
                "sesso": "F",
                "anni_ricovero": "4",
                "ODI_Total_PreOp": "3",
                "Vas_Back_PreOp": "3",
                "Vas_Leg_PreOp":"3",
                "SF36_GeneralHealth_PreOp": "3",
                "SF36_PhysicalFunctioning_PreOp": "3",
                "SF36_RoleLimitPhysical_PreOp": "3",
                "SF36_RoleLimitEmotional_PreOp": "3",
                "SF36_SocialFunctioning_PreOp": "3",
                "SF36_Pain_PreOp": "3",
                "SF36_EnergyFatigue_PreOp": "3",
                "SF36_EmotionalWellBeing_PreOp": "3",
                "SF36_MentalScore_PreOp": "3",
                "SF36_PhysicalScore_PreOp": "3",
                "FABQ_Work_PreOp": "3",
                "classe_asa_1": "3"
            }

input_data2 = {
                "nome_operazione": "Cifoplastiche",
                "sesso": "M",
                "anni_ricovero": "4",
                "ODI_Total_PreOp": "3",
                "Vas_Back_PreOp": "3",
                "Vas_Leg_PreOp":"3",
                "SF36_GeneralHealth_PreOp": "3",
                "SF36_PhysicalFunctioning_PreOp": "3",
                "SF36_RoleLimitPhysical_PreOp": "3",
                "SF36_RoleLimitEmotional_PreOp": "3",
                "SF36_SocialFunctioning_PreOp": "3",
                "SF36_Pain_PreOp": "3",
                "SF36_EnergyFatigue_PreOp": "3",
                "SF36_EmotionalWellBeing_PreOp": "3",
                "SF36_MentalScore_PreOp": "3",
                "SF36_PhysicalScore_PreOp": "3",
                "FABQ_Work_PreOp": "3",
                "classe_asa_1": "3",
                "MORBIDITY": "3"
            }

input_data = pd.DataFrame.from_dict(input_data, orient="index").T
input_data = preprocessSpine(input_data)
input_data['sesso'] = input_data['sesso'].apply(check_gender)
estimation = predictions_SpineR(input_data, "single_patient")

print("R: ", estimation)



input_data2 = pd.DataFrame.from_dict(input_data2, orient="index").T
input_data2 = preprocessSpine(input_data2)
input_data2['sesso'] = input_data2['sesso'].apply(check_gender)
predictionsC = predictions_SpineC(input_data2, "single_patient")

print("C: ",predictionsC)
"""





