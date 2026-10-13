from pathlib import Path

from flask import Blueprint, Flask, redirect

# 引擎仓库根（与 astronomyobserver/ 同级），页面里写死了 ../../build/ 和
# ../test-skydata/ 的相对引用，所以整体挂在一个 URL 前缀下、层级不能变。
ENGINE_ROOT = Path(__file__).resolve().parent.parent / "stellarium-web-engine-master"

stel = Blueprint(
    "stel",
    __name__,
    static_folder=str(ENGINE_ROOT),
    static_url_path="/stel",
)

app = Flask(__name__)
app.register_blueprint(stel)


@app.route("/")
def index():
    return redirect("/stel/apps/simple-html/stellarium-web-engine.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
