import pandas as pd 
import numpy as np
import pickle
import matplotlib.pyplot as plt 
import seaborn as sns
import xgboost
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
import os 
import os.path
from pathlib import Path
import json


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



def preprocessing(data):
    data = data.replace('#null', np.nan)
    
    data = data.apply(from_obj_to_num)

    data = data[~data['SF12 MentalScore 6months'].isna()]
    
    data = data[~data['SF12 PhysicalScore 6months'].isna()]
    
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

    def normalize_nomevento(x):
        if x in lista_nome_evento:
            nome_evento = x
        else:
            nome_evento = np.nan
        return nome_evento

    with open('lista_nome_evento.pkl', 'rb') as f:
        lista_nome_evento = pickle.load(f)
    
    data_preop['Nome evento'] = preproces_nomeevento(data_preop)

    data_preop['Nome evento'] = data_preop['Nome evento'].apply(normalize_nomevento)
    
    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.lower()
    
    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.replace('sx', 'sinistra')
    data_preop['Procedura intervento'] = data_preop['Procedura intervento'].str.replace('dx', 'destra')
    
    data_preop['Nome equipe'] = data_preop['Nome equipe'].str.lower().str.replace(' +', ' ',regex = True)
    
    data_preop = data_preop[data_preop['Nome equipe'] != 'chirurgia del ginocchio i']
    
    data_preop.Sesso = pd.get_dummies(data_preop.Sesso, drop_first= True) #0 F 1 M
    
    data_preop = pd.concat([data_preop.drop(['Nome evento'], axis = 1), pd.get_dummies(data_preop['Nome evento'])], axis = 1)

    data_preop = pd.concat([data_preop.drop(['Nome equipe'], axis = 1), pd.get_dummies(data_preop['Nome equipe'])], axis = 1)
    
    columns_to_drop = ['Data operazione', 'Data dimissione', 'Procedura intervento', 'HHS Function PreOp', 'HHS Total PreOp']
    
    data_preop.drop(columns_to_drop, axis  = 1, inplace = True)
    
    
    # dopo la colonna "Uid" (la prima) elimina tutte le colonne che non hanno nel nome "3months"/"6months"/"12months"
    data_3month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='3months', axis=1)], axis = 1)
    
    data_6month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='6months', axis=1)], axis = 1)
    
    data_12month = pd.concat([data_clean[['Uid']], data_clean.filter(regex='12months', axis=1)], axis = 1)
    
    
    return data_preop
    
    
def predictions_hip_6months(data):  
    data.drop('Uid', axis = 1, inplace = True)
    
    with open("model_6months_phy.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    predictionsP = loaded_model.predict(data)
    with open("model_6months_men.pkl", 'rb') as file:
        loaded_model2 = pickle.load(file)
    predictionsM = loaded_model2.predict(data)
    


#estimation = {"ID":patient_id.ID, "DATA_VISITA": patient_id['DATA VISITA'],
    #              "Sesso":patient_id.SESSO,"Age": observations["ETA'"].round(0),'Peso': patient_id['PESO (Kg)'],
              #    'Altezza':patient_id['ALTEZZA (cm)'], 'Age_Reader_Score': predictions.round(3),
                #  'Biological_Age':estimated_age,'Delta':delta.round(3)}

            #nel caso bisogni aggiungere dati al estimation qui :
            
            
    estimation = {"SF12 PhysicalScore 6months": predictionsP, 
                  "SF12 MentalScore 6months": predictionsM
    }            
            
    path = Path.cwd()
    path = path / "result.json"
        
    with open(path, 'w') as fp:
        json.dump(pd.DataFrame.from_dict(estimation,orient = 'columns').to_json(), fp)
    return True

#data_prepr = preprocessing(data)
#predictions_hip_6months(data_prepr)






    
