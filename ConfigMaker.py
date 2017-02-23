import glob, platform
from urllib.request import *
#from urllib.request import urlopen, Request
import urllib
import ssl
import os
import math
import shutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, point, amount):
    return s[point:point+amount]

def midAMOS(s, point, amount):
    if point==0:
        point=1
    return s[point-1:point-1+amount]


def MakeFullCD32Name(inName):
    ##' check the txt file  
    fname = "Settings/CD32ISO_Longname_Fixes.txt"
    content = ""

    if os.path.isfile(fname)==True:
        with open(fname) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        f.close()
        
    for ThisLine in content:
        if ThisLine.find("|") > -1:
            FindPart = left(ThisLine,ThisLine.find("|"))
            ReplacePart = right(ThisLine,len(ThisLine)-ThisLine.find("|")-1)

            if inName == FindPart:
                inName = ReplacePart
                
    return inName


def MakeFullName(inName):
    
## special "clean up" rules 
    inName = inName.replace("'n'"," 'n'")
    inName = inName.replace("+"," +")
    inName = inName.replace("&"," &")

    oldName = inName
    inName = inName+"___"

    firstlength=len(inName)

## special loop
##    for A in range(2,firstlength-3):
    A=1
    B=len(oldName)
    
    while A<len(inName) and A<B:
        A=A+1
        
        PREVCHAR2=ord(midAMOS(inName,A-2,1))
        PREVCHAR=ord(midAMOS(inName,A-1,1))
        THISCHAR=ord(midAMOS(inName,A,1))
        NECKCHAR=ord(midAMOS(inName,A+1,1))
        NECKCHAR2=ord(midAMOS(inName,A+2,1))

##  ===== add spaces
        
        if THISCHAR>=65 and THISCHAR<=90:
          #Rem   we are a capital letter
      
##      ' special MB rule
            if chr(THISCHAR)=="M" and chr(NECKCHAR)=="B" and(THISCHAR>=48 and THISCHAR<=57):
                pass
    ##  two underscores ... ignore 
            elif PREVCHAR==95 and PREVCHAR2==95:
                pass
    ##  previous is a capital A, but not part of AGA 
            elif PREVCHAR==65 and THISCHAR != 71 and NECKCHAR != 65:
                inName = AddSpace(inName,A)
                A=A+1
                B=B+1               
    ##  and the previous letter is not a space , and not also capital, or dash 
            elif PREVCHAR != 32 and PREVCHAR != 45 and not(PREVCHAR>=65 and PREVCHAR<=90):
                inName = AddSpace(inName,A)
                A=A+1
                B=B+1
              
##    ' =====: Rem   we are a number               
        elif THISCHAR>=48 and THISCHAR<=57:
      
##    'and previous number was not a number and not a space
           if not(PREVCHAR>=48 and PREVCHAR<=57) and PREVCHAR!=32:
                inName = AddSpace(inName,A)
                A=A+1
                B=B+1

        if A>firstlength:
            break 
        
## dirty manual fixes 
    inName=inName.replace("  "," ")
    inName=inName.replace("___","")
    inName=inName.replace("CD 32","CD32")
    inName=inName.replace(" CD32"," [CD32]")
    inName=inName.replace(" CDTV"," [CDTV]")
    inName=inName.replace(" AGA"," [AGA]")
    inName=inName.replace(" 512 Kb"," (512Kb)")
    inName=inName.replace(" 1 MB"," (1MB)")
    inName=inName.replace(" 2 MB"," (2MB)")
    inName=inName.replace(" 4 MB"," (4MB)")
    inName=inName.replace(" 8 MB"," (8MB)")
    inName=inName.replace(" 1 Disk"," (1 Disk)")
    inName=inName.replace(" 2 Disk"," (2 Disk)")
    inName=inName.replace(" 3 Disk"," (3 Disk)")
    inName=inName.replace(" 4 Disk"," (4 Disk)")
    inName=inName.replace(" Files"," (Files)")
    inName=inName.replace(" Image"," (Image)")
    inName=inName.replace(" Chip"," (Chip)")
    inName=inName.replace(" Fast"," (Fast)")
    inName=inName.replace("(Fast) Break","Fast Break")
    inName=inName.replace("R³sselsheim","Russelsheim")

