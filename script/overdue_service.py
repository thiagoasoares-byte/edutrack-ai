from flask import Flask, request, jsonify
from script.calculate_overdue_subjects import get_overdue_subject_ids
import os

app = Flask(__name__)

@app.route('/overdue_subjects', methods=['GET'])
def overdue_subjects():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'missing user_id'}), 400

    db_url = os.environ.get('DB_URL')
    if not db_url:
        return jsonify({'error': 'DB_URL not set'}), 500

    try:
        ids = get_overdue_subject_ids(db_url, user_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'subject_ids': ids})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
