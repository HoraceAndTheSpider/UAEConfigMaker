import argparse
import glob
import math
import os
import shutil
import platform

from utils import general_utils
from utils import text_utils
from utils import update_utils
from utils.text_utils import FontColours
from whdload import whdload_slave


def value_list(in_file, game_name):
    file_name = "settings/" + in_file

    if os.path.isfile(file_name) is False:
        return 0

    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    f.close()

    answer = 0

    for this_line in content:
        if not this_line == "":
            this_word = this_line.split()
            if this_word[0] == game_name:
                answer = this_word[1]
                break

    return answer


def check_list(in_file, game_name):

    temp_game = game_name

    if text_utils.right(temp_game.lower(),4) == ".iso" or text_utils.right(temp_game.lower(),4) == ".cue":
        temp_game = text_utils.left(temp_game,len(temp_game)-4)
        
    if text_utils.right(temp_game.lower(),4) == ".adf" or text_utils.right(temp_game.lower(),4) == ".hdf":
        temp_game = text_utils.left(temp_game,len(temp_game)-4)


    
    file_name = "settings/" + in_file

    if os.path.isfile(file_name) is False:
        return False

    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    f.close()

    answer = False

    for this_line in content:
        if this_line == temp_game:
            answer = True
            break

    return answer


def find_host_option(in_option):
    file_name = "hostconfig.uaetemp"

    if os.path.isfile(file_name) is False:
        return ""

    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    f.close()

    answer = ""

    for this_line in content:
        if text_utils.left(this_line, len(in_option)) == in_option:
            answer = this_line.replace(in_option, "")
            answer = answer.replace("=", "").strip()
            break

    return answer


def do_scan(input_directory, pathname,output_directory):
    if os.path.isdir(input_directory + pathname):
        print("Config Save Path: " + FontColours.OKBLUE + output_directory + FontColours.ENDC)
        print("Games Files Path: " + FontColours.BOLD + FontColours.OKBLUE + pathname + FontColours.ENDC)
        print()
    else:
        print(
            "Specified Scan path " + FontColours.FAIL + input_directory + pathname + FontColours.ENDC +
            " does not exist")
        return

    # what type of scan is it  --  default , WHDLOAD folder
    if pathname.find("WHDLoad") > -1 and pathname.find("_HDF") > -1:
        scan_mode = "WHDLoadHDF"
        hdsettings = ",0"

    elif pathname.find("WHDLoad") > -1:
        scan_mode = "WHDLoad"
        hdsettings = ",0"

    elif pathname.find("_HDF") > -1:
        scan_mode = "HDF"
        hdsettings = ",32,1,2,512,50,,uae"

##    elif pathname.lower().find(".hdf") > -1:
##        scan_mode = "HDF"
##        hdsettings = ",32,1,2,512,50,,uae"

    elif pathname.lower().find("_ADF") > -1:
        scan_mode = "ADF"

    elif pathname.lower().find("cd32") > -1:
        scan_mode = "CD32"

    elif pathname.lower().find("cdtv") > -1:
        scan_mode = "CD32"

    else:
        scan_mode = "WHDLoad"
        hdsettings = ",0"

    print("Scan Mode: " + FontColours.BOLD + FontColours.HEADER + scan_mode + FontColours.ENDC)
    print()
    the_filter = ""
    count = 1
    skip_all = 0

    # VARIOUS SETTINGS FROM HOST CONFIG ONLY
    #
    # command line forcing of overwrite of files
    if FORCE_OVERWRITE is True:
        skip_all = 1

#    quit_button = find_host_option("button_for_quit")#
#    menu_button = find_host_option("button_for_menu")
    quit_key = find_host_option("key_for_quit")
    menu_key = find_host_option("key_for_menu")
    
#    if quit_button == "":
#        quit_button = -1

