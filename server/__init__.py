from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html',title="AHRIAHRI")

@app.route('/us')
def US():
    return "FUCK World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
