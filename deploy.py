import modal
import os
import subprocess
import sys
from typing import Optional

# === 应用配置 ===
APP_NAME = "flask_sandbox"
WORKSPACE_PATH = "/workspace"
PORT = 8080  # 确保 app.py 监听此端口

# 初始化 Modal 应用
app = modal.App(name=APP_NAME)

# 构建自定义容器镜像
def build_custom_image() -> modal.Image:
    return (
        modal.Image.debian_slim()
        .apt_install("curl")  # 安装 curl
        .pip_install_from_requirements("requirements.txt")  # 安装 Python 依赖
        .add_local_dir(".", remote_path=WORKSPACE_PATH)  # 挂载当前目录
    )

# 定义可部署函数
@app.function(
    image=build_custom_image(),
    timeout=86400,           # 最大运行时长：24 小时
    min_containers=1,        # 最少保持 1 个实例
    max_containers=1,        # 最多同时运行 1 个实例
    web_server=True          # 开启 Web 服务器支持
)
def run_web_app() -> Optional[modal.web.Server]:
    try:
        os.chdir(WORKSPACE_PATH)
        print(f"🚀 Starting application in {os.getcwd()}")

        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line.strip())

        return modal.web.Server()  # 返回 Web 服务句柄（自动暴露 8080）

    except Exception as e:
        print(f"❌ Application failed: {str(e)}")
        raise

# 部署并立即运行（本地调用此脚本时）
if __name__ == "__main__":
    with app.run():
        web_server = run_web_app.remote()
        print(f"🌐 Web server ready at: {web_server.url}")
