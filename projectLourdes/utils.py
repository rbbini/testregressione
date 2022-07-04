import joblib
import pandas as pd
import numpy as np
import pickle
import statistics
import os
# from pyearth import Earth
from operator import itemgetter

# data = pd.read_excel(r'C:\Users\Loredana\Documents\epimetheus-project\testregressione\data\data_reg_anca.xls')


# dati che saranno ritornati in un json
dbPath = os.path.abspath("data/db_anca.xls")
db = pd.read_excel(dbPath)

ageDB = db['Anni ricovero'].to_numpy()
ageDB = ageDB.astype(int)
ageDB = ageDB.tolist()

DB_6months_p = db['SF12 MentalScore 6months'].tolist()
DB_6months_m = db['SF12 PhysicalScore 6months'].tolist()

medianP = statistics.median(DB_6months_p)
medianM = statistics.median(DB_6months_m)

columns_preop = ['Uid', 'Sesso', 'Anni ricovero', 'Data operazione', 'Data dimissione',
                 'Nome evento', 'Nome equipe', 'Procedura intervento', 'HHS Function PreOp',
                 'HHS Total PreOp', 'VAS PAIN risp PreOp', 'SF12 PhysicalScore PreOp',
                 'SF12 MentalScore PreOp', 'HOOSPS Total PreOp', 'BMI altezza risp PreOp',
                 'BMI peso risp PreOp', 'BMI Total PreOp']


def preproces_nomeevento(data_preop):
    data_preop['Nome evento'] = data_preop['Nome evento'].str.lower()  # replace('\s+', ' ').value_counts()
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace('\n', '', regex=True)
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace(' +', ' ', regex=True)
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace('([a-z]+)(protesi)', r'\1 protesi', regex=True)
    return data_preop['Nome evento']


def from_obj_to_num(x):
    try:
        res = x.astype(float)
    except ValueError:
        res = x
    return res


def check_gender(x):
    if x.lower() == 'm':
        gender = 0
    elif x.lower() == 'f':
        gender = 1
    else:
        gender = np.nan
    return gender


def check_equipe(df):
    if '36h orto - moroni' not in df.columns:
        df['36h orto - moroni'] = 0
    if '36p orto - parente' not in df.columns:
        df['36p orto - parente'] = 0
    if 'casco' not in df.columns:
        df['casco'] = 0
    if 'centro di traumatologia dello sport' not in df.columns:
        df['centro di traumatologia dello sport'] = 0
    if 'chirurgia anca i' not in df.columns:
        df['chirurgia anca i'] = 0
    if 'clinica ortopedica' not in df.columns:
        df['clinica ortopedica'] = 0
    if 'e.u.o.r.r.' not in df.columns:
        df['e.u.o.r.r.'] = 0
    if 'gspine4' not in df.columns:
        df['gspine4'] = 0
    if 'oraco' not in df.columns:
        df['oraco'] = 0
    if 'ot9 orto - ventura2' not in df.columns:
        df['ot9 orto - ventura2'] = 0
    return df


def check_event(df):
    if 'bilaterale protesi primo intervento' not in df.columns:
        df['bilaterale protesi primo intervento'] = 0
    if 'destra protesi primo intervento' not in df.columns:
        df['destra protesi primo intervento'] = 0
    if 'destra revisione' not in df.columns:
        df['destra revisione'] = 0
    if 'sinistra protesi primo intervento' not in df.columns:
        df['sinistra protesi primo intervento'] = 0
    if 'sinistra revisione' not in df.columns:
        df['sinistra revisione'] = 0
    return df


def most_similar_scores(all_scores, ages, input_score, input_age):
    to_sort = []
    sorted_scores = []

    for i in range(len(all_scores)):
        to_sort.append((all_scores[i], abs(input_score[0] - all_scores[i]), ages[i], abs(input_age[0] - ages[i])))

    to_sort.sort(key=itemgetter(1, 3))

    for x in range(0, 5):
        sorted_scores.append((to_sort[x][0], to_sort[x][2]))

    return sorted_scores


