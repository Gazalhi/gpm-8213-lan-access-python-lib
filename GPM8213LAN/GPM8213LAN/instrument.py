# -*- coding: utf-8 -*-
"""
`GPM8213LAN.instrument` implements the following classes:
    
`Instrument` High-level of GPM representation

@author: Hugo_MILAN
"""
from GPM8213LAN.variable import Variable
import socket as sk


class Instrument():
    "Correspond à un appareil"
    def __init__(self,HOST,PORT = 23,timeout = 2,variables = [], pattern = 4):
        "HOST :str, adresse ip local de l'appareil (voir System > Congig > LAN) \n PORT : int,23 pour les GPM \n timeout :float, temps en secondes pour lever une erreur en cas de non-réponse, \n variables = list of variable, que vous souhaiterez mesurer sur cette appareil (max 34) \n pattern :int de 1 à 4 ,ensemble de variable à mesurer prédéfinit voir page 94 et 95 du user manual"
        self.location = HOST
        self.port = PORT
        self.timeout = timeout 
        self.connect_to_instrument()
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
    def __del__(self):
        try :
            self.socket.getpeername()
            self.close_connection()
        except OSError :
            self.socket.close()
            pass
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
        self.socket.send(message.encode('ASCII'))
        self.socket.close()
        return
    def identification(self):
        data = self.send_query('*IDN?\r\n')
        self.name = data[0:-2].decode("utf-8")
    def send_query(self,message):
        print('query  '+message)
        # self.connect_to_instrument()
        self.socket.send(message.encode('ASCII'))
        try :     
            data = self.socket.recv(200)
        except :
            print(f'{self.location}::{self.port} doesn\'t answer')
            self.close_connection()
            raise
        # self.close_connection()
        return data
    def send_set(self,message):
        # self.connect_to_instrument()
        print('set  '+message)
        self.socket.send(message.encode('ASCII'))
        # self.close_connection()
    def set_a_variable(self,variable,number):
        self.send_set(f':NUM:NORM:ITEM{number} {variable.function}\r\n')
        self.send_set(f':NUM:NORM:NUMB {len(self.variables)}\r\n')
        return
    def set_variable(self):
        size = len(self.variables)
        self.send_set(f':NUM:NORM:NUMB {size}\r\n')
        for number in range(1,size+1) :
             self.send_set(f':NUM:NORM:ITEM{number} {self.variables[number-1].function}\r\n')
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
            self.send_set(f':NUM:NORM:PRES {new_patt}\r\n')
        else :
            raise TypeError('pattern doit être entre 1 et 4')
        return
    def ask_variable(self):
        data  = self.send_query(':NUM:NORM:VALUE?\r\n')
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