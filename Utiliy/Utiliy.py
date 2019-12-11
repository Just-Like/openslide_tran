# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:45
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : Utiliy.py

import tkinter
import time
import requests
import os
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from threading import Thread
from tkinter import messagebox
from config import Config
from Utiliy.config import Config as Singleton_config


class Utiliy:
    @staticmethod
    def messageInfo(title, content):
        messagebox.showinfo(title, content)

    @staticmethod
    def messageError(title, content):
        messagebox.showerror(title, content)

    @staticmethod
    def getMsize(root:tkinter):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        return Config.main_win_width, Config.main_win_height, (screenwidth - Config.main_win_width) / 2, (screenheight - Config.main_win_height) / 2

    @staticmethod
    def gefName(file_name, file_ext):
        return file_ext+'-'+time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

    @staticmethod
    def upload(file_path):
        config = Utiliy.get_config_object()
        upload_url = config.get('upload', 'url')
        response = requests.post(url=upload_url, files={'file': open(file_path, 'rb')})
        return response

    @staticmethod
    def get_config_object():
        config_path = os.getcwd()+'/config/config.ini'
        if not os.path.exists(config_path):
            Utiliy.messageError("提示", "配置文件不存在")
        else:
            return Singleton_config().config

    @staticmethod
    def upload_by_chunk_bak(filepath, *args):
        def callback(monitor):
            print(monitor.bytes_read)

        m = MultipartEncoder(fields={"file": ("img.png", open(filepath, "rb"))},
                             boundary='---------------------------7de1ae242c06ca'
                             )
        data = MultipartEncoderMonitor(m, callback)
        headers = {
            'Content-Type': m.content_type,
        }
        config = Utiliy.get_config_object()
        upload_url = config.get('upload', 'url')
        res = requests.post(upload_url, data=data, headers=headers)
        return res

    @staticmethod
    def upload_by_chunk(multipart_data, upload_url, callback, **kwargs):
        data = MultipartEncoderMonitor(multipart_data, callback)
        headers = {
            'Content-Type': multipart_data.content_type,
        }
        res = requests.post(upload_url, data=data, headers=headers, verify=False)
        return res






