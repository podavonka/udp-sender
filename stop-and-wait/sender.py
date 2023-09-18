import socket
import os
import hashlib
import time
from zlib import crc32



class Colors:
    DIALOG = '\033[95m'
    TEXT = '\033[35m'
    SKIN = '\033[33m'
    SUCC = '\033[42m'
    WAITING = '\033[5m'
    ENDC = '\033[0m'


# TARGET_IP = "192.168.30.18"
# TARGET_PORT = 5555
#
# LOCAL_IP = "192.168.30.19"
# LOCAL_PORT = 6666

#NetDerper
TARGET_IP = "127.0.0.1"
TARGET_PORT = 14000

LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 15001

DESTINATION_ADDRESS = (TARGET_IP, TARGET_PORT)

FOLDER_PATH = ""
FILE_NAME = "chlebopes.jpg"
FILE_PATH = FOLDER_PATH + FILE_NAME

BUFF_SIZE = 1024

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

def sendFileSpeed(fileSize, programSocket, speed):
    with open(FILE_PATH, "rb") as file:
        print(f"    ||{Colors.OKGREEN}The file has been successfully opened.{Colors.ENDC}\n")
        sentBytes = 0
        idx = 1
        print("Sending file")
        while sentBytes < fileSize:

            data = file.read(1014)
            binData = createPacket(data, idx)

            ret = StopNWait(programSocket, binData, idx)
            time.sleep(speed)
            if ret == 100:
                idx -= 1
                continue
            sentBytes += 1014
            print(sentBytes)
            idx += 1

    with open(FILE_PATH, "rb") as file:
        hash = hashlib.md5(file.read())
        print(hash)
        data = createPacket(str(hash).encode('utf-8'), idx)
        print(data)
        StopNWait(programSocket, data, idx)

        ret = StopNWait(programSocket, data, idx)
        if ret == 101:
            sendFile()

def sendFile(fileSize, programSocket):
    with open(FILE_PATH, "rb") as file:
        print(f"    [ {Colors.SUCC}File is ready to be sent.{Colors.ENDC} ]")
        sentBytes = 0
        idx = 1

        time.sleep(0.5)
        print(f"    [ Sending file... ]")

        while sentBytes < fileSize:

            data = file.read(1010)
            binData = createPacket(data, idx)
            print(binData)
            time.sleep(0.35)
            ret = StopNWait(programSocket, binData, idx)
            time.sleep(0.35)
            if ret == 100:
                idx -= 1
                continue
            sentBytes += 1010
            print(sentBytes)
            idx += 1

    with open(FILE_PATH, "rb") as file:
        hash = hashlib.md5(file.read())
        print(hash)
        data = createPacket(hash.hexdigest().encode('utf-8'), idx)
        print(data)
        StopNWait(programSocket, data, idx)



def StopNWait(programSocket, data, idx):
    ackFlag = False

    while not ackFlag:
        print(f"    [ Sending packet #", idx, " ]\n")
        programSocket.sendto(data, DESTINATION_ADDRESS)

        try:
            ack, addr_con = programSocket.recvfrom(8)
            print(ack)
            if ack == b'RECEIVED':
                # print(f"    [ New message: {Colors.OKGREEN} {ack} {Colors.ENDC} ]\n")
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


if __name__ == "__main__":

    # START
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
    info = FILE_NAME + str(fileSize)
    print(f"{Colors.DIALOG}> Now let's send {Colors.ENDC}{FILE_NAME}{Colors.DIALOG} with size of {Colors.ENDC}{fileSize}{Colors.DIALOG} bytes! {Colors.SKIN} (• – •){Colors.ENDC}\n")
    print(f"    [ Bob is sending file properties to Pepa... ]")
    data = createPacket(info, 0)
    StopNWait(programSocket, data, 0)

    sendFile(fileSize,programSocket)

    # END
    programSocket.close()
    time.sleep(1)
    print(f"{Colors.DIALOG}> That's all! File was successfully received (at least I hope).  {Colors.SKIN}〜(꒪–꒪)〜{Colors.ENDC}")
    time.sleep(1)
    print(f"{Colors.DIALOG}> Thank you for visiting me and my brother! See you later!  {Colors.ENDC}")
