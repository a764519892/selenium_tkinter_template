import time
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# GUI 程序
def generate_code():
    program_name = program_name_entry.get().strip()
    url = url_entry.get().strip()
    xpath_ip = xpath_ip_entry.get().strip()
    xpath_port = xpath_port_entry.get().strip()

    if not program_name:
        messagebox.showerror("错误", "程序名不能为空！")
        return

    if not url:
        messagebox.showerror("错误", "网址不能为空！")
        return

    if not xpath_ip or not xpath_port:
        messagebox.showerror("错误", "IP 和 Port XPath 不能为空！")
        return

    # 生成的代码模板
    code_template = f"""import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Crawler:
    def __init__(self, url, xpath_ip, xpath_port):
        self.url = url
        self.xpath_ip = xpath_ip 
        self.xpath_port = xpath_port
        self.driver = None

    def start_driver(self):
        options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        options.add_argument(f"user-agent="+user_agent)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')  # 启动时窗口最大化
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options
        )

    def fetch_ip_and_port(self):
        self.driver.get(self.url)
        time.sleep(5)
        ip_elements = self.driver.find_elements(By.XPATH, self.xpath_ip)
        port_elements = self.driver.find_elements(By.XPATH, self.xpath_port)
        ip_port_list = []
        if not ip_elements or not port_elements:
            raise ValueError("未能找到指定的 IP 或 Port 元素")
        for ip, port in zip(ip_elements, port_elements):
            if ip.text and port.text:
                ip_port_list.append(str(ip.text)+":"+str(port.text))
            else:
                print("IP 或 Port 为空，跳过该条记录")
        return ip_port_list

    def close_driver(self):
        if self.driver:
            self.driver.quit()

def main():
    crawler = Crawler("{url}", '''{xpath_ip}''', '''{xpath_port}''')
    crawler.start_driver()
    ip_ports = crawler.fetch_ip_and_port()
    crawler.close_driver()

    file_path = "{program_name}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for ip_port in ip_ports:
            f.write(ip_port + "\\n")
    print(f"IP:Port 已成功写入"+str(file_path))

if __name__ == "__main__":
    main()
"""
    
    # 让用户选择文件保存路径
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    if not file_path:
        return  # 如果用户取消了文件保存

    # 保存为本地文件
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_template)
        messagebox.showinfo("成功", f"代码已保存为 {file_path}")

        # 检查是否清空输入框
        if clear_check_var.get():
            program_name_entry.delete(0, tk.END)
            url_entry.delete(0, tk.END)
            xpath_ip_entry.delete(0, tk.END)
            xpath_port_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("错误", f"文件保存失败: {e}")

# 创建主窗口
root = tk.Tk()
root.title("模板生成器")
root.geometry("400x350")

# 标签和输入框
program_name_label = tk.Label(root, text="程序名:")
program_name_label.pack(pady=5)
program_name_entry = tk.Entry(root, width=40)
program_name_entry.pack(pady=5)

url_label = tk.Label(root, text="目标网址:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

xpath_ip_label = tk.Label(root, text="IP XPath:")
xpath_ip_label.pack(pady=5)
xpath_ip_entry = tk.Entry(root, width=40)
xpath_ip_entry.pack(pady=5)

xpath_port_label = tk.Label(root, text="Port XPath:")
xpath_port_label.pack(pady=5)
xpath_port_entry = tk.Entry(root, width=40)
xpath_port_entry.pack(pady=5)

# 选择框
clear_check_var = tk.BooleanVar(value=True)
clear_check_button = tk.Checkbutton(root, text="保存成功后清空输入框", variable=clear_check_var)
clear_check_button.pack(pady=5)

# 按钮
generate_button = tk.Button(root, text="生成代码", command=generate_code)
generate_button.pack(pady=20)

# 运行主循环
root.mainloop()