# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:57
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : ui.py

from Service import Convert
from config import Config
from Utiliy.Utiliy import Utiliy
from functools import partial
from requests_toolbelt import MultipartEncoder
import threading
import os
import filetype


class CmdUtiliy(Utiliy):
    @classmethod
    def messageInfo(cls, title, content):
        msg_body = [title, ":",content]
        msg = "".join(msg_body)
        print(msg)

    @classmethod
    def messageError(cls, title, content):
        msg_body = [title, ":", content]
        msg = "".join(msg_body)
        print(msg)


class Cmdexe(object):

    def __init__(self, blcheckno, file_path):
        self.convert = Convert.Convert(CmdUtiliy)
        self.file_path = file_path
        self.blcheckno = blcheckno

    def tran(self):
        blno = self.blcheckno
        file_path = self.file_path
        if not blno:
            print("请先填写病理号！！")

        if os.path.exists(file_path):
            tran_thr = threading.Thread(target=self.tran_ui, args=(file_path,))
            tran_thr.start()
        else:
            print("该文件不存在请重新上传")


    def callback(self, monitor, png_size):
        progress_num = (monitor.bytes_read / png_size) * 100
        progress_str = str(round(progress_num, 2)) + "%"
        print(progress_str)

    def tran_ui(self, path):
        kind = filetype.guess(path)
        file_mime = kind.mime
        if file_mime != "image/png":
            png_path = self.convert.tran(path)
        else:
            png_path = path
        png_size = os.path.getsize(png_path)
        config = CmdUtiliy.get_config_object()
        upload_url = config.get('upload', 'url')
        blcheckno = self.blcheckno
        fields = {
            "blcheckno": blcheckno,
            "file": ("img.png", open(png_path, "rb")),
        }
        multipart_data = MultipartEncoder(fields=fields, boundary='---------------------------7de1ae242c06ca')
        upload_response = CmdUtiliy.upload_by_chunk(multipart_data, upload_url,
                                                 partial(self.callback, png_size=png_size))
        upload_result = upload_response.json()
        print(upload_result)
        if upload_result:
            if upload_result['code'] == 0:
                CmdUtiliy.messageInfo("提示", "文件已上传至服务器！！")
            elif upload_result['code'] < 0:
                CmdUtiliy.messageError("错误", upload_result["msg"])