def preprocessing(data):
    data = data.replace('#null', np.nan)

    data = data.apply(from_obj_to_num)

    # data = data[~data['SF12 MentalScore 6months'].isna()]

    # data = data[~data['SF12 PhysicalScore 6months'].isna()]

    data = data[~data['SF12 MentalScore PreOp'].isna()]

    data = data[~data['SF12 PhysicalScore PreOp'].isna()]

    data = data[~data['HOOSPS Total PreOp'].isna()]

    data = data[~data['BMI altezza risp PreOp'].isna()]

    data = data[~data['BMI peso risp PreOp'].isna()]

    data['Data operazione'] = data['Data operazione'].str.replace('\s(00:00:00.0)', '', regex=True)

    data['Data operazione'] = pd.to_datetime(data['Data operazione'])

    data['Data operazione'] = data['Data operazione'].dt.strftime('%Y/%m/%d')

    # mask_date = data['Data operazione'] <= '2021/05/05'

    # data_clean = data.loc[mask_date, :]

    # data_preop = data_clean.loc[:, columns_preop]\

    data_preop = data.loc[:, columns_preop]

    with open('lista_nome_evento.pkl', 'rb') as f:
        lista_nome_evento = joblib.load(f)

    def normalize_nomevento(x):
        if x in lista_nome_evento:
            nome_evento = x
        else:
            nome_evento = np.nan
        return nome_evento

    data_preop['Nome evento'] = preproces_nomeevento(data_preop)

    data_preop['Nome evento'] = data_preop['Nome evento'].apply(normalize_nomevento)

    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.lower()

    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.replace('sx', 'sinistra')
    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.replace('dx', 'destra')

    data_preop['Nome equipe'] = data_preop['Nome equipe'].str.lower().str.replace(' +', ' ', regex=True)

    data_preop = data_preop[data_preop['Nome equipe'] != 'chirurgia del ginocchio i']

    data_preop = pd.concat([data_preop.drop(['Nome evento'], axis=1), pd.get_dummies(data_preop['Nome evento'])],
                           axis=1)

    data_preop = pd.concat([data_preop.drop(['Nome equipe'], axis=1), pd.get_dummies(data_preop['Nome equipe'])],
                           axis=1)

    # data_preop.Sesso = pd.get_dummies(data_preop.Sesso, drop_first= True) #0 F 1 M
    data_preop['Sesso'] = data_preop['Sesso'].apply(check_gender)
    data_preop = check_equipe(data_preop)
    data_preop = check_event(data_preop)

    columns_to_drop = ['Data operazione', 'Data dimissione', 'Procedura intervento', 'HHS Function PreOp',
                       'HHS Total PreOp']

    data_preop.drop(columns_to_drop, axis=1, inplace=True)

    # dopo la colonna "Uid" (la prima) elimina tutte le colonne che non hanno nel nome "3months"/"6months"/"12months"
    # data_3month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='3months', axis=1)], axis = 1)

    # data_6month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='6months', axis=1)], axis = 1)

    # data_12month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='12months', axis=1)], axis = 1)

    return data_preop

    # modifiche da fare - creare diversi prediction per gino/anca(insieme) regressive+classificatory - spine (regre classi odi e basico)
    # separazione regre+classi tra phy/mental +++


def predictions_hip_6months(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_6months_phy.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsP = loaded_model.predict(data_to_pred).tolist()
    with open("model_6months_men.pkl", 'rb') as file:
        loaded_model2 = joblib.load(file)
    predictionsM = loaded_model2.predict(data_to_pred).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsP,  # previsione score fisico dopo 6 mesi
                  "SF12_MentalScore_6months": predictionsM,  # previsione score mentale dopo 6 mesi
                  "age": age  # eta'
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
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsP, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)

        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsM, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)

        to_json.append(similar_scores)

    return to_json

    # regressiboy anca e gino

def predictions_hipAndKneeR(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_regression_physical.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPhakR = loaded_model.predict(data_to_pred.values).tolist()
    with open("model_regression_mental.pkl", 'rb') as file:
        loaded_model2 = joblib.load(file)
    predictionsMhakR = loaded_model2.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPhakR,  # previsione score fisico dopo 6 mesi
                  "SF12_MentalScore_6months": predictionsMhakR,  # previsione score mentale dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # classificatoz

def predictions_hipAndKneeC(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_classification_physical.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPhakC = loaded_model.predict(data_to_pred.values).tolist()
    with open("model_classification_mental.pkl", 'rb') as file:
        loaded_model2 = joblib.load(file)
    predictionsMhakC = loaded_model2.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPhakC,  # previsione score fisico dopo 6 mesi
                  "SF12_MentalScore_6months": predictionsMhakC,  # previsione score mentale dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene) 
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsPhakC, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)

        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsMhakC, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)

        to_json.append(similar_scores)

    return to_json

    # regressiboy per spine

def predictions_SpineR(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_regression_physical_spine.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPineRr = loaded_model.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPineRr,  # previsione score fisico dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene) 
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsPineRr, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)
        """
        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsM, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)
        """
        to_json.append(similar_scores)

    return to_json

    # odi-bro  regressivo con spine

def predictions_SpineOdi(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_regression_odi_spine.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPineOdiR = loaded_model.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPineOdiR,  # previsione score fisico dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene) 
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsPineOdiR, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)
        """
        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsM, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)
        """
        to_json.append(similar_scores)

    return to_json

    # da continuare con rob, porcod
    # classi spine

