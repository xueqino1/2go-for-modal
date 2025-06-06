import modal

app = modal.App(name="persistent_app")

# 构建镜像：安装 curl、Python 依赖，并挂载当前目录
image = (
    modal.Image.debian_slim()
    .apt_install("curl")  # ✅ 安装 curl
    .pip_install_from_requirements("requirements.txt")  # ✅ 安装 Flask、requests 等
    .add_local_dir(".", remote_path="/workspace")  # ✅ 挂载项目代码
)

@app.function(
    image=image,
    max_containers=1,  # ✅ 替换 concurrency_limit
    min_containers=1,  # ✅ 替换 keep_warm
    timeout=86400,     # ✅ 最长运行时间 1 天
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

# 主程序：部署并触发远程运行
if __name__ == "__main__":
    app.deploy()
