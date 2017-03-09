import ssl
import urllib
import urllib.request

try:
    from utils.text_utils import FontColours
except:
    from text_utils import FontColours

def download_update(in_file):


    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except:
        pass


    # get_file = "http://www.djcresswell.com/RetroPie/ConfigMaker/" +infile
    get_file = "https://raw.githubusercontent.com/HoraceAndTheSpider/UAEConfigMaker/master/" + in_file
    put_file = "" + in_file

    try:
        urllib.request.urlretrieve(get_file, put_file)
        print("Update downloaded for " + FontColours.OKBLUE + in_file + FontColours.ENDC + ".")
    except:
        print("No update downloaded for " + FontColours.FAIL + in_file + FontColours.ENDC + ". (Web Page not found)")
    return


def main():

# initialisations


# and these are the files to update
    download_update("ConfigMaker.py")
    download_update("README.md")
    download_update("TODO.md")
    download_update("whdload/whdload_slave.py")
    download_update("utils/general_utils.py")
    download_update("utils/text_utils.py")
    download_update("utils/update_utils.py")
    
    return

if __name__ == "__main__":
     main()

