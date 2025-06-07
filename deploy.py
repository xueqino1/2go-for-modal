import modal

app = modal.App(name="sandboxed-app")

image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

# ✅ 定义一个可持久复用的 Sandbox 对象
sandbox = modal.Sandbox.from_image(
    image=image,
    app=app,
    mounts=[
        modal.Mount.from_local_dir(".", remote_path="/workspace")
    ],
    # 可选：可定义重启策略
    restart_policy=modal.Sandbox.RestartPolicy.NEVER,
    # 可选：保持默认名称为 "sandbox"
    name="main_sandbox"
)

@app.local_entrypoint()
def main():
    print("Launching persistent sandbox...")
    sandbox.exec("python3", "-u", "/workspace/app.py")
    print("App started inside named sandbox.")
