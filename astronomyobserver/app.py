from pathlib import Path
from urllib.parse import urlencode

from flask import Blueprint, Flask, redirect, request

# 引擎仓库根（与 astronomyobserver/ 同级），页面里写死了 ../../build/ 和
# ../test-skydata/ 的相对引用，所以整体挂在一个 URL 前缀下、层级不能变。
ENGINE_ROOT = Path(__file__).resolve().parent.parent / "stellarium-web-engine-master"

# 与 appsource/ 下的语言文件夹一一对应。
LANGS = ("en", "zhs", "zht", "ja")

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
    # lat/lon/lang 原样透传给演示页；非法或缺失的参数直接丢掉。
    args = request.args
    lat = args.get("lat", type=float)
    lon = args.get("lon", type=float)
    lang = args.get("lang", "zhs")
    query = []
    if lat is not None and lon is not None and \
            -90 <= lat <= 90 and -180 <= lon <= 180:
        query += [("lat", lat), ("lon", lon)]
    if lang in LANGS:
        query.append(("lang", lang))
    url = "/stel/apps/simple-html/stellarium-web-engine.html"
    if query:
        url += "?" + urlencode(query)
    return redirect(url)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
