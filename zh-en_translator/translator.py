'''
有道、百度、腾讯中英互译工具

Created on Aug. 6, 2018
Email: xfffrank@gmail.com
'''

__author__ = 'Feng Xie'

from tkinter import *
from tkinter import ttk
import time
import hashlib
import requests
import json
from threading import Thread
import hmac
import base64
from urllib.parse import quote
import random


class UnitedTranslator(object):
    '''翻译器的后台处理方法
    收集百度、有道、腾讯的机器翻译结果
    
    '''

    def __init__(self, dest):
        """初始化数据
        
        Args:
            dest: 目标翻译语言
        """
        self.lang_from = 'auto'
        self.lang_to = dest
        # self.google_trans = Translator()
        
    def baidu_get_url_encoded_params(self, query_text):
        """按api调用要求拼接url
        
        Args:
            query_text: 待翻译的文本
            
        Returns:
            符合调用接口要求的参数dict
        """
        app_id = 'your_app_id'
        app_secret = 'your_app_secret'
        salt = str(round(time.time() * 1000))
        sign_raw = app_id + query_text + salt + app_secret
        sign = hashlib.md5(sign_raw.encode('utf8')).hexdigest()
        params = {
            'q': query_text,
            'from': self.lang_from,
            'to': self.lang_to,
            'appid': app_id,
            'salt': salt,
            'sign': sign
        }
        return params
    
    def baidu_trans(self, query_text):
        """解析有道api返回的 json 数据
        
        Args:
            query_text: 待翻译的字符串文本
            
        Returns:
            翻译好的文本
        """
        base_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        params = self.baidu_get_url_encoded_params(query_text)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(base_url, headers=headers, params=params).text
        json_data = json.loads(response)
        trans_text = json_data['trans_result'][0]['dst']
        return trans_text
    
    def youdao_get_url_encoded_params(self, query_text):
        """按api调用要求拼接url
        
        Args:
            query_text: 待翻译的文本
            
        Returns:
            符合调用接口要求的参数dict
        """
        app_key = 'your_app_key'
        app_secret = 'your_app_secret'
        salt = str(round(time.time() * 1000))
        sign_raw = app_key + query_text + salt + app_secret
        sign = hashlib.md5(sign_raw.encode('utf8')).hexdigest()
        params = {
            'q': query_text,
            'from': self.lang_from,
            'to': self.lang_to,
            'appKey': app_key,
            'salt': salt,
            'sign': sign
        }
        return params
    
    def youdao_trans(self, query_text):
        """解析有道api返回的 json 数据
        
        Args:
            query_text: 待翻译的字符串文本
            
        Returns:
            翻译好的文本
        """
        base_url = 'https://openapi.youdao.com/api'
        params = self.youdao_get_url_encoded_params(query_text)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(base_url, headers=headers, params=params).text
        json_data = json.loads(response)
        trans_text = json_data['translation'][0]
        return trans_text
    
    # def google_trans(self, query_text):
    #     lang_to = 'zh-CN' if self.lang_to == 'zh' else self.lang_to
    #     google_trans = Translator()
    #     result = google_trans.translate(query_text, dest=lang_to).text
    #     return result
    
    def tencent_get_url_encoded_params(self, query_text):
        action = 'TextTranslate'
        region = 'ap-guangzhou'
        timestamp = int(time.time())
        nonce = random.randint(1, 1e6)
        secret_id = 'your_secret_id'
        secret_key = 'your_secret_key'  # my secret_key
        version = '2018-03-21'
        lang_from = self.lang_from
        lang_to = self.lang_to

        params_dict = {
            # 公共参数
            'Action': action,
            'Region': region,
            'Timestamp': timestamp,
            'Nonce': nonce,
            'SecretId': secret_id,
            'Version': version,
            # 接口参数
            'ProjectId': 0,
            'Source': lang_from,
            'Target': lang_to,
            'SourceText': query_text
        }
        # 对参数排序，并拼接请求字符串
        params_str = ''
        for key in sorted(params_dict.keys()):
            pair = '='.join([key, str(params_dict[key])])
            params_str += pair + '&'
        params_str = params_str[:-1]
        # 拼接签名原文字符串
        signature_raw = 'GETtmt.tencentcloudapi.com/?' + params_str
        # 生成签名串，并进行url编码
        hmac_code = hmac.new(bytes(secret_key, 'utf8'), signature_raw.encode('utf8'), hashlib.sha1).digest()
        sign = quote(base64.b64encode(hmac_code))
        # 添加签名请求参数
        params_dict['Signature'] = sign
        # 将 dict 转换为 list 并拼接为字符串
        temp_list = []
        for k, v in params_dict.items():
            temp_list.append(str(k) + '=' + str(v))
        params_data = '&'.join(temp_list)
        return params_data

    def tencent_trans(self, query_text):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        url_with_args = 'https://tmt.tencentcloudapi.com/?' + self.tencent_get_url_encoded_params(query_text)
        res = requests.get(url_with_args, headers=headers)
        json_res = json.loads(res.text)
        trans_text = json_res['Response']['TargetText']
        return trans_text