#    if menu_button == "":
#        menu_button = -1

    if quit_key == "":
        quit_key = 0

    if menu_key == "":
        menu_key = 293


    # sort out the input items
    input_1 = find_host_option("controller_1")
    input_2 = find_host_option("controller_2")
    input_3 = find_host_option("controller_3")
    input_4 = find_host_option("controller_4")
    
    if input_1 == "":
        input_1 = "joy1"

    if input_2 == "":
        input_2 = "joy2"
        
    if input_3 == "":
        input_3 = "None"
        
    if input_4 == "":
        input_4 = "None"

    deadzone = find_host_option("joymouse_deadzone")
    if deadzone == "":
        deadzone = "33"

    stereo_seperation = find_host_option("stereo_seperation")
    if stereo_seperation == "":
        stereo_seperation = "7"


    # retroarch toggles
    
    retroarch_quit = find_host_option("retroarch_quit")
    retroarch_menu = find_host_option("retroarch_menu")
    retroarch_reset = find_host_option("retroarch_reset")

    if retroarch_quit == "":
        retroarch_quit = "True"
    if retroarch_menu == "":
        retroarch_menu = "True"
    if retroarch_reset == "":
        retroarch_reset = "False"



    
    # cycle through all folders / files
    for file in glob.glob(input_directory + pathname + "/*"):

        # remove the long filepath 
        this_file = os.path.basename(file)

        # Set criteria for each scan type
        scan_pass = False

        # WHDLOAD scanmode needs folders, mostly
        if (scan_mode == "WHDLoad" and os.path.isdir(file) is True):
            scan_pass = True
            
        # WHDLOAD scanmode will accept .zip
        if (scan_mode == "WHDLoad" and os.path.isfile(file) is True
            and text_utils.right(this_file.lower(), 4) == ".zip"):
            scan_pass = True

        # WHDLOAD HDF scanmode must have file extension as .hdf
        if (scan_mode == "WHDLoadHDF" and os.path.isfile(file) is True
            and text_utils.right(this_file.lower(), 4) == ".hdf"):
            scan_pass = True
                               
        # HDF scanmode must have file extension as .hdf
        if (scan_mode == "HDF" and os.path.isfile(file) is True
            and text_utils.right(this_file.lower(), 4) == ".hdf"):
            scan_pass = True

        # CD32 scanmode can have file extension as .iso
        if (scan_mode == "CD32" and os.path.isfile(file) is True
            and text_utils.right(this_file.lower(), 4) == ".iso"):
            scan_pass = True

        # CD32 folders need sub file with extension as .cue
        if (scan_mode == "CD32" and os.path.isdir(file) is True
            and os.path.isfile(file + "/" + this_file + ".cue") is True):
            scan_pass = True

        # name filter applies
        if the_filter != '' and this_file.find(the_filter) < 0:
            pass

        # we passed the 'type' scan
        elif scan_pass is True:
            # horrible work around for annoying game name
            temp_name = this_file.replace("R³sselsheim", "Russelsheim")
            print(FontColours.OKBLUE + str(count) + FontColours.ENDC +
                  ": Processing Game: " + FontColours.BOLD + temp_name + FontColours.ENDC)

            if this_file.lower().endswith(".zip"):
                this_file = text_utils.left(this_file, len(this_file) - 4)

            # standard 'expand name' for WHDLoad folders
            if scan_mode == "WHDLoad":
                full_game_name = text_utils.make_full_name(this_file)

            # standard 'expand name' for WHDLoad folders
            if scan_mode == "WHDLoadHDF":

               full_game_name = text_utils.make_full_name(text_utils.left(this_file, len(this_file) - 4))
               full_game_name = full_game_name + " [WHDLoad HDF]"
               
            # there is an alternative name changing for TOSEC CD32 images....
            elif scan_mode == "CD32":
                full_game_name = text_utils.make_full_cd32_name(this_file)

            # stock name for HDF files
            elif scan_mode == "HDF":
                if this_file.lower().endswith(".hdf"):
                    full_game_name = text_utils.left(this_file, len(this_file) - 4)

            # there will probably an alternative name changing for TOSEC ADF files if we ever add it....
            elif scan_mode == "ADF":
                continue

            # DISPLAY!
            print()
            print("     Full Name: " + FontColours.OKGREEN + full_game_name + FontColours.ENDC)

            # normal method for machine selection
            if full_game_name.find("AGA") > -1:
                machine_type = "A1200/020"

            elif scan_mode == "CD32":
                machine_type = "CD32"
                
                if full_game_name.find(" [CD32]")<0:
                        full_game_name += " [CD32] [ISO]"

            elif full_game_name.find("AGA") > -1:
                machine_type = "A1200/020"
                
            elif scan_mode == "WHDLoad" and full_game_name.find("CD32") > -1:
                machine_type = "A1200/020"
                
            else:
                machine_type = "A600+"

            # check if config already exists - yes/no to overwrite
            create_config = True
            answer = ""

            # create the full name of output file
            if NO_FILENAME_SPACES == False:                    
                config_file = output_directory + full_game_name + ".uae"
            else:
                config_file = output_directory + full_game_name.replace(" ","_") + ".uae"
                    

            if os.path.isfile(config_file) == True and skip_all == 0:
                while answer != "Y" and answer != "N" and answer != "S" and answer != "A":
                    answer = input(
                        FontColours.OKBLUE + "     Config already exists - overwrite? " + "(Yes/No/Always/Skip) "
                        + FontColours.ENDC)
                    if answer == "a" or answer == "s" or answer == "n" or answer == "y":
                        answer = answer.upper()
                    print()

            elif os.path.isfile(config_file) == True and skip_all == -1:
                create_config = False
                print(FontColours.OKBLUE + "     Skipping existing file." + FontColours.ENDC)
                print()

            # process the answers
            if answer == "N":
                create_config = False

            elif answer == "Y":
                create_config = True

            elif answer == "A":
                skip_all = 1

            elif answer == "S":
                skip_all = -1
                create_config = False 

            # what to do 'automatically'
            if skip_all == 1:
                create_config = True

            # this is where we start the code to actually build the config with changes
            if create_config is True:

                # lets do some work, based on what slave files we find.
# ===================                

                whd_chip_ram = 0
                whd_fast_ram = 0
                whd_aga = False
                whd_020 = False
                whd_cd32 = False
                whd_kicks = ['']
                
                whd_longname = ""
                whd_realname = ""
                whd_infoname = ""
                whd_date = None
                whd_page = ""
               
               # note that this *only* works with WHDLoad folder scanning.
                if scan_mode == "WHDLoad" and WHDLOAD_UPDATE==True:
                    
                    whd_update_message = ""
                    for slave_file in glob.glob(file + "/*"):
                        if slave_file.lower().endswith(".slave"):
                        
                            this_slave = whdload_slave.whdload_factory(slave_file)
                            # print (this_slave.name)
                            
                            # minimum chip ram
                            round_up = int(this_slave.base_mem_size/524288) + (this_slave.base_mem_size % 524288 > 0)
                            if round_up >= whd_chip_ram:
                                whd_chip_ram = round_up

                            if whd_chip_ram > 4:
                                whd_chip_ram = 4

                            # minimum fast ram
                            round_up = int(this_slave.exp_mem/1048576) + (this_slave.exp_mem % 1048576 >0)
                            if round_up >= whd_fast_ram: whd_fast_ram = round_up

                            # AGA needed
                            if this_slave.requires_aga == True: whd_aga = True

                            # 020 needed
                            if this_slave.requires_68020 == True: whd_020 = True

                            # CD32 controls patch is available
                            if this_slave.has_cd32_controls_patch == True: whd_cd32 = True

                            # Kickstarts (files needed to be checked in _BootWHD/devs/kickstarts
                            # and a warning produced if not present.
                            # put on hold until bugfix implemented
                            # (this_slave.kickstart_name)


                            # created date for slave will be needed for updates                            
                            # whd_dated = this_slave.created_timex
                            whd_longname = slave_file
                            whd_realname = os.path.basename(slave_file)


                            # +++ Lets scan for updates shall we? +++

                            # first, we'll find the WHDLoad web-page from the list
                            whd_page = text_utils.get_whdload_page(whd_realname)

