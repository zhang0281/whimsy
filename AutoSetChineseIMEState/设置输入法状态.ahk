; 锁定微软拼音输入法 中/英 状态。防止自动切换。

#Include %A_ScriptDir%
; 扫描隐藏窗口
DetectHiddenWindows(true)

;----------auto start start-------------
autostart := true
autostartLnk := (A_StartupCommon . "\设置输入法状态.lnk")

if (autostart) {
    if FileExist(autostartLnk) {
        FileGetShortcut(autostartLnk, &lnkTarget)
        if (lnkTarget != A_ScriptFullPath)
            FileCreateShortcut(A_ScriptFullPath, autostartLnk, A_WorkingDir)
    } else {
        FileCreateShortcut(A_ScriptFullPath, autostartLnk, A_WorkingDir)
    }
} else {
    if FileExist(autostartLnk) {
        FileDelete(autostartLnk)
    }
}
;----------auto start end-------------

;----------auto set IME state start-------------
; 设置中英文状态的等待时间
timeInterval := 500
; 现在的输入法状态是否是中文
nowImeModeIsChinese := true
; 根据按键设置中英文状态
Shift:: {
    global nowImeModeIsChinese
    
    id := DllCall("imm32\ImmGetDefaultIMEWnd", "Uint", WinGetID("A"), "Uint")
    if (InChsIme(id)) {
        nowImeModeIsChinese := nowImeModeIsChinese ? false : true
    }
}

; 获取是否是中文输入法
InChsIme(id) {
    ; SendMessage(WM_IME_CONTROL, wParam IMC_GETOPENSTATUS, lParam (NoArgs), Control (Window), WinTitle)
    result := SendMessage(0x283, 0x005, 0, , id)
    return result
}
; 获取是否是中文输入模式
InChsImeChineseMode(id) {
    ; SendMessage(WM_IME_CONTROL, wParam IMC_GETCONVERSIONMODE, lParam (NoArgs), Control (Window), WinTitle)
    result := SendMessage(0x283, 0x001, 0, , id)
    return result != 0
}
; 锁定输入法中英文状态
SwitchImeState(id) {
    global nowImeModeIsChinese
    if (nowImeModeIsChinese) {
        ; SendMessage(WM_IME_CONTROL, wParam IMC_SETCONVERSIONMODE, lParam (Chinese), Control (Window), WinTitle)
        SendMessage(0x283, 0x002, 1025, , id)
    } else {
        ; SendMessage(WM_IME_CONTROL, wParam IMC_SETCONVERSIONMODE, lParam (English), Control (Window), WinTitle)
        SendMessage(0x283, 0x002, 0, , id)
    }
}
outer:
    ; 主循环，监控并设置输入法状态
    Loop {
        try {
            ; 获取当前窗口
            hWnd := WinGetID("A")
            id := DllCall("imm32\ImmGetDefaultIMEWnd", "Uint", hWnd, "Uint")
            ; 如果中文输入法在运行且中英文状态与记录的不同时自动设置 中/英 状态为记录的值
            if (InChsIme(id)) {
                if (nowImeModeIsChinese != InChsImeChineseMode(id)) {
                    SwitchImeState(id)
                }
            }
        } catch Error as e {
            Sleep(timeInterval)
            ; 打开 ^Esc,^+Esc 开始菜单弹窗和任务管理器 的时候，可能会报错。
            continue("outer")
        }
        Sleep(timeInterval)
    }
;----------auto set IME state end-------------
