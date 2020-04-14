import subprocess
import os

def main():
    firstAddress = runcmd("ip route | awk '/default/ {print $3}'")
    secondAddress = runcmd("ip -4 addr show dev eth0 | grep inet")
    secondAddressArray = secondAddress.split()

    serverAddress = secondAddressArray[1]
    broadcastAddress = secondAddressArray[3]

    DNSaddress = runcmd("cat /etc/resolv.conf")
    DNSaddress = (DNSaddress.split())[7]

    CreateFile("/etc/systemd/network/10-eth0.netdev", "[Match]\nName=eth0\n\n[Network]\nDHCP=no\nprint("Now open the terminal and enter the command")
    print("sudo nano /etc/systemd/network/11-eth0.network" + "\n")
    print("now enter the following, then press ctrl+x followed by enter" + "\n")
    print("[Match]\nName=eth0\n\n[Network]\nAddress="+ serverAddress +"\nDNS="+ DNSaddress +"\n\n[Route]\nGateway="+ firstAddress +"\n")

    print("Now open the terminal and enter the command")
    print("sudo nano /etc/systemd/resolved.conf" + "\n")
    print("Scroll down until you see [Resolve]\nRemove the # from infront of DNS=\n and after the = enter "+ DNSaddress + "\n")

    runSudo('sudo systemctl enable systemd-networkd')
    print("Finally in terminal enter:")
    print("sudo Reboot")
    

def runcmd(command):
    stream = os.popen(command)
    output = stream.read()
    return output

def runSudo(commandString):
    cmd = [commandString,'restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != '':
        print('unexpected error occured')
        print(errors.decode('ascii'))

def CreateFile(filePath, contents)
    f = open(filePath, "w")
    f.write(contents)
    f.close()

main()
