# -*- coding: utf-8 -*-
"""
`GPM8213LAN.measurement` implements the following classes:
    
`Measurement` instance of measuring to automate the measure process

`Measurement_mode` type of measurement with specific parameter

@author: Hugo_MILAN
"""
from GPM8213LAN.instrument import Instrument


class Measurement():
    "Crée un Insantance de mesure pour spécifier le mode, les appareils et les grandeurs à mesurer \n Attention : ces appreils sont très peu réactifs et des mesures précises et synchronisées sont impossibles, nous vous conseillons de les utiliser pour des régimes permanants"
    def __init__(self,mode ='single',instruments = []):
        if type(mode)!=Measurement_mode :
            self.mode = Measurement_mode(mode)
        else :
            self.mode = mode
        self.instruments = instruments
    def __str__(self):
        return f"{self.mode}{self.instruments}"
    def __repr__(self):
        return f"{self.mode}{self.instruments}"
    def __sizeof__(self):
        "instruments"
        return len(self.instruments)
    def __call__(self):
        results = []
        if self.mode.name=='single' :
            
            for instrument in self.instruments : 
                results.append(instrument.mesure_variable())
                results[-1]['Instrument']=instrument.__repr__()
        elif self.mode.name=='continuous':
            print()
        return results
    def add_intruments(self,instrument):
        if type(instrument)!=Instrument : 
            self.instruments.append(Instrument(instrument)) 
        else : 
            self.instruments.append(instrument) 
        return
    
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