##' check the txt file  
    fname = "Settings/WHD_Longname_Fixes.txt"
    content = ""

    if os.path.isfile(fname)==True:
        with open(fname) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        f.close()
        
    for ThisLine in content:
        if ThisLine.find("|") > -1:
            FindPart = left(ThisLine,ThisLine.find("|"))
            ReplacePart = right(ThisLine,len(ThisLine)-ThisLine.find("|")-1)

            if inName == FindPart:
                inName = ReplacePart                   

    # language rules
    language=right(inName,3)

    if language == " De":
      inName=left(inName,len(inName)-3)+" (Deutsch)"
    elif language==" Pl":
      inName=left(inName,len(inName)-3)+" (Polski)"
    elif language==" It":
      inName=left(inName,len(inName)-3)+" (Italiano)"
    elif language==" Dk":
      inName=left(inName,len(inName)-3)+" (Dansk)"
    elif language==" Es":
      inName=left(inName,len(inName)-3)+" (Espanol)"
    elif language==" Fr":
      inName=left(inName,len(inName)-3)+" (Francais)"
    elif language==" Cz":
      inName=left(inName,len(inName)-3)+" (Czech)"
    elif language==" Se":
      inName=left(inName,len(inName)-3)+" (Svenska)"
    elif language==" Fi":
      inName=left(inName,len(inName)-3)+" (Finnish)"

      
    return inName

def AddSpace(inBit,pos):

    inBit=left(inBit,pos-1)+" "+right(inBit,len(inBit)-pos+1)
    return inBit 



def DownloadUpdate(infile):
    
 #   GetFile = "http://www.djcresswell.com/RetroPie/ConfigMaker/" +infile
    GetFile = "https://raw.githubusercontent.com/HoraceAndTheSpider/UAEConfigMaker/master/" +infile
    PutFile = "" + infile
    
    try:
        a = urllib.request.urlretrieve(GetFile, PutFile)
        print ("Update downloaded for " + bcolors.OKBLUE+ infile + bcolors.ENDC +  ".")
    
##    except urllib.error.HTTPError as err:
##        print ("No update downloaded for " + bcolors.FAIL + infile + bcolors.ENDC +  ". (Web Page not found)")
##
    except:
        print ("No update downloaded for " + bcolors.FAIL + infile + bcolors.ENDC +  ". (Web Page not found)")
        
    return 

def ChexList(inFile,GameName):

    fname = "Settings/"+inFile
    
    if os.path.isfile(fname) == False:
            return False
        
    with open(fname) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    f.close()

    answer = False
    
    for ThisLine in content:
        if ThisLine == GameName:
            answer = True
            break

    return answer

def FindHostOption(inOption):

    fname = "hostconfig.uaetemp"
    
    if os.path.isfile(fname) == False:
            return ""
        
    with open(fname) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    f.close()

    answer = ""
    
    for ThisLine in content:
        if left(ThisLine,len(inOption)) == inOption:
            answer = ThisLine.replace(inOption,"")
            answer = answer.replace("=","").strip()
                    
            break

    return answer


def DoScan(inputdir,pathname):
    
    
    if os.path.isdir(inputdir + pathname) == True:
        print("Config Save Path: " + bcolors.OKBLUE + inputdir + bcolors.ENDC )
        print("Games Files Path: " + bcolors.BOLD + bcolors.OKBLUE + pathname + bcolors.ENDC )
        print()
    else:
        print("Specified Scan path "+ bcolors.FAIL + inputdir + pathname + bcolors.ENDC + " does not exist")
        return

