from flask import Flask, render_template, jsonify
from analysis.core import SalesAnalyzer
import os
import json
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/get_analytics')
def get_analytics():
    with open('data/insights.json') as f:
        return jsonify(json.load(f))

def initialize_project():
    analyzer = SalesAnalyzer()
    analyzer.analyze()
    print("✅ Analysis complete - ready to serve dashboard")

if __name__ == '__main__':
    if not os.path.exists('data/insights.json'):
        print("⚙️ Initializing project for first run...")
        initialize_project()
    app.run(debug=True)