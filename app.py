from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from google_scraper import *
from organizing_urls import *
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'archivos'

@app.route('/')
def upload():
    return render_template("sample4.html")


@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        data = request.json
        query_input = data["query"]
        qoption_input = data["qoption"]
        qexception_input = data["qexception"]
        qrangedate_input = data["qrangedate"]
        qsite_input = data["qsite"]
        nqueries_input = data["nqueries"]
        
        
        if not os.path.exists('archivos'):
           os.makedirs('archivos')

        file_path = asyncio.run(main(nqueries=nqueries_input, query=query_input, qoption=qoption_input, qexception=qexception_input, qrangedate=qrangedate_input, qsite=qsite_input))
        
        return jsonify({'message': 'Scraping successful!', 'output_file': file_path})
    
    except Exception as e:
        return jsonify({'error scrape': str(e)})


@app.route('/visualize', methods=['GET'])
def visualize_data():
    try:
        # Verificar que existe el archivo de links
        if not os.path.exists('archivos/links.json'):
            return jsonify({'error': 'No data available. Please run the scraper first.'}), 404

        data = asyncio.run(states())
        
        if not data:
            return jsonify({
                'message': 'No data points found, using default',
                'Data': [[21.284259, -99.417428, 1]]  # Punto por defecto en México
            })

        return jsonify({
            'message': 'Visualization successful!', 
            'Data': data
        })
    
    except Exception as e:
        print(f"Error in visualization: {str(e)}")
        return jsonify({
            'message': 'Error occurred, using default data',
            'Data': [[21.284259, -99.417428, 1]]  # Punto por defecto en México
        })
  

@app.route('/download', methods=['GET'])
def download_results():
    try:
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'links.json')

        # Verificar si el archivo existe
        if not os.path.exists(json_path):
            return jsonify({'error': 'File not found'}), 404

        # Leer el JSON y convertirlo en DataFrame
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Crear DataFrame con título y link
        df_data = []
        for title, info in data.items():
            df_data.append({
                'Título': title,
                'Link': info['Link']
            })
            
        df = pd.DataFrame(df_data)

        # Generar nombre único basado en fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"noticias_scrapeadas_{timestamp}.xlsx"
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

        # Guardar en Excel
        df.to_excel(excel_path, index=False)

        return send_from_directory(app.config['UPLOAD_FOLDER'], excel_filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error download': str(e)})
    
@app.route('/table', methods=['GET'])
def table_data():
    try:       
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'links.json', as_attachment=True)
    
    except Exception as e:
        return jsonify({'error table': str(e)})
    
#Tabla de descargas
@app.route('/download/excel/<int:file_id>')
def download_excel(file_id):
    # Diccionario de archivos (podrías tener esto en una base de datos)
    excel_files = {
        1: 'Databases/Usumacinta_transform.xlsx',
        2: 'Databases/DD28176_transform.xlsx',
        3: 'Databases/DD11075_transform.xlsx',
        # ... más archivos
    }
    
    # Obtener la ruta del archivo
    file_path = excel_files.get(file_id)
    
    if not file_path or not os.path.exists(file_path):
        return "Archivo no encontrado", 404
    
    # Obtener el nombre del archivo
    filename = os.path.basename(file_path)
    
    return send_file(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
 
