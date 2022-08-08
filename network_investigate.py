# -*- coding: utf-8 -*-
# @Time: 2022/6/20 12:21
# @Author: Yaoqi

import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from log import create_log
from datetime import datetime


cwd = os.getcwd()
log = create_log('ping_result_log', 'INFO', True)


# 执行命令部分
def excCmd(cmd):
    """

    Args:
        cmd: command to execute

    Returns: result of the command output

    """
    try:
        log.info(f'The {cmd.strip} command is being executed')
        cmd_raw = [i.strip() for i in cmd.split(' ')]
        cmd_split = [i for i in cmd_raw if i != '']
        cmd_process = subprocess.check_output(cmd_split, shell=True)
        str1 = f'\n------------------- Result of running the {cmd} command -------------------\n'
        str2 = cmd_process.decode('gbk').replace('\r', '')
        res = str1 + str2
    except subprocess.CalledProcessError as e:
        str1 = f'\n------------------- Result of running the {cmd} command -------------------\n'
        str2 = e.output.decode('gbk').replace('\r', '')
        res = str1 + str2
    except Exception as e:
        log.info(f'Error: Command execution error, the specific reason is: {e}')
        os.system('pause')
        return
    return res


def main():
    log.info('Welcome to the ping-line tool')
    dateNow = datetime.now()

    # step1. Obtain the IP address and MAC address
    try:
        log.info('Getting IP and MAC address information ')
        ip_config = subprocess.check_output('ipconfig /all', shell=True)
        ip_config_result = ip_config.decode('utf-8').replace('\r', '')
        f = os.path.join(cwd, f'echo_information_{dateNow.year}{dateNow.month}{dateNow.day}{dateNow.hour}{dateNow.minute}{dateNow.second}.txt')
        with open(f, 'w', encoding='utf-8') as file:
            file.write('------------------- ipconfig echo information -------------------\n')
            file.write(ip_config_result)
        log.info('The IP address and MAC address information are obtained...')
    except Exception as e:
        log.info(f'Error: Run the "ipconfig /all" command to obtain the current network configuration is incorrect. The specific cause: {e}')
        log.info('Tool running interrupted, please press any key to exit, welcome to use next time. ')
        os.system('pause')
        return

    # step2. Obtaining the Default Gateway
    try:
        log.info('Obtaining the Default Gateway ')
        default_gateway = None
        for p_gateway in re.finditer(r'((Default Gateway)|(默认网关))([\s\S\d])+?(\n)', ip_config_result):
            if p_gateway.group(0).split(':')[1].strip() != '':
                default_gateway = p_gateway.group(0).split(':')[1].strip()
        if default_gateway is None:
            log.info(f'The default gateway is missing, the device is not connected to the Internet.')
        else:
            with open(f, 'a', encoding='utf-8') as file:
                file.write(f'\n------------------- Result of extracting the default gateway: {default_gateway} -------------------\n')
                log.info('The default gateway information is extracted successfully...')
            default_gateway_ping = subprocess.check_output(f'ping {default_gateway}', shell=True)
            with open(f, 'a', encoding='utf-8') as file:
                file.write(f'\n>Ping Default gateway information:\n')
                file.write(default_gateway_ping.decode('gbk').replace('\r', ''))
    except Exception as e:
        log.info(f'Error: ping default gateway error, cause: {e}')
        log.info('Tool running interrupted, please press any key to exit, welcome to use next time. ')
        os.system('pause')
        return

    # step3. Execute the command provided by the user
    log.info(f'The command in {os.path.join(cwd, "self-defined_commands.txt")} is being executed ')
    if not os.path.exists(os.path.join(cwd, 'self-defined_commands.txt')):
        log.info(
            f"The {os.path.join(cwd, 'self-defined_commands.txt')} file is missing. Please fill in the command line by line to {os.path.join(cwd, 'self-defined_commands.txt')}")
        url_file = open(os.path.join(cwd, 'self-defined_commands.txt'), 'w')
        url_file.close()
        log.info('Tool running interrupted, please press any key to exit, welcome to use next time. ')
        os.system('pause')
        return

    with open(os.path.join(cwd, 'self-defined_commands.txt'), 'r', encoding='utf-8') as cmd_f:
        cmd_lst = cmd_f.readlines()

    with open(f, 'a', encoding='utf-8') as file:
        file.write(f'\n>The command output is as follows:\n')

    temp = []
    output = []
    cmd_num = len(cmd_lst)

    for i in range(cmd_num):
        output.append(i)
        temp.append(i)

    index1 = 0
    index2 = 0

    # Setting the thread pool
    pool = ThreadPoolExecutor(max_workers=min(cmd_num+1, os.cpu_count()*5))
    for cmd in cmd_lst:
        temp[index1] = pool.submit(excCmd, cmd)
        index1 += 1

    # Store the thread results on the list
    for i in temp:
        output[index2] = i.result()
        index2 += 1

    # Writes a file from a list
    with open(f, 'a', encoding='utf-8') as file:
        for i in output:
            file.write(str(i))

    log.info('Execute the given command to complete...')
    log.info(f'Network diagnosis is complete. Please go to {f} for the results. ')
    os.system('exit')


if __name__ == '__main__':
    main()