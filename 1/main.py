import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import webbrowser
from utils import get_model_list, pull_model

env_var_name = "OLLAMA_MODELS"

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
        "yes": "是",
        "no": "否",
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
        "yes": "Yes",
        "no": "No",
        "language_toggle": "切换为中文"
    }
}

class OllamaInstallerApp:
    def __init__(self, root):
        self.root = root
        self.language = "zh"  # 默认语言为中文
        self.texts = LANGUAGES[self.language]

        self.root.title(self.texts["title"])
        self.root.geometry("500x450")

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

        self.model_listbox = tk.Listbox(root, width=50, height=10)
        self.model_listbox.pack()
        self.model_listbox.bind('<<ListboxSelect>>', self.model_selected)

        self.lang_btn = tk.Button(root, command=self.toggle_language)
        self.lang_btn.pack(pady=10)

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
        models = get_model_list()
        self.model_listbox.delete(0, tk.END)
        for model in models:
            self.model_listbox.insert(tk.END, model)

    def model_selected(self, event):
        if not self.path_entry.get():
            messagebox.showwarning(self.texts["title"], self.texts["warning_no_path"])
            return
        selected = self.model_listbox.get(self.model_listbox.curselection())
        if messagebox.askyesno(self.texts["title"], f"{self.texts['confirm_pull']} {selected}?"):
            pull_model(selected)

if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaInstallerApp(root)
    root.mainloop()
