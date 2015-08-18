#!/usr/bin/python

import json
import subprocess
import sys
import time

if len(sys.argv) < 3:
        print("we need 2 or 3 arguments")
        exit(1)

arg1 = sys.argv[1]
arg2 = sys.argv[2]

if arg1 == "discover":
        if arg2 == "GP":
                p = subprocess.Popen("vmsec status | grep 'GP_[0-9]*_Dir'", shell=True, stdout=subprocess.PIPE)
                output = p.communicate()[0]
        if arg2 == "SA":
                p = subprocess.Popen("vmsec status | grep 'SA_[0-9]*_NAME'", shell=True, stdout=subprocess.PIPE)
                output = p.communicate()[0]
#       else:
#               print("argument 2 needs to be GP or SA")
#               exit(1)

        data = list()
        for line in output.split("\n"):
                if line:
                        data.append({"{#VAL}": line.split("=", 1)[0].rsplit("_",1)[0]})

        print(json.dumps({"data": data}))

if arg1 == "read":
        p = subprocess.Popen("vmsec status | grep '^" + arg2 + "' | head -n 1", shell=True, stdout=subprocess.PIPE)
        output = p.communicate()[0]

        val = output.split("=",1)[1].replace("\n","")

        try:
                arg3 = sys.argv[3]
        except IndexError:
                arg3 = ""

        if arg3 == "timestamp":
                try:
                        print time.mktime(time.strptime(val,"%m/%d/%Y %H:%M:%S"))
                except ValueError:
                        try:
                                print time.mktime(time.strptime(val.split(".",1)[0],"%Y-%m-%d %H:%M:%S"))
                        except ValueError:
                                print val
        else:
                print val