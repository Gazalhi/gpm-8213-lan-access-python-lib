# -*- coding: utf-8 -*-
"""
`GPM8213LAN.measurement` implements the following classes:
    
:Measurement: instance of measuring to automate the measure process

:Measurement_mode: type of measurement with specific parameter

"""
from GPM8213LAN.instrument import Instrument


class Measurement():
    """:mode: *str* or *Measurement_mode*, 'single' or 'continuous' or 'integrator' \n
    :instruments: *list of Instrument* \n
    Creates a measurement Insantance to specify the **mode**, **devices** and `variables` to be measured. \n
You have to specifies variables of each Instrument or use homogenize_variables() \n
Warning: these devices are very little reactive and precise and synchronized measurements are impossible, we advise you to use them during steady-state
        \n"""
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
        """:instrument: *Instrument* \n 
        add an Instrument \n
        :return *None*
        \n"""
        if type(instrument)!=Instrument : 
            self.instruments.append(Instrument(instrument)) 
        else : 
            self.instruments.append(instrument) 
        return
    def homogenize_variables(self,variables=[],pattern=4): 
        """ :variables: *list of Variable*, variable to measure. \n
        :pattern: *int* de 1 à 4 ,preset varaibles see page 94 and 95 of user manual \n
        change variables/Preset of each instrument
        :return: *None*
        \n"""
        if variables==[]:
            for instrument in self.instruments :
                instrument.change_pattern(pattern)
        else :
            for instrument in self.instruments :
                instrument.change_variables(variables)
        return
class Measurement_mode():
    """defines type of measurment and its parameters \n
    :mode: *str* in : 
        single : one measure on  call
        continuous : multiple single measure
        integrator : interger power during time (see urser manual p53)
        \n"""
    def __init__(self,mode):
        if ((mode!='single') and (mode!='continuous') and (mode!='integrator')):
            raise TypeError('must be a string (str) in single, continuous and integrator')
        self.name = mode
        self.specification()
    def specification(self,sample_time= 1,time = 10):
        """:sample_time: *int*, sample time in secondes (continuous mode) \n 
        :time: *int*, time in secondes (continuous and integrator mode) \n
        defines time and sample time which will be use if necessary 
        :return: *None
        \n*"""
        self.sample_time = sample_time
        self.time = time
        return 
    def __str__(self):
        return f"<{self.name}>"
    def __repr__(self):
        return self.name