#                             print(whd_realname + " === " + str(whd_infoname) + " === " + whd_page)

                            if whd_page == "":
                                whd_update_message += whd_realname + " not found on master WHDLoad page list."  + chr(10) + "UAE Config Maker could not verify slave updates." + chr(10)
                                print ("     Slave file: " + FontColours.OKBLUE + whd_realname + FontColours.ENDC + " not found on master WHDLoad page list." + chr(10))
                                break
                            
                            # here's where we start checking again the WHDload page (OLLY!!!)

 #                           print("whd page:" + whd_page)
                            
                            have_found_slave = False

                            web_slaves = whdload_slave.whdload_factory(whd_page) 
                            
                            if isinstance(web_slaves,list):
                                for web_slave in web_slaves:
                                    if web_slave.name == this_slave.name:
                                        have_found_slave = True
                                        break
                            else:
                                web_slave = web_slaves 
                                if web_slave.name == this_slave.name:
                                    have_found_slave = True

                            
                            if have_found_slave == True and web_slave.modified_time.date() > this_slave.modified_time.date():
                                print()
                                print("     Slave file: " + FontColours.OKBLUE + whd_realname + FontColours.ENDC + " is an older version.")
                                print("     This version: " + FontColours.FAIL + str(this_slave.modified_time) + FontColours.ENDC
                                                            + "  New Version: " +  FontColours.OKGREEN + str(web_slave.modified_time) + FontColours.ENDC)
                                print()

                                whd_update_message = whd_update_message + "     Slave file:  " + whd_realname + " is an older version." + chr(10) + chr(10)
                                whd_update_message = whd_update_message + "     This version: " + str(this_slave.modified_time) + "" + chr(10)
                                whd_update_message = whd_update_message + "     Detected Version: " +str(web_slave.modified_time) + "" + chr(10)
                                # delete old slave

                                # copy in new slave

                                # delete auto-startup (if included)


                    # web_slaveslave loop is finished
                    if whd_update_message !="":
                        text_file = open(file + "/whdupdate_message", "w+")
                        text_file.write(whd_update_message)
                        text_file.close()
                        print()
                        #print("     "+whd_update_message)                                            
                        #continue
                            
