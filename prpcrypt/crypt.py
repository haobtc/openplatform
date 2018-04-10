# -*- coding: utf-8 -*-
import base64
import string
import random
import logging

from Crypto import Random
from Crypto.Cipher import AES


class Prpcrypt(object):

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.block_size = 16

    def encrypt(self, text):
        """对明文进行加密
        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """

        IV = Random.new().read(self.block_size)
        text = self.pkcs7_encode(text)
        cryptor = AES.new(self.key, self.mode, IV)
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码

            base64_ciphertext = base64.b64encode(IV + ciphertext)
            base64_ciphertext = str(base64_ciphertext).encode('utf-8')
            return base64_ciphertext
        except Exception as e:
            logging.info('encrypt exception: %s', e, exc_info=True)
            pass

    def decrypt(self, text):
        """对解密后的明文进行补位删除
        @param text: 密文
        @return: 删除填充补位后的明文
        """

        text = base64.b64decode(text)

        IV = text[:self.block_size]
        raw = text[self.block_size:]

        cryptor = AES.new(self.key, self.mode, IV)
        plain_text = cryptor.decrypt(raw)
        plain_text = self.pkcs7_decode(plain_text).decode('utf-8')

        return plain_text

    def get_random_str(self):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        rule = string.ascii_letters + string.digits
        str = random.sample(rule, 16)
        return "".join(str)

    def pkcs7_encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """

        text_length = len(text)

        # 计算需要填充的位数
        padding_length = self.block_size - (text_length % self.block_size)
        text += padding_length * chr(padding_length)

        return text

    def pkcs7_decode(self, text):
        if text:
            return text[:-ord(text[len(text) - 1:])]
        return text
