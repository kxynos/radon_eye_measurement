# Radon Eye Measurement script

Radon FTLab have created a detector of radon in the air. The model RD200 [http://radonftlab.com/radon-sensor-product/radon-detector/rd200/](http://radonftlab.com/radon-sensor-product/radon-detector/rd200/) has bluetooth capability and an application that communicates with it. It is possible to communicate with it with any bluetooth enabled device. 

It is possible to communicate with the device via bluetooth and the following GATT services:
```
UUID_CONTROL = "00001524-1212-EFDE-1523-785FEABCD123"
```
```
UUID_MEASUREMENT = "00001525-1212-EFDE-1523-785FEABCD123"
```

All you have to do is write ```0x51``` to the ```UUID_CONTROL``` service and you will get a measurement by reading GATT ```UUID_MEASUREMENT```.

The data that is returned is in the following format:

|Offset|length|Description|
|---|---|---|
|0x0|0x1 | command | 
|0x1|0x1 | message total length| 
|0x2| message total length - 2 | message body|

If the command is ```0x51``` then the message body is a float (4 bytes). The measurement is then a calculated by multiplying the reading by 37. 

The script I provide makes use of the ```bleak``` and ```construct``` Python libraries.

