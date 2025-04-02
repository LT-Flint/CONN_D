# -*- coding: utf-8 -*-
"""


Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.


"""
#import yaml
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
            print(dev['host'] + ' device_ip ' + ' not avaliable')
            return str("~ " + command + " ~ " + "UNDONE")


def send_conf_commands(device, commands, cmd_verify=True):
    try:
        with Netmiko(**device) as ssh:
            ssh.enable()
            out = ssh.send_config_set(commands, cmd_verify=cmd_verify)
            return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print(dev['host'] + ' device_ip ' + ' not avaliable')

def send_huawei_save(device):
    try:
        with Netmiko(**device) as ssh:
            out = ssh.send_command_timing("save", delay_factor=2)
            out += ssh.send_command_timing("Y", delay_factor=2)
            
            #out = ssh.send_config_set(commands, cmd_verify=cmd_verify)
            return out
    except (NetmikoBaseException, NetmikoAuthenticationException, SSHException) as error:
            #print(error)
            print(dev['host'] + ' device_ip ' + ' not avaliable')


if __name__ == "__main__":
    admins_dict = {
        'admin1': 'admin1_PASS',
        'admin2': 'admin2_PASS'
        }
    
    commands_http_cisco = ["no ip http server", "no ip http secure-server"]
    
    admin_pass_cisco = ['username admin5 privilege 15 secret 5 $1$Gjzn$4rU4sT5jxTlWIjEg7KpaE.',
'username admin1 privilege 15 secret 5 $1$7tVe$zu4W6hdA2oI.BDnOw6YMC0',
'username admin3 privilege 15 secret 5 $1$8Fsa$fEmKDnhNa8kOhSd/3fpo2.',
'username admintech privilege 15 secret 5 $1$M8sM$ybMAjGn1wjOl1SYBiOD2f.',
'username admin10 privilege 15 secret 5 $1$uT7n$FEJJCjF6B3hJ0gocEacl4.'
        ]
    admin_pass_huawei = [
        "aaa",
 "local-user admin1 password irreversible-cipher $1a$n$GIY3Q_o=$2cDkY$~9Q&IxJ+9`Bbs$E!m1V*-!PSnF04\"uYZhY$",
 "local-user admin3 password irreversible-cipher $1a$heT,;vA_j$$:h.nSn){\M;tcrN]S:T:4><qWYwL',XyrY>Vi,&($",
 "local-user admin5 password irreversible-cipher $1a$k9J&\"9Ts[O$n$jjO\"f1+Ii2k$1bcCEL~s'GD:lzN$|!7)Qg%c4&$",
 "local-user admin10 password irreversible-cipher $1a$L,yjSWRs6X$AJ\"kCFd|H)v2D_RDlwUO#6SmDMy8^,:PyhB2Ho}'$",
 "local-user admintech password irreversible-cipher $1a$v|R5Hod@c!$P)8gU+-#<\"Gq&$+Oaa'\"@J}M/S2bX83*yUG{$rc1$"
        
        ]
    admin_pass_eltex = [    
    "username admin1 password encrypted fa0493346fcbe36062e179192c28c138ad10445f privilege 15",
    "username admin3 password encrypted db10d0a16c58ee4ec297fa21696311f6d274073b privilege 15",
    "username admin5 password encrypted d4d285c5b1c6fe3e8bc44e910efb17210a0f1ac7 privilege 15",
    "username admin10 password encrypted 740dd218dfb1c15f704099e4da99452c59bcd3b0 privilege 15",
    "username admintech password encrypted 1a9b4fe6e6ac9e622c1de2f321f8bdc113410edc privilege 15"
    ]
    
    commands_http_eltex = [
        "no ip http server"        
        ]


    command_el = "sh clo"
    command_hu = 'dis ip int br'
    
    headers = ['device_type', 'host', 'username', 'password', 'secret','timeout']

    with open('test_dev.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=headers)  # задаём ключи вручную
        devices = [row for row in reader]

    for dev in devices:
        #print(dev)
        if dev['device_type'] == 'eltex':
            #print('Device ip = ' + dev['host'] + ' -> ' + send_conf_commands(dev, "do sh run | i hostna"))
            print(dev['host'] + ' ' + send_show_command(dev, "sh sntp status | i Clock is").strip())
            print(dev['host'] + ' ' + send_show_command(dev, "sh management access-class").strip())
            send_conf_commands(dev, "no ip telnet server")
            
            
            send_conf_commands(dev, commands_http_eltex)
            send_conf_commands(dev, ["line ssh","exec-timeout 9 59"])
            send_conf_commands(dev, admin_pass_eltex, cmd_verify=False)
            print(dev['host'] + ' device_ip ' + '-> DONE eltex')
        elif dev['device_type'] == 'huawei':
            #print(dev['host'] + ' ' + send_show_command(dev, "dis ntp-ser sta | i clock status").strip())
            #print(dev['host'] + ' ' + send_show_command(dev, "dis cur | i acl.*remote-admin-access").strip())
            #print(dev['host'] + ' ' + send_show_command(dev, "dis cur | i ssh server acl").strip())
            #send_conf_commands(dev, ["teln serv dis", "y"], cmd_verify=False)
            
            
            #send_conf_commands(dev, ["user-interface vty 0 4","idle-timeout 9 59"], cmd_verify=False)
            #send_conf_commands(dev, ["undo http server enable", "undo http secure-server enable"], cmd_verify=False)
            #send_conf_commands(dev, admin_pass_huawei, cmd_verify=False)
            
            print(send_huawei_save(dev))
            
            print(dev['host'] + ' device_ip ' + '-> DONE huawei')
        elif dev['device_type'] == 'cisco_ios':
            #print(send_show_command(dev, "show run | i admin"))
            print(dev['host'] + ' ' + send_show_command(dev, "sh ntp status | i Clock is"))
            print(dev['host'] + ' ' + send_show_command(dev, "sh run | i access-class remote-admin-access in"))
            send_conf_commands(dev, ["line vty 0 15","transport input ssh" , "exec-timeout 9 58"])
            
            
            
            send_conf_commands(dev, commands_http_cisco)
            send_conf_commands(dev, admin_pass_cisco)
            print(dev['host'] + ' device_ip ' + '-> DONE cisco')
