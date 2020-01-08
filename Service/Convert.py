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


class Convert:
    def __init__(self, utiliy):
        self.utiliy = utiliy

    def tran(self, path, show_message=1):
        if show_message:
            self.utiliy.messageInfo("提示", "开始转换！！")
        _, file_name = os.path.split(path)
        file_name, file_ext = file_name.split('.')

        if file_ext != 'kfb':
            png_path = self.tran_standard_slide(path, file_name, file_ext)
        else:
            temp_svs_path = self.tran_kfb_slide(path, file_name)
            png_path = self.tran_standard_slide(temp_svs_path, file_name, file_ext)
        return png_path

    def tran_standard_slide(self, path, file_name, file_ext):
        file_name = self.utiliy.gefName(file_name, file_ext)
        file_name = prefix_path + '\\pngs\\' + file_name
        if not os.path.isdir(prefix_path + '\\pngs\\'):
            os.mkdir(prefix_path + '\\pngs\\')
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
            self.utiliy.messageInfo("提示", "转换成功！！")
            return file_name + '.png'
        except MemoryError:
            print("文件太大内存不足！！！！！")
            self.utiliy.messageError("提示", "文件太大内存不足！！")
        except OSError as e:
            print("出现未知错误！！！！！")
            self.utiliy.messageError("提示", "出现未知错误！！")
        finally:
            pass

    def tran_kfb_slide(self, path, file_name):
        finsh_flag = False
        save_path = prefix_path + '\\kfb_temp\\' + file_name+'.svs'
        if not os.path.exists(prefix_path + '\\kfb_temp\\'):
            os.mkdir(prefix_path + '\\kfb_temp\\')
        kfb2tif_exe_path = prefix_path + r'\ext_package\kfb2tif\KFbioConverter.exe'
        kfb2tif_exe_exists = os.path.exists(kfb2tif_exe_path)
        if not kfb2tif_exe_exists:
            self.utiliy.messageError("提示", "KFbioConverter.exe工具不存在！！")
        comm_str = '{} {} {} 2'.format(kfb2tif_exe_path, path, save_path)
        obj = subprocess.Popen(comm_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if 'OK...转换完成' in obj.stdout.read().decode('gbk'):
            finsh_flag = True
        if finsh_flag:
            return save_path