class TranslatorGUI(UnitedTranslator):
    '''创建翻译器的GUI
    继承后台处理类 UnitedTranslator，创建GUI组件，完成翻译器程序
    '''

    def __init__(self):
        self.root = Tk()
        self.root.title('中英互译工具')
        self.root.iconbitmap(r'D:\coding\translate\中英互译工具\food.ico')
        self.create_widgets()   # 创建翻译器组件
        self.lang_from = 'auto'  # 源语言检测

    def create_text_frame(self, row, frame_text):
        '''创建文本组件
        
        :param int row: 放在哪一行（布局）
        :param str frame_text: frame 组件的显示名称
        :return: 返回已创建的文本组件类的实例
        :rtype: instance
        '''
        frame = ttk.LabelFrame(self.root, text=frame_text)
        frame.grid(row=row, column=0, padx=10, pady=10, columnspan=3) 
        t = Text(frame, height=8, width=80)
        s = Scrollbar(frame)
        s.config(command=t.yview)
        t.config(yscrollcommand=s.set)
        s.grid(row=row, column=2, sticky='ns')
        t.grid(row=row, column=0, sticky='ns', padx=10, pady=10)
        return t

    def create_widgets(self):
        b1 = ttk.Button(self.root, text='翻译', command=self.get_trans)
        b1.grid(row=1, column=2, padx=10,  pady=10)
        label1 = Label(self.root, text='目标语言：')
        label1.grid(row=1, column=0)
        self.T1 = self.create_text_frame(row=0, frame_text='待翻译文本')
        self.y_res = self.create_text_frame(row=2, frame_text='有道翻译')
        self.b_res = self.create_text_frame(row=3, frame_text='百度翻译')
        self.t_res = self.create_text_frame(row=4, frame_text='腾讯翻译')
        lang = StringVar()
        self.lang_chosen = ttk.Combobox(self.root, textvariable=lang, width=6, state='readonly')
        self.lang_chosen['values'] = ['英文', '中文']     # 设置下拉列表的值
        self.lang_chosen.grid(row=1, column=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
        self.lang_chosen.current(1)    # 设置下拉列表默认显示的值，0为 self.lang_chosen['values'] 的下标值

    def get_trans(self):
        start = time.time()
        lang = self.lang_chosen.get()
        print(lang)
        if lang == None:
            return
        elif lang == '中文':
            self.lang_to = 'zh'
        elif lang == '英文':
            self.lang_to = 'en'
        source_text = self.T1.get(1.0, 'end-1c')
        self.translate(source_text)
        print('翻译用时：', time.time() - start)
        
    def show_result(self, tag, text):
        '''调用翻译接口，在gui中展示结果

        :param str tag: 翻译接口名称
        :param str text: 待翻译文本
        '''
        if tag == 'youdao':
            res = self.youdao_trans(text)
            self.y_res.config(state=NORMAL)
            self.y_res.delete(1.0, END)
            self.y_res.insert(1.0, res)
            self.y_res.config(state=DISABLED)
        elif tag == 'baidu':
            res = self.baidu_trans(text)
            self.b_res.config(state=NORMAL)
            self.b_res.delete(1.0, END)
            self.b_res.insert(1.0, res)
            self.b_res.config(state=DISABLED)
        elif tag == 'tencent':
            res = self.tencent_trans(text)
            self.t_res.config(state=NORMAL)
            self.t_res.delete(1.0, END)
            self.t_res.insert(1.0, res)
            self.t_res.config(state=DISABLED)

    def translate(self, query_text):
        '''多线程调用翻译接口
        
        :param str query_text: 待翻译文本
        '''
        workers = []
        workers.append(Thread(target=self.show_result, args=('youdao', query_text)))
        workers.append(Thread(target=self.show_result, args=('baidu', query_text)))
        workers.append(Thread(target=self.show_result, args=('tencent', query_text)))
        for w in workers:
            w.start()
        # for w in workers:
        #     w.join()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    trans = TranslatorGUI()
    trans.run()