##' what type of scan is it  --  default , Whdload folder 

    if pathname.find("WHDLoad_HDF")>-1 and pathname.lower().find(".hdf"):
        scanmode="WHDLoadHDF"
        hdsettings=",0"
        
    elif pathname.find("WHDLoad")>-1:
        scanmode="WHDLoad"
        hdsettings=",0"

    elif pathname.lower().find(".hdf")>-1:
        scanmode="HDF"
        hdsettings=",32,1,2,512,50,,uae"

    elif pathname.lower().find(".adf")>-1:
        scanmode="ADF"

    elif pathname.lower().find("cd32")>-1:
        scanmode="CD32"
        
    elif pathname.lower().find("cdtv")>-1:
        scanmode="CD32"
        
    else:
        scanmode="WHDLoad"
        hdsettings=",0"


    print("Scan Mode: " + bcolors.BOLD + bcolors.HEADER + scanmode + bcolors.ENDC)
    print()
    thefilter = ""
    count = 1
    SkipAll = 0

    QuitButton = FindHostOption("button_for_quit")
    MenuButton = FindHostOption("button_for_menu")
    
    if QuitButton == "": QuitButton = -1
    if MenuButton == "": MenuButton = -1


  ## cycle through all folders / files       
    for filename in glob.glob(inputdir + pathname+"/*"):

        # WHDLOAD mode needs folders, the rest need files
        if scanmode == "WHDLoad":
            typetest = os.path.isdir(filename)
        else:
            typetest = os.path.isfile(filename)            

        thisfile = filename.replace(inputdir+pathname+"/","")

##        # type filter applies 
##   #     elif scanmode == "CD32" and (right(thisfile.lower(),4) != ".iso" and right(thisfile.lower(),4) != ".cue"):
##       #                                not a folder and no sub cue or iso file
##        elif scanmode == "CD32" and (os.path.isdir(filename) == False or os.path.isfile(filename + "/" + thisfile + ".cue")==False):
##             pass


        # name filter applies 
        if thefilter != '' and thisfile.find(thefilter) <0:
            pass
        
       # WHDLOAD will accept .zip
       # WHDLOAD mode needs folders, mostly
       # HDF file extension must be .hdf
       # CD32 file extension must be .iso
       # CD32 folders need sub file with extension as .cue
        elif (scanmode == "WHDLoad" and os.path.isfile(filename) == True and right(thisfile.lower(),4) == ".zip") or \
             (scanmode == "WHDLoad" and os.path.isdir(filename) == True) or \
             (scanmode == "HDF" and os.path.isfile(filename) == True and right(thisfile.lower(),4) == ".hdf") or \
             (scanmode == "CD32" and os.path.isfile(filename)==True and right(thisfile.lower(),4) == ".iso") or \
             (scanmode == "CD32" and os.path.isdir(filename) == True and os.path.isfile(filename + "/" + thisfile + ".cue")==True):

##            print ("Processed: "  + bcolors.OKBLUE +str(count)  + bcolors.ENDC )
##            print ()
            tempname = thisfile.replace("R³sselsheim","Russelsheim")
            print (bcolors.OKBLUE +str(count) + bcolors.ENDC + ": Processing Game: " + bcolors.BOLD + tempname + bcolors.ENDC)

            if thisfile.lower().endswith(".zip")==True:
                   thisfile=left(thisfile,len(thisfile)-4)
        
    # standard 'expand name' thing
            if scanmode=="WHDLoad":
                fullgamename = MakeFullName(thisfile)
                
            elif scanmode=="CD32":
                fullgamename = MakeFullCD32Name(thisfile)
                
    # there may be alternative one for TOSEC CD32 images....
            print ()
            print ("     Full Name: " + bcolors.OKGREEN + fullgamename + bcolors.ENDC)


          # normal method for selection
            if fullgamename.find("AGA") > -1:
                 MachineType="A1200/020"
                 
            elif scanmode == "CD32":
                 MachineType="CD32"
                 
            elif fullgamename.find("AGA") > -1:
                 MachineType="A1200/020"
            else:
                 MachineType="A600+"

            # check if config already exists - yes/no to overwrite

            CreateConfig = True
            answer = ""
            
            if os.path.isfile(inputdir+fullgamename+".uae") == True and SkipAll==0:

                while answer != "Y" and answer !="N" and answer !="S" and answer != "A":
                    answer = input (bcolors.OKBLUE + "     Config already exists - overwrite? "+"(Yes/No/Always/Skip) " + bcolors.ENDC)
                    if answer == "a" or answer =="s" or answer == "n" or answer == "y":
                        answer = answer.upper()
                    print()
                    
            elif os.path.isfile(inputdir+fullgamename+".uae") == True and SkipAll == -1:
                    CreateConfig = False
                    print(bcolors.OKBLUE + "     Skipping existing file."+bcolors.ENDC)
                    print()
                    
        # process the answers
            if answer == "N":
                CreateConfig = False
                
            elif answer == "Y":
                CreateConfig = True
                
            elif answer == "A":
                SkipAll = 1
                
            elif answer == "S":
                SkipAll = -1

        # what to do 'automatically'
            if SkipAll == 1:
                 CreateConfig = True
                 
