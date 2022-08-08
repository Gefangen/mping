# -*- coding: utf-8 -*-
# @Time: 2022/6/20 16:23
# @Author: Yaoqi

import logging
import datetime
import os


def create_log(func_name, level, stream=False):
    """
    创建日志文件
    Args:
        func_name:
        logger_format:
        level:
        stream:

    Returns:

    """
    if level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'INFO':
        level = logging.INFO
    elif level == 'WARNING':
        level = logging.WARNING
    elif level == 'ERROR':
        level = logging.ERROR
    elif level == 'CRITICAL':
        level = logging.CRITICAL

    logger_format = ('%(levelname)s %(asctime)s '
                     'Pos:%(filename)s[%(lineno)d] '
                     'Msg:%(message)s')

    new_logger = logging.getLogger(func_name)
    new_logger.setLevel(level)
    # log文件路径
    logging_file = os.path.join(os.getcwd(), 'LOG', 'log_' + datetime.datetime.now().strftime('%Y%m%d%H%M') + '.log')
    # 先确保log文件夹存在,不存在即创建
    if not os.path.exists(os.path.join(os.getcwd(), 'LOG')):
        os.mkdir(os.path.join(os.getcwd(), 'LOG'))

    if not os.path.exists(logging_file):
        # 创建 新的log文件,如果这个log文件不存在的话
        open(logging_file, 'a').close()

    fh = logging.FileHandler(logging_file)
    fh.setLevel(level)
    fh_formatter = logging.Formatter(logger_format)
    fh.setFormatter(fh_formatter)
    new_logger.addHandler(fh)
    new_logger.propagate = False
    if stream:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        ch.setFormatter(ch_formatter)
        new_logger.addHandler(ch)
    return new_logger