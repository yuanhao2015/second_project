#!/usr/bin/env python
#coding:utf8
import sys
import paramiko
import socket
hostname = sys.argv[1]
port = int(sys.argv[2])
username = sys.argv[3]
ssh_type = sys.argv[4]

if ssh_type == 'PASSWORD':
    password = sys.argv[5]
    cmd = sys.argv[6]
else:
    cmd = sys.argv[5]
#定义日志
success = 'succuss.log'
failure = 'failure.log'
#初始化日志
with open(success,'w+') as s:
    s.write('')
with open(failure,'w+') as f:
    f.write('')
#绑定实例
ssh = paramiko.SSHClient()
#加载本地host主机文件
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    if ssh_type == 'PASSWORD':
        ssh.connect(hostname,port,username,password,timeout=5)
    elif ssh_type == 'SSH_KEY':
        pkey_file = '/root/.ssh/id_rsa'
        key=paramiko.RSAKey.from_private_key_file(pkey_file)
        ssh.connect(hostname,port,username,pkey=key,timeout=5)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd_result = stdout.read(),stderr.read()
    print "\033[32;1m%s执行的结果:\033[0m"% hostname
    if not any(cmd_result):
        print "\033[31;1m命令为空!\033[0m"
        sys.exit(0)
    for line in cmd_result:
        print line,
    with open(success,'a+') as s:
        s.write("%s success \n"% hostname)		
    ssh.close()
except paramiko.AuthenticationException:
    print "\033[31;1m%s AuthenticationException Error!\033[0m"% hostname
    with open(failure,'a+') as f:
        f.write("%s failure \n"% hostname)
except socket.error:
    print "\033[31;1m%s Connection Refused!\033[0m"% hostname
    with open(failure,'a+') as f:
        f.write("%s failure \n"% hostname)