##            elif SkipAll == -1:
##                 CreateConfig = False                   


        # this is where we start the code to actually build the config with chnages
            if CreateConfig == True:

                    
                    #  check other parameters 
                    #  hardware options 

                # ======== SYSTEM HARDWARE =======  
                #  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # override the machine type, if on a list                
                    if ChexList("System_A500.txt",thisfile) == True:
                        MachineType = "A500"
                    elif ChexList("System_A1200.txt",thisfile) == True:
                        MachineType = "A1200/020"
                    elif ChexList("System_A4000.txt",thisfile) == True:
                        MachineType = "A4000/040"
                    elif ChexList("System_CD32.txt",thisfile) == True:
                        MachineType = "CD32"

                # PRESETS:  CPU / chipset/ kickstart 
                    Z3Ram=0
                    if MachineType=="A500":
                        ChipSet="OCS"
                        ACpu="68000"
                        Kickstart="kick13.rom"
                        KickstartExt=""
                        FastRam=0
                        ChipRam=1
                        ClockSpeed=0

                    elif MachineType=="A600+" or MachineType == "":
                        ChipSet="ECS_Agnus"
                        ACpu="68020"
                        Kickstart="kick31.rom"
                        KickstartExt=""
                        ChipRam=4
                        FastRam=8
                        ClockSpeed=14

                    elif MachineType=="A1200":
                        ChipSet="AGA"
                        ACpu="68ec020"
                        Kickstart="kick30.rom"
                        KickstartExt=""
                        ChipRam=4
                        FastRam=0
                        ClockSpeed=14

                    elif MachineType=="A1200/020":
                        ChipSet="AGA"
                        ACpu="68020"
                        Kickstart="kick31.rom"
                        KickstartExt=""
                        ChipRam=4
                        FastRam=4
                        ClockSpeed=14

                    elif MachineType=="A4000":
                        ChipSet="AGA"
                        ACpu="68040"
                        Kickstart="kick31.rom"
                        KickstartExt=""
                        ChipRam=4
                        FastRam=8
                        ClockSpeed=28

                    elif MachineType=="CD32":
                        ChipSet="AGA"
                        ACpu="68ec020"
                        Kickstart="cd32kick31.rom"
                        KickstartExt="cd32ext.rom"
                        ChipRam=4
                        FastRam=0
                        ClockSpeed=14

                    #'======== MEMORY SETTINGS =======
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' when we want different chip ram!!
                        
                    OldChipRam=ChipRam

                    for LCOUNT in range(0 , 4):

                        ChipRam = int(math.pow(2,LCOUNT))/2                           
                        if ChipRam >= 1:
                            ChipRam = int(ChipRam)

                        if ChexList("Memory_ChipRam_"+str(ChipRam)+".txt",thisfile)==True:
                            ChipRam = int(ChipRam*2)
                            break
                        ChipRam = OldChipRam

                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' when we want different fast ram!!
                        
                    OldFastRam=FastRam

                    for LCOUNT in range(0 , 4):

                        FastRam = int(math.pow(2,LCOUNT))
                        if ChexList("Memory_FastRam_"+str(FastRam)+".txt",thisfile)==True:
                            break
                        FastRam = OldFastRam

                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' when we want different Z3 ram!!

                    for LCOUNT in range(0 , 8):

                        Z3Ram = int(math.pow(2,LCOUNT))
                        if ChexList("Memory_Z3Ram_"+str(Z3Ram)+".txt",thisfile)==True:
                            break
                        Z3Ram=0

                    #'======== CHIPSET SETTINGS ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' sprite collisions
                    
                    SprtCol="playfields"
                    
                    if ChexList("Chipset_CollisionLevel_playfields.txt",thisfile)==True : SprtCol="playfields" 
                    if ChexList("Chipset_CollisionLevel_none.txt",thisfile)==True : SprtCol="none" 
                    if ChexList("Chipset_CollisionLevel_sprites.txt",thisfile)==True : SprtCol="sprites"
                    if ChexList("Chipset_CollisionLevel_full.txt",thisfile)==True : SprtCol="full"
                    
                     #' imm. blits & fast copper
            
                    FastCopper = not ChexList("Chipset_NoFastCopper.txt",thisfile)                    
                    ImmediateBlits = ChexList("Chipset_ImmediateBlitter.txt",thisfile)

                    #'======== CPU SETTINGS ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    
                    #' max emu speed
                    ACpuSpeed = "real"
                    if ChexList("CPU_MaxSpeed.txt",thisfile)==True : ACpuSpeed="max"
                    
                    #' clock speed
                    if ChexList("CPU_ClockSpeed_7.txt",thisfile)==True : ClockSpeed=7
                    if ChexList("CPU_ClockSpeed_14.txt",thisfile)==True : ClockSpeed=14
                    if ChexList("CPU_ClockSpeed_28.txt",thisfile)==True : ClockSpeed=28
                    
                    #' 24 bit addressing / compatible CPU / JIT Cache
                    _24BitAddress = not ChexList("CPU_No24BitAddress.txt",thisfile)
                    CompatibleCpu = ChexList("CPU_Compatible.txt",thisfile)
                    CycleExact = ChexList("CPU_CycleExact.txt",thisfile)
                    UseJIT = not ChexList("CPU_NoJIT.txt",thisfile)
                    #UseJIT =ChexList("CPU_ForceJIT.txt",thisfile)
                    
                    #'======== DISPLAY SETTINGS ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' screen Y/X Offsets

                    ScrnOffsetY=0
                    for Z in range(-16, 16):
                        if ChexList("Screen_OffsetY_"+str(Z)+".txt",thisfile) ==True : ScrnOffsetY=Z
                        
                    ScrnOffsetX=0
                    for Z in range(-16, 16):
                        if ChexList("Screen_OffsetX_"+str(Z)+".txt",thisfile) : ScrnOffsetX=Z 

                    #' screen heights
                    ScrnHight=240
                    if ChexList("Screen_Height_270.txt",thisfile)==True : ScrnHight=270
                    if ChexList("Screen_Height_262.txt",thisfile)==True : ScrnHight=262
                    if ChexList("Screen_Height_256.txt",thisfile)==True : ScrnHight=256
                    if ChexList("Screen_Height_240.txt",thisfile)==True : ScrnHight=240                        
                    if ChexList("Screen_Height_224.txt",thisfile)==True : ScrnHight=224
                    if ChexList("Screen_Height_216.txt",thisfile)==True : ScrnHight=216                          
                    if ChexList("Screen_Height_200.txt",thisfile)==True : ScrnHight=200
                    
                    #' screen widths
                    ScrnWidth=320
                    if ChexList("Screen_Width_384.txt",thisfile)==True : ScrnWidth=384
                    if ChexList("Screen_Width_352.txt",thisfile)==True : ScrnWidth=352
                    if ChexList("Screen_Width_320.txt",thisfile)==True : ScrnWidth=320
                    if ChexList("Screen_Width_768.txt",thisfile)==True : ScrnWidth=768
                    if ChexList("Screen_Width_704.txt",thisfile)==True : ScrnWidth=704
                    if ChexList("Screen_Width_640.txt",thisfile)==True : ScrnWidth=640

                    #' extras
                    _Aspect = bool(ChexList("Screen_Force43Aspect.txt",thisfile))
                    if FindHostOption("gfx_correct_aspect") !="" : _Aspect = FindHostOption("gfx_correct_aspect")
                    UseNTSC = ChexList("Screen_ForceNTSC.txt",thisfile)


                    #'======== CONTROL SETTINGS ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' mouse / mouse 2 / CD32

                    UseMouse1 = ChexList("Control_Port0_Mouse.txt",thisfile)
                    UseMouse2 = ChexList("Control_Port1_Mouse.txt",thisfile)
                    UseCD32Pad = ChexList("Control_CD32.txt",thisfile)

                    if scanmode=="CD32" : UseCD32Pad = True  

                    #'======== MISC SETTINGS ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' BSD Socket / Floppy Speed etc

                    UseBSDS = ChexList("Misc_BSDSocket.txt",thisfile)
                    FloppySpeed=800
                    Disk = ["","","",""]
                                       
                    if ChexList("Floppy_Speed_100.txt",thisfile) == True : FloppySpeed = 100
                    if ChexList("Floppy_Speed_200.txt",thisfile) == True : FloppySpeed = 200
                    if ChexList("Floppy_Speed_400.txt",thisfile) == True : FloppySpeed = 400
                    if ChexList("Floppy_Speed_800.txt",thisfile) == True : FloppySpeed = 800



                    #'======== SETUP CONFIG ======= 
                    #' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #' ....
                    
                    #print("we are making a config ....")
                    fname = inputdir + fullgamename + ".uae"
                    shutil.copyfile("uaeconfig.uaetemp", fname)
                    
                    if os.path.isfile(fname)==False:
                        print (bcolors.fail + "Error creating config." + bcolors.ENDC)
                    else:
                        print ("     Editing File: " + bcolors.HEADER + fname + bcolors.ENDC)

                    # put the text from the file into a string
                        text_file = open(fname, "r")
                        ConfigText = text_file.read()
                        text_file.close()


                     # all the major find/replaces
                        # game / path
                        ConfigText = ConfigText.replace("<<game>>",thisfile)
                            
                        ConfigText = ConfigText.replace("<<fullgame>>",fullgamename)                                                            
                        ConfigText = ConfigText.replace("<<hdpath>>",pathname)
                        ConfigText = ConfigText.replace("<<quitbutton>>",str(QuitButton))
                        ConfigText = ConfigText.replace("<<menubutton>>",str(MenuButton))

                        # screens
                        ConfigText = ConfigText.replace("<<screenheight>>",str(ScrnHight))
                        if ScrnWidth<321 : ScrnWidth=ScrnWidth*2
                        ConfigText = ConfigText.replace("<<screenwidth>>",str(ScrnWidth))
                        ConfigText = ConfigText.replace("<<offset_y>>",str(ScrnOffsetY))
                        ConfigText = ConfigText.replace("<<offset_x>>",str(ScrnOffsetX))
                        ConfigText = ConfigText.replace("<<43aspect>>",str(_Aspect))
                        ConfigText = ConfigText.replace("<<ntsc>>",str(bool(0-UseNTSC)))

                        # memory                        
                        ConfigText = ConfigText.replace("<<chipmem>>",str(ChipRam))
                        ConfigText = ConfigText.replace("<<fastmem>>",str(FastRam))
                        ConfigText = ConfigText.replace("<<z3mem>>",str(Z3Ram))

                        if Z3Ram>0 and (ACpu != "68020" and ACpu != "68040"):
                           ACpu="68020"

                        # chipset                        
                        ConfigText = ConfigText.replace("<<chipset>>",ChipSet)
                        ConfigText = ConfigText.replace("<<spritecollision>>",SprtCol)
                        ConfigText = ConfigText.replace("<<fastcopper>>",str(bool(0-FastCopper)))
                        ConfigText = ConfigText.replace("<<immediateblitter>>",str(bool(0-ImmediateBlits)))

                        # cpu                        
                        ConfigText = ConfigText.replace("<<kickstart>>",Kickstart)
                        ConfigText = ConfigText.replace("<<extkickstart>>",KickstartExt)
                        ConfigText = ConfigText.replace("<<cputype>>",ACpu)
                        ConfigText = ConfigText.replace("<<cpuspeed>>",ACpuSpeed)
                        if ClockSpeed==14:
                                ClockSpeed=1024
                        elif ClockSpeed==28:
                                ClockSpeed=128
                        else:
                                ClockSpeed=0
            
                        ConfigText = ConfigText.replace("<<clockspeed>>",str(ClockSpeed))
                        ConfigText = ConfigText.replace("<<cpucompatible>>",str(bool(0-CompatibleCpu)))
                        ConfigText = ConfigText.replace("<<cycleexact>>",str(bool(0-CompatibleCpu)))
                        ConfigText = ConfigText.replace("<<24bitaddress>>",str(bool(0-CycleExact)))
                        if UseJIT==False:
                            ConfigText = ConfigText.replace("<<jitcache>>","0")
                        else:
                            ConfigText = ConfigText.replace("<<jitcache>>","8192")

                        # misc 
                        ConfigText = ConfigText.replace("<<bsdsocket>>",str(bool(0-UseBSDS)))

                        # hard disk files
                    
                        DiskNr=0
                        if scanmode=="HDF" and os.path.isfile (pathname + thisfile.replace(".hdf","")+"_savedisk.adf") == True:
                            DiskNr=1
                            ConfigText = ConfigText.replace("<<diskpath0>>",pathname)
                            ConfigText = ConfigText.replace("<<disk0>>",thisfile.replace(".hdf","")+"_savedisk.adf")
                            ConfigText = ConfigText.replace("<<disktype0>>","0")
                            
                        # disable the HDF parameter
                        else:
                            ConfigText = ConfigText.replace("hardfile2=",";hardfile2=")
                            ConfigText = ConfigText.replace("filesystem2=rw,DH2",";filesystem2=rw,DH2")
                          
                        for LCOUNT in range(DiskNr,4):
                            ConfigText = ConfigText.replace("<<diskpath" + str(LCOUNT)+">>",pathname)
                            ConfigText = ConfigText.replace("<<disk" + str(LCOUNT)+">>",Disk[LCOUNT])

