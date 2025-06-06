import modal
import os
import subprocess
import sys

# 配置常量
APP_NAME = os.getenv("MODAL_APP_NAME", "python-sandbox")
WORKSPACE_PATH = "/workspace"
SCRIPT_NAME = "main.py"  # 替换为你的主脚本

app = modal.App(name=APP_NAME)

image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .add_local_directory(".", remote_path=WORKSPACE_PATH)
)

@app.function(
    image=image,
    timeout=86400,
    secrets=[modal.Secret.from_name("my-env-secrets")]  # 可选
)
def run_script():
    """执行目标Python脚本"""
    try:
        os.chdir(WORKSPACE_PATH)
        print(f"🏃 Starting {SCRIPT_NAME} in {os.getcwd()}")
        
        result = subprocess.run(
            [sys.executable, SCRIPT_NAME],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Execution succeeded:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Execution failed (code {e.returncode}):")
        print(e.stderr)
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.run:
        print("🚀 Deploying and running...")
        with app.run():
            success = run_script.remote()
            if not success:
                raise SystemExit(1)
    else:
        print("🚀 Deploying only...")
        app.deploy("sandbox-deployment")
