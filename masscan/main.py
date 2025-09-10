from pathlib import Path
import os
import subprocess

def scan_ip(ip_address):
    # masscan 可执行文件路径
    masscan_path = Path.cwd() / 'masscan'

    # 检查 masscan 文件是否存在
    if not masscan_path.exists():
        print(f"文件 '{masscan_path}' 不存在。")
        return []

    # 检查文件是否可执行，没有则赋予执行权限
    if not os.access(masscan_path, os.X_OK):
        subprocess.run(['chmod', '+x', str(masscan_path)])

    # 构建 masscan 命令
    command = [
        str(masscan_path),
        ip_address,
        '-p0-65535',
        '--rate', '100000000',
        '--wait', '5'
    ]

    # 执行命令并获取输出，每行作为列表元素
    try:
        output_lines = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        ).stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print("扫描失败:", e)
        return []

    # 解析扫描结果
    open_ports = []
    for line in output_lines:
        line = line.strip()
        if 'open' in line:
            # masscan 输出格式类似: "Discovered open port 22/tcp on 1.2.3.4"
            parts = line.split(' ')
            port_info = parts[3]  # "22/tcp"
            port_number = port_info.split('/')[0]
            open_ports.append(f"{ip_address}:{port_number}")

    return open_ports


# 调用示例
if __name__ == "__main__":
    target_ip = '139.59.183.8'
    open_ports = scan_ip(target_ip)
    print("开放端口:", open_ports)
