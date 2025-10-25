from flask import Flask, render_template, request, send_file, jsonify
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from scripts.encode import encode
from scripts.decode import decode
from scripts.prob_loader import load_probs
from scripts.measurement_loader import simulate_measurement

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/encode", methods=["POST"])
def enc():
    file = request.files["file"]
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp_image.png")
    file.save(temp_path)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "encoded_image.qimg")
    encode(temp_path, filepath)
    response = send_file(
        filepath, as_attachment=True, download_name="encoded_image.qimg"
    )
    return response


@app.route("/decode", methods=["POST"])
def dec():
    file = request.files["file"]
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp_qimg.qimg")
    file.save(temp_path)
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], "decoded_image.png")
    decode(temp_path, output_path)
    return send_file(output_path, as_attachment=True, download_name="decoded_image.png")


@app.route("/view_prob", methods=["POST"])
def view_prob():
    file = request.files["file"]
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp_view.qimg")
    file.save(temp_path)
    temp_png = os.path.join(app.config["UPLOAD_FOLDER"], "temp_prob.png")
    try:
        img = load_probs(temp_path)
        img.save(temp_png)
        return send_file(temp_png, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/view_measurement", methods=["POST"])
def view_measurement():
    file = request.files["file"]
    samples = int(request.form.get("samples", 10000))
    count_steps = int(request.form.get("count_steps", 1))
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp_view.qimg")
    file.save(temp_path)
    temp_png = os.path.join(app.config["UPLOAD_FOLDER"], "temp_measurement.png")
    try:
        img = simulate_measurement(temp_path, samples, count_steps)
        img.save(temp_png)
        return send_file(temp_png, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
