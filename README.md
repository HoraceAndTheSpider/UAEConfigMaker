# UAEConfigMaker

Amiga UAE Configuration Maker, primarily for UAE4ARM/Amiberry on the Raspberry Pi. 

Concept by HoraceAndTheSpider (Dom Cresswell)
Additions by Olly Ainger (oainger) and Chris Dyken (cdyk)

This program can be used to build .uae config files for UAE4Arm/Amiberry from a template file.

Pre-defined paths are 'scanned' and various scanning modes used to recognise different file setups.
- WHDLoad folder mode
- WHDLoad .zip mode
- CD32 ISO/CUE mode
- HDF mode

Specific settings can be applied to games, by including the scanned folder/file for the game in one of the many Settings/ text files.


## Command Line Options

* **[none]**  
  * *Specify any paths which are wanted to be scanned.*
  	* *Defaults to /home/pi/RetroPie/roms/amiga-data/ if not stated.*

* **--outputdir -o**
  * *Specify which path the .uae files are to be outputted to*
  	* *Defaults to /home/pi/RetroPie/roms/amiga/ if not stated.*
  	
  
* **--no-update -n**
  * *stop config maker from downloading the text data from github (for development purposes)*


* **--force-pi-paths**
  * *forces input paths to be made into '/home/pi/RetroPie/roms/amiga-data/' within .uae file regardless of source.*
  	* *Defaults to using actual path*
  

* **--force-config-overwrite**
	* *don't wait for user input before wiping all Config Files with new ones. This may be used for integration with RetroPie*
  
  
## Installation
  
  https://www.facebook.com/groups/1854320841462593?view=permalink&id=1940407532853923
  
From Linux Command Line or via SSH, use the following:

### Install/ Running
```bash
cd /home/pi
wget https://github.com/HoraceAndTheSpider/UAEConfigMaker/archive/master.zip
unzip master.zip
rm master.zip
mv UAEConfigMaker-master .uaeconfigmaker
```

### Updating/Running:
```bash
cd /home/pi
cd .uaeconfigmaker
python3 update_config_maker.py
python3 uae_config_maker.py 
```
