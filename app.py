from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

pengetahuan = {
    "programming": {"skor": 0, "pekerjaan": ["Web Developer", "Software Engineer", "Mobile App Developer"]},
    "networking": {"skor": 0, "pekerjaan": ["Network Administrator", "Network Engineer", "Information Security Analyst"]},
    "database": {"skor": 0, "pekerjaan": ["Database Administrator", "Data Analyst", "Data Scientist"]},
    "graphics": {"skor": 0, "pekerjaan": ["UI/UX Designer", "Graphic Designer", "Game Developer"]}
}

aturan = [
    {
        "pertanyaan": "Pada skala 1 hingga 5, Seberapa suka Anda dengan programming?",
        "kategori": "programming",
        "threshold": 3,
        "opsi": [
            {"teks": "Sangat tidak suka", "nilai": 1},
            {"teks": "Tidak suka", "nilai": 2},
            {"teks": "Netral", "nilai": 3},
            {"teks": "Suka", "nilai": 4},
            {"teks": "Sangat suka", "nilai": 5}
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam penggunaan HTML, CSS, & Javascript?",
        "kategori": "programming",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Tingkat pemula", "nilai": 2},
            {"teks": "Tingkat lanjutan", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam menggunakan framework?",
        "kategori": "programming",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Bisa", "nilai": 2},
            {"teks": "Sangat bisa", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Apakah Anda tertarik dengan networking / jaringan komputer?",
        "kategori": "networking",
        "threshold": 3,
        "opsi": [
            {"teks": "Sangat tidak tertarik", "nilai": 1},
            {"teks": "Tidak tertarik", "nilai": 2},
            {"teks": "Netral", "nilai": 3},
            {"teks": "Tertarik", "nilai": 4},
            {"teks": "Sangat tertarik", "nilai": 5}
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam penggunaan Linux, Microtik, Virtual Machine dan GNS3?",
        "kategori": "networking",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Tingkat pemula", "nilai": 2},
            {"teks": "Tingkat lanjutan", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam mengatur dan mengkonfigurasi router, DNS, dan Server proxy?",
        "kategori": "networking",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Bisa", "nilai": 2},
            {"teks": "Sangat bisa", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 5, Seberapa suka Anda bekerja dengan database?",
        "kategori": "database",
        "threshold": 3,
        "opsi": [
            {"teks": "Sangat tidak suka", "nilai": 1},
            {"teks": "Tidak suka", "nilai": 2},
            {"teks": "Netral", "nilai": 3},
            {"teks": "Suka", "nilai": 4},
            {"teks": "Sangat suka", "nilai": 5}
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam penggunaan relational database (MySQL, Oracle, MariaDB dll)?",
        "kategori": "database",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Tingkat pemula", "nilai": 2},
            {"teks": "Tingkat lanjutan", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam menggunakan bahasa program python?",
        "kategori": "database",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Bisa", "nilai": 2},
            {"teks": "Sangat bisa", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Apakah Anda tertarik dengan grafis dan desain?",
        "kategori": "graphics",
        "threshold": 3,
        "opsi": [
            {"teks": "Sangat tidak tertarik", "nilai": 1},
            {"teks": "Tidak tertarik", "nilai": 2},
            {"teks": "Netral", "nilai": 3},
            {"teks": "Tertarik", "nilai": 4},
            {"teks": "Sangat tertarik", "nilai": 5}
        ]
    },
    {
        "pertanyaan": "Pada skala 1 hingga 3, Seberapa ahli Anda dalam menggunakan Wireframing (Figma, Adobe XD dan Sketch)?",
        "kategori": "graphics",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Tingkat pemula", "nilai": 2},
            {"teks": "Tingkat lanjutan", "nilai": 3},
        ]
    },
    {
        "pertanyaan": "Apakah Anda dapat membuat desain suatu produk?",
        "kategori": "graphics",
        "threshold": 2,
        "opsi": [
            {"teks": "Tidak bisa", "nilai": 1},
            {"teks": "Bisa", "nilai": 2},
            {"teks": "Sangat bisa", "nilai": 3},
        ]
    }
]

def updatePengetahuan(jawab, kategori):
    pengetahuan[kategori]["skor"] += jawab

@app.route('/', methods=['GET'])
def index():
    # Reset the session and pengetahuan scores
    session['current_question'] = 0
    for k in pengetahuan:
        pengetahuan[k]['skor'] = 0
    return render_template('index.html')

@app.route('/pertanyaan', methods=['GET', 'POST'])
def pertanyaan():
    current_question = session.get('current_question', 0)

    if request.method == 'POST':
        jawab = int(request.form.get('jawaban'))
        kategori = aturan[current_question]['kategori']
        updatePengetahuan(jawab, kategori)
        session['current_question'] = current_question + 1
        if session['current_question'] >= len(aturan):
            return redirect(url_for('hasil'))
        return redirect(url_for('pertanyaan'))

    if current_question < len(aturan):
        pertanyaan = aturan[current_question]
        return render_template('pertanyaan.html', pertanyaan=pertanyaan, current_question=current_question + 1,
                               total_questions=len(aturan))

    return redirect(url_for('hasil'))

@app.route('/hasil', methods=['GET'])
def hasil():
    rekomendasi = []
    for kategori in pengetahuan:
        if pengetahuan[kategori]["skor"] >= sum([item['threshold'] for item in aturan if item['kategori'] == kategori]):
            rekomendasi.append(random.choice(pengetahuan[kategori]["pekerjaan"]))
    return render_template('hasil.html', rekomendasi=rekomendasi)

if __name__ == '__main__':
    app.run(debug=True)
