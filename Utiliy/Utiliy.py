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
from tkinter import messagebox
from config import Config
from Utiliy.config import Config as Singleton_config


class Utiliy:
    @classmethod
    def messageInfo(cls, title, content):
        messagebox.showinfo(title, content)

    @classmethod
    def messageError(cls, title, content):
        messagebox.showerror(title, content)

    @classmethod
    def getMsize(cls, root:tkinter):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        return Config.main_win_width, Config.main_win_height, (screenwidth - Config.main_win_width) / 2, (screenheight - Config.main_win_height) / 2

    @classmethod
    def gefName(cls, file_name, file_ext):
        return file_ext+'-'+time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

    @classmethod
    def upload(cls, file_path):
        config = cls.get_config_object()
        upload_url = config.get('upload', 'url')
        response = requests.post(url=upload_url, files={'file': open(file_path, 'rb')})
        return response

    @classmethod
    def get_config_object(cls):
        config_path = os.getcwd()+'/config/config.ini'
        if not os.path.exists(config_path):
            cls.messageError("提示", "配置文件不存在")
        else:
            return Singleton_config().config

    @classmethod
    def upload_by_chunk_bak(cls, filepath, *args):
        def callback(monitor):
            print(monitor.bytes_read)

        m = MultipartEncoder(fields={"file": ("img.png", open(filepath, "rb"))},
                             boundary='---------------------------7de1ae242c06ca'
                             )
        data = MultipartEncoderMonitor(m, callback)
        headers = {
            'Content-Type': m.content_type,
        }
        config = cls.get_config_object()
        upload_url = config.get('upload', 'url')
        res = requests.post(upload_url, data=data, headers=headers)
        return res

    @classmethod
    def upload_by_chunk(cls,multipart_data, upload_url, callback, **kwargs):
        data = MultipartEncoderMonitor(multipart_data, callback)
        headers = {
            'Content-Type': multipart_data.content_type,
        }
        res = requests.post(upload_url, data=data, headers=headers, verify=False)
        return res






