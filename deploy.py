import modal

app = modal.App(name="sandboxed-app")

image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

# ✅ 用新式 API 创建 sandbox
sandbox = modal.Sandbox.from_image(
    image=image,
    mounts=[
        modal.Mount.from_local_dir(".", remote_path="/workspace")
    ],
    name="main-sandbox"
)

@app.local_entrypoint()
def main():
    print("Creating sandbox...")
    p = sandbox.exec("python3", "-u", "/workspace/app.py")
    print(p.stdout.read())
