#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import os
from core import db_handler
from conf import settings
from core import accounts
import json
import time
import datetime

def acc_auth(account, password):
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    # print(account_file)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                exp_time_stamp = datetime.datetime.strptime(account_data['expire_date'], "%Y-%m-%d")
                status = account_data['status']
                if datetime.datetime.now() > exp_time_stamp:
                    print("\033[31;1mAccount [%s] has expired,please contact the admin to get a new card!\033[0m" % account)
                elif status == 0 or status == 8:  # 状态正常，或者为admin
                    return account_data
                else:
                    print("Account \033[31;1m%s\033[0m] status is abnormal,please contact the admin.")
            else:
                print("\033[31;1m帐号密码输入错误~\033[0m")
    else:
        print("\033[31;1m用户不存在，请重试~\033[0m")


def acc_login(user_data, log_obj):
    exit_count = 3
    retry_count = 0
    same_account = 0
    last_account = ""
    while user_data['is_authenticated'] is not True and retry_count < exit_count:
        account = input("\033[32;1m登录帐号>>>\033[0m:").strip()
        password = input("\033[32;1m登录密码\033[0m:").strip()
        if account == last_account:
            same_account += 1
        auth = acc_auth(account, password)
        last_account = account
        if auth:
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            return auth
        retry_count += 1
    else:
        if same_account == exit_count - 1:
            log_obj.error("用户登录错误次数已经超过3次，帐号已经被锁定")
        exit()


def acc_check(account):
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            status = account_data['status']
            if status == 8:
                print("\033[31;1m[%s]是管理员帐号\033[0m" % account)
                return False

            exp_time_stamp = datetime.datetime.strptime(account_data['expire_date'], "%Y-%m-%d")
            if datetime.datetime.now() > exp_time_stamp:
                print("\033[31;1mAccount [%s] has expired!\033[0m" % account)
                return False
            else:
                return account_data
    else:
        return False


def sign_up():
    """

    :return:
    """
    pay_day = 22
    exist_flag = True
    while exist_flag is True:
        account = input("\033[32;1m请输入注册ID>>>\033[0m:").strip()
        password = input("\033[32;1m请输入注册密码>>>\033[0m:").strip()
        exist_flag = acc_check(account)
        if exist_flag:
            print("\033[31;1m%s用户ID也存在，请注册其他ID~\033[0m" % account)
            exist_flag = True
            continue
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            after_5_years = int(datetime.datetime.now().strftime('%Y')) + 10
            after_5_years_today = datetime.datetime.now().replace(year = after_5_years)
            expire_day = (after_5_years_today + datetime.timedelta(-1)).strftime('%Y-%m-%d')
            account_data = {"enroll_date": today, "balance": 20000, "password": password, "id": account,
                            "credit": 20000, "status": 0, "expire_date": expire_day,"pay_day": pay_day}
            accounts.dump_account(account_data)
            print("用户添加成功,信息详情如下：")
            print (account_data)
            return True


def modify():
    """
    :return:
    """
    # 可以修改的项目
    items = ["password", "credit", "status", "expire_date", "pay_day"]
    acc_data = False
    continue_flag = False
    while acc_data is False:
        account = input("\033[32;1m请输入修改的用户ID>>>\033[0m:").strip()
        account_data = acc_check(account)
        if account_data is False:
            print("输入的用户不存在")
            continue
        else:
            while continue_flag is not True:
                print ('温馨提示：'
                       '修改的项目："password", "credit", "status", "expire_date", "pay_day"'
                       '\n修改格式:{"credit":30000,"pay_day": 23}')
                modify_items = input('请输入修改内容>>>:').strip()
                try:
                    modify_items_dict = json.loads(modify_items)
                except Exception as e:
                    print("\033[31;1m输入的数据格式错误\033[0m")
                    continue

                error_flag = False
                for index in modify_items_dict:
                    if index in items:
                        account_data[index] = modify_items_dict[index]
                    else:
                        print("Your input item [\033[31;1m%s\033[0m] is error!" % index)
                        error_flag = True
                        continue

                if error_flag:
                    continue
                accounts.dump_account(account_data) # 更新到数据库
                time.sleep(2)
                print("\033[32;1m用户数据更新成功！\033[0m")
                print(account_data)
                continue_flag = True
                acc_data = True
    return True