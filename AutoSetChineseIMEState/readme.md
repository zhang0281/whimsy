# 锁定输入法状态

一个在 **微软拼音 输入法** 开启时，自动锁定 **中/英** 状态的ahk脚本。

## 使用方法及注意事项

1. 该脚本需要[AutoHotKey2](https://www.autohotkey.com/download/ahk-v2.exe)环境。如有需要请自行编译为EXE。
2. 该脚本第一次运行时需要以管理员权限运行以创建开机自启的快捷方式。开机自启快捷方式的路径为```"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"```。
3. 该脚本启动时会自动将输入法输入状态设置为中文。
4. 该脚本默认您使用Shift来切换 中/英 状态。如果您使用其他按键，请将代码中的
```Shift::```
按键修改为其他按键。如：
```Shift 修改为 ^Space(Ctrl+空格)```。详情可参考 [按键列表](https://wyagd001.github.io/v2/docs/KeyList.htm)。

## 参考链接

[判断微软拼音 中/英 状态](https://blog.csdn.net/wu837449776/article/details/115496353)

[切换输入法状态ahk脚本](https://gist.github.com/maokwen/4d99f5c0aa2e7c0c114c708b03fb73ae)

[开机自启参考](https://blog.csdn.net/liuyukuan/article/details/127557206)

[判断微软拼音是否在运行](https://stackoverflow.com/questions/64280975)