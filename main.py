import json
import requests
import sys

def managePackageFile(name="", version=0):
    open("spigetcli.json", "w").close()
    with open("spigetcli.json", "r+") as pckfile:
        pckcontents = json.loads(pckfile.read() or "{}")
        if "name" not in pckcontents:
            pckcontents["name"] = "A Minecraft Server"
        if "plugins" not in pckcontents:
            pckcontents["plugins"] = []
        if(name != ""):
            if name not in pckcontents["plugins"]:
                pckcontents["plugins"].append({name: {"version": version}})
            else:
                pckcontents["plugins"]["name"]["version"] = {"version": version}
        pckfile.write(json.dumps(pckcontents))

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
        if len(installreq) != 1:
            print("Could not find package {0}".format(sys.argv[2]))
            exit(1)
        try:
            with open("plugins/" + installreq[0]["name"] + ".jar", "wb") as jar:
                managePackageFile(installreq[0]["name"], installreq[0]["version"]["id"])
                jar.write(requests.get("https://api.spiget.org/v2/resources/{0}/download".format(installreq[0]["id"])).content)
        except Exception as e:
            print(e)
            print("""Error occured while downloading plugin. Check that
1) you are in a minecraft server folder
2) you have a plugins/ folder on your current working directory
3) spigot isn't down""")
            exit(1)

if __name__ == "__main__":
    main()