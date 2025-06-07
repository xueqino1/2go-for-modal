import modal

app = modal.App(name="sandboxed-app")

image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.local_entrypoint()
def main():
    print("Creating sandbox...")

    sb = modal.Sandbox.create(
        app=app,
        image=image,
        mounts=[
            modal.Mount.from_local_dir(".", remote_path="/workspace")
        ],
        name="main_sandbox"
    )

    sb.exec("python3", "-u", "/workspace/app.py")

    print("App started inside sandbox.")
