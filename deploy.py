import modal

app = modal.App(name="persistent_app")

image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    max_containers=1,      # ✅ 正确的新参数名
    min_containers=1,      # ✅ 正确的新参数名
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

# ❌ 不需要 app.deploy()，因为你是通过 CLI 部署
# ✅ 可选：添加一个 local_entrypoint 手动触发 run_app（在本地或 CLI 运行用）
@app.local_entrypoint()
def main():
    run_app.remote()
