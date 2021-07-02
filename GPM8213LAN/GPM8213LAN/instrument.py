# -*- coding: utf-8 -*-
"""
`GPM8213LAN.instrument` implements the following classes:
    
`Instrument` High-level of GPM representation

"""
from GPM8213LAN.variable import Variable
import socket as sk


class Instrument():
    "HOST :str,  local ip address of the GPM (voir System > Congig > LAN on the GPM) \n PORT : int,23 for the GPM ,Telnet protocol \n timeout :float, time seconds to raise an error, \n variables = list of Variable, variable to measure \n pattern :int de 1 à 4 ,preset varaibles see page 94 and 95 of user manual"
    def __init__(self,HOST,PORT = 23,timeout = 2,variables = [], pattern = 4):
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
        "add a Variable to the list of varaible (max : 34), don't use self.variables.append(variable)"
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
        "Establishes the connection with a GPM (via the socket library) and verifies that it is accessible"
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
        "close the connection and remove the remote control on the GPM"
        message = ':COMM:REM 0\r\n'
        self.socket.send(message.encode('ASCII'))
        self.socket.close()
        return
    def identification(self):
        "fetch the basics data about the GPM used"
        data = self.send_query('*IDN?\r\n')
        self.name = data[0:-2].decode("utf-8")
    def send_query(self,message):
        "Send a query, see user manual to know which command are query or set"
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
        "Send a set, see user manual to know which command are query or set"
        # self.connect_to_instrument()
        print('set  '+message)
        self.socket.send(message.encode('ASCII'))
        # self.close_connection()
    def set_a_variable(self,variable,number):
        "DO NOT USE, send set to change 1 Variable of VALUE? command"
        self.send_set(f':NUM:NORM:ITEM{number} {variable.function}\r\n')
        self.send_set(f':NUM:NORM:NUMB {len(self.variables)}\r\n')
        return
    def set_variable(self):
        "DO NOT USE, send set to change VariableS of VALUE? command"
        size = len(self.variables)
        self.send_set(f':NUM:NORM:NUMB {size}\r\n')
        for number in range(1,size+1) :
             self.send_set(f':NUM:NORM:ITEM{number} {self.variables[number-1].function}\r\n')
        return
    def variables_pattern(self):
        "DO NOT USE, associate variables with the current PRESET"
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
        "Change the Preset (pattern) with the new one (new_patt)"
        if (new_patt>=1) and (new_patt<=4) :
            self.pattern = new_patt
            self.variables_pattern()
            self.send_set(f':NUM:NORM:PRES {new_patt}\r\n')
        else :
            raise TypeError('pattern doit être entre 1 et 4')
        return
    def ask_variable(self):
        "Retrun variables in string format"
        data  = self.send_query(':NUM:NORM:VALUE?\r\n')
        return data
    def mesure_variable(self):
        "Retrun variables in dico of float format"
        data_pars = self.parser_variables(self.ask_variable())
        return data_pars
    def parser_variables(self,data):
        "Convert string format to  dico of float format"
        values = data.decode("utf-8").split(',')
        dict_values = {}
        for number in range(0,len(values)) :
            dict_values[self.variables[number]]=float(values[number])
        return dict_values