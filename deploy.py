import modal

app = modal.App(name="persistent_app")

image = (
    modal.Image.debian_slim()
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
    with subprocess.Popen(
        ["python3", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        print("Starting app.py...")
        for line in process.stdout:
            print(line.strip())

# ✅ 增加 local_entrypoint，modal run 时触发远程调用
@app.local_entrypoint()
def main():
    print("Triggering run_app remotely...")
    run_app.remote()
