from flask import Flask, render_template
import pandas as pd
import os
import pymysql
from models import db
from config import Config
from controllers.contact_controller import contact

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Helper to create database if not exists
def create_db_if_not_exists():
    try:
        # Extract connection info from env or config
        # Assuming localhost and root/empty for simplicity based on typical local setups if env is used
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USERNAME', 'root')
        password = os.getenv('DB_PASSWORD', '')
        port = int(os.getenv('DB_PORT', 3306))
        dbname = os.getenv('DB_NAME', 'persona_blog')

        conn = pymysql.connect(host=host, user=user, password=password, port=port)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
        conn.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

# Create DB and Tables
with app.app_context():
    create_db_if_not_exists()
    db.create_all()

@app.route('/')
def halaman_index():
    return render_template('index.html')

@app.route('/Biodata1')
def halaman_astri():
    return render_template('astri.html')

@app.route('/Biodata2')
def halaman_ghifar():
    return render_template('ghifar.html')

@app.route('/dashboard')
def dashboard():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file = 'Prak_AAS_LiTek_Jumlah Pengunjung ke Akomodasi Wisata Berdasarkan Jenis Wisatawan dan KabupatenKota di Jawa Barat 2014-2023.xlsx'
    file_path = os.path.join(base_dir, excel_file)
    
    try:
        # Membaca data dari file excel
        df = pd.read_excel(file_path, sheet_name='Datset')
        
        # Prepare untuk chart
        # Total Pengunjung untuk line chart
        yearly_data = df.groupby('tahun')['jumlah_pengunjung'].sum().reset_index()
        years = yearly_data['tahun'].tolist()
        visitors_per_year = yearly_data['jumlah_pengunjung'].tolist()
        
        # Jenis Pengunjung untuk pie chart
        type_data = df.groupby('jenis_wisatawan')['jumlah_pengunjung'].sum().reset_index()
        types = type_data['jenis_wisatawan'].tolist()
        visitors_per_type = type_data['jumlah_pengunjung'].tolist()
        
        # Top 10 Kota/Kabupaten untuk bar chart
        city_data = df.groupby('nama_kabupaten_kota')['jumlah_pengunjung'].sum().sort_values(ascending=False).head(10).reset_index()
        cities = city_data['nama_kabupaten_kota'].tolist()
        visitors_per_city = city_data['jumlah_pengunjung'].tolist()
        
        # Data KPI
        total_visitors = df['jumlah_pengunjung'].sum()
        
        return render_template('dashboard.html', 
                               years=years, 
                               visitors_per_year=visitors_per_year,
                               types=types,
                               visitors_per_type=visitors_per_type,
                               cities=cities,
                               visitors_per_city=visitors_per_city,
                               total_visitors=total_visitors)
                               
    except Exception as e:
        return f"Error reading Excel file: {e}"

@app.route('/about')
def about():
    return render_template('about.html')

# Route Contact now uses the controller
app.add_url_rule('/contact', view_func=contact, methods=['GET', 'POST'])

@app.route('/ppt_aas')
def ppt_aas():
    return render_template('ppt_aas.html')

@app.route('/ppt_std')
def ppt_std():
    return render_template('ppt_std.html')

@app.route('/makalah_postal')
def makalah_postal():
    return render_template('makalah_postal.html')

@app.route('/ppt_alpro')
def ppt_alpro():
    return render_template('ppt_alpro.html')

@app.route('/ppt_peluang')
def ppt_peluang():
    return render_template('ppt_peluang.html')

if __name__ == '__main__':
    app.run(debug=True)

    