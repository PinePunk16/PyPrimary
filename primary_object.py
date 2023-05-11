# made by PinePunk16 on GitHub

from typing import Dict
import json
import os
import random
import string


# Run "super().__init__(<directory>)" in the constructor of child classes.
# To make different objects be related, in an object store the "id" attribute of the other.
# It's not adviced to change an object's "id".
# To modify the saving and loading directory, modify the "_directory" attribute.

class Primary_object:
    # Generates an ID and saves the desired folder. If not given it's assumed as project root
    def __init__(self, directory = "") -> None:
        self._directory: str = directory
        self.id: int = 0
        
        if not os.path.exists(self._directory):
            os.mkdir(self._directory)
        
        while True:
            self.id = "".join(random.choices(string.ascii_letters + string.digits, k = 12))
            if self.id not in os.listdir(self._directory):
                break
    # Saves to json. Ignores attributes that start with "_"
    def save(self) -> None:
        data: Dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if not isinstance(value, (int, float, str, bool, dict, list, tuple)):
                    value = str(value)
                data[key] = value
        
        with open(f"{self._directory}/{self.id}.json", "w") as json_file:
            json.dump(data, json_file, indent = 4)
    # Loads from json. Sets attributes that start with "_" to None, except for saving and loading directory
    def load(self) -> None:
        data: Dict = {}
        with open(f"{self._directory}/{self.id}.json", "r") as json_file:
            data = json.load(json_file)
    
        for key, value in data.items():
            setattr(self, key, value)
            
        for key, value in self.__dict__.items():
            if key not in data and key != "_directory":
                setattr(self, key, None)
    # Shows the value of all attributes
    def show(instance) -> None:
        print(",   ".join([f"{key}: {value}" for key, value in instance.__dict__.items()]))