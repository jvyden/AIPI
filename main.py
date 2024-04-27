from flask import Flask, jsonify, request
import scanner
import traceback

app = Flask("AIPI")

def error(message: str):
    return jsonify({'success': False, 'reason': message})

@app.route('/')
def index():
    return "AIPI scanning service"

@app.route('/scan_image', methods=['POST'])
def scan_image():
    # Get the value of 'threshold' query parameter as a float
    threshold = request.args.get('threshold', type=float)

    if threshold is None:
        threshold = 0.5

    try:
        image = scanner.load_image(request.data)
        results = scanner.predict(image, threshold)
    except Exception as e:
        traceback.print_exc()
        return error(str(e)), 500
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=False)