##                            print ("disk... "+Disk[LCOUNT])
                            if Disk[LCOUNT] == "":
                                DiskOn = "0"
                            else:
                                DiskNr=DiskNr+1
                                DiskOn = "1"
                                ConfigText = ConfigText.replace(";floppy" + str(LCOUNT),"floppy" + str(LCOUNT))
                                
                            ConfigText = ConfigText.replace("<<disktype"+ str(LCOUNT) + ">>",str(DiskOn))
                            ConfigText = ConfigText.replace("<<floppyspeed>>",str(FloppySpeed))
                            ConfigText = ConfigText.replace("<<totaldisks>>",str(DiskNr))

                        if MachineType == "CD32":
                            ConfigText = ConfigText.replace("uaehf1=",";uaehf1=")
                            ConfigText = ConfigText.replace("uaehf0=",";uaehf0=")
                            ConfigText = ConfigText.replace("filesystem2=",";filesystem2=")
                            ConfigText = ConfigText.replace("<<cd32mode>>","1") 
                        else:
                            ConfigText = ConfigText.replace("<<cd32mode>>","0")                           

                        # controls (TO BE WORKED ON)                           
                        if UseMouse1==True:
                            ConfigText = ConfigText.replace("pandora.custom_dpad=1",pathname)
                            ConfigText = ConfigText.replace("<<port0>>","mouse")
                            ConfigText = ConfigText.replace("<<port0mode>>","mousenowheel")

