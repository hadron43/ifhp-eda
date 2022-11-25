
from flask import Flask, render_template, redirect, send_from_directory, send_file

from dtale.app import build_app, initialize_process_props
from dtale.views import startup
from dtale.utils import build_url
import dtale.global_state as gstate
import os
import json
import pandas as pd

HOST = "0.0.0.0"
PORT = 8080

initialize_process_props(HOST, PORT)
app_url = build_url(HOST, str(PORT))
app = build_app(app_url, additional_templates="templates")

no_of_instances = 0

@app.route("/")
def create_df():
    global no_of_instances
    if no_of_instances > 2:
        gstate.cleanup()
        no_of_instances = 0
    print("started")
    with open("data.json") as f:
        data = json.load(f)
    
    leng = len(data)
    
    return render_template("index.html", lst=data, leng=leng)

@app.route("/dt/<file>")
def dt(file):
    if os.stat("data/" + file).st_size < 10:
        return "Empty file"
    df = pd.read_csv(f"data/{file}")
    instance = startup("", data=df, hide_shutdown=True)
    # f = open("instance.txt", "")
    global no_of_instances
    no_of_instances += 1
    return redirect(f"/dtale/main/{instance._data_id}")

@app.route("/test")
def test():
    df1=pd.read_excel("Dry_Bean_Dataset.xlsx")
    instance = startup("", data=df1, hide_shutdown=True)
    return redirect(f"/dtale/main/{instance._data_id}")

@app.route("/data/<filename>")
def data(filename):
    cwd = os.getcwd()
    return send_from_directory(cwd + '/data', filename)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=False)