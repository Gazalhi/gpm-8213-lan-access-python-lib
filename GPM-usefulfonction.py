# -*- coding: utf-8 -*-
"""
Class de comm et de parsage  pour GPM-8213

@author: Hugo_MILAN
"""
__author__ = "Hugo MILAN"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Hugo MILAN"
__email__ = "hugo.milan@ens-paris-saclay.fr"
__status__ = "Education"

import socket as sk
import numpy as np
import time as tm







class Instrument():
    "Correspond à un appareil"
    def __init__(self,HOST,PORT = 23,timeout = 2,variables = [], pattern = 4):
        "HOST :str, adresse ip local de l'appareil (voir System > Congig > LAN) \n PORT : int,23 pour les GPM \n timeout :float, temps en secondes pour lever une erreur en cas de non-réponse, \n variables = list of variable, que vous souhaiterez mesurer sur cette appareil (max 34) \n pattern :int de 1 à 4 ,ensemble de variable à mesurer prédéfinit voir page 94 et 95 du user manual"
        self.location = HOST
        self.port = PORT
        self.timeout = timeout       
        self.identification()
        self.variables = []
        if len(variables)>0 : 
            pattern = 0
            if len(variables)>= 34 : 
                raise OverflowError('Pas plus de 34 variables')
            self.add_variable(variables)
        self.pattern = pattern
        if pattern!=0:
            self.change_pattern(pattern)
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return f"{self.name},{self.location},{self.port}"
    def add_variable(self,variable):
        self.pattern = 0
        if len(self.variables)>= 34 : 
            raise OverflowError('Pas plus de 34 variables')
        if type(variable)==list :
            for var in variable:
                if type(var)!=Variable : 
                    self.variables.append(Variable(var)) 
                else : 
                    self.variables.append(var) 
            if len(self.variables)>= 34 : 
                raise OverflowError('Pas plus de 34 variables')
            self.set_variable()
        elif type(variable)!=Variable : 
            self.variables.append(Variable(variable)) 
            if len(self.variables)>= 34 : 
                raise OverflowError('Pas plus de 34 variables')
            self.set_a_variable(self.variables[-1], len(self.variables))
        else : 
            self.variables.append(variable)
            if len(self.variables)>= 34 : 
                raise OverflowError('Pas plus de 34 variables')
            self.set_a_variable(self.variables[-1], len(self.variables))
        return
    def connect_to_instrument(self):
        "Établis la connexion avec un GPM (par le biliothèque socket) et vérifie qu'il est accessible"
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        try :
            self.socket.connect((self.location, self.port))
        except : 
            print(f'impossible d\'ouvrir la liaison avec {self.location}::{self.port}' )
            self.socket.close()
            raise
        return
    def close_connection(self): 
        message = ':COMM:REM 0\r\n'
        self.send_set(message)
        self.socket.close()
        return
    def identification(self):
        self.connect_to_instrument()
        data = self.send_query('*IDN?\r\n')
        self.name = data[0:-2].decode("utf-8")
        self.close_connection()
    def send_query(self,message):
        self.socket.sendall(message.encode())
        try :     
            data = self.socket.recv(300)
        except :
            print(f'{self.location}::{self.port} doesn\'t answer')
            self.close_connection()
            raise
        return data
    def send_set(self,message): 
        self.socket.sendall(message.encode())
    def set_a_variable(self,variable,number):
        self.connect_to_instrument()
        self.send_set(f':NUM:NORM:ITEM{number} {variable.function}\r\n')
        self.send_set(f':NUM:NORM:NUMB {len(self.variables)}\r\n')
        self.close_connection()
        return
    def set_variable(self):
        self.connect_to_instrument()
        size = len(self.variables)
        self.send_set(f':NUM:NORM:NUMB {size}\r\n')
        for number in range(1,size+1) :
             self.send_set(f':NUM:NORM:ITEM{number} {self.variables[number-1].function}\r\n')
        self.close_connection()
        return
    def variables_pattern(self):
        self.variables = [Variable('U'),Variable('I'),Variable('P')]
        if self.pattern>=2 :
            self.variables += [Variable('S'),Variable('Q'),Variable('LAMB'),Variable('PHI'),Variable('FU'),Variable('FI')]
        if self.pattern>=3 :
            self.variables += [Variable('UPPeak'),Variable('UMPeak'),Variable('IPPeak'),Variable('IMPeak'),Variable('PPPeak'),Variable('PMPeak')]
        if self.pattern>=4 :
            self.variables[13] = Variable('TIME')
            self.variables[14] = Variable('WH')
            self.variables += [Variable('WHP'),Variable('WHM'),Variable('AH'),Variable('AHP'),Variable('AHM'),Variable('PPPeak'),Variable('PMPeak'),Variable('CFU'),Variable('CFI'),Variable('UTHD'),Variable('ITHD'),Variable('URANge'),Variable('IRANge')]
    def change_pattern(self,new_patt):
        if (new_patt>=1) and (new_patt<=4) :
            self.pattern = new_patt
            self.variables_pattern()
            self.connect_to_instrument()
            self.send_set(f':NUM:NORM:PRES {new_patt}')
            self.close_connection()
        else :
            raise TypeError('pattern doit être entre 1 et 4')
        return
    def ask_variable(self):
        self.connect_to_instrument()
        data  = self.send_query(':NUM:NORM:VALUE?\r\n')
        self.close_connection()
        return data
    def mesure_variable(self):
        data_pars = self.parser_variables(self.ask_variable())
        return data_pars
    def parser_variables(self,data):
        values = data.decode("utf-8").split(',')
        dict_values = {}
        for number in range(0,len(values)) :
            dict_values[self.variables[number]]=float(values[number])
        return dict_values
       
    
    
