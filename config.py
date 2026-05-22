#!/usr/bin/env python3


import typing


def read_config(file_name: str) -> dict[str, str]:
    with open(file_name) as file:
        config: dict[str, str] = {}
        for line in file.readlines():
            line = line.rstrip('\n')
            key, value = line.split('=')
            config[key] = value
        return config