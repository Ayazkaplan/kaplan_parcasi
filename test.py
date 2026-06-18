"""
test.py - VX tarafından oluşturuldu / güncellendi
"""
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Aslan Parçası Widget</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            text-align: center;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 { font-size: 3em; margin-bottom: 10px; }
        p { font-size: 1.2em; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 VERTIXORION OMEGA</h1>
        <p>Aslan Parçası Widget - Test Sayfası</p>
        <p>VX tarafından oluşturuldu 🚀</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
