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

pre_filename=[path+"/log", current_time, ".txt"]
filename="".join(pre_filename)
f = open(filename, "x")
f.write(str(pre_yap))
f.close()
print(filename)

def run_command(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    output = str(output.stdout)
    write_to_log(command, output)
    return output

def write_to_log(command, output):
    global filename
    current_time = str(datetime.now())
    pretty_time=str("["+current_time+"]: ")
    pretty_command_list=["Command: ", pretty_time, command]
    pretty_output_list=["Output:", pretty_time, output]
    pretty_command=str(" ".join(pretty_command_list))
    pretty_output=str(" ".join(pretty_output_list))
    f = open(filename, 'a')
    f.write("\n"+pretty_command)
    f.write("\n"+pretty_output)
    f.close()

def ts_options():
    output=run_command("tailscale status")
    if "100" in output:
        print("Tailscale is running.\n")
        ts_decision=input("Tailscale is Connected, Do you want to disconnect?(y/n)")
        if ts_decision == ("y"):
            output=run_command("tailscale down")
        elif ts_decision == ("n"):
            pass
        else:
            print("That wasn't an option, please use y/n")
            ts_options()
    if "stopped" in output:
        ts_decision=input("Tailscale is Disconnected, Do you want to connect?(y/n)")
        if ts_decision == ("y"):
            output=run_command("tailscale up")
        elif ts_decision == ("n"):
            pass
        else:
            print("That wasn't an option, please use y/n")
            ts_options()

def cf_options():
    output=run_command("warp-cli status")
    if "Connected" in output:
        cf_decision=input("Warp is Connected, Do you want to disconnect?(y/n)")
        if cf_decision == ("y"):
            output=run_command("warp-cli disconnect")
        elif cf_decision == ("n"):
            pass
        else:
            print("That wasn't an option, please use y/n")
            cf_options()
    if "Disconnected" in output:
        cf_decision=input("Warp is Disconnected, Do you want to connect?(y/n)")
        if cf_decision == ("y"):
            output=run_command("warp-cli connect")
        elif cf_decision == ("n"):
            pass
        else:
            print("That wasn't an option, please use y/n")
            cf_options()
    if "Connecting" in output:
        print("Warp is currently connecting, please wait and we will reload...")
        time.sleep(10)

def prechecks():
    output=run_command("warp-cli status")
    if "Connected" in output:
        print("Cloudflare Warp Is Connected")
    elif "Disconnected" in output:
        print("Cloudflare Warp is Disonnected")
    elif "Connecting" in output:
        print("Warp is currently connecting")
    output=run_command("tailscale status")
    if "stopped" in output:
        print("Tailscale Is Disconnected")
    elif "100" in output:
        print("Tailscale Is Connected")

def options():
    while True:
        prechecks()
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
