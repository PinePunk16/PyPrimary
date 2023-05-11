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
        
        try:
            if not os.path.isdir(self._directory):
                os.mkdir(self._directory)
            
            with open(f"{self._directory}/{self.id}.json", "w") as json_file:
                json.dump(data, json_file, indent = 4)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return None
    # Loads from json. Sets attributes that start with "_" to None, except for saving and loading directory
    def load(self) -> None:
        data: Dict = {}
        try:
            with open(f"{self._directory}/{self.id}.json", "r") as json_file:
                data = json.load(json_file)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return None
        
        for key, value in data.items():
            setattr(self, key, value)
            
        for key, value in self.__dict__.items():
            if key not in data and key != "_directory":
                setattr(self, key, None)
    # Shows the value of all attributes
    def show(self) -> None:
        print("\t".join([f"{key}: {value}" for key, value in self.__dict__.items()]))
    # Loads a random line from a pool file and gives it to the parameter with name passed as string, converting it to its type in the process
    # The pool file for any parameter is "<directory>/pools/<parameter name>.txt"
    def generate_parameter(self, parameter: str) -> None:
        try:
            if not os.path.isdir(f"{self._directory}/pools"):
                os.mkdir(f"{self._directory}/pools")
            if not os.path.isfile(f"{self._directory}/pools/{parameter}.txt"):
                open(f"{self._directory}/pools/{parameter}.txt", 'w').close()
                
            with open(f"{self._directory}/pools/{parameter}.txt", "r") as file:
                setattr(self, parameter, random.choice(file.readlines()).strip())
        except Exception as exception:
            print(f"ERROR: {exception}")
    # Calls the function "generate_parameter" for all parameters, except for "id" and "_directory"
    def generate(self) -> None:
        for key, value in self.__dict__.items():
            if not key == "id" and not key == "_directory":
                self.generate_parameter(key)