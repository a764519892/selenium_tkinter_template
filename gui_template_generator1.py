import os
import tkinter as tk
from tkinter import messagebox

# GUI 程序
def generate_code():
    program_name = program_name_entry.get().strip()
    url = url_entry.get().strip()
    file_path=''
    if not program_name:
        messagebox.showerror("错误", "程序名不能为空！")
        return

    if not url:
        messagebox.showerror("错误", "网址不能为空！")
        return

    # 生成的代码内容
    code_template = f"""import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

# 设置连接到 Docker 中的 Selenium Hub
hub_url = "http://localhost:4444/wd/hub"  # Docker Hub 地址

# 配置浏览器驱动
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 创建远程 WebDriver
driver = webdriver.Remote(
    command_executor=hub_url,
    options=options,
    keep_alive=True
)
# 写入文件
file_path = "{program_name}"+".txt"
try:
    # 访问目标网址
    driver.get("{url}")
    time.sleep(5)  # 等待页面加载

    # 示例 XPath 和 CSS 选择器抓取
    xpath_ip = r'''
    //*[contains(concat( " ", @class, " " ), concat( " ", "kdl-table-tbody", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "kdl-table-cell", " " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]
    '''
    xpath_port = r'''
    //*[contains(concat( " ", @class, " " ), concat( " ", "kdl-table-tbody", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "kdl-table-cell", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]
    '''
    
    css_selector_ip = ''
    css_selector_port= ''

    # 获取 XPath 元素内容
    try:
        xpath_elements_ip = driver.find_elements(By.XPATH, xpath_ip)
        xpath_elements_port = driver.find_elements(By.XPATH, xpath_port)
        print("找到IP" + str(len(xpath_elements_ip)) + "个")
        print("找到PORT" + str(len(xpath_elements_port)) + "个")
        ip_port_zonng=[]
        if len(xpath_elements_ip) == len(xpath_elements_port):
            for i in range(len(xpath_elements_ip)):
                ip_port = str(xpath_elements_ip[i].text) + ":" + str(xpath_elements_port[i].text)
                ip_port_zonng.append(ip_port)
        try:
            # 以写入模式打开文件，如果文件不存在则会创建
            with open(file_path, "w", encoding="utf-8") as f:  # 使用 "a" 以追加模式写入
                for ip in ip_port_zonng:       
                    f.write(ip + "\\n")  # 写入 IP:Port，并换行
            print(f"IP:Port 已成功写入 {file_path}")
        except Exception as e:
            print("写入文件失败:", e)
    except Exception as e:
        print("XPath 抓取失败:", e)

    # 获取 CSS 元素内容
    # 
    # try:
    #     css_elements_ip = driver.find_elements(By.CSS_SELECTOR, css_selector_ip)
    #     css_elements_port = driver.find_elements(By.CSS_SELECTOR, css_selector_port)
    #     print("找到IP"+ str(len(css_elements_ip)) + "个")
    #     print("找到PORT" + str(len(css_elements_port)) + "个")
    #     for css_element in css_elements:
    #         print("CSS 内容:", css_element.get_attribute("content"))
    # except Exception as e:
    #     print("CSS 抓取失败:", e)
    # 
except Exception as e:
    print("访问失败:", e)

finally:
    driver.quit()

"""

    # 保存为本地文件
    file_name = f"{program_name}.py"
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(code_template)
        messagebox.showinfo("成功", f"代码已保存为 {file_name}")
    except Exception as e:
        messagebox.showerror("错误", f"文件保存失败: {e}")

# 创建主窗口
root = tk.Tk()
root.title("模板生成器")
root.geometry("400x200")

# 标签和输入框
program_name_label = tk.Label(root, text="程序名:")
program_name_label.pack(pady=5)
program_name_entry = tk.Entry(root, width=40)
program_name_entry.pack(pady=5)

url_label = tk.Label(root, text="目标网址:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

# 按钮
generate_button = tk.Button(root, text="生成代码", command=generate_code)
generate_button.pack(pady=20)

# 运行主循环
root.mainloop()