##                        if UseMouse2==True:
##                            ConfigText = ConfigText.replace("<<port1>>","mouse")
##                            ConfigText = ConfigText.replace("<<port1mode>>","mousenowheel")

                        if UseCD32Pad==True:
                            ConfigText = ConfigText.replace("<<port0>>","joy2")
                            ConfigText = ConfigText.replace("<<port0mode>>","cd32joy")
                            ConfigText = ConfigText.replace("<<port1>>","joy1")
                            ConfigText = ConfigText.replace("<<port1mode>>","cd32joy")
                        else:
                            ConfigText = ConfigText.replace("<<port0>>","joy2")
                            ConfigText = ConfigText.replace("<<port0mode>>","djoy")
                            ConfigText = ConfigText.replace("<<port1>>","joy1")
                            ConfigText = ConfigText.replace("<<port1mode>>","djoy")
                                                    

                    # save out the config changes
                        text_file = open(fname, "w")
                        text_file.write(ConfigText)
                        text_file.close()
        
            print ()
            count = count + 1

    print ("Folder Scan of "+ pathname +" Complete.")
    print ()
    return


## main section starting here...

print()
print(bcolors.BOLD + bcolors.OKBLUE + "HoraceAndTheSpider" + bcolors.ENDC + "'s "  + bcolors.BOLD + "UAE Configuration Maker" + bcolors.ENDC + bcolors.OKGREEN + " (v2.1)" + bcolors.ENDC +  " | " + "" + bcolors.FAIL + "www.ultimateamiga.co.uk" + bcolors.ENDC)
print()

