import pandas as pd
import numpy as np
import pickle
import statistics
import os

# data = pd.read_excel(r'C:\Users\Loredana\Documents\epimetheus-project\testregressione\data\data_reg_anca.xls')


# dati che saranno ritornati in un json
dbPath = os.path.abspath("data/db_anca.xls")
db = pd.read_excel(dbPath)

ageDB = db['Anni ricovero'].to_numpy()
ageDB = ageDB.astype(int)

DB_6months_p = db['SF12 MentalScore 6months']
DB_6months_m = db['SF12 PhysicalScore 6months']

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

    mask_date = data['Data operazione'] <= '2021/05/05'

    data_clean = data.loc[mask_date, :]

    data_preop = data_clean.loc[:, columns_preop]

    with open('lista_nome_evento.pkl', 'rb') as f:
        lista_nome_evento = pickle.load(f)

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


def predictions_hip_6months(data_to_pred):
    # drop dell'id perchè non riesce a convertirlo in float
    data_to_pred.drop('Uid', axis=1, inplace=True)

    with open("model_6months_phy.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    predictionsP = loaded_model.predict(data_to_pred)
    with open("model_6months_men.pkl", 'rb') as file:
        loaded_model2 = pickle.load(file)
    predictionsM = loaded_model2.predict(data_to_pred)

    age = data_to_pred['Anni ricovero'].to_numpy()
    age = age.astype(int)

    # stime fatte sui dati in input
    estimation = {"SF12_PhysicalScore_6months": predictionsP,  # score fisico dopo 6 mesi
                  "SF12_MentalScore_6months": predictionsM,  # score mentale dopo 6 mesi
                  "age": age  # eta'
                  }

    # dati dei pazienti nel nostro db (data_reg_anca.xls)
    DBstuff = {"SF12_PhysicalScore_6months_DB": DB_6months_p,  # score fisico dopo 6 mesi
               "SF12_MentalScore_6months_DB": DB_6months_m,  # score mentale dopo 6 mesi
               "ageDB": ageDB,  # eta'
               "medianaP": medianP,  # mediana degli score fisici
               "medianaM": medianM  # mediana degli score mentali
               }

    return estimation, DBstuff


# data_prepr = preprocessing(data)
# predictions_hip_6months(data_prepr)


# -------------------- PER TESTING --------------------------------------------
"""
data_prepr = preprocessing(data)
e = predictions_hip_6months(data_prepr)
print(e)
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
estimation = predictions_hip_6months(data_preprocessed)
print(estimation)
"""
