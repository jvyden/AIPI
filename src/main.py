from flask import Flask
from ai import aipi_eva
# from ai import aipi_deepdanbooru

app = Flask("AIPI")

@app.route('/')
def index():
    return "AIPI scanning service"

# app.register_blueprint(aipi_deepdanbooru.bp, url_prefix='/deepdanbooru')
app.register_blueprint(aipi_eva.bp, url_prefix='/eva')

if __name__ == '__main__':
    app.run(debug=False)