import modal
from typing import Optional

# 定义应用配置
APP_NAME = "webapp"
WORKSPACE_PATH = "/workspace"
PORT = 8080  # 确保 app.py 监听此端口

# 初始化 Modal 应用
app = modal.App(name=APP_NAME)

def build_custom_image() -> modal.Image:
    """
    构建自定义容器镜像：
    1. 基于 Debian 精简版
    2. 安装系统依赖 (curl)
    3. 安装 Python 依赖
    4. 挂载本地项目目录
    """
    return (
        modal.Image.debian_slim()
        .apt_install("curl")  # 安装 curl 工具
        .pip_install_from_requirements("requirements.txt")  # 从文件安装依赖
        .add_local_directory(".", remote_path=WORKSPACE_PATH)  # 挂载整个项目
    )

@app.function(
    image=build_custom_image(),
    timeout=86400,  # 24小时超时
    keep_warm=1,    # 保持至少1个容器预热
    concurrency_limit=1,  # 单实例运行
    web_server=True,  # 启用Web服务模式
)
def run_web_app() -> Optional[modal.web.Server]:
    """
    运行Web应用服务：
    1. 切换到工作目录
    2. 启动Python应用
    3. 自动暴露HTTP端口
    """
    import os
    import subprocess
    import sys
    
    try:
        # 切换到项目目录
        os.chdir(WORKSPACE_PATH)
        print(f"🚀 Starting application in {os.getcwd()}")
        
        # 启动子进程（确保app.py监听0.0.0.0:PORT）
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # 实时输出日志
        for line in process.stdout:
            print(line.strip())
            
        return modal.web.Server()  # 返回Web服务器句柄
    
    except Exception as e:
        print(f"❌ Application failed: {str(e)}")
        raise

if __name__ == "__main__":
    # 部署并立即运行
    with app.run():
        web_server = run_web_app.remote()
        print(f"🌐 Web server ready at: {web_server.url}")
