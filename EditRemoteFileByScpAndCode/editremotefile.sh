#!/bin/bash

# 这个脚本用于编辑远程主机上的文件
# 用法：$(basename $0) -h {host} -p {filePath} -f {fileName}

# 使用getopts工具解析命令行参数，并赋值给相应的变量
while getopts "h:p:f:" opt; do
  case $opt in
    h)
      host=$OPTARG
      ;;
    p)
      file_path=$OPTARG
      ;;
    f)
      file_name=$OPTARG
      ;;
    \?)
      echo "无效选项：-$OPTARG"
      echo "$usage"
      exit 1
      ;;
    :)
      echo "选项 -$OPTARG 需要一个参数"
      echo "$usage"
      exit 1
      ;;
  esac
done

# 定义一个函数，用于编辑远程主机上的文件，接受三个参数：主机名，文件路径和文件名，并在函数名前加上local关键字，以避免污染全局变量
edit_file() {
  # 检查远程主机上是否存在该文件，如果不存在，打印错误信息并退出。使用[[ ]]而不是[ ]来进行条件判断，并且不需要对变量进行引用。
  ssh "$1" "[[ -f /\"$2\"/\"$3\" ]]" || {
    echo "远程主机 $1 上不存在文件 /$2/$3 。"
    exit 1
  }
  
  # 对文件名进行转义，以防止空格或特殊字符导致scp命令出错。使用$()而不是反引号来进行命令替换。
  file_name_escaped=$(printf '%q' "$3")
  
  # 把远程主机上的文件复制到本地目录中，并使用scp工具来同步变化（注意这里没有使用-rsync的选项）
  scp "$1:/$2/$file_name_escaped" "./$file_name_escaped"
  
  # 使用code编辑器在后台打开本地文件，并监控本地文件的变化，并把变化同步到远程主机上。使用printf而不是echo来输出格式化的字符串。
  code "./$file_name_escaped" &
  printf '按 Ctrl-C 停止编辑并退出。\n'
  
  # 捕捉Ctrl-C信号，并杀死后台进程，然后退出。使用双引号来引用变量。
  trap 'printf "正在退出...\n"; kill $!' INT
  
  inotifywait -m -e close_write --format '%w%f' "./$file_name_escaped" | while read f; do
    
    scp "$f" "$1:/$2/$file_name_escaped"
    
    printf "本地文件 %s 已经同步到远程主机 %s 上的 /%s/%s 。\n" "$f" "$1" "$2" "$file_name_escaped"
    
 done &
 wait
 
}
# 调用edit_file函数，并传入相应的参数。使用双引号来引用变量。
edit_file "$host" "$file_path" "$file_name"
