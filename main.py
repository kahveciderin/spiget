import json
import requests
from os import path
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

def downloadPlugin(pluginName):
    print("Downloading {0}...".format(pluginName))
    try:
        installreq = json.loads(requests.get("https://api.spiget.org/v2/search/resources/" + pluginName + "?field=name&size=1").content)
    except:
        print("Error occured while fetching the API.")
        exit(1)
    if len(installreq) != 1:
        print("Could not find package {0}, skipping...\n".format(pluginName))
    try:
        with open("spigetcli.json", "r") as pckfile:
            pckcontents = json.loads(pckfile.read() or "{}")
            if "plugins" in pckcontents:
                parr = [x for x in pckcontents["plugins"] if [*x][0] == pluginName][0][pluginName]
                if parr["version"] == installreq[0]["version"]["id"]:
                    print("Plugin {0} is already up to date.\n".format(pluginName))
                else:
                    with open("plugins/" + installreq[0]["name"] + ".jar", "wb") as jar:
                        managePackageFile(installreq[0]["name"], installreq[0]["version"]["id"])
                        response = requests.get("https://api.spiget.org/v2/resources/{0}/download".format(installreq[0]["id"]), stream=True)
                        total_length = response.headers.get('content-length')
                        if total_length is None: # shouldn't happen but whatever
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size=4096):
                                dl += len(data)
                                jar.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                            print("\nSuccessfully downloaded {0}\n".format(pluginName))
    except Exception as e:
        print(e)
        print("""Error occured while downloading {0}. Skipping. Check that
1) you are in a minecraft server folder
2) you have a plugins/ folder on your current working directory
3) spigot isn't down""".format(pluginName))

def main():
    if len(sys.argv) < 2:
        print("Usage: haha no")
        exit(-1)
    if sys.argv[1] == "install":
        if(len(sys.argv) < 3):
            print("I need to know what I am supposed to install!")
            exit(1)
        downloadPlugin(sys.argv[2])
    if sys.argv[1] == "ci":
        if not path.exists("spigetcli.json"):
            print("Cannot find spigetcli.json")
            exit(1)
        with open("spigetcli.json", "r") as pckfile:
            pckcontents = json.loads(pckfile.read() or "{}")
            if "name" in pckcontents:
                print("Setting up {0}\n".format(pckcontents["name"]))
            if "plugins" in pckcontents:
                for plugin in pckcontents["plugins"]:
                    downloadPlugin([*plugin][0])
if __name__ == "__main__":
    main()