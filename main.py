import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: haha no")
        exit(-1)
    if sys.argv[1] == "install":
        if(len(sys.argv) < 3):
            print("I need to know what I am supposed to install!")
            exit(1)
        installreq = json.loads(requests.get("https://api.spiget.org/v2/search/resources/" + sys.argv[2]).content)
        print(installreq) # for debug only. TODO: remove
