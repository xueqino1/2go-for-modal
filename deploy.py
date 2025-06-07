import modal
import subprocess
import os

app = modal.App("webapp")

image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    timeout=86400,
    max_retries=0,
)
def run_app():
    os.chdir("/workspace")
    print("Starting app.py ...")
    # 用 subprocess 调用 app.py，捕获输出
    result = subprocess.run(["python3", "app.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

@app.local_entrypoint()
def main():
    print("Triggering run_app remotely...")
    run_app.remote()
