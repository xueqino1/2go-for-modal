import modal

app = modal.App(name="persistent_app")

image = (
    modal.Image.debian_slim()
    .apt_install("curl")  # ✅ 加上你需要的 curl
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    max_containers=1,
    min_containers=1,
    timeout=86400,
)
def run_app():
    import os
    import subprocess

    os.chdir("/workspace")
    with subprocess.Popen(
        ["python3", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        print("Starting app.py...")
        for line in process.stdout:
            print(line.strip())

# 👇 主程序里部署并立即远程执行
if __name__ == "__main__":
    app.deploy()
    run_app.remote()
