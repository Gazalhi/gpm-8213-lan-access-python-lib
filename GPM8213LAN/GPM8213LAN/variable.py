# -*- coding: utf-8 -*-
"""
`GPM8213LAN.variable` implements the following classes:
    
:Variable: variable which GPM-8213 can measure

"""
def variable_available():
    """:return: *list of str*, all function of GPM-8213
        \n"""
    return ['U', 'I', 'P', 'S', 'Q', 'LAMB', 'PHI', 'FU', 'FI', 'UPPeak', 'UMPeak', 'IPPeak', 'IMPeak', 'TIME', 'WH', 'WHP', 'WHM', 'AH', 'AHP', 'AHM', 'PPPeak', 'PMPeak', 'CFU', 'CFI', 'UTHD', 'ITHD', 'URANge', 'IRANge']

class Variable():
    """:function: *str* in variable_available
    Function to display, to find the list go to page 76 and 77 in user manual
    see `variable_available` to see variable of GPM-8213
        \n"""
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
    
    

