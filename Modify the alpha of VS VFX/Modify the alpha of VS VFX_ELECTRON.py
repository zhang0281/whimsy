import os
import winreg
from tkinter import simpledialog, messagebox

import vdf
from PIL import Image

# steam注册表所在位置
steam32key = r'SOFTWARE\Valve\Steam'
steam64key = r'SOFTWARE\Wow6432Node\Valve\Steam'
# 用于存储steam库目录的文件
steamLibraryVdfPath = r'steamapps\libraryfolders.vdf'
# 吸血鬼幸存者steam id
vampire_survivors_steam_id = r'1794680'
# vfx.png相关信息
vs_img_folder = r'resources\app\.webpack\renderer\assets\img'
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
    file_backup_full_path = os.path.join(file_folder, file_name[:-4] + '_old' + file_name[-4:])
    file = Image.open(file_full_path)
    if not os.path.exists(file_backup_full_path):
        file.save(file_backup_full_path)
    else:
        file = Image.open(file_backup_full_path)
    return file


def edit_img_alpha(file_folder: str, file_name: str, alpha: float):
    """
    根据alpha修改指定图片的透明度。
    :param file_folder: 文件路径
    :param file_name: 文件名称
    :param alpha: 将透明度修改为指定值(0~1)。
    :return: None
    """
    file_full_path = os.path.join(file_folder, file_name)

    img = backup_file(file_folder, file_name)

    img = img.convert('RGBA')
    x, y = img.size

    for x_num in range(x):
        for y_num in range(y):
            color = img.getpixel((x_num, y_num))
            if color[3] != 0:
                color = color[:-1] + (int(color[3] * alpha),)
                img.putpixel((x_num, y_num), color)
    img.save(file_full_path)


def input_alpha() -> float:
    """
    输入透明度
    :return: None
    """
    alpha = simpledialog.askfloat('吸血鬼幸存者特效贴图透明度修改工具',
                                  prompt='需要更改的透明度？(0到1之间的小数)(输入1可还原)',
                                  initialvalue=0.3, minvalue=0, maxvalue=1)
    if alpha is None:
        messagebox.showerror(title='错误', message='需要输入一个数字.')
        exit(1)
    return alpha


def main():
    """
    主函数
    :return: None
    """
    steam_path = get_steam_install_folder()
    if steam_path is None:
        print('ERROR: Steam path not found.')
        return
    vampire_survivors_folder = get_vampire_survivors_folder(steam_path)
    if vampire_survivors_folder is None:
        print('ERROR: Vampire Survivors not installed.')
        return
    alpha = input_alpha()
    edit_img_alpha(file_folder=os.path.join(vampire_survivors_folder, vs_img_folder), file_name=vs_vfx_name,
                   alpha=alpha)
    messagebox.showinfo('成功', '已成功将vfx.png的透明度设置为{alpha}%'.format(alpha=alpha * 100))


if __name__ == '__main__':
    main()
