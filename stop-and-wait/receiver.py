import time
import socket
import re
import hashlib
from zlib import crc32

class Colors:
    DIALOG = '\033[95m'
    TEXT = '\033[35m'
    SKIN = '\033[33m'
    SUCC = '\033[42m'
    WAITING = '\033[5m'
    ENDC = '\033[0m'


LOCAL_IP = "192.168.30.14"
LOCAL_PORT = 15000

TARGET_IP = "192.168.30.20"
TARGET_PORT = 14001

FULL_ADDRESS = (TARGET_IP, TARGET_PORT)

BUFF_SIZE = 1024

def countPackets(fileSize):
    return int(fileSize / 988)

def checkHash(rHash, receivedData):
    hash = hashlib.md5(receivedData.encode('utf-8')).hexdigest().encode("utf-8")
    if rHash.encode('utf-8') == hash:
        return True
    return False

def checkHashe(rHash, receivedData):
    hash = hashlib.md5(receivedData).hexdigest().encode("utf-8")
    if rHash == hash:
        return True
    return False

def getData(idTemp):
    ackFlag = False
    while not ackFlag:

        data, addr_con = program_socket.recvfrom(1024)

        try:
            idx = int(data[:4])
        except:
            pass
        if idx < idTemp:
            print(f"{Colors.DIALOG}> I already have package #{idx}!  {Colors.SKIN}(ノ•̀o•́)ノ{Colors.ENDC}")
            program_socket.sendto(b'RECEIVED', FULL_ADDRESS)
            continue
        elif idx > idTemp:
            print(f"{Colors.DIALOG}> You are too fast, slow down, Bob!  {Colors.SKIN}(ヘ･_･)ヘ{Colors.ENDC}")
            program_socket.sendto(b'SLOW', FULL_ADDRESS)
            continue


        rHash = data[4:36]
        receivedData = data[36:]


        if checkHashe(rHash, receivedData):
            print(f"{Colors.DIALOG}> Got it! {Colors.SKIN}(~‾▿‾)~{Colors.ENDC}\n")
            print(f"    [ {Colors.SUCC}Package #{idx} received.{Colors.ENDC} ]")
            program_socket.sendto(b'RECEIVED', FULL_ADDRESS)
            ackFlag = True
        else:
            print(f"{Colors.DIALOG}> Hmm, this package is strange... Try it again, Bob! {Colors.SKIN}(‘•⌓•’){Colors.ENDC}\n")
            print(f"    [ Package #{idx} is corrupted. ]\n")
            program_socket.sendto(b'AGAIN', FULL_ADDRESS)


    return receivedData

def getInfo():
    ackFlag = False
    while not ackFlag:
        data, addr_con = program_socket.recvfrom(1024)

        data = data.decode('utf-8')

        idx = data[:4]
        rHash = data[4:36]
        receivedData = data[36:]
        fileSize = int(re.search(r'\d+', receivedData).group())
        fileName = receivedData.replace(str(fileSize),'')



        if checkHash(rHash, receivedData):
            print(f"{Colors.DIALOG}> Got it! {Colors.SKIN}(~‾▿‾)~{Colors.ENDC}\n")
            print(f"    [ {Colors.SUCC}Data properties received.{Colors.ENDC} ]\n")
            program_socket.sendto(b'RECEIVED', FULL_ADDRESS)
        else:
            print(f"{Colors.DIALOG}> Hey, Bob, try it again! {Colors.SKIN}＼(°o°)／{Colors.ENDC}\n")
            print(f"    [ Resending data properties. ]\n")
            program_socket.sendto(b'AGAIN', FULL_ADDRESS)
            continue
        ackFlag = True

    return fileName, fileSize

def receiveFile():
    print(f"    [ Pepa is preparing platform for getting file. ]\n")
    with open(fileName, "wb") as file:
        readBytes = 0
        idx = 1
        while readBytes < fileSize:
            data = getData(idx)
            bytes = file.write(data)
            readBytes += bytes
            print(f"    [ {readBytes} / {fileSize} ]\n")
            idx += 1

    with open(fileName, "rb") as file:
        print(f"{Colors.DIALOG}> Now let me check CRC-32 and that's gonna be all!  {Colors.SKIN}(◍•ᴗ•◍){Colors.ENDC}\n")
        crc = crc32(file.read())
        r_crc = getData(idx)

        if crc != int(r_crc):
            receiveFile()
        else:
            print(f"\n{Colors.DIALOG}> CRC-32 is absolutely the same, congratulations to me and Bob!!!  {Colors.SKIN}(･–･) \(･◡･)/{Colors.ENDC}\n")


if __name__ == "__main__":
    # START of the program
    print(f"{Colors.DIALOG}> Hello, my name is Pepa!  {Colors.SKIN}(◍•ᴗ•◍){Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.DIALOG}> Now me and my brother Bob will help you with sending file via UDP protocol.   {Colors.SKIN}(･–･) \(･◡･)/{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.DIALOG}> Bob is going to throw data to me and i will try to catch it.                    {Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.DIALOG}> He is a bad basketball player, so i don't promise to catch everything.  {Colors.SKIN}乁( •_• )ㄏ{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.DIALOG}> But I will try very hard...  {Colors.ENDC}\n")
    time.sleep(2)

# Creates a new socket
    print(f"    [ {Colors.WAITING}Pepa is trying to create a new socket... {Colors.ENDC}]")
    program_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    program_socket.bind((LOCAL_IP, LOCAL_PORT))
    print(f"    [ {Colors.SUCC}The socket has been created.{Colors.ENDC} ]\n")

    time.sleep(1)

    print(f"{Colors.DIALOG}> Now I am waiting for Bob to send me file properties...{Colors.ENDC}")

    fileName, fileSize = getInfo()

    print(f"{Colors.DIALOG}> Let's get {Colors.ENDC}{fileName}{Colors.DIALOG} with size of {Colors.ENDC}{fileSize}{Colors.DIALOG} bytes! {Colors.SKIN} (• ‿ •){Colors.ENDC} \n")

    receiveFile()

    time.sleep(1)
    print(f"{Colors.DIALOG}> That's all! File was successfully received (at least I hope).  {Colors.SKIN}〜(꒪‿꒪)〜{Colors.ENDC}")
    time.sleep(1)
    print(f"{Colors.DIALOG}> Thank you for visiting me and my brother! See you later!  {Colors.ENDC}")





