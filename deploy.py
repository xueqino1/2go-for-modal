import modal

# 定义 Modal App 名称
app = modal.App(name="sandboxed-app")

# 构建镜像：包含你项目依赖和文件
image = (
    modal.Image.debian_slim()
    .run_commands("apt-get update && apt-get install -y curl")  # 如有需要
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")  # 把整个目录上传进去
)

@app.local_entrypoint()
def main():
    print("Creating sandbox...")

    # 创建 Sandbox 容器，使用自定义镜像
    sb = modal.Sandbox.create(app=app, image=image)

    # 可选：进入工作目录
    sb.exec("cd", "/workspace")

    # 启动 app.py（后台运行）
    sb.exec("python3", "-u", "/workspace/app.py")  # -u 关闭缓冲，立即输出

    print("App started inside sandbox.")
