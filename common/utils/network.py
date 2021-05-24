# -*- coding: utf-8 -*-
"""网络相关工具
时间: 2020/12/5 11:10

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import requests
import socket

from common import params


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


def get_ip_info(ipaddr):
    """获取IP地址相关信息

    Args:
        ipaddr(str): ip地址

    Returns:
        data(dict): IP地址相关信息
    """
    url = f'{params.SeoIpaddressInfoApi}/{ipaddr}?lang=zh-CN'
    try:
        response = requests.get(url)
    except Exception:
        return dict()
    return response.json() if response.status_code == 200 else dict()


def baidu_api_put(site, token, data):
    """Baidu 收录推送

    Args:
        site(str): 推送网站
        token(str): 网站token
        data(list): 推送地址列表

    Returns:
        result(dict): 结果
    """
    headers = {
        'Host': 'data.zz.baidu.com',
        'Content - Type': 'text/plain',
    }
    api = f'{params.SeoBaiduApi}?site={site}&token={token}'
    try:
        response = requests.post(api, headers=headers, data='\n'.join(data), timeout=5)
    except Exception as e:
        return '400', e
    return response.status_code, response.json()


