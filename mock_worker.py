import threading
import time
import random

class Reader:
    port = None
    baudrate = None
    ser = None
    value_store = {}
    weather_data = [
        {
        "plaats": "Spijkenisse",
        "timestamp": 1709547484,
        "time": "04-03-2024 11:18:04",
        "temp": 9.3,
        "gtemp": 8.7,
        "samenv": "Licht bewolkt",
        "lv": 75,
        "windr": "W",
        "windrgr": 279.7,
        "windms": 1.62,
        "windbft": 2,
        "windknp": 3.1,
        "windkmh": 5.8,
        "luchtd": 1012.44,
        "ldmmhg": 759,
        "dauwp": 5.2,
        "zicht": 28700,
        "gr": 524,
        "verw": "Vandaag in het zuidwesten zon. Dinsdag bewolkt en plaatselijk lichte regen",
        "sup": "07:18",
        "sunder": "18:29",
        "image": "lichtbewolkt",
        "alarm": 0,
        "lkop": "Er zijn geen waarschuwingen",
        "ltekst": "Er zijn momenteel geen waarschuwingen van kracht.",
        "wrschklr": "groen",
        "wrsch_g": "-",
        "wrsch_gts": 0,
        "wrsch_gc": "-"
        }
    ]
    translation_table = {
        '1-0:1.8.1': 'verbruik stand 1',
        '1-0:1.8.2': 'verbruik stand 2',
        '1-0:2.8.1': 'lever stand 1',
        '1-0:2.8.2': 'lever stand 2',
        '1-0:1.7.0': 'verbruik',
        '1-0:2.7.0': 'leveren',
        '0-1:24.2.1': 'aardgas'
    }
    
    def __init__(self):
        pass
    
    # function that continuously reads data from the serial port and keeps the connection open
    def read_continuously(self):
        while True:
            for key in self.translation_table.keys():
                self.value_store[self.translation_table[key]] = random.randint(-100, 100)
            
            time.sleep(2)

class collector:
    _instance = None
    database = "data.db" # TODO: use the existing database instead of creating a new one
    reader = Reader()

    def __init__(self):
        pass
        
    def __new__(cls):
      if cls._instance is None:
        cls._instance = super(collector, cls).__new__(cls)
      return cls._instance

    def start(self):
        # create a thread that will run in the background and collect data
        thread = threading.Thread(target=self.collect)
        thread.daemon = True
        thread.start()

    def collect(self):
        # start reading data from the serial port
        self.reader.read_continuously()