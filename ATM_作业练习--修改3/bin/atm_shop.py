#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import os
import sys

base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))  # 返回文件上一级的上一级绝对路径

sys.path.append(base_dir)  # 添加环境变量

# from conf import settings   # 导入模块
from core import main
from core import shopping


if __name__ == "__main__":
    print ("-*-*-*-*-*-*-*-*-*-*- 欢迎访问ATM购物商城中心 -*-*-*-*-*-*-*-*-*-*-")
    menu = u"""\033[32;1m
        0. 退出系统
        1. 管理员平台
        2. ATM信用卡中心
        3. 购物商城
        \033[0m"""

    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input("请选择操作接口[0=exit]>>>:").strip()
        if user_option == "0":
            print ("\n")
            exit("退出ATM购物商城".center(40,"-"))

        if user_option == "1":
            main.manage_run()

        if user_option == "2":
            main.run()

        if user_option == "3":
            shopping.shop_run()

        else:
            print("\033[41;1m操作错误，请重新输入\033[0m")
            continue


