from flask import Flask, render_template, request, jsonify, send_file
import worker
import mock_worker
import random

class api:
    debug = False
    app = Flask(__name__)

    if debug:
        collector = mock_worker.collector()
    else:
        collector = worker.collector()

    @app.route('/', methods=['GET'])
    def index():
        return render_template('dashboard.html')
    
    @app.route('/index.css', methods=['GET'])
    def index_css():
        return send_file('./templates/index.css')

    @app.route('/api', methods=['GET'])
    def api():
        return "501 Not Implemented" # TODO: implement historical data retrieval and filtering
        
    @app.route('/api/latest', methods=['GET'])
    def latest():
        return jsonify(api.collector.reader.value_store)
    
    @app.route('/api/weather', methods=['GET'])
    def weather():
        return jsonify(api.collector.reader.weather_data)
    
    @app.route('/api/day', methods=['GET'])
    def day():
        return jsonify([random.random()*100 for _ in range(24)])
    
    @app.route('/api/year', methods=['GET'])
    def year():
        return jsonify([random.random()*100 for _ in range(12)])
    
    @app.route('/images/<path:path>', methods=['GET'])
    def images(path):
        if '..' in path:
            return "403 Forbidden"

        return send_file(f'./images/{path}.svg')

    def run():
        api.collector.start()
        api.app.run(host='0.0.0.0')
