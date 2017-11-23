#!/bin/bash
pushd /home/pi/

if [ ! -d ".uaeconfigmaker" ]; then
	wget https://github.com/HoraceAndTheSpider/UAEConfigMaker/archive/master.zip
	unzip master.zip
	rm master.zip
	mv UAEConfigMaker-master .uaeconfigmaker
fi
	
	cd .uaeconfigmaker

	sudo python3 update_config_maker.py
     	sudo python3 uae_config_maker.py --force-config-overwrite --whdload-update --create-autostartup
	sudo chown -hR pi:pi /home/pi/RetroPie/roms/amiga-data
popd
