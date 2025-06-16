#!/usr/bin/env python3
"""
简单测试八码数图求解器
直接运行 puzzle-8.py 来测试示例
"""

import subprocess
import sys

def test_example():
    """测试示例问题"""
    print("测试八码数图求解器")
    print("示例输入：")
    print("378")
    print("416")
    print("2*5")
    print()
    print("运行 puzzle-8.py 进行测试...")
    print("=" * 50)

    # 运行主程序
    try:
        result = subprocess.run([sys.executable, "puzzle-8.py"],
                              input="378\n416\n2*5\n",
                              text=True,
                              capture_output=True,
                              timeout=30)

        print("程序输出：")
        print(result.stdout)

        if result.stderr:
            print("错误信息：")
            print(result.stderr)

        print(f"程序退出码: {result.returncode}")

    except subprocess.TimeoutExpired:
        print("程序运行超时（30秒）")
    except Exception as e:
        print(f"运行程序时发生错误: {e}")

if __name__ == "__main__":
    test_example()
