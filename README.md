# UDP-Socket-connection-SQLite-DB

Client:
Client side connects to file witch saves data of station (ID and detector state 0\empty or 1\full)
the user can change the states of detectors on his station and send data to server by TCP connection

Server:
The server gets data, checks and updates table by station ID in SQLite (creates new table if not exist)