def predictions_SpineC(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_classification_physical_spine.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPineC = loaded_model.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPineC,  # previsione score fisico dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene) 
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsPineC, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)
        """
        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsM, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)
        """
        to_json.append(similar_scores)

    return to_json

def predictions_SpineCOdi(data_to_pred, mode):
    # drop dell'id perchè non riesce a convertirlo in float
    #data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_classification_odi_spine.pkl", 'rb') as file:
        loaded_model = joblib.load(file)
    predictionsPineCodi = loaded_model.predict(data_to_pred.values).tolist()

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)
    age = age.tolist()

    # possibile modifica di estimation, per tornare i dati del M o P regressive/class senza impazzire(?)

    estimation = {"SF12_PhysicalScore_6months": predictionsPineCodi,  # previsione score fisico dopo 6 mesi
                  "age": age  # eta'
                  }

    # lista da convertire in json
    to_json = [estimation]
    # lista che avra' i dati dei pazienti nel DB
    others = []

    ###da controllare con rob!?!

    # ciclo da 0 a len(ageDB)-1 (anche len(DB_6months_m/p) sarebbe andato bene) 
    # prendo il valore in pos i e lo metto in un dict che poi appendo a others
    for i in range(len(ageDB)):
        dict = {
            "SF12_PhysicalScore_6months": DB_6months_p[i],
            "SF12_MentalScore_6months": DB_6months_m[i],
            "age": ageDB[i]
        }
        others.append(dict)

    other_patients = {"others": others}
    to_json.append(other_patients)

    median_data = {"medianaM": medianM,
                   "medianaP": medianP}
    to_json.append(median_data)

    if mode == "single_patient":
        similar_scores = []
        similar_p = most_similar_scores(DB_6months_p, ageDB, predictionsPineCodi, data_to_pred['Anni ricovero'])
        for x in range(len(similar_p)):
            similar_p_dict = {"SF12_PhysicalScore_6months": similar_p[x][0],
                              "age": similar_p[x][1]
                              }
            similar_scores.append(similar_p_dict)
        """
        similar_m = most_similar_scores(DB_6months_m, ageDB, predictionsM, data_to_pred['Anni ricovero'])
        for x in range(len(similar_m)):
            similar_m_dict = {"SF12_MentalScore_6months": similar_m[x][0],
                              "age": similar_m[x][1]
                              }
            similar_scores.append(similar_m_dict)
        """
        to_json.append(similar_scores)

    return to_json


# da modificare la parte del single patient - with rob


# data_prepr = preprocessing(data)
# predictions_hip_6months(data_prepr)


# -------------------- PER TESTING --------------------------------------------
"""
data_prepr = preprocessing(data)
e = predictions_hip_6months(data_prepr)
print(e)
"""
"""
input_data = {
    "Uid": 'IOG1RH100000001',#.id_paziente.data
    "Sesso": 'M', #.sesso.data
    "Anni ricovero": '10',
    "Data operazione": '2013-01-07 00:00:00.0',
    "Data dimissione": '2013-01-11 00:00:00.0',
    "Nome evento": 'SINISTRA protesi primo intervento',
    "Nome equipe": 'ORACO',
    "Procedura intervento": 'PROTESI ANCA  SIN',
    "HHS Function PreOp": '#null',
    "HHS Total PreOp": '54999',
    "VAS PAIN risp PreOp": '0',
    "SF12 PhysicalScore PreOp": '29',
    "SF12 MentalScore PreOp": '41.1',
    "HOOSPS Total PreOp": '37.7',
    "BMI altezza risp PreOp": '0',
    "BMI peso risp PreOp": '0',
    "BMI Total PreOp": '0'
    }
input_data = pd.DataFrame.from_dict(input_data, orient='index').T
data_preprocessed = preprocessing(input_data)
estimation = predictions_hip_6months(data_preprocessed, "single_patient")
print(estimation)

"""
"""input_data = {
    "sesso": 'M',
    "Anni ricovero": '10',
    "classeasa": '1',
    "vastotalpreop": '2',
    "SF12physicalscorepreop": '5',
    "SF12_MentalScore_PreOp": '2',
    "bmialtezzapreop": '180',
    "bmipesopreop": '80',
    "SF12autovalsaluterisp0": '5',
    "SF12scalerisp0": '8',
    "sf12ultimomeseresarisp0": '5',
    "sf12ultimomeselimiterisp0": '5',
    "sf12ultimomeseemorisp0": '5',
    "sf12ultimomeseostacolorisp0": '5',
    "sf12ultimomeseserenorisp0": '5',
    "sf12ultimomeseneergiarisp0": '5',
    "sf12ultimomesetristerisp0": '5',
    "sf12ultimomesesocialerisp0": '5',
    "zonaoperazione": '0'
}

input_data = pd.DataFrame.from_dict(input_data, orient='index').T
estimation = predictions_hipAndKneeR(input_data, "single_patient")
print(estimation)
"""