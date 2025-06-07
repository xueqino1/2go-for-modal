import modal
import subprocess
import os

app = modal.App(name="persistent_app")

image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    timeout=86400,  # 只加timeout，别加max_containers等
)
def run_app():
    os.chdir("/workspace")
    print("Starting app.py...")
    with subprocess.run(
        ["python3", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:
        for line in process.stdout:
            print(line.strip())

@app.local_entrypoint()
def main():
    print("Triggering run_app remotely...")
    run_app.remote()
