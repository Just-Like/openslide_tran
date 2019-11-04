# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:42
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : Convert.py


import os
prefix_path = ''
if __name__ == '__main__':
    prefix_path = ".."
else:
    prefix_path = os.getcwd()
openslide_bin_path = prefix_path + r'\ext_package\openslide-win64-20171122\bin'
os.environ['path'] = os.environ['path'] + ';' + openslide_bin_path

import subprocess
import openslide
from Utiliy import Utiliy


class Convert:
    def __init__(self):
        pass

    def tran(self, path):
        Utiliy.Utiliy.messageInfo("提示", "开始转换！！")
        _, file_name = os.path.split(path)
        file_name, file_ext = file_name.split('.')

        if file_ext != 'kfb':
            self.tran_standard_slide(path,file_name)
        else:
            self.tran_kfb_slide(path,file_name)

    def tran_standard_slide(self, path, file_name):
        file_name = prefix_path + '\\pngs\\' + file_name
        try:
            try:
                slide = openslide.open_slide(path)
            except OSError as e:
                slide = openslide.ImageSlide(path)
            try:
                img = slide.get_thumbnail(slide.dimensions)
            except OverflowError as e:
                img = slide.get_thumbnail((15000, 15000))
            img.save(file_name + '.png')
            print("转换成功！！！！！")
            Utiliy.Utiliy.messageInfo("提示", "转换成功！！")
        except MemoryError:
            print("文件太大内存不足！！！！！")
            Utiliy.Utiliy.messageError("提示", "文件太大内存不足！！")
        except OSError as e:
            print("出现未知错误！！！！！")
            Utiliy.Utiliy.messageError("提示", "出现未知错误！！")
        finally:
            print('1')

    def tran_kfb_slide(self, path, file_name):
        finsh_flag = False
        save_path = prefix_path + '\\kfb_temp\\' + file_name+'.svs'
        print(save_path)
        kfb2tif_exe_path = prefix_path + r'\ext_package\kfb2tif\KFbioConverter.exe'
        kfb2tif_exe_exists = os.path.exists(kfb2tif_exe_path)
        if not kfb2tif_exe_exists:
            print('KFbioConverter.exe工具不存在')
        comm_str = '{} {} {} 2'.format(kfb2tif_exe_path, path, save_path)
        obj = subprocess.Popen(comm_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # for item in iter(obj.stdout.readline, 'b'):
        #     if item:
        #         encode_type = chardet.detect(item)
        #         if encode_type['encoding'] == 'utf-8':
        #             print(item.decode('utf-8'))
        #         elif encode_type['encoding'] == 'Windows-1252':
        #             print(item.decode('Windows-1252'))
        #         else:
        #             print(item.decode('gbk'))
        if 'OK...转换完成' in obj.stdout.read().decode('gbk'):
            finsh_flag = True
            print("kfb2svs成功")
        if finsh_flag:
            self.tran(save_path)

