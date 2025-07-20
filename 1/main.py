import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import webbrowser
import requests
from bs4 import BeautifulSoup

env_var_name = "OLLAMA_MODELS"
model_library_url = "https://ollama.com/library"

# 中英语言资源
LANGUAGES = {
    "zh": {
        "title": "Ollama 快速安装器",
        "select_path": "请选择模型存储路径：",
        "browse": "浏览...",
        "set_env": "设置 OLLAMA_MODELS 环境变量",
        "open_download": "打开 Ollama 官网下载安装包",
        "model_list": "可选模型列表（点击安装）：",
        "warning_no_path": "请先选择路径",
        "success_env": "环境变量已设置为：",
        "confirm_pull": "是否下载模型：",
        "language_toggle": "切换为 English"
    },
    "en": {
        "title": "Ollama Quick Installer",
        "select_path": "Please select model storage path:",
        "browse": "Browse...",
        "set_env": "Set OLLAMA_MODELS environment variable",
        "open_download": "Open Ollama website to download",
        "model_list": "Available models (click to install):",
        "warning_no_path": "Please select a path first",
        "success_env": "Environment variable set to:",
        "confirm_pull": "Do you want to download the model:",
        "language_toggle": "切换为中文"
    }
}

class OllamaInstallerApp:
    def __init__(self, root):
        self.root = root
        self.language = "zh"
        self.texts = LANGUAGES[self.language]

        self.root.title(self.texts["title"])
        self.root.geometry("500x500")

        self.path_label = tk.Label(root)
        self.path_label.pack()

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack()

        self.browse_btn = tk.Button(root, command=self.select_folder)
        self.browse_btn.pack()

        self.env_btn = tk.Button(root, command=self.set_env_var)
        self.env_btn.pack(pady=10)

        self.download_btn = tk.Button(root, command=self.open_download_page)
        self.download_btn.pack(pady=10)

        self.model_label = tk.Label(root)
        self.model_label.pack(pady=5)

        self.model_listbox = tk.Listbox(root, width=50, height=15)
        self.model_listbox.pack()
        self.model_listbox.bind('<<ListboxSelect>>', self.model_selected)

        self.lang_btn = tk.Button(root, command=self.toggle_language)
        self.lang_btn.pack(pady=10)

        self.models = []
        self.load_models()
        self.update_language()

    def update_language(self):
        self.texts = LANGUAGES[self.language]
        self.root.title(self.texts["title"])
        self.path_label.config(text=self.texts["select_path"])
        self.browse_btn.config(text=self.texts["browse"])
        self.env_btn.config(text=self.texts["set_env"])
        self.download_btn.config(text=self.texts["open_download"])
        self.model_label.config(text=self.texts["model_list"])
        self.lang_btn.config(text=self.texts["language_toggle"])

    def toggle_language(self):
        self.language = "en" if self.language == "zh" else "zh"
        self.update_language()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

    def set_env_var(self):
        path = self.path_entry.get()
        if not path:
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        os.system(f'setx {env_var_name} "{path}" /M')
        messagebox.showinfo(self.texts["title"], f"{self.texts['success_env']} {path}")

    def open_download_page(self):
        webbrowser.open("https://ollama.com/download/windows")

    def load_models(self):
        self.models = self.fetch_online_models()
        self.model_listbox.delete(0, tk.END)
        for model in self.models:
            self.model_listbox.insert(tk.END, model)

    def fetch_online_models(self):
        try:
            response = requests.get(model_library_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            model_list = []
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("/library/"):
                    model = a["href"].split("/library/")[1]
                    if model and model not in model_list:
                        model_list.append(model)
            return model_list
        except Exception as e:
            print(f"⚠️ 模型列表获取失败，使用默认列表: {e}")
            return ["llama3", "phi3", "mistral", "deepseek-coder", "codellama"]

    def model_selected(self, event):
        if not self.path_entry.get():
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        selected = self.model_listbox.get(self.model_listbox.curselection())
        if messagebox.askyesno(self.texts["title"], f"{self.texts['confirm_pull']} {selected}?"):
            self.pull_model(selected)

    def pull_model(self, model_name):
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
        except Exception as e:
            messagebox.showerror("错误", f"下载模型失败：{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaInstallerApp(root)
    root.mainloop()
