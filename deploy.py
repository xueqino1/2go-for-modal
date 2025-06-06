import modal

APP_NAME = "flask_and_worker"
WORKSPACE_PATH = "/workspace"

# 初始化 Modal 应用
app = modal.App(name=APP_NAME)

# 构建镜像
image = (
    modal.Image.debian_slim()
    .apt_install("curl")  # 安装 curl
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path=WORKSPACE_PATH)
)

# ✅ Web 服务（Flask）
@app.wsgi(image=image)
def web():
    import os
    os.chdir(WORKSPACE_PATH)
    from app import app as flask_app
    return flask_app

# ✅ 后台任务（定时 curl、守护进程）
@app.function(
    image=image,
    timeout=86400,
    max_containers=1,
    min_containers=1,
)
def background_worker():
    import os
    import subprocess
    import sys

    os.chdir(WORKSPACE_PATH)
    print("🚀 Starting app.py as background worker...")

    with subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        for line in process.stdout:
            print(line.strip())
