import modal
import os

# 配置常量
APP_NAME = os.getenv("MODAL_APP_NAME", "python-sandbox")
WORKSPACE_PATH = "/workspace"
SCRIPT_NAME = "app.py"  # 替换为你的主脚本

# 初始化应用
app = modal.App(name=APP_NAME)

def build_image():
    """构建包含依赖的镜像"""
    return (
        modal.Image.debian_slim()
        .pip_install_from_requirements("requirements.txt")
        .add_local_directory(".", remote_path=WORKSPACE_PATH)
    )

@app.function(
    image=build_image(),
    timeout=86400,  # 24小时超时
    secrets=[
        modal.Secret.from_name("my-env-secrets")  # 可选：添加环境变量
    ]
)
def run_script():
    """执行目标Python脚本"""
    import subprocess
    import sys
    
    # 切换到工作目录
    os.chdir(WORKSPACE_PATH)
    print(f"🏃 Starting {SCRIPT_NAME} in {os.getcwd()}")
    
    # 执行脚本（同步阻塞式）
    result = subprocess.run(
        [sys.executable, SCRIPT_NAME],
        capture_output=True,
        text=True
    )
    
    # 输出结果
    if result.returncode == 0:
        print("✅ Execution succeeded:")
        print(result.stdout)
    else:
        print(f"❌ Execution failed (code {result.returncode}):")
        print(result.stderr)
        raise modal.exception.ExecutionError("Script execution failed")

if __name__ == "__main__":
    # 仅部署不自动运行
    print(f"🚀 Deploying {APP_NAME}...")
    app.deploy("sandbox-deployment")
