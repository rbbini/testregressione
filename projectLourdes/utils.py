import pandas as pd 
import numpy as np
import pickle
import statistics


data = pd.read_excel(r'C:\Users\rober\Desktop\PROMS\data\data_reg_anca.xls')

columns_preop = ['Uid', 'Sesso', 'Anni ricovero', 'Data operazione', 'Data dimissione',
           'Nome evento', 'Nome equipe', 'Procedura intervento', 'HHS Function PreOp',	
           'HHS Total PreOp', 'VAS PAIN risp PreOp','SF12 PhysicalScore PreOp',	
           'SF12 MentalScore PreOp', 'HOOSPS Total PreOp', 'BMI altezza risp PreOp',
           'BMI peso risp PreOp','BMI Total PreOp']
columns_3mon = ['Uid', 'Sesso', 'Anni ricovero', 'Data operazione', 'Data dimissione',
           'Nome evento', 'Nome equipe', 'Procedura intervento', 'HHS Function 3months',	
           'HHS Total 3months', 'VAS PAIN risp 3months','SF12 PhysicalScore 3months',	
           'SF12 MentalScore 3months', 'HOOSPS Total 3months', 'BMI altezza risp 3months',
           'BMI peso risp 3months','BMI Total 3months']
columns_6mon = ['Uid', 'Sesso', 'Anni ricovero', 'Data operazione', 'Data dimissione',
           'Nome evento', 'Nome equipe', 'Procedura intervento', 'HHS Function 6months',	
           'HHS Total 6months', 'VAS PAIN risp 6months','SF12 PhysicalScore 6months',	
           'SF12 MentalScore 6months', 'HOOSPS Total 6months', 'BMI altezza risp 6months',
           'BMI peso risp 6months','BMI Total 6months']




def preproces_nomeevento(data_preop):
    data_preop['Nome evento'] = data_preop['Nome evento'].str.lower()#replace('\s+', ' ').value_counts()
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace('\n', '', regex = True)
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace(' +', ' ', regex = True)
    data_preop['Nome evento'] = data_preop['Nome evento'].str.replace('([a-z]+)(protesi)', r'\1 protesi',regex = True)
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
    if not '36h orto - moroni' in df.columns:
        df['36h orto - moroni'] = 0
    if not '36p orto - parente' in df.columns:
        df['36p orto - parente'] = 0
    if not 'casco' in df.columns:
        df['casco'] = 0   
    if not 'centro di traumatologia dello sport' in df.columns:
        df['centro di traumatologia dello sport'] = 0
    if not 'chirurgia anca i' in df.columns:
        df['chirurgia anca i'] = 0
    if not 'clinica ortopedica' in df.columns:
        df['clinica ortopedica'] = 0
    if not 'e.u.o.r.r.' in df.columns:
        df['e.u.o.r.r.'] = 0
    if not 'gspine4' in df.columns:
        df['gspine4'] = 0
    if not 'oraco' in df.columns:
        df['oraco'] = 0
    if not 'ot9 orto - ventura2' in df.columns:
        df['ot9 orto - ventura2'] = 0
    return df


def check_event(df):
    if not 'bilaterale protesi primo intervento' in df.columns:
        df['bilaterale protesi primo intervento'] = 0
    if not 'destra protesi primo intervento' in df.columns:
        df['destra protesi primo intervento'] = 0
    if not 'destra revisione' in df.columns:
        df['destra revisione'] = 0
    if not 'sinistra protesi primo intervento' in df.columns:
        df['sinistra protesi primo intervento'] = 0
    if not 'sinistra revisione' in df.columns:
        df['sinistra revisione'] = 0
    return df


def preprocessing(data):
    data = data.replace('#null', np.nan)
    
    data = data.apply(from_obj_to_num)

    #data = data[~data['SF12 MentalScore 6months'].isna()]

    #data = data[~data['SF12 PhysicalScore 6months'].isna()]
    
    data = data[~data['SF12 MentalScore PreOp'].isna()]
    
    data = data[~data['SF12 PhysicalScore PreOp'].isna()]
    
    data = data[~data['HOOSPS Total PreOp'].isna()]
    
    data = data[~data['BMI altezza risp PreOp'].isna()]
    
    data = data[~data['BMI peso risp PreOp'].isna()]
    
    data['Data operazione'] = data['Data operazione'].str.replace('\s(00:00:00.0)','', regex = True)
    
    data['Data operazione'] = pd.to_datetime(data['Data operazione'])
    
    data['Data operazione'] = data['Data operazione'].dt.strftime('%Y/%m/%d')
    
    mask_date = data['Data operazione'] <= '2021/05/05'
    
    data_clean = data.loc[mask_date,:]
    
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
    
    data_preop['Nome equipe'] = data_preop['Nome equipe'].str.lower().str.replace(' +', ' ',regex = True)
    
    data_preop = data_preop[data_preop['Nome equipe'] != 'chirurgia del ginocchio i']
    
    data_preop = pd.concat([data_preop.drop(['Nome evento'], axis = 1), pd.get_dummies(data_preop['Nome evento'])], axis = 1)

    data_preop = pd.concat([data_preop.drop(['Nome equipe'], axis = 1), pd.get_dummies(data_preop['Nome equipe'])], axis = 1)
    
    #data_preop.Sesso = pd.get_dummies(data_preop.Sesso, drop_first= True) #0 F 1 M
    data_preop['Sesso'] = data_preop['Sesso'].apply(check_gender)
    data_preop = check_equipe(data_preop)
    data_preop = check_event(data_preop)
    
    columns_to_drop = ['Data operazione', 'Data dimissione', 'Procedura intervento', 'HHS Function PreOp', 'HHS Total PreOp']
    
    data_preop.drop(columns_to_drop, axis  = 1, inplace = True)
    
    
    # dopo la colonna "Uid" (la prima) elimina tutte le colonne che non hanno nel nome "3months"/"6months"/"12months"
    #data_3month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='3months', axis=1)], axis = 1)
    
    #data_6month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='6months', axis=1)], axis = 1)
    
    #data_12month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='12months', axis=1)], axis = 1)
    
    
    return data_preop
    
    
def predictions_hip_6months(data):  
    # drop dell'id perchè non riesce a convertirlo in float
    data.drop('Uid', axis = 1, inplace = True)
    
    with open("model_6months_phy.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    predictionsP = loaded_model.predict(data)
    with open("model_6months_men.pkl", 'rb') as file:
        loaded_model2 = pickle.load(file)
    predictionsM = loaded_model2.predict(data)
    
    age = data['Anni ricovero'].to_numpy()
    age = age.astype(int)           
            
    estimation = {"SF12 PhysicalScore 6months": predictionsP, 
                  "SF12 MentalScore 6months": predictionsM,
                  "age": age,
                  "medianaP": statistics.median(predictionsP), # la mediana è sui valori giusti?
                  "medianaM": statistics.median(predictionsM)
    }      

    # "eta'": data[['Anni ricovero']]
    # QUESTA RIGA RIPORTA I VALORI IN UN FORMATO DIVERSO RISPETTO A QUELLE SOPRA. CREA PROBLEMI?
    # print(data['Anni ricovero'])
    return estimation






# -------------------- PER TESTING --------------------------------------------
"""
data_prepr = preprocessing(data)
e =predictions_hip_6months(data_prepr)
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



    
