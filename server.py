from socket import *
import sqlite3

with socket(AF_INET, SOCK_DGRAM) as s:
    s.bind(('', 12345))
    # create table in SQLite and fill data ----------------------------------------
    with sqlite3.connect('waterStatons.sqlite') as conn:
        conn.execute(
            """
            CREATE TABLE if not exists StationsData (
            sid INTEGER PRIMARY KEY,
            msgdate TEXT,
            msgtime TEXT,
            detector1 TEXT,
            detector2 TEXT
            );
            """
        )
        # main server loop getting data -------------------------------------------------
        while True:
            data, adress = s.recvfrom(1024)
            dataList = data.decode().split()
            if len(dataList) == 5:
                print(dataList)
                station1ID = str(dataList[0])
                station1MsgDate = str(dataList[1])
                station1MsgTime = str(dataList[2])
                station1Det1 = str(dataList[3])
                station1Det2 = str(dataList[4])
                print(station1ID, station1MsgDate, station1MsgTime, station1Det1, station1Det2)
                # try to insert data in SQLite file---------------------------------
                try:
                    # insert data or replace if exist ------------------------------------------
                    with sqlite3.connect('waterStatons.sqlite') as conn:
                        conn.execute(
                            """
                            insert or replace into StationsData (sid, msgdate, msgtime, detector1, detector2)
                            values (?, ?, ?, ?, ?)
                            """, (station1ID, station1MsgDate, station1MsgTime, station1Det1, station1Det2)

                        )
                        s.sendto('The data saved'.encode(), adress)
                except:
                    # retern error to client if DB file could not be opened--------------------------------
                    s.sendto('there is some problems with DB connection, please try again later!'.encode(), adress)
            else:
                # send message to the client if in data miss information--------------------------
                s.sendto('Please check if you filled in all the data and and try to send again.'.encode(), adress)
