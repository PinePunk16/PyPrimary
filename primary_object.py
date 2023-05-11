from typing import Dict, List

import json
import os
import random
import string


class Primary_object:
    # Generates an ID and saves the desired folder. If not given it's assumed as project root
    def __init__(self, directory = "") -> None:
        self._directory_: str = directory
        self.id_: str = ""

        if not os.path.exists(self._directory_):
            os.mkdir(self._directory_)

        while True:
            self.id_ = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            if self.id_ not in os.listdir(self._directory_):
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
            if not os.path.isdir(self._directory_):
                os.mkdir(self._directory_)
            
            with open(os.path.join(self._directory_, f"{self.id_}.json"), "w") as json_file:
                json.dump(data, json_file, indent = 4)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return None       
    # Loads from json. Sets attributes that start with "_" to None, except for saving and loading directory
    def load(self) -> None:
        data: Dict = {}
        try:
            with open(os.path.join(self._directory_, f"{self.id_}.json"), "r") as json_file:
                data = json.load(json_file)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return None
        
        for key, value in data.items():
            if type(getattr(self, key)) == tuple:
                setattr(self, key, tuple(value))
            elif type(getattr(self, key)) == set:
                setattr(self, key, set(value))
            else:
                setattr(self, key, value)
            
        for key, value in self.__dict__.items():
            if key not in data and key != "_directory_":
                setattr(self, key, None)
    # Shows the value of all attributes
    def show(self) -> None:
        print("\t".join([f"{key}: {value}" for key, value in self.__dict__.items()]))   
    # Loads a random line from a pool file and gives it to the parameter with name passed as string, converting it to its type in the process
    # The pool file for any parameter is "<directory>/pools/<parameter name>.txt"
    def generate_parameter(self, parameter: str) -> None:
        try:
            directory_path = os.path.join(self._directory_, "pools")
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            
            file_path = os.path.join(directory_path, f"{parameter}.txt")
            if not os.path.isfile(file_path):
                open(file_path, 'w').close()
                
            with open(file_path, "r") as file:
                lines = file.readlines()
                if lines:
                    setattr(self, parameter, random.choice(lines).strip())
        except Exception as e:
            print(f"ERROR: {e}")
    # Calls the function "generate_parameter" for all parameters, except parameters ending in "_"
    def generate(self) -> None:
        for key, value in self.__dict__.items():
            if not key.endswith("_"):
                self.generate_parameter(key)