import modal

app = modal.App(name="flask_web_app")

image = (
    modal.Image.debian_slim()
    .pip_install("flask")
    .add_local_dir(".", remote_path="/app")  # 把当前目录挂载进去
)

@app.function(image=image)
@modal.web_server(port=5000)  # 监听 Flask 默认端口
def web():
    from app import app as flask_app  # ⬅️ 从 app.py 导入 Flask 实例
    return flask_app
