import win32gui
import win32con

# from pymouse import PyMouse
hwnd_title = {}

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd) and
        win32gui.IsWindowEnabled(hwnd) and
        win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)


for h, t in hwnd_title.items():
    if t :
        if t == 'Skul':
            win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)