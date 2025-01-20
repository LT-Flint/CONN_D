# -*- coding: utf-8 -*-
"""


Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.


"""
import yaml
from netmiko import Netmiko

def send_show_command(device, command):
    with Netmiko(**device) as ssh:
        print(ssh.enable())
        out = ssh.send_command(command)
        
    return out

if __name__ == "__main__":
    command_el = "sh ip int"
    command_hu = 'dis ip int br'
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        if dev['device_type'] == 'eltex':
            print(send_show_command(dev, command_el))
        elif dev['device_type'] == 'huawei':
            print(send_show_command(dev, command_hu))
