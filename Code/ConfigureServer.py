import subprocess
import os

def main():
    firstAddress = runcmd("ip route | awk '/default/ {print $3}'")
    secondAddress = runcmd("ip -4 addr show dev eth0 | grep inet")
    secondAddressArray = secondAddress.split()

    serverAddress = secondAddressArray[1]
    serverAddressNoPort = (serverAddress.split('/'))[0]
    broadcastAddress = secondAddressArray[3]

    DNSaddress = runcmd("cat /etc/resolv.conf")
    DNSaddress = (DNSaddress.split())[7]

    createFile("/etc/systemd/network/10-eth0.netdev", "[Match]\nName=eth0\n\n[Network]\nDHCP=no\n")

    createFile("/etc/systemd/network/11-eth0.network", "[Match]\nName=eth0\n\n[Network]\nAddress="+ serverAddress +"\nDNS="+ DNSaddress +"\n\n[Route]\nGateway="+ firstAddress)

    createFile("/etc/systemd/resolved.conf", "[Resolve]\nDNS="+DNSaddress)


    runSudo('sudo systemctl enable systemd-networkd')
    runSudo(sudo reboot)
    

def runcmd(command):
    stream = os.popen(command)
    output = stream.read()
    return output

def runSudo(commandString):
    cmd = [commandString,'restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != ' ':
        print('unexpected error occured')
        print(errors.decode('ascii'))

def createFile(directroy, contents):
    try:
        f.open(directory, "x")
    except:
        print('\n')
        
    f = open(directory, "w")
    f.write(contents)
    f.close()

main()

