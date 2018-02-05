# UAEConfigMaker (Version 3.0)

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

* **--scandirs -s**  
  * *Specify any paths which are wanted to be scanned.*
  	* *Defaults to /home/pi/RetroPie/roms/amiga-data/ if not stated.*

* **--outputdir -o**
  * *Specify which path the .uae files are to be outputted to*
  	* *Defaults to /home/pi/RetroPie/roms/amiga/ if not stated.*
 
 * **--config-template -t**
   * *Specify which template .uae files should be used when generating the configs*
   * *The user can create their own choice of template in the folder `/templates/` usnig a plain text file labeled as X.uaetemp*
   	* *Defaults to amiberry format .uae file (amiberry.uaetemp) if not stated.*
 
* **--no-update -n**
  * *stop config maker from downloading the text data from github (for development purposes)*

* **--ignore-output-path**
  * *Use scanned input path as output location for saving of .uae files*
  
* **--force-paths**
  * *forces input paths to be made into a specific location within .uae file regardless of source location.*
  	* *If unspecified, defaults to using actual scan path*
  * * `--force-paths=pi` will shortcut to '/home/pi/RetroPie/roms/amiga-data/'
  * * `--force-paths=android` will shortcut to '/storage/emulated/0/roms/'

* **--rom-path**
  * *forces kickstart rom path to be made into a specific location within .uae file*
  	* *If unspecified, defaults to pi locationh*
  * * `--rom-path=pi` will shortcut to '/home/pi/RetroPie/BIOS/Amiga/'
  * * `--rom-path=android` will shortcut to 'storage/emulated/0/roms/kickstarts/'

* **--force-config-overwrite**
  * *don't wait for user input before wiping all Config Files with new ones. This may be used for integration with RetroPie*

* **--whdload-update**
  * *WHDLoad scanning will check for .slave files requiring update and provide message on game loading.
 
* **--create-autostartup**
  * *Generate auto-startup script file for WHDLoad folders
 
* **--no-filename-spaces**
  * *Spaces in file-names will be replaced with underscores to assist on Android systems.
  
   


## hostconfig.uaetemp Options
  
  The options which can be set in the file `hostconfig.uaetemp` and will be inherited by all generated configurations, and exist to be set by the user in order to tailor the generated .uae configurations to the user's requirements, are detailed in the following wiki page:

https://github.com/HoraceAndTheSpider/UAEConfigMaker/wiki/Settings:-Host-Options



* **no_update / ignore_output_path / force_paths / rom_path**
* ** / force_config_overwrite / whdload_update / create_autostartup / no_filename_spaces**

	* *These command-line options can also be entered into hostconfig and will take priority*

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
wget https://raw.githubusercontent.com/HoraceAndTheSpider/UAEConfigMaker/master/UAE%20Config%20Maker.sh
chmod +x "UAE Config Maker.sh"
```

### Updating/Running:
```bash
cd /home/pi
cd .uaeconfigmaker
python3 update_config_maker.py
python3 uae_config_maker.py 
```