# ===================
                
                #  check other parameters
                #  hardware options

                # ======== SYSTEM HARDWARE =======
                #  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # override the machine type, if on a list
                if check_list("System_A500.txt", this_file) is True:
                    machine_type = "A500"
                elif check_list("System_A1200.txt", this_file) is True:
                    machine_type = "A1200/020"
                elif check_list("System_A4000.txt", this_file) is True:
                    machine_type = "A4000/040"
                elif check_list("System_CD32.txt", this_file) is True:
                    machine_type = "CD32"

                # PRESETS:  CPU / chipset/ kickstart

                # WHD overrides are easier if we look at a base machine type                
                if whd_020 is True and machine_type == "A500":
                    machine_type = "A600+"

                if whd_aga is True and (machine_type == "A500" or machine_type == "A600+"):
                    machine_type = "A1200/020"

                # TODO: Convert settings to a dictionary or object ... yeah.... i'll leave this to you ;)
                z3_ram = 0
                if machine_type == "A500":
                    chipset = "OCS"
                    a_cpu = "68000"
                    kickstart = "kick13.rom"
                    kickstart_ext = ""
                    fast_ram = 0
                    chip_ram = 1
                    clock_speed = 0

                elif machine_type == "A600+" or machine_type == "":
                    chipset = "ECS_Agnus"
                    a_cpu = "68020"
                    kickstart = "kick31.rom"
                    kickstart_ext = ""
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 0

                elif machine_type == "A1200":
                    chipset = "AGA"
                    a_cpu = "68ec020"
                    kickstart = "kick30.rom"
                    kickstart_ext = ""
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 14

                elif machine_type == "A1200/020":
                    chipset = "AGA"
                    a_cpu = "68020"
                    kickstart = "kick31.rom"
                    kickstart_ext = ""
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 14

                elif machine_type == "A4000":
                    chipset = "AGA"
                    a_cpu = "68040"
                    kickstart = "kick31.rom"
                    kickstart_ext = ""
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 28

                elif machine_type == "CD32":
                    chipset = "AGA"
                    a_cpu = "68ec020"
                    kickstart = "cd32kick31.rom"
                    kickstart_ext = "cd32ext.rom"
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 14

                elif machine_type == "A1200/32":
                    chipset = "AGA"
                    a_cpu = "68ec020"
                    kickstart = "cd32kick31.rom"
                    kickstart_ext = "cd32ext.rom"
                    chip_ram = 4
                    fast_ram = 8
                    clock_speed = 14

                # '======== MEMORY SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' when we want different chip ram!!

                old_chip_ram = chip_ram
                for i in range(0, 4):
                    chip_ram = int(math.pow(2, i)) / 2
                    if chip_ram >= 1:
                        chip_ram = int(chip_ram)

                    if check_list("Memory_ChipRam_" + str(chip_ram) + ".txt", this_file) is True:
                        chip_ram = int(chip_ram * 2)
                        break
                    chip_ram = old_chip_ram

                # whd chip-memory overwrite
                if whd_chip_ram >= chip_ram: chip_ram = whd_chip_ram

                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' when we want different fast ram!!

                old_fast_ram = fast_ram
                for i in range(0, 4):
                    fast_ram = int(math.pow(2, i))
                    if check_list("Memory_FastRam_" + str(fast_ram) + ".txt", this_file) is True:
                        break
                    fast_ram = old_fast_ram

                # whd fast-memory overwrite
                if whd_fast_ram >= fast_ram and whd_fast_ram <= 8 : fast_ram = whd_fast_ram


                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' when we want different Z3 ram!!

                for i in range(0, 8):
                    z3_ram = int(math.pow(2, i))
                    if check_list("Memory_Z3Ram_" + str(z3_ram) + ".txt", this_file) is True:
                        break
                    z3_ram = 0

                # whd z3-memory overwrite
                if whd_fast_ram >= z3_ram and whd_fast_ram > 8 : z3_ram = whd_chip_ram
                

                # '======== CHIPSET SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' sprite collisions

                sprite_collisions = "playfields"

                if check_list("Chipset_CollisionLevel_playfields.txt", this_file) is True:
                    sprite_collisions = "playfields"
                if check_list("Chipset_CollisionLevel_none.txt", this_file) is True:
                    sprite_collisions = "none"
                if check_list("Chipset_CollisionLevel_sprites.txt", this_file) is True:
                    sprite_collisions = "sprites"
                if check_list("Chipset_CollisionLevel_full.txt", this_file) is True:
                    sprite_collisions = "full"

                # ' imm. blits & fast copper

                fast_copper = not check_list("Chipset_NoFastCopper.txt", this_file)
                immediate_blits = check_list("Chipset_ImmediateBlitter.txt", this_file)

                # '======== CPU SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # ' max emu speed
                a_cpu_speed = "real"
                if check_list("CPU_MaxSpeed.txt", this_file) is True:
                    a_cpu_speed = "max"

                # ' clock speed
                if check_list("CPU_ClockSpeed_7.txt", this_file) is True:
                    clock_speed = 7
                if check_list("CPU_ClockSpeed_14.txt", this_file) is True:
                    clock_speed = 14
                if check_list("CPU_ClockSpeed_28.txt", this_file) is True:
                    clock_speed = 28

                # ' cpu model 040
                if check_list("CPU_040.txt", this_file) is True:
                    a_cpu = "68040"
                    _24_bit_address = False

                # ' 24 bit addressing / compatible CPU / JIT Cache
                _24_bit_address = not check_list("CPU_No24BitAddress.txt", this_file)
                compatible_cpu = check_list("CPU_Compatible.txt", this_file)
                cycle_exact = check_list("CPU_CycleExact.txt", this_file)

                use_jit = False
                if ChexList("CPU_ForceJIT.txt",this_file) == True:
                        use_jit = True
                else if check_list("CPU_NoJIT.txt", this_file) == False:
                        use_jit = False

                # '======== DISPLAY SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' screen Y/X Offsets

                screen_offset_y = value_list("Screen_OffsetY.txt", this_file)
                #for Z in range(-16, 16):
                #    if check_list("Screen_OffsetY_" + str(Z) + ".txt", this_file) is True:
                #        screen_offset_y = Z

                screen_offset_x = value_list("Screen_OffsetX.txt", this_file)
                #for Z in range(-16, 16):
                #    if check_list("Screen_OffsetX_" + str(Z) + ".txt", this_file) is True:
                #        screen_offset_x = Z

                # ' screen heights
                screen_height = 240
                if check_list("Screen_Height_270.txt", this_file) is True:
                    screen_height = 270
                if check_list("Screen_Height_262.txt", this_file) is True:
                    screen_height = 262
                if check_list("Screen_Height_256.txt", this_file) is True:
                    screen_height = 256
                if check_list("Screen_Height_240.txt", this_file) is True:
                    screen_height = 240
                if check_list("Screen_Height_224.txt", this_file) is True:
                    screen_height = 224
                if check_list("Screen_Height_216.txt", this_file) is True:
                    screen_height = 216
                if check_list("Screen_Height_200.txt", this_file) is True:
                    screen_height = 200

                # ' screen widths
                screen_width = 640
                if check_list("Screen_Width_384.txt", this_file) is True:
                    screen_width = 384
                if check_list("Screen_Width_352.txt", this_file) is True:
                    screen_width = 352
                if check_list("Screen_Width_320.txt", this_file) is True:
                    screen_width = 320
                if check_list("Screen_Width_768.txt", this_file) is True:
                    screen_width = 768
                if check_list("Screen_Width_704.txt", this_file) is True:
                    screen_width = 704
                if check_list("Screen_Width_640.txt", this_file) is True:
                    screen_width = 640

                # ' extras
                aspect_ratio = bool(check_list("Screen_Force43Aspect.txt", this_file))
                if find_host_option("gfx_correct_aspect") != "":
                    aspect_ratio = find_host_option("gfx_correct_aspect")

                use_frameskip = 0
                if find_host_option("gfx_framerate") != "":
                    use_frameskip = find_host_option("gfx_framerate")

                use_ntsc = check_list("Screen_ForceNTSC.txt", this_file)

                # '======== CONTROL SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' mouse / mouse 2 / CD32

                use_mouse1 = check_list("Control_Port0_Mouse.txt", this_file)
                use_mouse2 = check_list("Control_Port1_Mouse.txt", this_file)
                use_cd32_pad = check_list("Control_CD32.txt", this_file)

                if scan_mode == "CD32" or full_game_name.lower().find("[cd32]") > -1:
                    use_cd32_pad = True

                # '======== MISC SETTINGS =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' BSD Socket / Floppy Speed etc

                use_bsd_socket = check_list("Misc_BSDSocket.txt", this_file)
                floppy_speed = 400
                disk = ["", "", "", ""]

                if check_list("Floppy_Speed_100.txt", this_file) is True:
                    floppy_speed = 100
                if check_list("Floppy_Speed_200.txt", this_file) is True:
                    floppy_speed = 200
                if check_list("Floppy_Speed_400.txt", this_file) is True:
                    floppy_speed = 400
                if check_list("Floppy_Speed_800.txt", this_file) is True:
                    floppy_speed = 800

                # '======== SETUP CONFIG =======
                # ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # ' ....

                # print("we are making a config ....")
      
                shutil.copyfile("uaeconfig.uaetemp", config_file)

                if os.path.isfile(config_file) is False:
                    print(FontColours.FAIL + "Error creating config." + FontColours.ENDC)
                else:
                    print("     Editing File: " + FontColours.HEADER + config_file + FontColours.ENDC)

                    # put the text from the file into a string
                    text_file = open(config_file, "r")
                    config_text = text_file.read()
                    text_file.close()

                    # all the major find/replaces from below....

                    # I needed an "override" option
                    #    to force //home/pi/RetroPie/roms/amiga/ on
                    #      external machines (allowing WHD packs to be created on external machines)

                    if FORCE_PATHS.lower() == "pi":
                        config_text = config_text.replace("<<inputdir>>", "/home/pi/RetroPie/roms/amiga-data/")
                        
                    elif FORCE_PATHS.lower()  == "android":
                        config_text = config_text.replace("<<inputdir>>", "/storage/emulated/0/roms/")
                        
                    elif FORCE_PATHS != "":
                        config_text = config_text.replace("<<inputdir>>", FORCE_PATHS)
                        
                    else:
                        config_text = config_text.replace("<<inputdir>>", input_directory)

                    # do somthing almost the same, for rom/kickpath
                    if ROM_PATH.lower() == "pi":
                        config_text = config_text.replace("<<romdir>>", "/home/pi/RetroPie/BIOS/Amiga/")

                    elif ROM_PATH.lower()  == "android":
                        config_text = config_text.replace("<<romdir>>", "/storage/emulated/0/roms/kickstarts/")

                    else:
                        config_text = config_text.replace("<<romdir>>", ROM_PATH)
                        

                    # game / path
                    config_text = config_text.replace("<<game>>", this_file)

                    config_text = config_text.replace("<<fullgame>>", full_game_name)
                    config_text = config_text.replace("<<hdpath>>", pathname)
 #                   config_text = config_text.replace("<<quitbutton>>", str(quit_button))
