from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
import os, json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_forbidden_key_to_be_used!!")

directoryname = "contactmessage/"
json_file = "message.json"

try:
    os.makedirs(directoryname, exist_ok=True)
    print(f"Created the directory sweetly {directoryname} !!!")
except OSError as e:
    print(f"An error occured when creating the directory {directoryname} as {e}")
    exit()
json_path = os.path.join(directoryname, json_file)

try:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=4)
        print(f"{json_path} created successfully!!!")
except IOError as e:
    print(f"An error occured when creating the file in the filepath {json_path} as {e}")
    exit()


@app.route("/")
def contact():
    return render_template("contact.html")

@app.route("/contactform/", methods=["GET", "POST"])
def contactform():
    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                   data =  json.load(f)

            data.append(form_data)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            return {"Error":str(e)}, 500
            exit()
        flash("Message was sent successfully!!")
        return redirect(url_for("contact"))
    return render_template("contact.html")
if __name__ == "__main__":
    app.run(port=4000, debug=True, use_debugger=True)