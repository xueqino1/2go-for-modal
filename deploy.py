import modal

app = modal.App(name="persistent_app")

image = (
    modal.Image.debian_slim()
    .run_commands(
        "apt-get update && apt-get install -y curl"
    )
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    max_containers=1,      # ✅ 新参数名，替换掉旧的
    min_containers=1,
    timeout=86400,
)
def run_app():
    import os
    import subprocess

    os.chdir("/workspace")
    subprocess.Popen(
        ["python3", "app.py"],
        preexec_fn=os.setsid  # 启动独立 session，Modal 函数结束不杀它
    )
    print("Started app.py")

# ✅ 增加 local_entrypoint，modal run 时触发远程调用
@app.local_entrypoint()
def main():
    print("Triggering run_app remotely...")
    run_app.remote()
