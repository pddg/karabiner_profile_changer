import json
import os
import time
import usb


try:
    with open(os.path.abspath(os.path.dirname(__file__)) + "/config.json") as f:
        CONFIG = json.loads(f.read())
except Exception:
    raise


class ConfigError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def check_config():
    if os.path.isfile(CONFIG["config_file"]):
        if len(CONFIG["devices"]) == 0:
            raise ConfigError("There are no devices in config.json.")
    else:
        raise ConfigError("karabiner.json can't be found.")


def change_config(mode):
    with open(CONFIG["config_file"]) as f:
        profiles = json.loads(f.read())
    for (i, profile) in enumerate(profiles['profiles']):
        profiles['profiles'][i]["selected"] = True if profile['name'] == mode else False
    with open(CONFIG["config_file"], "w") as f:
        json.dump(profiles, fp=f, indent=4, sort_keys=True)


def check():
    current_profile = CONFIG["default_proflie"]
    while True:
        usblist = [b.devices for b in usb.busses()]
        usblist = [e for ilist in usblist for e in ilist]
        usblist = [(hex(b.idVendor), hex(b.idProduct)) for b in usblist]
        for mode in CONFIG["devices"]:
            device = (mode["vendor_id"], mode["product_id"])
            if device in usblist:
                if mode["profile_name"] != current_profile:
                    change_config(mode["profile_name"])
                    current_profile = mode["profile_name"]
            elif CONFIG["default_proflie"] != current_profile:
                    change_config(CONFIG["default_proflie"])
                    current_profile = CONFIG["default_proflie"]
        time.sleep(CONFIG["interval"])


if __name__ == "__main__":
    check_config()
    check()
