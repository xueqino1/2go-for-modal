import modal

app = modal.App(name="sandboxed-app")

# 构造 image：使用 requirements.txt 安装依赖
image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")
    .pip_install_from_requirements("requirements.txt")  # ✅ 重点修改
)

@app.local_entrypoint()
def main():
    print("Creating sandbox (legacy-compatible)...")

    # ✅ 使用旧 SDK 兼容方式创建 Sandbox
    sb = modal.Sandbox.create(
        app=app,
        image=image,
        mounts=[(".", "/workspace")],  # ✅ 旧 SDK 的写法
        name="main_sandbox"
    )

    # ✅ 启动你实际的 Python 应用
    sb.exec("python3", "-u", "/workspace/app.py")

    print("App started inside sandbox.")
