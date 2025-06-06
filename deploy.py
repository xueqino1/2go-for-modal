import modal
import subprocess

# 初始化应用 - 注意这行后面没有括号
app = modal.App(name="persistent-app")

# 构建镜像 - 特别注意括号对齐
image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .copy_local_dir(".", remote_path="/workspace")
)

# 定义函数 - 注意缩进统一4个空格
@app.function(
    image=image,
    concurrency_limit=1,
    keep_warm=1,
    timeout=86400
)
def run_app():
    import os
    import subprocess
    
    os.chdir("/workspace")
    print("Starting app.py...")
    
    with subprocess.Popen(
        ["python3", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        for line in process.stdout:
            print(line.strip())

# 主程序 - 注意缩进
if __name__ == "__main__":
    app.deploy()
