# Microfluidic Sample Loader for the Elveflow System
![](https://i.imgur.com/TyRVHWe.jpg)
This repository allows the user to simultaneously control the OB1 MK3+ Flow Controller (equipped with a flow sensor) and the MUX Distributor 12 with Python. The code was based on the Elveflow SDK and utilizes the Python64 software library to control both instruments. The intent behind this code is to provide users with some extra functionality not included in the Elveflow Smart Interface, such as:
* Pausing for an indefinite amount of time between steps in a sequence.
* Controlling flow by measuring volume passed, rather than relying on inconsistent pressure sensor/flow sensor controls.  
* Reliable initialization of instruments, this is ocassionally an issue when attempting to control the MUX Distributor with the Elveflow Smart Interface. 

It is highly recommended to read the Elveflow SDK User Guide before running the example file. The guide is included as part of the SDK download, and includes information on adding sensors to instruments and ensuring that instruments are connected to your computer through NI MAX. 
