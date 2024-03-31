from flask import Flask, send_file, request
import os

app = Flask(__name__)

img_url = "uploads"
app.config["Upload_Url"] = img_url

@app.route("/images/<image_url>")
def getImage(image_url):
    return send_file("uploads/%s"%(image_url), mimetype="image/%s"%(image_url.split(".")[-1]))

@app.route("/uploadFile", methods=["GET", "POST"])
def Uploads():
    request_file = request.files["image"]
    filename = request.args.get("img_url")
    request_file.save(os.path.join(app.config["Upload_Url"], filename))
    request_file.save("mysite/uploads/%s.%s"%(filename, request_file.filename.split('.')[-1]))
    return "p"

if __name__ == "__main__":
    app.run(debug=True, port=1234)
