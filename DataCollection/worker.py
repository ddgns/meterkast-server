import time
import threading
import sqlite3

class collector:
    instance = None
    database = "data.db" # TODO: use the existing database instead of creating a new one
    
    def __init__(self):
        # create the database if it doesn't exist
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Data (type INTEGER, time INTEGER, data INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS DataTypes (type INTEGER, name TEXT, unit TEXT)")
        conn.commit()
        conn.close()

        # make sure only one instance of the collector is running
        if collector.instance is not None:
            raise Exception("Only one instance of the collector can be running at a time")
        collector.instance = self

    def start(self):
        # create a thread that will run in the background and collect data
        thread = threading.Thread(target=self.collect)
        thread.daemon = True
        thread.start()

    def collect(self):
        while True:
            print("Collecting data...") # TODO: create a function that actually collects data
            time.sleep(5)
            self.store_data()

    def store_data(self):
        pass

    def fill_data_types(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("INSERT INTO DataTypes VALUES (0, 'verbruik stand', 'kWh')")
        c.execute("INSERT INTO DataTypes VALUES (1, 'lever stand', 'kWh')")

        c.execute("INSERT INTO DataTypes VALUES (2, 'verbruik', 'kW')")
        c.execute("INSERT INTO DataTypes VALUES (3, 'leveren', 'kW')")

        c.execute("INSERT INTO DataTypes VALUES (4, 'aardgas', 'm3')")
        conn.commit()
        conn.close()
