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
import csv

#from netmiko import Netmiko
from netmiko import (Netmiko, NetmikoBaseException, NetmikoAuthenticationException)
from paramiko.ssh_exception import SSHException
from rich import inspect

def send_show_command(device, command):
    try:
        with Netmiko(**device) as ssh:
            #inspect(ssh)
            print(ssh.enable())
            print(command)
            out = ssh.send_command(command)
            ssh.exit_enable_mode()
        return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print('Device ip = ' + device['host'] + ' not avaliable')

def send_conf_commands(device, commands):
    try:
        with Netmiko(**device) as ssh:
            ssh.enable()
            out = ssh.send_config_set(commands)
            return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print('Device ip = ' + device['host'] + ' not avaliable')


if __name__ == "__main__":
    admins_dict = {
        'admin1': 'admin1_PASS',
        'admin2': 'admin2_PASS'
        }
    
    commands_http_cisco = ["no ip http server", "no ip http secure-server"]
    
    admin_pass = ['username admin5 privilege 15 secret 5 $1$Gjzn$4rU4sT5jxTlWIjEg7KpaE.',
'username admin1 privilege 15 secret 5 $1$7tVe$zu4W6hdA2oI.BDnOw6YMC0',
'username admin3 privilege 15 secret 5 $1$8Fsa$fEmKDnhNa8kOhSd/3fpo2.',
'username admintech privilege 15 secret 5 $1$M8sM$ybMAjGn1wjOl1SYBiOD2f.',
'username admin10 privilege 15 secret 5 $1$uT7n$FEJJCjF6B3hJ0gocEacl4.'
        
        ]
    
    
    command_el = "sh clo"
    command_hu = 'dis ip int br'
    
    headers = ['device_type', 'host', 'username', 'password', 'secret','timeout']

    with open('test_dev.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=headers)  # задаём ключи вручную
        devices = [row for row in reader]


       
    
    
    
    
    
    
    #with open("devices.yaml") as f:
    #    devices = yaml.safe_load(f)
    for dev in devices:
        print(dev)
        if dev['device_type'] == 'eltex':
            print(send_show_command(dev, "show run | i admin"))

        elif dev['device_type'] == 'huawei':
            print(send_show_command(dev, command_hu))
        elif dev['device_type'] == 'cisco_ios':
            #print(send_show_command(dev, "show run | i admin"))
            send_conf_commands(dev, commands_http_cisco)
            send_conf_commands(dev, admin_pass)
