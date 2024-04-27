from flask import Flask
import ai.aipi_deepdanbooru

app = Flask("AIPI")

@app.route('/')
def index():
    return "AIPI scanning service"

app.register_blueprint(ai.aipi_deepdanbooru.bp, url_prefix='/deepdanbooru')

if __name__ == '__main__':
    app.run(debug=False)