## initialisations

try:
        ssl._create_default_https_context = ssl._create_unverified_context
except:
        pass
    
## -------- input dir  ... i.e. where we will scan for Sub-Folders
if platform.system()=="Darwin":
    inputdir="/Volumes/roms/amiga/"
    inputdir = "/Users/horaceandthespider/Documents/Gaming/AmigaWHD/WorkingFolder2/"

 ## -------- I SEE YOU AINGER! o_o
elif platform.node()=="RAVEN":
    inputdir="C:\\Users\\oaing\\Desktop\\whdload\\"
    
else:
    inputdir="//home/pi/RetroPie/roms/amiga/"
    
# paths/folders if needed
os.makedirs("Settings", exist_ok=True)


## we can go through all files in 'settings' and attempt a download of the file
for filename in glob.glob('Settings/*.txt'):

    DownloadUpdate(filename)
        
## do similar for 
DownloadUpdate("uaeconfig.uaetemp")

if os.path.isfile("uaeconfig.uaetemp")==False:
    print(bcolors.FAIL + "Essential file: " + bcolors.BOLD + bcolors.OKBLUE + "uaeconfig.uaetemp" + bcolors.FAIL + bcolors.ENDC + " missing."+ bcolors.ENDC)
    raise SystemExit



print()

## go through the paths
##DoScan(inputdir,"Games_WHDLoad_DomTest")
##raise SystemExit

DoScan(inputdir,"Games_WHDLoad")
DoScan(inputdir,"Games_WHDLoad_AGA")
DoScan(inputdir,"Games_WHDLoad_CDTV")
DoScan(inputdir,"Games_WHDLoad_CD32")
DoScan(inputdir,"Games_WHDLoad_DemoVersions")
DoScan(inputdir,"Games_WHDLoad_AltVersions")
DoScan(inputdir,"Games_WHDLoad_AltLanguage")
DoScan(inputdir,"Games_WHDLoad_AGACD32_AltLanguage")
DoScan(inputdir,"Games_WHDLoad_AGACD32_AltVersions")
DoScan(inputdir,"Games_WHDLoad_Unofficial")
DoScan(inputdir,"Games_HDF")
DoScan(inputdir,"Games_CD32")
DoScan(inputdir,"Games_WHDLoad_HDF")
#DoScan(inputdir,"Games_CDTV")
#DoScan(inputdir,"Games_ADF")
#DoScan(inputdir,"Games_Script_Unreleased")

DoScan(inputdir,"Demos_WHDLoad")

raise SystemExit



