import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO

# 默认的服务器地址
default_server_address = "0.0.0.0:7777（请修改为您想下载的网站的地址）"
search_url = f"http://{default_server_address}/content/search"
get_data_url = f"http://{default_server_address}/content/getData"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=utf-8"
}


class PDFDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("历史文献下载器")
        self.root.geometry("500x450")  # 缩小窗口大小
        self.root.resizable(False, False)

        # 设置默认的样式
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 9))
        self.style.configure("TButton", font=("Arial", 9), padding=5)
        self.style.configure("TEntry", font=("Arial", 9), padding=4)
        self.style.configure("TCombobox", font=("Arial", 9), padding=4)
        self.style.configure("TListbox", font=("Arial", 9), selectbackground="#D1E7DD")
        self.style.configure("TScrollbar", thickness=10)

        # 顶部服务器地址框
        self.server_frame = ttk.Frame(root, padding=5)
        self.server_frame.pack(fill="x", padx=5, pady=10)

        ttk.Label(self.server_frame, text="服务器地址:").pack(side="left", anchor="w", padx=5)
        self.server_entry = ttk.Entry(self.server_frame, width=30)
        self.server_entry.pack(side="left", padx=5)
        self.server_entry.insert(0, default_server_address)

        self.update_server_button = ttk.Button(self.server_frame, text="更新地址", command=self.update_server_address)
        self.update_server_button.pack(side="left", padx=5)

        # 搜索设置框
        self.search_frame = ttk.Frame(root, padding=5)
        self.search_frame.pack(fill="x", padx=5)

        ttk.Label(self.search_frame, text="选择类别:").grid(row=0, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.search_frame, textvariable=self.category_var, state="readonly", width=10)
        self.category_menu['values'] = ("文书集", "单册文书", "零散单页")
        self.category_menu.grid(row=0, column=1, padx=5)
        self.category_menu.current(2)

        ttk.Label(self.search_frame, text="搜索内容:").grid(row=0, column=2, sticky="w", pady=5)
        self.search_entry = ttk.Entry(self.search_frame, width=20)
        self.search_entry.grid(row=0, column=3, padx=5)

        self.search_button = ttk.Button(self.search_frame, text="搜索", command=self.search_records)
        self.search_button.grid(row=0, column=4, padx=5)

        # 搜索结果框
        self.result_frame = ttk.Frame(root, padding=5)
        self.result_frame.pack(fill="both", padx=5, pady=10, expand=True)

        self.result_listbox = tk.Listbox(self.result_frame, width=50, height=8, selectmode=tk.MULTIPLE, font=("Arial", 9))
        self.result_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.result_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_listbox.yview)
        self.result_listbox.config(yscrollcommand=self.result_scrollbar.set)
        self.result_scrollbar.pack(side="right", fill="y")

        # 下载按钮
        self.download_button = ttk.Button(root, text="下载选中记录", command=self.download_selected_records)
        self.download_button.pack(pady=10)

        # 状态显示和进度条
        self.status_frame = ttk.Frame(root, padding=5)
        self.status_frame.pack(fill="x", padx=5, pady=10)

        self.status_label = ttk.Label(self.status_frame, text="状态: 等待操作", foreground="green")
        self.status_label.pack(anchor="w", pady=5)

        self.progressbar = ttk.Progressbar(self.status_frame, orient="horizontal", length=400, mode="determinate")
        self.progressbar.pack(fill="x", padx=5, pady=5)

        self.records = []  # 保存搜索结果

    def update_server_address(self):
        """更新服务器地址"""
        global search_url, get_data_url
        server_address = self.server_entry.get().strip()

        if server_address:
            search_url = f"http://{server_address}/content/search"
            get_data_url = f"http://{server_address}/content/getData"
            messagebox.showinfo("地址更新成功", f"服务器地址已更新为：{server_address}")
        else:
            messagebox.showwarning("无效地址", "请输入有效的服务器地址！")

    def search_records(self):
        """搜索记录"""
        category_id = {"归户": "1", "另册": "2", "散叶": "3"}.get(self.category_var.get(), "3")
        search_content = self.search_entry.get().strip()

        search_data = {"categoryId": category_id, "searchContent": search_content}

        try:
            response = requests.post(search_url, headers=headers, json=search_data)
            if response.status_code == 200:
                self.records = response.json().get("data", [])
                self.result_listbox.delete(0, tk.END)
                if self.records:
                    for idx, record in enumerate(self.records):
                        title = record.get("title", "无标题")
                        self.result_listbox.insert(idx, f"{idx + 1}. {title}")
                    self.status_label.config(text=f"找到 {len(self.records)} 条记录。", foreground="blue")
                else:
                    self.status_label.config(text="没有找到任何记录。", foreground="red")
                    messagebox.showinfo("结果", "没有找到任何记录！")
            else:
                messagebox.showerror("请求失败", f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")

    def download_selected_records(self):
        """下载选中的记录"""
        selected_indices = self.result_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("未选择", "请从搜索结果中选择一条或多条记录！")
            return

        selected_records = [self.records[idx] for idx in selected_indices]

        total_pages = sum(int(record.get("pages", 1)) for record in selected_records)
        self.progressbar.config(maximum=total_pages)
        self.progressbar["value"] = 0

        current_page = 0
        for record in selected_records:
            title = record.get("title", "无标题")
            cloud_file_path = record.get("content", "")
            pages = int(record.get("pages", 1))

            pdf_writer = PdfWriter()

            try:
                for page in range(1, pages + 1):
                    get_data_payload = {
                        "cloudFilePath": cloud_file_path,
                        "page": page,
                        "title": title
                    }
                    pdf_response = requests.post(get_data_url, headers=headers, json=get_data_payload)

                    if pdf_response.status_code == 200:
                        pdf_reader = PdfReader(BytesIO(pdf_response.content))
                        for page_num in range(len(pdf_reader.pages)):
                            pdf_writer.add_page(pdf_reader.pages[page_num])

                        # 更新进度条
                        current_page += 1
                        self.progressbar["value"] = current_page
                        self.status_label.config(text=f"正在下载：{title} 第 {page}/{pages} 页")
                        self.root.update()
                    else:
                        raise Exception(f"下载第 {page} 页失败，状态码：{pdf_response.status_code}")

                pdf_filename = f"{title}.pdf"
                with open(pdf_filename, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)

                self.status_label.config(text=f"{title} 下载完成！", foreground="green")

            except Exception as e:
                messagebox.showerror("下载失败", f"下载 {title} 失败：{str(e)}")
                return


# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFDownloaderApp(root)
    root.mainloop()
