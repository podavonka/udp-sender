import socket
import os
import hashlib
import time
import math
from zlib import crc32



class Colors:
    DIALOG = '\033[95m'
    TEXT = '\033[35m'
    SKIN = '\033[33m'
    SUCC = '\033[42m'
    WAITING = '\033[5m'
    ENDC = '\033[0m'

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


TARGET_IP = "192.168.30.18"
TARGET_PORT = 5555

LOCAL_IP = "192.168.30.19"
LOCAL_PORT = 6666


#NetDerper
# TARGET_IP = "127.0.0.1"
# TARGET_PORT = 14000
#
# LOCAL_IP = "127.0.0.1"
# LOCAL_PORT = 15001

DESTINATION_ADDRESS = (TARGET_IP, TARGET_PORT)

FOLDER_PATH = ""
FILE_NAME = "chlebopes.jpg"
FILE_PATH = FOLDER_PATH + FILE_NAME

BUFF_SIZE = 1024
WINDOW_SIZE = 25

def createPacket(data, idx):
    if idx == 0:
        binData = data.encode("utf-8")
    else:
        binData = data

    binIdx = str(idx).encode("utf-8")
    binIdx = formatIdx(binIdx)

    crc = formatCRC(crc32(binData))

    binCRC = crc.encode("utf-8")

    binData = binIdx + binCRC + binData
    return binData

def formatCRC(crc):
    crc = str(crc)
    while len(crc) != 10:
        crc += '0'
    return crc

def formatIdx(binIdx):
    while len(binIdx) != 4:
        binIdx = b'0' + binIdx
    return binIdx

def sendFileSR(programSocket, filePackages):
    recvdPacks = []
    for i in range(len(filePackages)):
        recvdPacks.append(False)
    print(len(recvdPacks))
    print(recvdPacks)
    winStartId = 0
    while all(recvdPacks) != True:


        recvdPacks = SelectiveRepeat(filePackages,recvdPacks,winStartId)
        print(recvdPacks)


        flag = True
        for i in range(winStartId,WINDOW_SIZE + winStartId):
            if i < len(recvdPacks):
                if recvdPacks[i] == False:
                    flag = False
        if flag:
            winStartId += WINDOW_SIZE
        while recvdPacks[winStartId]:
            if recvdPacks[len(recvdPacks) - 1]:
                break
            winStartId += 1


def SelectiveRepeat(packages, receivedPackages, winStartId):

    for i in range(winStartId, winStartId + WINDOW_SIZE):
        if i < len(packages):
            print(f"    [ Sending packet #", i, f" {packages[i]}]")
            time.sleep(0.15)
            programSocket.sendto(packages[i], DESTINATION_ADDRESS)

    for i in range(winStartId, winStartId + WINDOW_SIZE):
        if i < len(packages):
            try:
                ack, addr_con = programSocket.recvfrom(12)
                print(ack)
                word = ack[:8].decode('utf-8')

                if word == 'RECEIVED':
                    num = ack[8:]
                    num = int(num.decode('utf-8'))
                    print(f"    [ New message: {Colors.OKGREEN} {ack} {Colors.ENDC} ]\n")
                    receivedPackages[num] = True
                else:
                    num = ack[5:]
                    num = int(num.decode('utf-8'))
                    print(f"    [ New message: {Colors.WARNING} {ack} {Colors.ENDC} ]\n")
                    receivedPackages[num] = False

            except:
                # print(f"{Colors.DIALOG}> Pepa, did you get it? I'm sending again.  {Colors.SKIN}(◍•–•◍){Colors.ENDC}\n")
                print(f"    [ TIMEOUT: packet #", i, " ]\n")

    return receivedPackages;

def StopNWait(programSocket, data, idx):
    ackFlag = False

    while not ackFlag:
        # print("sending packet #", idx)
        print(f"    [ Sending packet #", idx, " ]\n")
        programSocket.sendto(data, DESTINATION_ADDRESS)

        try:
            ack, addr_con = programSocket.recvfrom(8)

            if ack == b'RECEIVED':
                print(f"    [ New message: {Colors.OKGREEN} {ack} {Colors.ENDC} ]\n")
                ackFlag = True
            elif ack == b'SLOW':
                print(f"    [ New message: {Colors.WARNING} {ack} {Colors.ENDC} ]\n")
                return 100
            else:
                print(f"    [ New message: {Colors.WARNING} {ack} {Colors.ENDC} ]\n")

        except:
            print(f"{Colors.DIALOG}> Pepa, did you get it? I'm sending again.  {Colors.SKIN}(◍•–•◍){Colors.ENDC}\n")
            print(f"    [ TIMEOUT: trying to resend packet #", idx, " ]")
    return 101

def storePackages(numOfPacks, filePackages):
    with open(FILE_PATH, "rb") as file:
        print(f"    ||{Colors.OKGREEN}The file has been successfully opened.{Colors.ENDC}\n")
        for i in range(numOfPacks):
            data = file.read(1010)
            package = createPacket(data, i+1)
            filePackages.append(package)
        return filePackages


if __name__ == "__main__":

    print(f"{Colors.DIALOG}> Hello, my name is Bob...  {Colors.SKIN}(◍•–•◍){Colors.ENDC}")
    # time.sleep(0.5)
    print(f"{Colors.DIALOG}> Now me and my brother Pepa will help you with sending file via UDP protocol.  {Colors.SKIN}(･–･) \(･◡･)/{Colors.ENDC}")
    # time.sleep(0.5)
    print(f"{Colors.DIALOG}> I am going to throw data to Pepa and he will try to catch it.{Colors.ENDC}\n")
    # time.sleep(2)


    print(f"    [ Bob is trying to create a new socket... ]")
    socket.setdefaulttimeout(1)
    programSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    programSocket.bind((LOCAL_IP, LOCAL_PORT))
    print(f"    [ {Colors.SUCC}The socket has been created.{Colors.ENDC} ]\n")

    time.sleep(1)

    fileSize = os.stat(FILE_NAME).st_size


    info = FILE_NAME + str(math.ceil(fileSize / 1010) + 1)
    print(f"{Colors.DIALOG}> Now let's send {Colors.ENDC}{FILE_NAME}{Colors.DIALOG} with size of {Colors.ENDC}{fileSize}{Colors.DIALOG} bytes! {Colors.SKIN} (• – •){Colors.ENDC}\n")
    print(f"    [ Bob is sending file properties to Pepa... ]")
    packageWithInfo = createPacket(info, 0)
    filePackages = []
    filePackages.append(packageWithInfo)
    numOfPacks = math.ceil(fileSize / 1010)

    filePackages = (storePackages(numOfPacks, filePackages))

    sendFileSR(programSocket, filePackages)

    programSocket.close()
    time.sleep(1)
    print(f"{Colors.DIALOG}> That's all! File was successfully received (at least I hope).  {Colors.SKIN}〜(꒪–꒪)〜{Colors.ENDC}")
    time.sleep(1)
    print(f"{Colors.DIALOG}> Thank you for visiting me and my brother! See you later!  {Colors.ENDC}")
