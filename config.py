#!/usr/bin/env python3


class Config:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.width: int = 0
        self.height: int = 0
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = False
        self.content = self.read_config(file_name)
        self.valid = True

    def print(self) -> None:
        print(f"WIDTH = {self.width} ({type(self.width)})")
        print(f"HEIGHT = {self.height} ({type(self.height)})")
        print(f"ENTRY = {self.entry} ({type(self.entry[0])}, "
              f"{type(self.entry[1])})")
        print(f"EXIT = {self.exit} ({type(self.exit[0])}, "
              f"{type(self.exit[1])})")
        print(f"OUTPUT_FILE = {self.output_file} ({type(self.output_file)})")
        print(f"PERFECT = {self.perfect} ({type(self.perfect)})")

    def setup(self) -> None:
        config = self.read_config(self.file_name)
        self.parse_config(config)

    def read_config(self, file_name: str) -> dict[str, str]:
        with open(file_name) as file:
            config: dict[str, str] = {}
            for line in file.readlines():
                line = line.rstrip('\n')
                key, value = line.split('=')
                config[key] = value
            return config

    def parse_config(self, config: dict[str, str]) -> None:
        self.width = self.validate_int("WIDTH", config["WIDTH"])
        self.height = self.validate_int("HEIGHT", config["HEIGHT"])
        entry = config["ENTRY"].split(',')
        self.entry = (self.validate_int("ENTRY", entry[0]),
                      self.validate_int("ENTRY", entry[1]))
        exit = config["EXIT"].split(',')
        self.exit = (self.validate_int("EXIT", exit[0]),
                     self.validate_int("EXIT", exit[1]))
        self.output_file = self.validate_str("OUTPUT_FILE",
                                             config["OUTPUT_FILE"])
        self.perfect = self.validate_bool("PERFECT", config["PERFECT"])
        if not self.valid:
            raise ConfigError("Configuration errors found, exiting program.")

    def validate_int(self, key: str, value: str) -> int:
        arg = -1
        try:
            arg = int(value)
            if key in ["HEIGHT", "WIDTH"] and arg <= 0:
                raise (ConfigError(f"invalid value '{arg}', expected positive "
                                   "<int>"))
            elif key in ["ENTRY", "EXIT"] and arg < 0:
                raise (ConfigError(f"invalid value '{arg}', expected non "
                                   "negative <int>"))
        except (ValueError, ConfigError, TypeError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}")
            # raise ConfigError(f"Error found in '{key}' at "
            #                   f"'{self.file_name}': {err}") from err
        return arg

    def validate_str(self, key: str, value: str) -> str:
        arg = ""
        try:
            arg = str(value)
        except (ValueError, ConfigError, TypeError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}")
            # raise ConfigError(f"Error found in '{key}' at "
            #                   f"'{self.file_name}': {err}") from err
        return arg

    def validate_bool(self, key: str, value: str) -> bool:
        arg = False
        try:
            value = self.bool_str(value)
            arg = bool(value)
        except (ValueError, ConfigError, TypeError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}")
            # raise ConfigError(f"Error found in '{key}' at "
            #                   f"'{self.file_name}': {err}") from err
        return arg

    @staticmethod
    def bool_str(s: str) -> str:
        s = s.lower()
        dict_bool = {"false": "", "true": "true"}
        if s in dict_bool:
            return dict_bool[s]
        raise ValueError(f"invalid value '{s}', expected <bool>")


class ConfigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()
