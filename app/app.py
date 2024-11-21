from flask import Flask, render_template, request
import sys
import os

# Adiciona o caminho raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa funções necessárias
from test import check_token, query, remove_token

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/submit", methods=["POST", "GET"])
def submit():
    try:
        data = request.form

        # Debug: Exibe os dados recebidos
        print("Dados recebidos:", data)

        # Verifica se os campos necessários estão presentes no request
        if 'text[]' not in data or 'length[]' not in data:
            return render_template('index.html', suggestion_text="Erro: Dados incompletos enviados.")

        example = check_token(data['text[]'])

        # Calcula o comprimento do texto de entrada
        input_len = len(example.split())
        size = int(data['length[]'])  # Valor fornecido pelo usuário ou padrão

        # Chama a função query para gerar texto
        output = query({
            "inputs": example,
            "parameters": {
                'repetition_penalty': 1.2,
                'num_beams': 5,
                'no_repeat_ngram_size': 3,
                'max_length': input_len + size
            }
        })

        # Debug: Verifica o retorno de query
        print("Output recebido da query:", output)

        # Verifica se a saída possui o formato esperado
        if isinstance(output, list) and len(output) > 0 and 'generated_text' in output[0]:
            generated_text = output[0].get('generated_text')
        else:
            generated_text = "Erro: Não foi possível gerar o texto."

        # Remove tokens indesejados do texto gerado
        suggestion_text = remove_token(generated_text)

        return render_template('index.html', suggestion_text=suggestion_text)

    except Exception as e:
        # Log do erro para depuração
        print("Erro no endpoint /submit:", e)
        return render_template('index.html', suggestion_text=f"Erro interno: {str(e)}")

@app.route("/social")
def social():
    return render_template('social.html')

@app.route("/members")
def members():
    return render_template('members.html')

if __name__ == "__main__":
    app.run()
