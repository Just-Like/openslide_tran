# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:42
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : Convert.py

import os
import openslide
from Utiliy import Utiliy


class Convert:
    def __init__(self):
        pass

    def tran(self,path):
        print("开始转换！！！！！")
        Utiliy.Utiliy.messageInfo("提示","开始转换！！")
        _,file_name = os.path.split(path)
        file_name = file_name.split('.')[0]
        slide = None
        img = None
        try:
            try:
                slide = openslide.open_slide(path)
            except OSError as e:
                slide = openslide.ImageSlide(path)
            try:
                img = slide.get_thumbnail(slide.dimensions)
            except OverflowError as e:
                img = slide.get_thumbnail((15000,15000))
            img.save(file_name + '.png')
            print("转换成功！！！！！")
            Utiliy.Utiliy.messageInfo("提示","转换成功！！")
        except MemoryError:
            print("文件太大内存不足！！！！！")
            Utiliy.Utiliy.messageError("提示","文件太大内存不足！！")
        except OSError as e:
            print("出现未知错误！！！！！")
            Utiliy.Utiliy.messageError("提示","出现未知错误！！")
        finally:
            print('1')
