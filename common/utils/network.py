# -*- coding: utf-8 -*-
"""网络相关工具
时间: 2020/12/5 11:10

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import socket


def ip_connect_check(fqdn, port):
    """
    根据给定的IP和端口判断与目标接口的连通性
    :param fqdn: 符合点分十进制规则的IP地址或者域名
    :param port: 端口号
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((fqdn, int(port)))
    return result == 0