#                    config_text = config_text.replace("<<menubutton>>", str(menu_button))

                    config_text = config_text.replace("<<retroarch_quit>>", str(retroarch_quit))
                    config_text = config_text.replace("<<retroarch_menu>>", str(retroarch_menu))
                    config_text = config_text.replace("<<retroarch_reset>>", str(retroarch_reset))

                    config_text = config_text.replace("<<quitkey>>", str(quit_key))
                    config_text = config_text.replace("<<menukey>>", str(menu_key))

                    # screens
                    config_text = config_text.replace("<<screenheight>>", str(screen_height))
                    if screen_width < 320:
                        screen_width == 640
                    config_text = config_text.replace("<<screenwidth>>", str(screen_width))
                    config_text = config_text.replace("<<offset_y>>", str(screen_offset_y))
                    config_text = config_text.replace("<<offset_x>>", str(screen_offset_x))
                    config_text = config_text.replace("<<43aspect>>", str(aspect_ratio))
                    config_text = config_text.replace("<<frameskip>>", str(use_frameskip))                 
                    config_text = config_text.replace("<<ntsc>>", str(bool(0 - use_ntsc)))

                    # memory
                    config_text = config_text.replace("<<chipmem>>", str(chip_ram))
                    config_text = config_text.replace("<<fastmem>>", str(fast_ram))
                    config_text = config_text.replace("<<z3mem>>", str(z3_ram))

                    if z3_ram > 0 and (a_cpu != "68020" and a_cpu != "68040"):
                        a_cpu = "68020"

                    # chipset
                    config_text = config_text.replace("<<chipset>>", chipset)
                    config_text = config_text.replace("<<spritecollision>>", sprite_collisions)
                    config_text = config_text.replace("<<fastcopper>>", str(bool(0 - fast_copper)))
                    config_text = config_text.replace("<<immediateblitter>>", str(bool(0 - immediate_blits)))

                    # cpu
                    if a_cpu_speed == "max":
                        config_text = config_text.replace("finegrain_cpu_speed=", ";finegrain_cpu_speed=")
                    else:
                        if clock_speed == 14:
                            clock_speed = 1024
                        elif clock_speed == 28:
                            clock_speed = 128
                        else:
                            clock_speed = 0

                    config_text = config_text.replace("<<kickstart>>", kickstart)
                    config_text = config_text.replace("<<extkickstart>>", kickstart_ext)
                    config_text = config_text.replace("<<cputype>>", a_cpu)
                    config_text = config_text.replace("<<cpuspeed>>", a_cpu_speed)
                    if a_cpu_speed == "real":
                        config_text = config_text.replace("cpu_speed=real", ";cpu_speed=real")                        

                    config_text = config_text.replace("<<clockspeed>>", str(clock_speed))
                    config_text = config_text.replace("<<cpucompatible>>", str(bool(0 - compatible_cpu)))
                    config_text = config_text.replace("<<cycleexact>>", str(bool(0 - cycle_exact)))
                    config_text = config_text.replace("<<24bitaddress>>", str(bool(0 - _24_bit_address)))
                    if use_jit is False:
                        config_text = config_text.replace("<<jitcache>>", "0")
                    else:
                        config_text = config_text.replace("<<jitcache>>", "8192")

                    # misc
                    config_text = config_text.replace("<<bsdsocket>>", str(bool(0 - use_bsd_socket)))

                    # hard disk files

                    disk_nr = 0
                    if scan_mode == "HDF" and os.path.isfile(
                                            pathname + this_file.replace(".hdf", "") + "_savedisk.adf") is True:
                        disk_nr = 1
                        config_text = config_text.replace("<<diskpath0>>", pathname)
                        config_text = config_text.replace("<<disk0>>", this_file.replace(".hdf", "") + "_savedisk.adf")
                        config_text = config_text.replace("<<disktype0>>", "0")

                    if scan_mode == "HDF":

                        # remove the boot drive-system (folder) DH0:
                        config_text = config_text.replace("uaehf0=dir,rw,DH0:DH0:", ";uaehf0=dir,rw,DH0:DH0:")
                        config_text = config_text.replace("filesystem2=rw,DH0:DH0:", ";filesystem2=rw,DH0:DH0:")
                        
                        # remove the file-system (folder) DH1:
                        config_text = config_text.replace("uaehf1=dir,rw,DH1", ";uaehf1=dir,rw,DH1")
                        config_text = config_text.replace("filesystem2=rw,DH1", ";filesystem2=rw,DH1")

                        config_text = config_text.replace("uaehf1=hdf,rw,DH2", "uaehf0=hdf,rw,DH0")
                        config_text = config_text.replace("hardfile2=rw,DH2", "hardfile2=rw,DH0")                        
                        
                    # WHDLoad HDF scanning
                    elif scan_mode == "WHDLoadHDF":

                        # remove the file-system (folder) DH1:
                        config_text = config_text.replace("uaehf1=dir,rw,DH1", ";uaehf1=dir,rw,DH1")
                        config_text = config_text.replace("filesystem2=rw,DH1", ";filesystem2=rw,DH1")

                        # adjust parameters for DH2 to become DH1:
                        config_text = config_text.replace(",32,1,2,512,50,,uae", ",32,1,2,512,-50,,uae")
                        config_text = config_text.replace("uaehf1=hdf,rw,DH2:", "uaehf1=hdf,rw,DH1:")
                        config_text = config_text.replace("hardfile2=rw,DH2", "hardfile2=rw,DH1")
     
                    # disable the HDF parameter
                    else:
                        config_text = config_text.replace("hardfile2=", ";hardfile2=")
                        config_text = config_text.replace("uaehf1=hdf,rw,DH2:", ";uaehf1=hdf,rw,DH2:")

                    for i in range(disk_nr, 4):
                        config_text = config_text.replace("<<diskpath" + str(i) + ">>", pathname)
                        config_text = config_text.replace("<<disk" + str(i) + ">>", disk[i])

                        #print ("disk... "+disk[i])
                        if disk[i] == "":
                            disk_on = "0"
                        else:
                            disk_nr += 1
                            disk_on = "1"
                            config_text = config_text.replace(";floppy" + str(i), "floppy" + str(i))

                        config_text = config_text.replace("<<disktype" + str(i) + ">>", str(disk_on))
                        config_text = config_text.replace("<<floppyspeed>>", str(floppy_speed))
                        config_text = config_text.replace("<<totaldisks>>", str(disk_nr))

                    if machine_type == "CD32":
                        config_text = config_text.replace("uaehf1=", ";uaehf1=")
                        config_text = config_text.replace("uaehf0=", ";uaehf0=")
                        config_text = config_text.replace("filesystem2=", ";filesystem2=")
                        config_text = config_text.replace("hardfile2=", ";hardfile2=")
                        config_text = config_text.replace("<<cd32mode>>", "1")
                    else:
                        config_text = config_text.replace("<<cd32mode>>", "0")
                        config_text = config_text.replace("cdimage0=", ";cdimage0=")

                        # controls (TO BE WORKED ON)
                    if use_mouse1 is True:
                        config_text = config_text.replace("<<port0>>", "mouse")
                        config_text = config_text.replace("<<port0mode>>", "mousenowheel")

                    #    if use_mouse2==True:
                    #      config_text = config_text.replace("<<port1>>","mouse")
                    #      config_text = config_text.replace("<<port1mode>>","mousenowheel")

                    if use_cd32_pad is True:
                        config_text = config_text.replace("<<port0>>", "joy2")
                        config_text = config_text.replace("<<port0mode>>", "cd32joy")
                        config_text = config_text.replace("<<port1>>", "joy1")
                        config_text = config_text.replace("<<port1mode>>", "cd32joy")
                    else:
                        config_text = config_text.replace("<<port0>>", "joy2")
                        config_text = config_text.replace("<<port0mode>>", "djoy")
                        config_text = config_text.replace("<<port1>>", "joy1")
                        config_text = config_text.replace("<<port1mode>>", "djoy")

                    config_text = config_text.replace("<<port2>>", input_3)
                    config_text = config_text.replace("<<port3>>", input_4)
                    config_text = config_text.replace("<<deadzone>>", deadzone)
                    config_text = config_text.replace("<<stereo_seperation>>", stereo_seperation)

                    # put the text from the file into a string

                    custom_file = "customcontrols/" + full_game_name + ".controls"
                    custom_text = ""
                    
                    if os.path.isfile(custom_file) == True:

                        # remove any items which are not amiberry custom settings
                        with open(custom_file) as f:
                            content = f.readlines()
                        f.close()
                        
                        for this_line in content:
                            if this_line.find("amiberry_custom") > -1:
                                custom_text += this_line

                    config_text = config_text.replace("<<custom_controls>>", custom_text)

                    
                    # save out the config changes
                    text_file = open(config_file, "w")
                    text_file.write(config_text)
                    text_file.close()
                    
                ## this point we can jump in, having created a config.

                # we'll need to check we are on WHDLoad mode and creation of auto-startup is ON
                if scan_mode == "WHDLoad" and CREATE_AUTOSTARTUP == True:                   
                    slave_count = 0
                    for slave_file in glob.glob(file + "/*"):
                        if slave_file.lower().endswith(".slave"):
                            
                            this_slave = whdload_slave.whdload_factory(slave_file)
                            slave_count += 1

                # then check that there is 1 slave file only
                    if slave_count == 1 and os.path.isfile(file + "/auto-startup") == False:

                    # if so, we can make an auto-startup file
                        data_path = (this_slave.current_dir)
                        if data_path !="": data_path += "/"
                        
                        autostart_text = 'CD "WHDLoadGame:"' + chr(10)
                        autostart_text += 'WHDLOAD SLAVE="WHDLoadGame:' + this_slave.file_name +'"'
                        autostart_text += ' PRELOAD NOWRITECACHE NOREQ SPLASHDELAY=0'
                        autostart_text += ' data="WHDLoadGame:' + data_path +'"'
                        autostart_text += ' NOREQ >"WHDLoadGame:whdscript_debug"' + chr(10)
                        autostart_text += 'uae-configuration SPC_QUIT 1' + chr(10)

                        #print (autostart_text)
                        
                        text_file = open(file + "/auto-startup", "w+")
                        text_file.write(autostart_text)
                        text_file.close()


                    # we will also leave a message about kickstarts
                        if len(this_slave.kickstarts) > 0:
                            kick_text = ""

                            kick_text += "This WHDLoad slave cannot be run without one of the " + chr(10)
                            kick_text += "following kickstart roms in BootWHD:devs/kickstarts/" + chr(10) + chr(10)
                            
                            for kick in (this_slave.kickstarts):
                                kick_text += "kick" + kick.name + chr(10)

                            kick_text += chr(10) + "Should this game fail to load, please check for these files." + chr(10)
                            #print (kick_text)
                            
                            text_file = open(file + "/whdkickstarts_message", "w+")
                            text_file.write(kick_text)
                            text_file.close()
  
                            #whdupdate_message
                            #whdscript_debug

                        print()
                        print (FontColours.OKBLUE + "     Created 'auto-startup' file." + FontColours.ENDC)
                                   
            # this point we can jump in, config creation or not
            
            print()
            count += 1

    print("Folder Scan of " + pathname + " Complete.")
    print()
    return


