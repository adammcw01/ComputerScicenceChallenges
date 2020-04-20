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
    
    runSudo('sudo apt install tcpdump dnsmasq')
    runSudo('sudo systemctl enable dnsmasq')
    runSudo('echo | sudo tee /etc/dnsmasq.conf')

    createFile('/etc/dnsmasq.conf', 'port=0\ndhcp-range='+ broadcastAddress + ',proxy\nlog-dhcp\nenable-tftp\ntftp-root=/tftpboot\npxe-service=0,"Raspberry Pi Boot"')

    runSudo('sudo mkdir /tftpboot')
    runSudo('sudo chmod 777 /tftpboot')
    runSudo('sudo systemctl enable dnsmasq.service')
    runSudo('sudo systemctl restart dnsmasq.service')

    runSudo('cp -r /boot/* /tftpboot')
    runSudo('sudo systemctl restart dnsmasq')

    runSudo('sudo apt install nfs-kernel-server')
    runSudo('echo "/nfs/client1 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports')
    runSudo('echo "/tftpboot *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports')

    runSudo('sudo systemctl enable rpcbind')
    runSudo('sudo systemctl restart rpcbind')
    runSudo('sudo systemctl enable nfs-kernel-server')
    runSudo('sudo systemctl restart nfs-kernel-server')

    createFile('/tftpboot/cmdline.txt','console=serial0,115200 console=tty1 root=/dev/nfs nfsroot='+ serverAddressNoPort +':/nfs/client1,vers=4.1,proto=tcp rw ip=dhcp rootwait elevator=deadline')
    createFile('/nfs/client1/etc/fstab','proc            /proc           proc    defaults          0       0')
    runSudo('echo "'+ serverAddressNoPort +':/tftpboot /boot nfs defaults,vers=4.1,proto=tcp 0 0" | sudo tee -a /nfs/client1/etc/fstab')

    

    
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

##original cmdline.txt contents
##kept just as a note in the event I make a mistake
##
##console=serial0,115200 
##console=tty1 
##root=PARTUUID=97709164-02 
##rootfstype=ext4 
##elevator=deadline 
##fsck.repair=yes 
##rootwait 
##quiet 
##splash 
##plymouth.ignore-serial-consoles

