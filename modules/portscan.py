class PortScan(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)
        self.name = "portscan"
        # define attributes and set initial values
        self.attr['ports'] = []
        self.attr['ip'] = None
        self.attr['bgrab'] = False

    def usage(self):
        print("When I can be arsed I will add some usage information for this module here")

    def setAttribute(self, attr, val):
        attr, val = attr.lower().replace(" ", ""), val.lower().replace(" ","")
        if self.validate(attr,val):
            if attr == 'ports':
                self.attr['ports'] = [int(port) for port in val.split(',')]
            elif attr == 'ip':
                self.attr['ip'] = val
            elif attr == 'bgrab':
                if val == 'true':
                    self.attr['bgrab'] = True
                elif val == 'false':
                    self.attr['bgrab'] = False
            return True
        else:
            return False
    
    def validate(self, attr, val):
        if attr == 'ip' and not self.isIp(val):
            return False
        elif attr == 'ports' and not self.isPortList(val):
            return False
        elif attr == 'bgrab' and( val != "false" and val != "true"):
            return False
        elif attr not in self.attr.keys():
            return False
        else:
            return True
    
    def isIp(self, val):
        """ checks if val is valid ipv4 network address """
        exp = "^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"
        if re.match(exp, val):
            return True
        else:
            return False

    def isPortList(self, val):
        """ checks if val is, after removing white space, a valid list of comma separate ports"""
        exp = "^([0-9]+,)*[0-9]+$"
        if re.match(exp, val):
            return True
        else:
            return False
    
    def bannerGrab(self, s):
        """ Attempt to grab the banner of the service running on a known open port, time out after
            5 seconds."""
        s.settimeout(5.0)
        try:
            banner = s.recv(1024).decode()
            return banner
        except socket.timeout:
            print('[-] Connection timed out')
            return None

    def run(self):
        if len(self.attr['ports']) > 1:
            print(f"[*] Scanning {self.attr['ip']} on ports {', '.join([str(port) for port in self.attr['ports'][:-1]])} and {str(self.attr['ports'][-1])}")
        else:
            print(f"[*] Scanning {self.attr['ip']} on port {self.attr['ports'][0]}")

        for port in self.attr['ports']:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((self.attr['ip'],port))
            if result == 0:
                print(f"[+] Port {port} is open")
                if self.attr['bgrab']:
                    print('[*] Attempting banner grab')
                    banner = self.bannerGrab(s)
                    if banner:
                        print("[+] Grabbed the following banner: ")
                        print(banner)
                    else:
                        print("[-] Failed to grab banner")
            else:
                print(f"[-] Port {port} is closed")
            s.close()
        return True

self.loaded_modules['portscan'] = PortScan()
