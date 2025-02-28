import os
import shutil
import time
import tkinter as tk
import traceback
import winreg
from dataclasses import dataclass
from tkinter import messagebox, simpledialog
from typing import List, Optional

import pywinauto
import vdf
from PIL import Image
from pywinauto import Application


@dataclass
class AssetInfo:
    folder: str
    file_name: str
    texture_name: str
    asset_path: str
    is_bundle: bool = False

    def get_full_path(self, base_path: str) -> str:
        return os.path.join(base_path, self.folder, self.file_name)


class SteamPathFinder:
    STEAM_32_KEY = r'SOFTWARE\Valve\Steam'
    STEAM_64_KEY = r'SOFTWARE\Wow6432Node\Valve\Steam'
    LIBRARY_VDF_PATH = r'steamapps\libraryfolders.vdf'
    VS_STEAM_ID = '1794680'

    @staticmethod
    def get_registry_value(key: int, sub_key: str, find_key_name: str = 'InstallPath') -> Optional[str]:
        key_handle = winreg.OpenKey(key, sub_key)
        i = 0
        result = None
        while True:
            try:
                enum = winreg.EnumValue(key_handle, i)
                if enum[0] == find_key_name:
                    result = enum[1]
                i += 1
            except OSError:
                winreg.CloseKey(key_handle)
                break
        return result

    @classmethod
    def get_steam_path(cls) -> Optional[str]:
        steam_path = cls.get_registry_value(winreg.HKEY_LOCAL_MACHINE, cls.STEAM_32_KEY)
        if steam_path is None:
            steam_path = cls.get_registry_value(winreg.HKEY_LOCAL_MACHINE, cls.STEAM_64_KEY)
        return steam_path

    @classmethod
    def get_vs_path(cls, steam_folder: str) -> Optional[str]:
        library_vdf = vdf.load(open(os.path.join(steam_folder, cls.LIBRARY_VDF_PATH)))
        for value in library_vdf.get('libraryfolders').values():
            if cls.VS_STEAM_ID in value.get('apps'):
                result = os.path.join(value.get('path'), 'steamapps')
                vs_acf = vdf.load(open(
                    os.path.join(result, f'appmanifest_{cls.VS_STEAM_ID}.acf')))
                return os.path.join(result, 'common', vs_acf.get('AppState').get('installdir'))
        return None


class UABEAManager:
    def __init__(self):
        self.app = None
        self.app_win32 = None
        self.assets_info = None

    def start(self):
        Application(backend="uia").start('.\\UABE\\UABEAvalonia.exe')
        self.app = Application(backend="uia").connect(path="UABEAvalonia.exe", title="UABEA")
        self.app_win32 = Application(backend="win32").connect(path="UABEAvalonia.exe", title="UABEA")

    def open_file(self, file_path: str):
        uabea = self.app.window(title="UABEA")
        uabea.wait('ready')
        uabea.type_keys("^O")

        open_dialog = self.app_win32.window(title="Open assets or bundle file")
        open_dialog.wait('ready')
        open_dialog.Edit.set_text(file_path)
        time.sleep(0.5)
        open_dialog.Button.click()

        try:
            uabea.window(title="Message Box").MemoryButton.click()
            uabea.info.click()
        except (pywinauto.findwindows.ElementNotFoundError, pywinauto.findbestmatch.MatchError) as err:
            print(f"Warning: {err}")

        self.assets_info = self.app.window(title="Assets Info")

    def export_texture(self, texture_name: str, output_path: str):
        self.assets_info.type_keys("^F")
        search = self.assets_info.window(title="Search")
        search.Edit.set_text(texture_name)
        search.Ok.click()

        self.assets_info.Plugins.click()
        plugins = self.assets_info.child_window(title="Plugins", control_type="Window")
        plugins.ListBox['Export texture'].select()
        plugins.OkButton.click()

        save_dialog = self.app_win32.window(title="Save texture")
        print(output_path)
        save_dialog.Edit.set_text(output_path)
        time.sleep(0.5)
        save_dialog.Button.click()

        try:
            self.app_win32['确认另存为'].type_keys("%Y")
        except (pywinauto.findwindows.ElementNotFoundError, pywinauto.findbestmatch.MatchError) as err:
            print(f"Warning: {err}")

        time.sleep(0.025)

    def import_texture(self, texture_path: str):
        time.sleep(0.5)
        self.assets_info.Plugins.click()
        plugins = self.assets_info.child_window(title="Plugins", control_type="Window")
        plugins.ListBox['Edit texture'].select()
        plugins.OkButton.click()

        texture_edit = self.assets_info.window(title="Texture Edit")
        texture_edit.Load.click()

        open_dialog = self.app_win32.window(title="Open texture")
        open_dialog.Edit.set_text(texture_path)
        open_dialog.Button.click()

        texture_edit.Save.click()
        time.sleep(0.3)
        self.assets_info.type_keys("^S")
        time.sleep(0.3)
        self.assets_info.type_keys("^W")


