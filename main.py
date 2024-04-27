from flask import Flask, jsonify, request
import scanner
import traceback

app = Flask("AIPI")

def error(message: str, code: int = 500):
    return jsonify({'success': False, 'reason': message}), code

def success(data):
    return jsonify({'success': True, 'data': data}), 200

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
        return error(str(e))
    
    return success(results)

if __name__ == '__main__':
    app.run(debug=False)