def do_scan_base(inputdir,outputdir):
    # go through the paths

    # DoScan(inputdir,"Games_WHDLoad_DomTest")
    # DoScan(inputdir,"Games_CDTV")
    # DoScan(inputdir,"Games_ADF")
    # DoScan(inputdir,"Games_Script_Unreleased")

    do_scan(inputdir, "Games_WHDLoad", outputdir)
    do_scan(inputdir, "Games_WHDLoad_AGA", outputdir)
    do_scan(inputdir, "Games_WHDLoad_CDTV", outputdir)
    do_scan(inputdir, "Games_WHDLoad_CD32", outputdir)
    do_scan(inputdir, "Games_WHDLoad_DemoVersions", outputdir)
    
    do_scan(inputdir, "Games_WHDLoad_AltVersions", outputdir)
    do_scan(inputdir, "Games_WHDLoad_AltLanguage", outputdir)
    do_scan(inputdir, "Games_WHDLoad_AGACD32_AltLanguage", outputdir)
    do_scan(inputdir, "Games_WHDLoad_AGACD32_AltVersions", outputdir)
    do_scan(inputdir, "Games_WHDLoad_Unofficial", outputdir)

    do_scan(inputdir, "Games_WHDLoad_HDF", outputdir)
    do_scan(inputdir, "Games_WHDLoad_HDF_AGA", outputdir)
    do_scan(inputdir, "Games_WHDLoad_HDF_CDTV", outputdir)
    do_scan(inputdir, "Games_WHDLoad_HDF_DemoVersions", outputdir)
    do_scan(inputdir, "Games_WHDLoad_HDF_AltLanguage", outputdir)
    
    do_scan(inputdir, "Games_HDF", outputdir)
    do_scan(inputdir, "Games_CD32", outputdir)

    do_scan(inputdir, "Demos_WHDLoad", outputdir)
    # raise SystemExit

