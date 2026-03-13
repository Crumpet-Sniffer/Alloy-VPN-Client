import subprocess
from datetime import datetime
import time
from pathlib import Path


BASE_DIR = Path(__file__).parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
path=str(LOG_DIR)

nowtime=str(datetime.now())
pre_yap=("####################################################\n### Log Started At: ["+nowtime+"] ###\n####################################################")
current_time = str(datetime.now().strftime("%Y%m%d%H%M%S"))

pre_filename=[path+"\\log", current_time, ".txt"]
filename="".join(pre_filename)
f = open(filename, "x")
f.write(str(pre_yap))
f.close()
print(filename)

def wtl():
    global command
    global filename
    global output
    current_time = str(datetime.now())
    pretty_time=str("["+current_time+"]: ")
    logged=["Output:", pretty_time, output]
    command=["\nCommand: "+command]
    pretty_logged=str(" ".join(logged))
    pretty_command=str(" ".join(command))
    f = open(filename, 'a')
    f.write("\n"+pretty_command)
    f.write("\n"+pretty_logged)
    f.close()

def run_command():
    global output
    global command
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = str(output.stdout)
    wtl()

def ts_options():
    global command
    global output
    command=("tailscale status")
    run_command()
    if output == ("Tailscale is stopped.\n"):
        ts_decision=input("Tailscale is: Stopped, Do you want to start it?(y/n)")
        if ts_decision == ("y"):
            command=("tailscale up")
            run_command()
            options()
        if ts_decision == ("n"):
            options()
        elif():
            print("That wasn't an option, please use y/n")
            ts_options()
    if (output[0:3])==("100"):
        print("Tailscale is running.\n")
        ts_decision=input("Tailscale is: Running, Do you want to stop it?(y/n)")
        if ts_decision == ("y"):
            command=("tailscale down")
            run_command()
            options()
        if ts_decision == ("n"):
            options()
        elif():
            print("That wasn't an option, please use y/n")
            ts_options()

def cf_options():
    global command
    global output
    command=("warp-cli status")
    run_command()
    cf_status = ((output)[15:27])
    if cf_status == ("Connected\nNe"):
        cf_decision=input("Warp is: Connected, Do you want to stay connected?(y/n)")
        if cf_decision == ("y"):
            options()
        if cf_decision == ("n"):
            command=("warp-cli disconnect")
            run_command()
    elif():
            print("That wasn't an option, please use y/n")
            cf_options()
    if cf_status == ("Disconnected"):
        cf_decision=input("Warp is: Disconnected, Do you want to connect?(y/n)")
        if cf_decision == ("y"):
            command=("warp-cli connect")
            run_command()
        if cf_decision == ("n"):
            options()
        elif():
            print("That wasn't an option, please use y/n")
            cf_options()
    if cf_status == ("Connecting\nR"):
        print("Warp is currently connecting, please wait and we will reload...")
        time.sleep(10)
        cf_options()

def options():
    print("1: Tailscale")
    print("2: Cloudflare Warp")
    print("3: Exit")
    option=input("Please select an option:")
    if option == ("1"):
        ts_options()
    elif option == ("2"):
        cf_options()
    elif option == ("3"):
        exit()
    else:
        print("That wasn't an option, please select 1, 2, or 3")
        options()
    options()
options()