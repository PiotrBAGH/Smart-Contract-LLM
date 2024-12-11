import os
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from Services.Parser.ContractParser import Parser  # Załaduj Parser

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def parse_smart_contract():
    """
    Wyświetla formularz HTML do przesyłania plików i przetwarza pliki .sol.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="Nie wybrano pliku.", functions=[])

        file = request.files['file']
        if not file.filename.endswith('.sol'):
            return render_template('index.html', error="Plik musi mieć rozszerzenie .sol.", functions=[])

        # Zapis pliku tymczasowo
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Parsuj funkcje za pomocą Parsera
            parser = Parser(file_path)
            functions = parser.extract_functions()

            os.remove(file_path)  # Usuń plik po przetworzeniu
            return render_template('index.html', functions=functions, file_name=os.path.splitext(file.filename)[0])

        except Exception as e:
            return render_template('index.html', error=str(e), functions=[])

    return render_template('index.html', functions=[])


@app.route('/save_function', methods=['POST'])
def save_function():
    """
    Zapisuje pojedynczą funkcję do pliku .txt w folderze o nazwie wczytanego pliku.
    """
    try:
        function_text = request.form.get('function')
        file_name = request.form.get('file_name')

        if not function_text or not file_name:
            return jsonify({"error": "Nie podano funkcji lub nazwy pliku."}), 400

        # Tworzenie folderu o nazwie pliku wewnątrz uploads
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        os.makedirs(folder_path, exist_ok=True)

        # Generowanie dynamicznej nazwy pliku
        timestamp = datetime.now().strftime("%H-%M-%S_%d-%m-%y")
        file_path = os.path.join(folder_path, f"function_{timestamp}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(function_text)

        app.logger.info(f"Funkcja zapisana: {file_path}")
        return jsonify({"message": f"Funkcja zapisana jako {file_path}"}), 200

    except Exception as e:
        app.logger.error(f"Błąd podczas zapisywania funkcji: {str(e)}")
        return jsonify({"error": "Wystąpił błąd podczas zapisywania funkcji."}), 500


if __name__ == '__main__':
    app.run(debug=True)
