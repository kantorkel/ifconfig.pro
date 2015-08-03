from flask import Flask, render_template, send_from_directory, request
import os, socket, time, re, logging

socket.setdefaulttimeout(3)

app = Flask(__name__)
app.debug=False
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

def lookup(addr):
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return "No dns record for host", "No dns record for host", "No dns record for host"

@app.route('/')
def main():
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    agent=str(request.user_agent)
    if "curl" in agent:
        return ip + "\n"
    elif "PowerShell" in agent:
        return ip + "\n"
    elif "Wget" in agent:
        return ip + "\n"
    else:
        hostname = lookup(ip)[0]
        return render_template('main.html', 
                ip=ip, 
                hostname=hostname, 
                agent=agent,
                lang=request.accept_languages,
                enco=request.accept_encodings,
                xip=request.access_route[0]
                )
    
    
@app.route('/ip.host')
def iphost():
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    hostname=lookup(ip)[0]
    return ip + " - " + hostname + "\n"

@app.route('/ip')
def ip():
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return ip + "\n"


@app.route('/host')
def host():
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    hostname = lookup(ip)[0]
    return hostname + "\n"


if __name__ == '__main__':
    app.run(host='127.0.0.1')
