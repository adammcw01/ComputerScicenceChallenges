import os
import subprocess


def main():
    doesDirectExist = bool(checkForDirectory())
    if doesDirectExist == True:
        print('The directory already exists')
        confirmAction()
        
    makeDirectory()

    createNFS()
    RegenSSHKeys = ['cd /nfs/client1', 'sudo mount --bind /dev dev', 'sudo mount --bind /sys sys', 'sudo mount --bind /proc proc', 'sudo chroot .', 'rm /etc/ssh/ssh_host_*', 'dpkg-reconfigure openssh-server', 'exit', 'sudo umount dev sys proc']
    for x in RegenSSHKeys:
        runCommand(x)

    raise SystemExit

def confirmAction():
    while True:
        confirmInput = input("Would you like to continue (Y/N)")
        if confirmInput == "Y" or confirmInput == "y":
            return
        elif confirmInput == "N" or confirmInput == "n":
            raise SystemExit


def checkForDirectory():
    stream = os.popen('[ -e /nfs ]&& echo 1 || echo 0')
    output = str(stream.read())
    output = output.strip()
    if output == '1':
        return True
    else:
        return False

def makeDirectory():
    cmd = ['sudo mkdir -p /nfs/client1','restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != '':
        print('unexpected error occured')
        print(errors.decode('ascii'))

def createNFS():
    cmd = ['sudo apt install rsync','restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != '':
        print('unexpected error occured')
        print(errors.decode('ascii'))
    cmd = ['sudo rsync -xa --progress --exclude /nfs / /nfs/client1','restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != '':
        print('unexpected error occured')
        print(errors.decode('ascii'))

def runCommand(commandString):
    cmd = [commandString,'restart']
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if errors.decode('ascii') != '':
        print('unexpected error occured')
        print(errors.decode('ascii'))

main()
