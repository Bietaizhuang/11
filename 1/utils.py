import subprocess
import json
import requests
import os

MODEL_LIST_URL = "https://ollama.com/library"

def get_model_list():
    # 模拟：返回静态列表（也可以解析官网或读取缓存文件）
    return [
        "deepseek-coder:6.7b",
        "deepseek-math:7b",
        "llama3:8b",
        "mistral:7b",
        "phi3:3.8b",
        "codellama:13b"
    ]

def pull_model(model_name):
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
    except subprocess.CalledProcessError:
        print(f"下载模型 {model_name} 失败")
