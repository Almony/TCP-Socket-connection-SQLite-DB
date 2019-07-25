# API socket connection ---------------------------------------------------------------
from socket import *

SERVER_ADRESS = ('127.0.0.1', 12345)
s = socket(AF_INET, SOCK_DGRAM)

# Current time var --------------------------------------------------------------------
from time import gmtime, strftime
currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

# load file of station data ------------------------------------------------------------
try:
    fileST1 = open("ST1.txt", "r")
    st1ID = fileST1.readline()  # ID of station
    detector1 = fileST1.readline()  # first water detector (1 - full, 0 - empty)
    detector2 = fileST1.readline()  # second water detector (1 - full, 0 - empty)
    fileST1.close()
except(FileNotFoundError):
    print("File not found")

# the func is loading current data on client side--------------------------------------
def load_func():
    global st1ID, detector1, detector2, currentTime
    try:
        with open("ST1.txt", "r") as fileST1:
            st1ID = fileST1.readline()  # ID of station
            detector1 = fileST1.readline()  # first water detector (1 - full, 0 - empty)
            detector2 = fileST1.readline()  # second water detector (1 - full, 0 - empty)
            currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print("date is:", currentTime)
            print("ID station: ", st1ID)
            print("first detector: ", detector1)
            print("second detector: ", detector2)
    except(FileNotFoundError):
        print("File not found")

# the func change status of first detector --------------------------------------------
def first_detector_saver():
    global detector1, detector2, st1ID
    try:
        detector1 = int(input("enter status of first detector(1 - full, 0 - empty)"))
    except(ValueError):
        print("please enter only 0 for empty or 1 for full")
    else:
        if detector1 == 1 or detector1 == 0:
            try:
                with open("ST1.txt", "w") as fileST1:
                    fileST1.write(str(st1ID))
                    # fileST1.write('\n')
                    fileST1.write(str(detector1))
                    fileST1.write('\n')
                    fileST1.write(str(detector2))
                    print("the data is saved!")
            except(FileNotFoundError):
                print("File not found")
        else:
            print("the digit should be 1 or 0 only!")


# the func change status of second detector --------------------------------------------
def second_detector_saver():
    global detector1, detector2, st1ID
    try:
        detector2 = int(input("enter status of first detector(1 - full, 0 - empty)"))
    except(ValueError):
        print("please enter only 0 for empty or 1 for full")
    else:
        if detector2 == 1 or detector2 == 0:
            with open("ST1.txt", "w") as fileST1:
                fileST1.write(str(st1ID))
                # fileST1.write('\n')
                fileST1.write(str(detector1))
                #fileST1.write('\n')
                fileST1.write(str(detector2))
        else:
            print("the digit should be 1 or 0 only!")


def send_data_func():
    global detector1, detector2, st1ID, currentTime, s, SERVER_ADRESS
    currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    try:
        bigDataMsg = st1ID + ' ' + currentTime + ' ' + detector1 + ' ' + detector2
        s.sendto(bigDataMsg.encode(), SERVER_ADRESS)
        # message from server if data is saved ------------------------
        dataList = data, adress = s.recvfrom(1024)
        print("SERVER MESSAGE: ", data.decode())
    except:
        print("The server is not reachable, try to send data later.")


# main loop of client side ------------------------------------------------------------
while True:
    print(
        """
        1) press "L" to load data
        2) press "O" to change status of first water detector
        3) press "T" to change status of second water detector
        4) press "S" to send data
        5) press "Q" to quit
        """
    )
    userOpt = input("Enter your option: ")  # input user option
    userOpt = userOpt.upper()
    if userOpt == 'L' or userOpt == 'O' or userOpt == 'T' or userOpt == 'S' or userOpt == 'Q':  # check of user option
        if userOpt == 'L':
            load_func()
        elif userOpt == 'O':
            first_detector_saver()
        elif userOpt == 'T':
            second_detector_saver()
        elif userOpt == 'S':
            send_data_func()
        elif userOpt == 'Q':
            break
        else:
            print("Unexpected error!!!")
            break
    else:
        print("Invalid option, try again.")

