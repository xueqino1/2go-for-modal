import modal
import os
import subprocess

# 创建 Modal 应用
app = modal.App(name="persistent_app")

# 定义镜像并添加本地目录（使用最新SDK方法名）
image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .copy_local_dir(".", remote_path="/workspace")  # 修改为copy_local_dir
)

# 定义运行主函数
@app.function(
    image=image,
    concurrency_limit=1,  # 新版SDK仍支持
    keep_warm=1,         # 新版SDK仍支持
    timeout=86400,       # 24小时超时
)
def run_app():
    import os
    import subprocess

    os.chdir("/workspace")
    print("🔄 Starting app.py...")
    
    with subprocess.Popen(
        ["python3", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        for line in process.stdout:
            print(line.strip())  # 实时输出日志

# 部署应用（不自动运行）
if __name__ == "__main__":
    print("🚀 Deploying application...")
    app.deploy("my-persistent-app")  # 添加部署名称便于管理
