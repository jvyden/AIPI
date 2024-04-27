from flask import jsonify

def error(message: str, code: int = 500):
    return jsonify({'success': False, 'reason': message}), code

def success(data):
    return jsonify({'success': True, 'data': data}), 200