class Measurement():
    "Crée un Insantance de mesure pour spécifier le mode, les appareils et les grandeurs à mesurer \n Attention : ces appreils sont très peu réactifs et des mesures précises et synchronisées sont impossibles, nous vous conseillons de les utiliser pour des régimes permanants"
    def __init__(self,mode ='single',instruments = []):
        if type(mode)!=Measurement_mode :
            self.mode = Measurement_mode(mode)
        else :
            self.mode = mode
        self.instruments = instruments
    def __str__(self):
        return f"{self.instruments}\n{self.functions}"
    def __repr__(self):
        return self.instruments,self.functions
    def __sizeof__(self):
        "(instruments,functions)"
        return (len(self.instruments),len(self.functions))
    def __call__(self):
        if self.mode.name=='single' :
            results = []
            for instrument in self.instruments : 
                results.append(instrument.mesure_variable())
                results[-1]['Instrument']=instrument.__repr__()
        return results
    def add_intruments(self,instrument):
        if type(instrument)!=Instrument : 
            self.instruments.append(Instrument(instrument)) 
        else : 
            self.instruments.append(instrument) 
        return

        
class Variable():
    "Function to display, to find the list go to page 76 and 77 in user manual"
    def __init__(self,function):
        self.variable_available =['U', 'I', 'P', 'S', 'Q', 'LAMB', 'PHI', 'FU', 'FI', 'UPPeak', 'UMPeak', 'IPPeak', 'IMPeak', 'TIME', 'WH', 'WHP', 'WHM', 'AH', 'AHP', 'AHM', 'PPPeak', 'PMPeak', 'CFU', 'CFI', 'UTHD', 'ITHD', 'URANge', 'IRANge']
        if type(function)!=str:
            raise TypeError('must be a string (str)')
        if not(function in self.variable_available):
            raise TypeError('{function} not available')
        self.function = function
    def __str__(self):
        return f'{self.function}'
    def __repr__(self):
        return self.function
    
    
class Measurement_mode():
    "defines type of measurment and its parameters \n single : one measure on  call \n continuous : multiple single measure \n integrator : interger power during time (see urser manual p53)"
    def __init__(self,mode):
        if ((mode!='single') and (mode!='continuous') and (mode!='integrator')):
            raise TypeError('must be a string (str) in single, continuous and integrator')
        self.name = mode
        self.specification()
    def specification(self,sample_time= 1,time = 10):
        "defines time and sample time which will be use if necessary"
        self.sample_time = sample_time
        self.time = time
        return 
    def __str__(self):
        return f"<{self.name}>"
    def __repr__(self):
        return self.name
    
            
        
    


# %% test 
variable_available =['U', 'I', 'P', 'S', 'Q', 'LAMB', 'PHI', 'FU', 'FI', 'UPPeak', 'UMPeak', 'IPPeak', 'IMPeak', 'TIME', 'WH', 'WHP', 'WHM', 'AH', 'AHP', 'AHM', 'PPPeak', 'PMPeak', 'CFU', 'CFI', 'UTHD', 'ITHD', 'URANge', 'IRANge']
GPM_1 = Instrument("138.231.71.232",pattern=4)
# GPM_2 = Instrument("138.231.71.233",pattern=4)
# inst = Measurement(instruments=[GPM_1,GPM_2])
# data =inst()
# print(data)
# GPM_1 = Instrument("138.231.71.232",variables=variable_available)
# print(GPM_1.mesure_variable())


