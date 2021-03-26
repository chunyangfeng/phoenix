# -*- coding: utf-8 -*-
"""加密相关工具
时间: 2020/12/5 11:16

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import hashlib
import base64

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from binascii import b2a_hex, a2b_hex

from common.params import AES_SALT


class AesHandler:
    def __init__(self):
        self._salt = AES_SALT
        self._key = self._get_key(self._salt)
        self._iv = b'0000000000000000'
        self._mode = AES.new(self._key, AES.MODE_CBC, self._iv)
        self._block_size = 32

    @staticmethod
    def _get_key(salt):
        """获取key

        Args:
            salt(str): 混淆字符串

        Returns:
            key(str): key
        """
        return base64.b64decode(salt)

    def fill_text(self, text):
        """文本长度不足位的，补充空格至最大位数

        Args:
            text(str): 原始文本

        Returns:
            text(str): 填充后的文本
        """
        if len(text) < self._block_size:
            text += '\0' * (self._block_size - len(text))
        return text.encode("utf-8")

    def encrypt(self, text, salt=None):
        """加密文本

        Args:
            text(str): 原始文本
            salt(str): 混淆字符串，如果不传值则使用默认的混淆字符串

        Returns:
            text(str): 加密后的文本
        """
        key = self._key
        if salt is not None:
            key = self._get_key(salt)
        text = self.fill_text(text)

        mode = AES.new(key, AES.MODE_CBC, self._iv)
        cipher_text = mode.encrypt(text)
        return str(b2a_hex(cipher_text), encoding='utf-8')

    def decrypt(self, text, salt=None):
        """解密文本

        Args:
            text(str): 加密的文本
            salt(str): 混淆字符串，如果不传值则使用默认的混淆字符串

        Returns:
            text(str): 原始文本
        """
        key = self._key
        if salt is not None:
            key = self._get_key(salt)

        mode = AES.new(key, AES.MODE_CBC, self._iv)
        plain_text = mode.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\0")


def get_md5(obj):
    """获取传入的不可变对象的md5

    Args:
        obj(any): 任意的不可变对象

    Returns:
        md5(str): md5
    """
    md5 = hashlib.md5()
    md5.update(obj.encode("utf8"))
    return md5.hexdigest()


def rsa_generate():
    """生成RSA公私钥对

    Returns:
        pubic_key(str): 公钥
        private_key(str): 私钥
    """
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    private_key = rsa.exportKey()  # 生成私钥

    public_key = rsa.publickey().exportKey()  # 生成公钥
    return str(public_key, encoding='utf-8'), str(private_key, encoding='utf-8')


def rsa_encrypt(msg, public_key):
    """RSA加密

    Args:
        msg(str): 待加密文本
        public_key(str): 加密公钥

    Returns:
        result(str): 加密后的文本
    """
    public_key = RSA.import_key(bytes(public_key, encoding='utf-8'))
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')


def rsa_decrypt(msg, private_key):
    """RSA解密

    Args:
        msg(str): 已加密文本
        private_key(str): 私钥

    Returns:
        result(str): 解密后的文本
    """
    private_key = RSA.import_key(bytes(private_key, encoding='utf-8'))
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(msg), 0)
    return back_text.decode('utf-8')


