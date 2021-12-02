# Radon Eye Measurement script

Radon FTLab have created a detector of radon in the environment. The model RD200 [http://radonftlab.com/radon-sensor-product/radon-detector/rd200/](http://radonftlab.com/radon-sensor-product/radon-detector/rd200/) has bluetooth capability and an application that communicates with it. It is possible to communicate with it with any bluetooth enabled device. 

We are connecting to the following GATT service:

```
UUID_SERVICE = "00001523-1212-efde-1523-785feabcd123"
```

It is possible to communicate with the device via bluetooth and the following GATT characteristic UUIDs:

```
UUID_CONTROL = "00001524-1212-EFDE-1523-785FEABCD123"
```
```
UUID_MEASUREMENT = "00001525-1212-EFDE-1523-785FEABCD123"
```

All you have to do is write ```0x50``` to the ```UUID_CONTROL``` service and you will get a measurement by reading GATT ```UUID_MEASUREMENT```.

The data that is returned to ```UUID_MEASUREMENT``` is in the following format:

|Offset|length bytes|Description| Type |
|---|---|---|---| 
|0x0|1 | command |int| 
|0x1|1 | message total length| int|
|0x2|4 | current measurement| float|
|0x6|4 | average day measurement| float|
|0xA|4 | average month measurement| float|
|0xE|2 | pulse | int |
|0x10|2 | pulse 10 min| int |

The command should read ```0x50``` (this is now the reply to the command ```0x50``` sent). So for example, the current measurement is a float (4 bytes). The currrent measurement is then calculated by multiplying the float reading by 37 (for Bq/m^3, which is what I have it set it).

I provide a 010 Editor Template [radon-measure.bt](radon-measure.bt)

## Example

Example reply data :

```50 10 71 3D 8A 3F 71 3D AA 3F E1 7A B4 3F 06 00```

|Offset|Value (hex)|Description| Type | Converted\* (Bq/m^3)|
|---|---|---|---|---| 
|0x0|50 | command |80 int| - |
|0x1|10 | message total length| 16 int|- |
|0x2|71 3D 8A 3F | current measurement| 1.08 float| 39.96|
|0x6|71 3D AA 3F| average day measurement| 1.33 float|49.21|
|0xA|E1 7A B4 3F | average month measurement| 1.41 float|52.17|
|0xE|06 | pulse | 6 int |-|
|0xF|00 | pulse 10 min| 0 int |-|

\* Keep in mind the device may round down or cut decimal points. 

## Python Script

The script I provide makes use of the ```bleak``` and ```construct``` Python libraries. Check the [requirements.txt](requirements.txt) file.

### How to get started:

```
$ git clone https://github.com/kxynos/radon_eye_measurement
$ cd radon_eye_measurement
$ virtualenv pyenv
$ source pyenv/bin/activate
(pyenv)$ pip3 install -r requirements.txt
(pyenv)$ python3 radon_eye_measurement.py

```
Scan mode (when ```get_device = True```, this is the default initial state of the script)

```
[+] Running scan
Address: Description
XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX: FR:R20:SNXXXX
```
Open ```radon_eye_measurement.py``` with your favourit editor and paste this value ```XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX``` into the variable ```address```. Look for the FR:R20:SNXXX string at the end of the each line; this is the device name(address)(ini MS Windows it will have a different format) and serial number (you can match it with the one on the device). Also set ```get_device = False``` (we don't need it anymore, you might need it again if you change devices or get another one).

Example changes to ```radon_eye_measurement.py``` to get it connecting to the RadonEye device:

```
def main():
    print_debug = False
    command_line = True
    get_device = False # can be True or False
    
    address = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" # copy the address here

```