class TextureModifier:
    @staticmethod
    def modify_alpha(image_path: str, alpha: float):
        img = Image.open(image_path)
        img = img.convert('RGBA')
        x, y = img.size

        for x_num in range(x):
            for y_num in range(y):
                color = img.getpixel((x_num, y_num))
                if color[3] != 0:
                    color = color[:-1] + (int(color[3] * alpha),)
                    img.putpixel((x_num, y_num), color)
        img.save(image_path)


class VFXModifier:
    def __init__(self):
        self.assets: List[AssetInfo] = [
            AssetInfo('VampireSurvivors_Data', 'resources.assets', 'vfx', 'vfx.png'),
            AssetInfo('2887680', 'firstblood_persistent_assets_all.bundle', 'FirstBlood', 'FirstBlood.png', True),
            AssetInfo('3210350', 'thosepeople_persistent_assets_all.bundle', 'ThosePeople', 'ThosePeople.png', True),
            AssetInfo('2690330', 'chalcedony_persistent_assets_all.bundle', 'chalcedony', 'chalcedony.png', True)
        ]
        self.uabea = UABEAManager()

    def modify_texture(self, vs_folder: str, asset: AssetInfo, alpha: float):
        texture_path = os.path.join(os.getcwd(), asset.asset_path)
        if os.path.exists(texture_path):
            os.remove(texture_path)

        self.uabea.start()
        self.uabea.open_file(asset.get_full_path(vs_folder))
        self.uabea.export_texture(asset.texture_name, texture_path)

        TextureModifier.modify_alpha(texture_path, alpha)

        self.uabea.import_texture(texture_path)

    def run(self):
        root = tk.Tk()
        root.withdraw()

        steam_path = SteamPathFinder.get_steam_path()
        if steam_path is None:
            messagebox.showerror('错误', '未找到Steam安装路径')
            return

        vs_folder = SteamPathFinder.get_vs_path(steam_path)
        if vs_folder is None:
            messagebox.showerror('错误', '未找到吸血鬼幸存者安装路径')
            return

        alpha = simpledialog.askfloat('吸血鬼幸存者特效贴图透明度修改工具',
                                      prompt='需要更改的透明度？(0到1之间的小数)',
                                      initialvalue=0.3, minvalue=0, maxvalue=1, parent=root)
        if alpha is None:
            messagebox.showerror('错误', '需要输入一个数字')
            return

        try:
            for asset in self.assets:
                if os.path.exists(asset.get_full_path(vs_folder)):
                    self.modify_texture(vs_folder, asset, alpha)

            messagebox.showinfo('成功', f'已成功将所有特效贴图的透明度设置为{alpha * 100}%')
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror('错误', f'修改过程中发生错误: {str(e)}')
        finally:
            root.destroy()


def main():
    modifier = VFXModifier()
    modifier.run()


if __name__ == '__main__':
    main()
