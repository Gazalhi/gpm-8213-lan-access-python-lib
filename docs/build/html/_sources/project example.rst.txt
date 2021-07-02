Project Example
======================================

Import
------

::
	from GPM8213LAN import instrument,measurement,variable
	


Mesure all variable of one GPM
------------------------------ 

Code to measure a single time ::

	GPM_1 = instrument.Instrument("ip address",pattern=4)
	inst = measurement.Measurement(instruments=[GPM_1,GPM_2])
	data =inst()
	print(data)
	GPM_1.__del__() 

or ::
	
	GPM_1 = instrument.Instrument("ip address",pattern=4)
	data = GPM_1.mesure_variable()
	print(data)
	GPM_1.close_connection()





Mesure all variable of multiple GPM
-----------------------------------

Code to measure a single time ::

	GPM_1 = instrument.Instrument("138.231.71.232",pattern=4)
	GPM_2 = instrument.Instrument("138.231.71.233",pattern=4)
	inst = measurement.Measurement(instruments=[GPM_1,GPM_2])
	data =inst()
	print(data)
	GPM_1.__del__() 
	GPM_2.__del__()
