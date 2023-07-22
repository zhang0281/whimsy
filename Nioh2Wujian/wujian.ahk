;当前窗口是仁王2时
#IfWinActive, ahk_exe nioh2.exe
;鼠标侧键触发
XButton1::
;(XButton1=热鍵)
;自动切换架势
Send {WheelUp Down}
Sleep 30
Send {WheelUp Up}
Sleep 30
;(WheelUp=上架势)
Sleep 80
;触发无间
Send {LShift Down}
Sleep 40
;(以下的时间很重要)
Send {LButton Down}
Sleep 40
Send {LButton Up}
Sleep 40
Send {LShift Up}
Sleep 1253
;第一段加速
Send {LButton Down}
Sleep 40
Send {LButton Up}
Sleep 890
;第二段加速
if not getkeystate("XButton1","P")
return
Send {LButton Down}
Sleep 40
Send {LButton Up}
Sleep 790
;第三段加速
if not getkeystate("XButton1","P")
return
Send {LButton Down}
Sleep 40
Send {LButton Up}
Sleep 890
;第四段加速
if not getkeystate("XButton1","P")
return
Send {LButton Down}
Sleep 40
Send {LButton Up}
Sleep 40
return
;(LShift=防御)
;(LButton=轻攻击)
#IfWinActive