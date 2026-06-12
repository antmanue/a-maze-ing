#!/usr/bin/env python3

import random as rand


class Config:
    """Tracks structural setups and validations from setup properties."""
    def __init__(self, file_name: str):
        """Initializes variables and reads external text profiles."""
        self.file_name = file_name
        self.width: int = 0
        self.height: int = 0
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = False
        self.content = ""
        self.valid = True
        self.seed: str = ""
        self.setup()

    def print(self) -> None:
        """Prints current configuration."""
        print(f"WIDTH = {self.width} ({type(self.width)})")
        print(f"HEIGHT = {self.height} ({type(self.height)})")
        print(f"ENTRY = {self.entry} ({type(self.entry[0])}, "
              f"{type(self.entry[1])})")
        print(f"EXIT = {self.exit} ({type(self.exit[0])}, "
              f"{type(self.exit[1])})")
        print(f"OUTPUT_FILE = {self.output_file} ({type(self.output_file)})")
        print(f"PERFECT = {self.perfect} ({type(self.perfect)})")
        print(f"SEED = {self.seed} ({type(self.seed)})")

    def setup(self) -> None:
        """Initialization pipeline to parse configuration text file."""
        try:
            config = self.read_config(self.file_name)
            self.parse_config(config)
        except ConfigError as err:
            print(err)
            exit()
        except ValueError:
            print("Wrong syntax, usage <KEY=VALUE>")
            exit()

    def read_config(self, file_name: str) -> dict[str, str]:
        """Reads text lines to extract valid key-value pairs."""
        with open(file_name) as file:
            config: dict[str, str] = {}
            for line in file.readlines():
                if '#' in line[0]:
                    continue
                line = line.rstrip('\n')
                key, value = line.split('=')
                config[key] = value
            return config

    def parse_config(self, config: dict[str, str]) -> None:
        """Converts and validates parsed keys to appropriate type."""
        expected_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                         "OUTPUT_FILE", "PERFECT"]
        for key in expected_keys:
            self.check_key(key, config)
        try:
            self.width = self.validate_int("WIDTH", config["WIDTH"])
            self.height = self.validate_int("HEIGHT", config["HEIGHT"])
            self.entry = (self.validate_coord("ENTRY", config["ENTRY"]))
            self.exit = (self.validate_coord("EXIT", config["EXIT"]))
            self.validate_entry_exit()
            self.output_file = self.validate_str("OUTPUT_FILE",
                                                 config["OUTPUT_FILE"])
            self.perfect = self.validate_bool("PERFECT", config["PERFECT"])
            if "SEED" in config.keys():
                self.seed = self.validate_str("SEED", config["SEED"])
        except KeyError:
            self.valid = False
        except ConfigError as err:
            print(f"Error found at '{self.file_name}': {err}.")
            self.valid = False
        if not self.valid:
            raise ConfigError("Configuration errors found, exiting program.")

    def check_key(self, key: str, config: dict[str, str]) -> None:
        """Checks for required properties."""
        try:
            config[key] = config[key]
        except KeyError as err:
            print(f'Error found in {self.file_name}: {err} not found')

    def validate_int(self, key: str, value: str) -> int:
        """Ensure integer values for a map."""
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
            print(f"Error found in '{key}' at '{self.file_name}': {err}.")
        return arg

    def validate_coord(self, key: str, value: str) -> tuple[int, int]:
        """Validate each coordinate value and ensure size requirements."""
        x = -1
        y = -1
        try:
            x_str, y_str = value.split(',')
            if not x_str or not y_str:
                raise ConfigError(f"missing value '{value}', expected "
                                  "<int,int>")
            x = self.validate_int(key, x_str)
            y = self.validate_int(key, y_str)
            if x >= self.width:
                raise (ConfigError(f"invalid value '{(x, y)}', x must be "
                                   "less than 'WIDTH'"))
            elif y >= self.height:
                raise (ConfigError(f"invalid value '{(x, y)}', y must be "
                                   "less than 'HEIGHT'"))
        except (ValueError, ConfigError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}.")
        return (x, y)

    def validate_str(self, key: str, value: str) -> str:
        """Confirms provided alpha configurations exists."""
        arg = ""
        try:
            arg = str(value)
            if not arg:
                raise ConfigError(f"{key} is empty")
        except (ValueError, ConfigError, TypeError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}.")
        return arg

    def validate_bool(self, key: str, value: str) -> bool:
        """Converts alphanumeric flags to boolean data."""
        arg = False
        try:
            value = self.bool_str(value)
            arg = bool(value)
        except (ValueError, ConfigError, TypeError) as err:
            self.valid = False
            print(f"Error found in '{key}' at '{self.file_name}': {err}.")
        return arg

    def validate_entry_exit(self) -> None:
        """Ensures distinct coordinates from entrance and exit."""
        try:
            if self.exit == self.entry:
                raise ConfigError("'ENTRY' and 'EXIT' must be different.")
        except ConfigError as err:
            self.valid = False
            print(f"Error found in 'ENTRY'/'EXIT' at "
                  f"'{self.file_name}': {err}")

    @staticmethod
    def bool_str(s: str) -> str:
        """Normalizes string and validate for boolean type."""
        s = s.lower()
        dict_bool = {"false": "", "true": "true"}
        if s in dict_bool:
            return dict_bool[s]
        raise ValueError(f"invalid value '{s}', expected <bool>")


class ConfigError(Exception):
    """Custom exception identifying structural initialization errors."""
    def __init__(self, *args: object) -> None:
        """Initializes baseline exception fields."""
        super().__init__(*args)

    def __str__(self) -> str:
        """Formats exception errors as legible text representations."""
        return super().__str__()
