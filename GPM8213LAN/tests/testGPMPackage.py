# -*- coding: utf-8 -*-
"""
test GPM-package

@author: Hugo_MILAN
"""
# from GPM8213LAN import instrument,measurement

import GPM8213LAN.instrument as gpm
variable_available =['U', 'I', 'P', 'S', 'Q', 'LAMB', 'PHI', 'FU', 'FI', 'UPPeak', 'UMPeak', 'IPPeak', 'IMPeak', 'TIME', 'WH', 'WHP', 'WHM', 'AH', 'AHP', 'AHM', 'PPPeak', 'PMPeak', 'CFU', 'CFI', 'UTHD', 'ITHD', 'URANge', 'IRANge']
GPM_1 = gpm.Instrument("138.231.71.232",pattern=4)
GPM_2 = gpm.Instrument("138.231.71.233",pattern=4)
inst = gpm.Measurement(instruments=[GPM_1,GPM_2])
data =inst()
print(data)
GPM_1.__del__()
GPM_2.__del__()
# GPM_1 = Instrument("138.231.71.232",variables=variable_available)
# print(GPM_1.mesure_variable())