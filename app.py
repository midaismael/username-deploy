from flask import Flask, render_template, request, send_file, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def lookup_accounts():
    if request.method == "POST":
        username = request.form["username"]

        # Run the `sherlock.py` script with the provided username
        try:
            # Run the sherlock.py script and wait for it to complete
            subprocess.run(
                ["python", "sherlock.py", username],
                check=True
            )

            # Path to the generated file
            file_path = f"{username}.txt"

            # Check if the file exists
            if os.path.exists(file_path):
                # Redirect to a new route that shows the download link
                return redirect(url_for("download_file", filename=file_path))
            else:
                return f"File {file_path} not found."

        except subprocess.CalledProcessError as e:
            return f"An error occurred while running Sherlock: {e}"

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    # Show the download page with the link to download the file
    return render_template("download.html", filename=filename)

@app.route("/files/<filename>")
def serve_file(filename):
    # Serve the file for download
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

