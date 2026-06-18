# Modern Flask Web Sitesi Uygulaması

Bu script, kullanıcının isteğine göre hazırlanan, modern ve responsive bir Flask web sitesidir. Tahmini 200+ satır içermektedir ve aşağıdaki özelliklere sahiptir:

## Özellikler
- Flask web framework kullanımı
- Modern UI tasarımı (responsive)
- Bootstrap 5 entegrasyonu
- Çok sayıda sayfa ve bileşen
- JavaScript etkileşimleri
- CSS stilleri
- Form işlemleri
- API entegrasyon örneği

```python
"""
Modern Flask Web Sitesi Uygulaması
Tahmini 250+ satır içermektedir
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'modern_flask_app_secret_key_123'  # Üretimde değiştirilmeli
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Gerekli klasörleri oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Örnek veritabanı (gerçek uygulamada SQLAlchemy kullanılmalı)
users_db = {}
posts_db = []
messages_db = []

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html',
                         title="Ana Sayfa",
                         active_page="home",
                         posts=posts_db[:3])

# Hakkımızda sayfası
@app.route('/about')
def about():
    return render_template('about.html',
                         title="Hakkımızda",
                         active_page="about")

# Hizmetler sayfası
@app.route('/services')
def services():
    services = [
        {"title": "Web Tasarım", "description": "Modern ve responsive web siteleri", "icon": "bi-globe"},
        {"title": "UI/UX Tasarım", "description": "Kullanıcı dostu arayüzler", "icon": "bi-palette"},
        {"title": "SEO Hizmetleri", "description": "Arama motoru optimizasyonu", "icon": "bi-rocket"},
        {"title": "Web Geliştirme", "description": "Özel web uygulamaları", "icon": "bi-code-slash"}
    ]
    return render_template('services.html',
                         title="Hizmetlerimiz",
                         active_page="services",
                         services=services)

# Blog sayfası
@app.route('/blog')
def blog():
    return render_template('blog.html',
                         title="Blog",
                         active_page="blog",
                         posts=posts_db)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        return redirect(url_for('blog'))
    return render_template('blog_post.html',
                         title=post['title'],
                         post=post)

# İletişim sayfası
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        messages_db.append({
            'id': len(messages_db) + 1,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'date': datetime.now().strftime("%d %B %Y %H:%M")
        })

        return redirect(url_for('contact_success'))
    return render_template('contact.html',
                         title="İletişim",
                         active_page="contact")

@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html',
                         title="Mesajınız Alındı")

# Kullanıcı profili
@app.route('/profile')
def profile():
    return render_template('profile.html',
                         title="Profilim",
                         active_page="profile")

# API örneği
@app.route('/api/posts', methods=['GET'])
def api_posts():
    return jsonify(posts_db)

# Dinamik route örneği
@app.route('/page/<int:page_id>')
def dynamic_page(page_id):
    return render_template('dynamic_page.html',
                         title=f"Sayfa {page_id}",
                         page_id=page_id)

# Özel 404 sayfası
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Sayfa Bulunamadı"), 404

# Özel hata sayfası
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Sunucu Hatası"), 500

# Template filtreleri
@app.template_filter('format_date')
def format_date_filter(value, format='%d %B %Y'):
    return datetime.strptime(value, '%Y-%m-%d').strftime(format)

# Başlangıç verilerini yükle
def load_initial_data():
    global posts_db

    initial_posts = [
        {
            'id': 1,
            'title': 'Modern Web Tasarım Trendleri 2023',
            'author': 'Ahmet Yıldız',
            'date': '2023-01-15',
            'content': '''Web tasarım dünyası hızla değişiyor. 2023 yılında da bazı önemli trendler öne çıkıyor.
            İlk olarak, minimalizm ve boşluk kullanımı çok önemli hale geldi. Kullanıcıların dikkatini dağıtan
            gereksiz öğelerden kaçınmak gerekiyor.

            Diğer bir trend ise karanlık mod desteği. Hem estetik hem de kullanıcı konforu açısından önemli.
            Ayrıca, mikro animasyonlar ve micro-interactions kullanımı da kullanıcı deneyimini önemli ölçüde
            artırıyor.

            Son olarak, accessibility (erişilebilirlik) standartlarına daha fazla önem veriliyor. Bu sadece
            yasal bir zorunluluk değil, aynı zamanda daha geniş bir kitleye ulaşmanın da yoludur.''',
            'image': 'trends-2023.jpg',
            'category': 'Tasarım'
        },
        {
            'id': 2,
            'title': 'Flask ile REST API Geliştirme',
            'author': 'Mehmet Demir',
            'date': '2023-02-20',
            'content': '''RESTful API'ler modern web uygulamalarının olmazsa olmazıdır. Flask framework'ü,
            bu konuda oldukça esnek ve kullanımı kolay bir seçenektir.

            İlk olarak, Flask-RESTful veya Flask-RESTPlus gibi eklentiler kullanabilirsiniz. Bu eklentiler
            size otomatik dokümantasyon, doğrulama ve hata işleme gibi birçok avantaj sunar.

            Örnek bir endpoint şöyle görünebilir:

            ```python
            from flask_restful import Resource, reqparse

            class UserAPI(Resource):
                def get(self, user_id):
                    # Kullanıcıyı getir
                    return {'user': 'data'}
            ```

            Ayrıca, Flask-JWT-Extended ile JWT token tabanlı kimlik doğrulama da kolayca uygulanabilir.
            Bu sayede güvenli API'ler geliştirebilirsiniz.''',
            'image': 'flask-api.jpg',
            'category': 'Geliştirme'
        },
        {
            'id': 3,
            'title': 'Responsive Tasarım İlkeleri',
            'author': 'Elif Kaya',
            'date': '2023-03-10',
            'content': '''Responsive tasarım, bir web sitesinin farklı cihazlarda (mobil, tablet, masaüstü)
            sorunsuz çalışmasını sağlayan yaklaşımdır. Bu konuda dikkat edilmesi gereken bazı temel ilkeler:

            1. **Flexible Layouts**: Esnek ızgara sistemleri kullanın. Bootstrap gibi framework'ler bu konuda
            oldukça yardımcıdır.

            2. **Media Queries**: Farklı ekran boyutlarına özel stiller tanımlayın. Örneğin:
            ```css
            @media (max-width: 768px) {
                .container { width: 100%; padding: 0 15px; }
            }
            ```

            3. **Responsive Images**: Görsellerin farklı ekranlarda uygun boyutta görüntülenmesi önemlidir.
            ```html
            <img src="image.jpg" srcset="image-480w.jpg 480w,
                                     image-800w.jpg 800w"
                 sizes="(max-width: 600px) 480px,
                        800px" alt="Responsive Image">
            ```

