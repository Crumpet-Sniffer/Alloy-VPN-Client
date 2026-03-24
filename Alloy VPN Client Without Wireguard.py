import subprocess
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
WG_DIR = BASE_DIR / "Wireguard_Configs"
LOG_DIR = BASE_DIR / "Logs"
SUB_LOG_DIR = LOG_DIR / str(datetime.today().date())#
LOG_DIR.mkdir(exist_ok=True)
SUB_LOG_DIR.mkdir(exist_ok=True)
WG_DIR.mkdir(exist_ok=True)
log_path=str(SUB_LOG_DIR)
wg_path=str(WG_DIR)

now=time.strftime("%Y-%m-%d %H:%M:%S")
log_header=("####################################################\n### Log Started At: ["+now+"] ###\n####################################################")
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
filename = log_path + "/log" + current_time + ".txt"
with open(filename, "x") as f:
    f.write(log_header)
print(filename)

def run_command(command): #Call to run command and give output
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    output = str(output.stdout)
    write_to_log(command, output)
    return output

def run_command_lines(command): #Only used in admin version to get the interface name for the wireguard subroutine but it's usefull to have anyway in case future expansions need to parse other outputs
    output = run_command(command)
    return output.splitlines()

def write_to_log(command, output): #Writes to a log file
    global filename
    current_time = str(datetime.now())
    pretty_time="["+current_time+"]: "
    pretty_command_list=["Command: ", pretty_time, command]
    pretty_output_list=["Output:", pretty_time, output]
    pretty_command= " ".join(pretty_command_list)
    pretty_output= " ".join(pretty_output_list)
    with open(filename, 'a') as f:
        f.write("\n"+pretty_command)
        f.write("\n"+pretty_output)

def ts_options(): #Tailscale VPN
    output=run_command("tailscale status")
    while True:
        if "100." in output:
            decision=input("Tailscale is Connected, Do you want to disconnect?(y/n)")
            if decision == ("y"):
                output=run_command("tailscale down")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
        elif "stopped" in output:
            decision=input("Tailscale is Disconnected, Do you want to connect?(y/n)")
            if decision == ("y"):
                output=run_command("tailscale up")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
                break
        else:
            break

def cf_options(): #Cloudflare Warp VPN
    output=run_command("warp-cli status")
    while True:
        if "Connected" in output:
            decision=input("Warp is Connected, Do you want to disconnect?(y/n)")
            if decision == ("y"):
                output=run_command("warp-cli disconnect")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
        if "Disconnected" in output:
            decision=input("Warp is Disconnected, Do you want to connect?(y/n)")
            if decision == ("y"):
                output=run_command("warp-cli connect")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
        if "Connecting" in output:
            print("Warp is currently connecting, please wait...")
            while "Connecting" in output:
                time.sleep(3)
                print("Still connecting, retrying in 3 seconds...")
                output=run_command("warp-cli status")
            break

def mv_options(): #Mullvad VPN
    output=run_command("mullvad status")
    while True:
        if "Connected" in output:
            decision=input("Mullvad is Connected, Do you want to disconnect?(y/n)")
            if decision == ("y"):
                output=run_command("mullvad disconnect")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
        if "Disconnected" in output:
            decision=input("Mullvad is Disconnected, Do you want to connect?(y/n)")
            if decision == ("y"):
                output=run_command("mullvad connect")
                break
            elif decision == ("n"):
                break
            else:
                print("That wasn't an option, please use y/n")
        if "Connecting" in output:
            print("Mullvad is currently connecting, please wait...")
            while "Connecting" in output:
                time.sleep(3)
                print("Still connecting, retrying in 3 seconds...")
                output=run_command("mullvad status")
            break

def prechecks(): #Runs checks before the options menu
    output=run_command("tailscale status")
    if "stopped" in output:
        print("Tailscale Is Disconnected")
    elif "100." in output:
        print("Tailscale Is Connected")
    output=run_command("warp-cli status")
    if "Connected" in output:
        print("Cloudflare Warp Is Connected")
    elif "Disconnected" in output:
        print("Cloudflare Warp is Disonnected")
    elif "Connecting" in output:
        print("Warp is currently connecting")
    output=run_command("mullvad status")
    if "Connected" in output:
        print("Mullvad Is Connected")
    elif "Disconnected" in output:
        print("Mullvad is Disonnected")
    elif "Connecting" in output:
        print("Mullvad is currently connecting")

def options():
    while True:
        prechecks()
        print("1: Tailscale")
        print("2: Cloudflare Warp")
        print("3: Mullvad")
        print("4: Exit")
        option=input("Please select an option:")
        if option == ("1"):
            ts_options()
        elif option == ("2"):
            cf_options()
        elif option == ("3"):
            mv_options()
        elif option == ("4"):
            exit()
        else:
            print("That wasn't an option, please select 1, 2, 3, or 4")
options()
