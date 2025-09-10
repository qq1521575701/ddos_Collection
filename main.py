from flask import Flask,request,jsonify
import config
import ipaddress

app = Flask(__name__)

def is_valid_ip(ip_str):
    """
    验证字符串是否为合法 IPv4 地址
    返回 True 或 False
    """
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except ValueError:
        return False


@app.route('/masscan')
def masscan():

    try:

        ip = request.args.get("ip")

        if not ip:
            return jsonify({"status": "error", "msg": "IP 参数缺失"})
        
        if is_valid_ip(ip) == False:
            return jsonify({"status":"error","msg":"ip错误"})
        
        r = config.scan_ip(ip)

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})
    
    return jsonify({"status": "success", "result": r})


@app.route('/hping3')
def hping3():
    try:
        ip = request.args.get("ip")
        port = request.args.get("port")
        time_sec = request.args.get("time")
        flag = request.args.get("flag")

        flag = flag.upper()

        if not all([ip, port, time_sec, flag]):
            return jsonify({"status": "error", "msg": "缺少必要参数 ip/port/time/flag"})
        
        if is_valid_ip(ip) == False:
            return jsonify({"status":"error","msg":"ip错误"})
        
        if int(port) > 65535 and int(port) < 1:
            return jsonify({'status':'error','msg':"端口输入错误,应为1-65535"})
        
        if int(time_sec) > 1000 and int(time_sec) < 1:
            return jsonify({'status':'error','msg':"时间应该为1-1000秒之间"})

        if flag not in ['A','S','F','R','P','U']:
            return jsonify({'status':'error','msg':"标志位应为'A','S','F','R','P','U'"})

        
        config.hping3(ip,port,time_sec,flag)

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})
    
    return jsonify({"status": "success", "msg": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)



# 调用测试

# http://220.158.234.74:8000/hping3?ip=1.1.1.1&port=80&time=10&flag=a
# http://220.158.234.74:8000/masscan?ip=1.1.1.1
