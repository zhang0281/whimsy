@echo off
setlocal enabledelayedexpansion

REM 创建输出文件夹
mkdir "%~dp0done"

REM 遍历当前文件夹中的所有mp4文件
for %%f in (*.mp4) do (
    set "filename=%%~nf"
    REM 检查对应的m4a文件是否存在
    if exist "%%~nf.m4a" (
        echo 正在合并 "%%~nf.mp4" 和 "%%~nf.m4a"
        ffmpeg -i "%%~nf.mp4" -i "%%~nf.m4a" -c copy "done/%%~nf.mp4"
    ) else (
        echo 缺少对应的m4a文件: "%%~nf.m4a"
    )
)

echo 完成合并
pause