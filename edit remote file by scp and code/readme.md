# 远程文件编辑器

这是一个用于编辑远程主机上的文件的bash脚本，它使用scp和code工具来实现文件的同步和编辑。

## 提示以及部分补充说明

* 该脚本完全由Bing AI生成。
* 该脚本的说明，也就是该文件，由Bing AI生成，经过了部分修改以显示正确的格式，以及一些其他说明。
* 如果是windows系统，推荐在wsl环境下使用本脚本。
* 本脚本需要先安装好 ```inotify-tools``` 这个包。并且 code 指令可用。

## 用法

```bash
$(basename $0) -h {host} -p {filePath} -f {fileName}
```
* -h 参数指定远程主机的名称或IP地址。
* -p 参数指定远程文件所在的路径。
* -f 参数指定远程文件的名称。

## 示例
```
./editremotefile.sh -h 192.168.1.100 -p /home/user/documents -f report.txt
```
这个命令会把远程主机192.168.1.100上的/home/user/documents/report.txt文件复制到本地目录中，并使用code编辑器打开。当本地文件发生变化时，会自动同步到远程主机上。按Ctrl-C可以停止编辑并退出。