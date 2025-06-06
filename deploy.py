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
    max_containers=1,
    min_containers=1,
    timeout=86400,
)
def run_app():
    import subprocess
    import os

    os.chdir("/workspace")
    # 后台执行，立刻返回
    subprocess.Popen(
        ["python3", "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("App launched in background")

@app.local_entrypoint()
def main():
    print("Triggering run_app remotely...")
    run_app.remote()
