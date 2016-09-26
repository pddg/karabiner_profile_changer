# karabiner_profile_changer

To change profiles of [karabiner-elements](https://github.com/tekezo/Karabiner-Elements) depends on connecting devices.  

## Requirements

This script was tested on macOS 10.12.

* Python 3.5.2
* Homebrew 1.0.4
* PyUSB
* lsusb

## Usage

You should install `lsusb` and `PyUSB`.

```bash
$ brew install lsusb
$ pip install --pre pyusb
```

Install `karabiner-elements` and create its config file.

```bash
$ mkdir -p ~/.karabiner.d/configuration/
$ cd ~/.karabiner.d/configuration/
$ touch karabiner.json
$ open karabiner.json
```

Edit `karabiner.json`.  
Clone this repository.

```bash
$ git clone https://github.com/pddg/karabiner_profile_changer
$ cd karabiner_profile_changer
$ cp config.json.sample config.json
$ cp karabiner_profile_changer.plist.sample karabiner_profile_changer.plist
```

First, you should check VendorID and ProductID of your device which you want to connect to your Mac.  
Edit `config.json` as follows.

```json
{
    "default_proflie": "Default",
    "config_file": "/path/to/karabiner.json",
    "interval": 10,
    "devices": [
        {
            "profile_name": "Profile name1",
            "vendor_id": "0x4d12",
            "product_id": "0x2021"
        },
        {
            "profile_name": "Profile name2",
            "vendor_id": "0x3a55",
            "product_id": "0x3019"
        }
    ]
}
```

`default_profile` and `profile_name` is related to profile name of your `karabiner.json`. `interval` is the interval of check USB devices connected to Mac.
if you write `"interval": 10`, this script check USB devices and change profile at 10-seconds intervals.  

Second you edit `karabiner_profile_changer.plist` as follows.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Disabled</key>
	<false/>
	<key>Label</key>
	<string>karabiner_profile_changer</string>
	<key>OnDemand</key>
	<false/>
	<key>ProgramArguments</key>
	<array>
		<string>/path/to/python</string>
		<string>/path/to/karabiner_profile_changer/main.py</string>
	</array>
	<key>UserName</key>
	<string>{{Your user name}}</string>
</dict>
</plist>
```

Set absolute path of python interpriter and main.py in karabiner_profile_changer. And set your username in `.plist`.

Finally, you registered that plist file.

```bash
$ cp karabiner_profile_changer.plist ~/Library/LaunchAgents/
$ launchctl load ~/Library/LaunchAgents/karabiner_profile_changer.plist
```

If you change `config.json`, you should use `launchctl stop`. `stop` this process, but it automatically restart.  
