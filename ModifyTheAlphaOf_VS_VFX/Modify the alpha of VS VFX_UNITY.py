import os
import shutil
import time
import tkinter as tk
import winreg
from tkinter import messagebox, simpledialog

import pywinauto
import vdf
from PIL import Image
from pywinauto import Application

# steam注册表所在位置
steam32key = r'SOFTWARE\Valve\Steam'
steam64key = r'SOFTWARE\Wow6432Node\Valve\Steam'
# 用于存储steam库目录的文件
steamLibraryVdfPath = r'steamapps\libraryfolders.vdf'
# 吸血鬼幸存者steam id
vampire_survivors_steam_id = r'1794680'
# vfx.png相关信息
vs_resources_folder = r'VampireSurvivors_Data'
vs_resources_name = 'resources.assets'
vs_vfx_name = 'vfx.png'


def get_steam_install_folder_by_registry(key: int, sub_key: str, find_key_name: str = 'InstallPath') -> str or None:
    """
    查找指定注册表键的值。
    :param key: 主键
    :param sub_key: 自键
    :param find_key_name: 要查找的Key
    :return: steam的安装路径
    """
    key = winreg.OpenKey(key, sub_key)
    i = 0
    result = None
    while True:
        try:
            # 获取注册表对应位置的键和值
            enum = winreg.EnumValue(key, i)
            if enum[0] == find_key_name:
                result = enum[1]
            i += 1
        except OSError:
            winreg.CloseKey(key)
            break
    return result


def get_steam_install_folder() -> str or None:
    """
    获取steam安装路径。
    :return: steam 安装路径。
    """
    steam_path = get_steam_install_folder_by_registry(winreg.HKEY_LOCAL_MACHINE, steam32key)
    if steam_path is None:
        steam_path = get_steam_install_folder_by_registry(winreg.HKEY_LOCAL_MACHINE, steam64key)
    return steam_path


def get_vampire_survivors_folder(steam_folder: str) -> str or None:
    """
    获取Vampire Survivors的安装路径。
    :param steam_folder: Vampire Survivors安装路径
    :return:
    """
    result = None
    library_vdf = vdf.load(open(os.path.join(steam_folder, steamLibraryVdfPath)))
    for value in library_vdf.get('libraryfolders').values():
        if vampire_survivors_steam_id in value.get('apps'):
            result = os.path.join(value.get('path'), 'steamapps')

            vampire_survivors_acf = vdf.load(open(
                os.path.join(result, 'appmanifest_{vs_steam_id}.acf'.format(vs_steam_id=vampire_survivors_steam_id))))
            result = os.path.join(result, 'common', vampire_survivors_acf.get('AppState').get('installdir'))

    return result


def backup_file(file_folder: str, file_name: str):
    """
    根据路径和文件名备份指定的文件，并且在已经备份的情况下读取备份完毕的文件
    :param file_folder: 文件路径
    :param file_name: 文件名
    :return: 备份后的文件
    """
    file_full_path = os.path.join(file_folder, file_name)

    if os.path.exists(file_full_path):
        file_name, file_extension = os.path.splitext(file_full_path)
        backup_file_path = f"{file_name}_old{file_extension}"
        if not os.path.exists(backup_file_path):
            shutil.copy(file_full_path, backup_file_path)
            print(f"文件备份成功，备份文件名为：{backup_file_path}")
    return file_full_path


