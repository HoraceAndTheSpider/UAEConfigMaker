# UAEConfigMaker (Version 2.3)

Amiga UAE Configuration Maker, primarily for UAE4ARM/Amiberry on the Raspberry Pi. 

Concept by HoraceAndTheSpider (Dom Cresswell)
Additions by Olly Ainger (oainger) and Chris Dyken (cdyk)

This program can be used to build .uae config files for UAE4Arm/Amiberry from a template file.

Pre-defined paths are 'scanned' and various scanning modes used to recognise different file setups.
- WHDLoad folder mode
- WHDLoad .zip mode
- WHDLoad HDF (data only) mode
- CD32 ISO/CUE mode
- Self-Booting HDF mode

Specific settings can be applied to games, by including the scanned folder/file for the game in one of the many Settings/ text files.

## A note on KickStart ROMs: 
The Generated UAE files assume that KickStart files are to be located in /home/pi/RetroPie/BIOS/Amiga  (be aware, this is case-sensitive) , and the minimum requirement is for an A1200 Kickstart 3.1 rom file to be located there as 'kick31.rom'.

CD32 KickStarts files are required for CD32 ISO/CUE scanning, and should be named cd32kick31.rom (main v3.1 KickStart) and cd32ext.rom (Extended Rom)

## Command Line Options

* **[none]**  
  * *Specify any paths which are wanted to be scanned.*
  	* *Defaults to /home/pi/RetroPie/roms/amiga-data/ if not stated.*

* **--outputdir -o**
  * *Specify which path the .uae files are to be outputted to*
  	* *Defaults to /home/pi/RetroPie/roms/amiga/ if not stated.*
  	
* **--no-update -n**
  * *stop config maker from downloading the text data from github (for development purposes)*

* **--ignore-output-path**
  * *Use input path as output location*
  
* **--force-pi-paths**
  * *forces input paths to be made into '/home/pi/RetroPie/roms/amiga-data/' within .uae file regardless of source.*
  	* *Defaults to using actual path*

* **--force-config-overwrite**
  * *don't wait for user input before wiping all Config Files with new ones. This may be used for integration with RetroPie*
  
* **--create-autostartup**
  * *Generate auto-startup script file for WHDLoad folders
  
## hostconfig.uaetemp Options
  
  The following options can be set in the file `hostconfig.uaetemp` and will be inherited by all generated configurations, and exist to be set by the user in order to tailor the generated .uae configurations to the user's requirements.
  
* **button_for_menu= [number]**
	* *Pick the input/controller button to enter the emulator (Amiberry) menu.*
	
* **button_for_quit= [number]**
	* *Pick the input/controller button to quit the emulator (Amiberry) back to RetroPie.*

* **key_for_menu= [number]**
	* *Pick the keyboard input to enter the emulator (Amiberry) menu.*

* **key_for_quit= [number]**
	* *Pick the keyboard input to quit the emulator (Amiberry) back to RetroPie.*

* **gfx_correct_aspect= [True / False]**
	* *Select whether the 4:3 aspect ratio is maintained with a screen size change.v

* **gfx_framerate= [0 / 1]**
	* *Select whether or not frameskip should be switched on (1) or off (0).*


## Installation
  
From Linux Command Line or via SSH, use the following:

### Install Direct
```bash
cd /home/pi
wget https://github.com/HoraceAndTheSpider/UAEConfigMaker/archive/master.zip
unzip master.zip
rm master.zip
mv UAEConfigMaker-master .uaeconfigmaker
```

### Alternative Install to the RetroPie Menu
```
cd /home/pi/RetroPie/retropiemenu/ 
wget http://www.ultimateamiga.co.uk/HostedProjects/RetroPieAmiga/downloads/UAE%20Config%20Maker.sh 
chmod +x "UAE Config Maker.sh"
```

### Updating/Running:
```bash
cd /home/pi
cd .uaeconfigmaker
python3 update_config_maker.py
python3 uae_config_maker.py 
```