# main section starting here...

print()
print(
    FontColours.BOLD + FontColours.OKBLUE + "HoraceAndTheSpider" + FontColours.ENDC + "'s " + FontColours.BOLD +
    "UAE Configuration Maker" + FontColours.ENDC + FontColours.OKGREEN + " (3.0)" + FontColours.ENDC + " | " + "" +
    FontColours.FAIL + "www.ultimateamiga.co.uk" + FontColours.ENDC)
print()

# initialisations
#
# Setup Commandline Argument Parsing
#

parser = argparse.ArgumentParser(description='Create UAE Configs for WHDLoad Packs.')
parser.add_argument('--scandirs', '-s',  # command line argument
                    nargs='*',  # any number of space seperated arguments
                    help='Directories to Scan',
                    default=['/home/pi/RetroPie/roms/amiga-data/']  # Default directory if none supplied
                    )

parser.add_argument('--outputdir', '-o',  # command line argument
                    help='Target output path for .uae files',
                    default='/home/pi/RetroPie/roms/amiga/'  # Default directory if none supplied
                    )

parser.add_argument('--no-update', '-n',  # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Disable the updater"
                    )

parser.add_argument('--ignore-output-path', # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Use input path as output location"
                    )

parser.add_argument('--force-config-overwrite',  # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Force Overwrite of the .uae config files"
                    )

parser.add_argument('--force-paths',  # command line argument
                    default='',
                    help="Force Specific Paths"
                    )