def export_vs_vfx_png_file(file_folder: str, file_name: str):
    """
    自动使用UABEA导出vfx.png
    :return: Null
    """
    if os.path.exists(os.path.join(os.getcwd(), vs_vfx_name)):
        os.remove(os.path.join(os.getcwd(), vs_vfx_name))

    # # 备份resources.assets
    resources_path = backup_file(file_folder, file_name)
    # 打开UABE
    Application(backend="uia").start('.\\net6.0\\UABEAvalonia.exe')
    # 连接应用程序
    app = Application(backend="uia").connect(path="UABEAvalonia.exe", title="UABEA")
    appwin32 = Application(backend="win32").connect(path="UABEAvalonia.exe", title="UABEA")
    # 获取窗口
    UABEA = app.window(title="UABEA")
    # 等待加载完成
    UABEA.wait('ready')
    # 点击File->Open Ctrl+O
    UABEA.type_keys("^O")
    # 获取打开文件对话框
    open_vfx_dialog = appwin32.window(title="Open assets or bundle file")
    # 输入路径
    open_vfx_dialog.wait('ready')
    open_vfx_dialog.Edit.set_text(resources_path)
    time.sleep(0.5)
    # 点击 打开 按钮
    open_vfx_dialog.Button.click()
    # 获取资源列表对话框并且唤起搜索
    assets_info = app.window(title="Assets Info")
    assets_info.type_keys("^F")
    # 搜索vfx
    search = assets_info.window(title="Search")
    search.Edit.set_text(vs_vfx_name[:-4])
    search.Ok.click()
    # 导出vfx
    assets_info.Plugins.click()
    plugins = assets_info.child_window(title="Plugins", control_type="Window")
    plugins.ListBox['Export texture'].select()
    plugins.OkButton.click()
    # 获取保存vfx对话框
    save_vfx_dialog = appwin32.window(title="Save texture")
    # 输入路径
    print(os.path.join(os.getcwd(), vs_vfx_name))
    save_vfx_dialog.Edit.set_text(os.path.join(os.getcwd(), vs_vfx_name))
    time.sleep(0.5)
    # 点击 保存 按钮
    save_vfx_dialog.Button.click()
    try:
        appwin32['确认另存为'].type_keys("%Y")
    except pywinauto.findwindows.ElementNotFoundError as Err:
        pass
    except pywinauto.findbestmatch.MatchError as Err:
        pass
    time.sleep(0.025)


def edit_img_alpha(file_folder: str, file_name: str, alpha: float):
    """
    根据alpha修改指定图片的透明度。
    :param file_folder: 文件路径
    :param file_name: 文件名称
    :param alpha: 将透明度修改为指定值(0~1)。
    :return: None
    """
    file_full_path = os.path.join(file_folder, file_name)
    img = Image.open(file_full_path)

    img = img.convert('RGBA')
    x, y = img.size

    for x_num in range(x):
        for y_num in range(y):
            color = img.getpixel((x_num, y_num))
            if color[3] != 0:
                color = color[:-1] + (int(color[3] * alpha),)
                img.putpixel((x_num, y_num), color)
    img.save(file_full_path)


def import_vs_vfx_png_file(vfx_path: str):
    # 连接应用程序
    app = Application(backend="uia").connect(path="UABEAvalonia.exe", title="UABEA")
    appwin32 = Application(backend="win32").connect(path="UABEAvalonia.exe", title="UABEA")
    # 获取资源列表对话框并且唤起搜索
    assets_info = app.window(title="Assets Info")
    time.sleep(0.5)
    assets_info.Plugins.click()
    plugins = assets_info.child_window(title="Plugins", control_type="Window")
    plugins.ListBox['Edit texture'].select()
    plugins.OkButton.click()
    texture_edit = assets_info.window(title="Texture Edit")
    texture_edit.Load.click()
    # 获取打开文件对话框
    open_texture_dialog = appwin32.window(title="Open texture")
    # 输入路径
    open_texture_dialog.Edit.set_text(vfx_path)
    # 点击 打开 按钮
    open_texture_dialog.Button.click()

    texture_edit.Save.click()
    time.sleep(0.5)
    assets_info.type_keys("%W")


def input_alpha(parent_window: tk.Tk) -> float:
    """
    输入透明度
    :return: None
    """
    alpha = simpledialog.askfloat('吸血鬼幸存者特效贴图透明度修改工具',
                                  prompt='需要更改的透明度？(0到1之间的小数)',
                                  initialvalue=0.3, minvalue=0, maxvalue=1, parent=parent_window)
    if alpha is None:
        messagebox.showerror(title='错误', message='需要输入一个数字.')
        exit(1)
    return alpha


def main():
    """
    主函数
    :return: None
    """
    root = tk.Tk()
    steam_path = get_steam_install_folder()
    if steam_path is None:
        print('ERROR: Steam path not found.')
        return

    vampire_survivors_folder = get_vampire_survivors_folder(steam_path)
    if vampire_survivors_folder is None:
        print('ERROR: Vampire Survivors not installed.')
        return

    alpha = input_alpha(parent_window=root)

    export_vs_vfx_png_file(file_folder=os.path.join(vampire_survivors_folder, vs_resources_folder),
                           file_name=vs_resources_name)

    edit_img_alpha(file_folder=os.getcwd(), file_name=vs_vfx_name, alpha=alpha)

    import_vs_vfx_png_file(vfx_path=os.path.join(os.getcwd(), vs_vfx_name))

    tk.messagebox.showinfo('成功', '已成功将vfx.png的透明度设置为{alpha}%'.format(alpha=alpha * 100))


if __name__ == '__main__':
    main()
