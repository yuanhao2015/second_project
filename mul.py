#!/usr/bin/env python
#coding:utf8
import multiprocessing
import sys,os,time
result = []
f = file('client.txt')
cmd = sys.argv[1:]
excution_list = []
cmd = ' '.join(cmd)
for line in f.readlines():
    f_line = line.strip().split()
    hostname = f_line[0]
    port = f_line[1]
    username = f_line[2]
    if f_line[3] == 'PASSWORD':
        password = f_line[4]
        call_ssh = 'python remote_ssh.py %s %s %s PASSWORD %s \'%s\'' %(hostname,port,username,password,cmd)
    else:
        call_ssh = 'python remote_ssh.py %s %s %s SSH_KEY \'%s\'' %(hostname,port,username,cmd)
    excution_list.append(call_ssh)

def run_cmd(run_task):
    os.system(run_task)
#定义线程数
p = multiprocessing.Pool(processes=len(excution_list))
for task in excution_list:
    result.append(p.apply_async(run_cmd,(task,)))
p.close()
for res in result:
    res.get(timeout=5)

