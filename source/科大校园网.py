#导入函数库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,os,socket
import yaml

class Login(object):
    def __init__(self,username,passwd,url,interval_time):
        self.__username = username
        self.__passwd = passwd
        self.__url = url
        self.__interval_time = interval_time
        
    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self,value):
        self.__username = value
        
    @property
    def passwd(self):
        return self.__passwd
    @passwd.setter
    def passwd(self,value):
        self.__passwd = value

    @property
    def password(self):
        return self.__passwd
    @passwd.setter
    def password(self,value):
        self.__passwd = value
    
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self,value):
        self.__url = value
    
    @property
    def URL(self):
        return self.__url
    @url.setter
    def URL(self,value):
        self.__url = value
    
    @property
    def interval_time(self):
        return self.__interval_time
    @interval_time.setter
    def interval_time(self,value):
        self.__interval_time = value
    
    def is_net_ok(self):
        s=socket.socket()
        s.settimeout(3)
        try:
            status = s.connect_ex(('www.baidu.com',443))
            if status == 0:
                s.close()
                return True
            else:
                return False
        except Exception as e:
            return False
    
    
    @property
    def net_status(self):
        return self.is_net_ok()
    
    def login(self):
        #导入chrome默认选项
        chrome_options = webdriver.ChromeOptions()
        #无头模式
        chrome_options.add_argument('--headless')

        #设置全屏窗口
        chrome_options.add_argument('--maximize_window')
        browser = webdriver.Chrome(options=chrome_options)
        
        #打开特定链接
        browser.get(self.url)
        login_username = browser.find_element_by_id("uname")
        login_username.send_keys(self.username)
        login_passwd= browser.find_element_by_id("upass")
        login_passwd.send_keys(self.password)
        
#        #保存用户名和密码，并打勾(默认不开启)
        #保存用户名和密码，并打勾(默认不开启)
#        checkbox = browser.find_element_by_name("savePWD")
#        checkbox.click()
        
        #登录
        login_button= browser.find_element_by_css_selector("input[value=登录]")
        login_button.click()  

        #退出浏览器
        browser.quit()

        
    def logout(self):
        #导入chrome默认选项
        chrome_options = webdriver.ChromeOptions()
        #无头模式
        chrome_options.add_argument('--headless')

        #设置全屏窗口
        chrome_options.add_argument('--maximize_window')
        browser = webdriver.Chrome(options=chrome_options)
        
        #打开链接
        browser.get(self.url)
        
        logout_button =  browser.find_elements_by_css_selector('input[value=本机注销]')
        logout_button.click()
        
        #退出浏览器
        browser.quit()
    
    def autologin(self):
        interval_time = self.interval_time
        while True:
            try:
                print(self.is_net_ok())
                if not self.is_net_ok():
                    print("正在登录")
                    self.login()
                    print("登录成功")
            except Exception as e:
                    print(e)
            time.sleep(self.interval_time)

def read_config():
    current_path=os.getcwd()
    config_file=os.path.join(current_path,"config.yaml")

    with open(config_file,"r",encoding='utf-8') as f:
        value = yaml.load(f,Loader=yaml.FullLoader)
    return value

def main():
    config = read_config()
    username = config["username"]
    passwd = config["password"]
    url = config["url"]
    interval_time = config["interval_time"]
    
    lg = Login(username,passwd,url,interval_time)
    lg.autologin()

if __name__ =="__main__":
    main()
