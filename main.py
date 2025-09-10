from masscan.main import scan_ip
from flask import Flask, request

app = Flask(__name__)

@app.route('/scanip', methods=['GET'])
def scanip():
    ip = request.args.get('ip')

    try:
        r = scan_ip(ip)
    except:
        return "error"

    return r

# 主程序入口
if __name__ == '__main__':
    # debug=True 可以自动重载，方便开发
    app.run(host='0.0.0.0', port=8000, debug=True)
