import modal

app = modal.App("persistent_app")

image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.schedule(cron="0 0 * * *")  # 每天凌晨
@app.function(
    image=image,
    max_containers=1,
    min_containers=1,
    timeout=86400,   # 可选：每次最多活一天
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
        for line in process.stdout:
            print(line.strip())