parser.add_argument('--rom-path',  # command line argument
                    default='/home/pi/RetroPie/BIOS/Amiga/',# Default directory if none supplied
                    help="Optional Kickstart ROM path"
                    )

parser.add_argument('--whdload-update',  # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Check for WHDLoad Updates"
                    )

parser.add_argument('--create-autostartup',  # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Generate auto-startup file for WHDLoad folders"
                    )

parser.add_argument('--no-filename-spaces',  # command line argument
                    action="store_true",  # if argument present, store value as True otherwise False
                    help="Replace 'spaces' in output filenames with underscores"
                    )

#parser.add_argument('--whdload-update',  # command line argument
#                    action="store_true",  # if argument present, store value as True otherwise False
#                    help="Check for WHDLoad Updates"
#                    )
#
#parser.add_argument('--create-autostartup',  # command line argument
#                    action="store_true",  # if argument present, store value as True otherwise False
#                    help="Generate auto-startup file for WHDLoad folders"
#                    )

# Parse all command line arguments
args = parser.parse_args()

# Get the directories to scan (or default)
inputdirs = args.scandirs

# check hostconfig for directories to scan
if find_host_option("scandir") !="":
    inputdirs = [find_host_option("scandir")]

# Dom's special directory override :P
if platform.system() == "Darwin":
    inputdirs = ["/Users/horaceandthespider/Documents/Gaming/AmigaWHD/WorkingFolder2/Test/"]

# Check Directories are valid
inputdirs = general_utils.check_inputdirs(inputdirs)

# >> Setup Bool Constant for use input as output
INPUT_AS_OUTPUT = args.ignore_output_path

# if hostconfig specifies no_update, use as override
if text_utils.str2bool(find_host_option("ignore_output_path")) == True : INPUT_AS_OUTPUT = True

# >> set an output follder for .uae location
outputdir = args.outputdir

# Check Directories are valid
if INPUT_AS_OUTPUT==False:
    outputdir = general_utils.check_singledir(outputdir)



# >> Setup Bool Constant for No Update
NO_UPDATE = args.no_update

# if hostconfig specifies no_update, use as override
if text_utils.str2bool(find_host_option("no_update")) == True : NO_UPDATE = True


# >> Setup Bool Constant for Config Overwrite
FORCE_OVERWRITE = args.force_config_overwrite

# if hostconfig specifies force_config_overwrite, use as override
if text_utils.str2bool(find_host_option("force_config_overwrite")) == True : FORCE_OVERWRITE = True


# >> Setup Bool Constant for Pi Paths
FORCE_PATHS = args.force_paths

# if hostconfig specifies ..., use as override
if find_host_option("force_paths") != "" : FORCE_PATHS = find_host_option("force_paths") 


# >> Setup Bool Constant for WHDLOAD Slave updating
WHDLOAD_UPDATE = args.whdload_update

# if hostconfig specifies ...., use as override
if text_utils.str2bool(find_host_option("whdload_update")) == True : WHDLOAD_UPDATE = True


# >> Setup Bool Constant for WHDLOAD Slave updating
CREATE_AUTOSTARTUP = args.create_autostartup

# if hostconfig specifies ...., use as override
if text_utils.str2bool(find_host_option("create_autostartup")) == True : CREATE_AUTOSTARTUP = True


# >> Setup Bool Constant for using underscores
NO_FILENAME_SPACES = args.no_filename_spaces

# if hostconfig specifies ...., use as override
if text_utils.str2bool(find_host_option("no_filename_spaces")) == True : NO_FILENAME_SPACES = True



# >> Setup Bool Constant for Pi Paths
ROM_PATH = args.rom_path

# if hostconfig specifies ..., use as override
if find_host_option("rom_path") != "" : ROM_PATH = find_host_option("rom_path") 



# >> Setup Bool Constant for WHDLOAD Slave updating
WHDLOAD_UPDATE = args.whdload_update

# if hostconfig specifies ...., use as override
if text_utils.str2bool(find_host_option("whdload_update")) == True : WHDLOAD_UPDATE = True


# >> Setup Bool Constant for WHDLOAD Slave updating
CREATE_AUTOSTARTUP = args.create_autostartup

# if hostconfig specifies ...., use as override
if text_utils.str2bool(find_host_option("create_autostartup")) == True : CREATE_AUTOSTARTUP = True


# paths/folders if needed
os.makedirs("settings", exist_ok=True)


# If we're developing don't overwrite our changes.
if NO_UPDATE is True:
     print(FontColours.FAIL + "No update requests. (Manual override)"+ FontColours.ENDC)
   
else:
    # we can go through all files in 'settings' and attempt a download of the file
    for filename in glob.glob('settings/*.txt'):
        update_utils.download_update(filename,"")

    # do similar for main template
 #   update_utils.download_update("uaeconfig.uaetemp","")

    # lets download all of the custom configs
    if os.path.isfile("settings/Control_Custom_Gamelist.txt") == True:
        
        # remove any items which are not amiberry custom settings
        with open("settings/Control_Custom_Gamelist.txt") as f:
             content = f.readlines()
             content = [x.strip() for x in content]
        f.close()
                            
        for this_line in content:
            update_utils.download_update("customcontrols/" + this_line,"")

    

if os.path.isfile("uaeconfig.uaetemp") is False:
    print(
        FontColours.FAIL + "Essential file: " + FontColours.BOLD + FontColours.OKBLUE + "uaeconfig.uaetemp" +
        FontColours.FAIL + FontColours.ENDC + " missing." + FontColours.ENDC)
    raise SystemExit

print()

for inputdir in inputdirs:
    
    if INPUT_AS_OUTPUT==True:
        outputdir = inputdir
        
    do_scan_base(inputdir,outputdir)

raise SystemExit
