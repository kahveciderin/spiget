import json
import requests
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: haha no")
        exit(-1)
    if sys.argv[1] == "install":
        if(len(sys.argv) < 3):
            print("I need to know what I am supposed to install!")
            exit(1)
        try:
            installreq = json.loads(requests.get("https://api.spiget.org/v2/search/resources/" + sys.argv[2] + "?field=name&size=1").content)
        except:
            print("Error occured while fetching the API.")
            exit(1)
        downloadLink = installreq[0]["file"]["url"]
        name = installreq[0]["name"]
        print(downloadLink) # for debug only. TODO: remove
        
        with open(name + ".jar", "wb") as f:
            requests.get("https://spigot.com/" + downloadLink)
        
        if len(installreq) != 1:
            print("Could not find package {0}".format(sys.argv[2]))
            exit(1)


if __name__ == "__main__":
    main()