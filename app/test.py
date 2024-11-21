import requests

# URL do modelo no Hugging Face
API_URL = "https://api-inference.huggingface.co/models/Felipehonorato/storIA"
headers = {"Authorization": "Bearer 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"}

# Função para remover tokens do início do texto gerado
def remove_token(text):
    return " ".join(text.split()[1:])

# Função para verificar e adicionar o token necessário no input
def check_token(input):
    token = '<|startoftext|>'
    if not input.startswith(token):
        return token + " " + input
    return input

# Função para fazer requisição ao modelo da Hugging Face
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Gera erro se o status não for 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return {"error": str(e)}

# Input do usuário
input_text = 'it was a dark night'  # Texto do usuário
input_len = len(input_text.split())  # Número de palavras no texto de entrada
size = 20  # Comprimento adicional especificado pelo usuário

# Verifica e ajusta o input com o token necessário
input_text = check_token(input_text)

# Faz a chamada ao modelo
output = query({
    "inputs": input_text,
    "parameters": {
        "max_length": input_len + size,
        "repetition_penalty": 1.2,
        "num_beams": 5,
        "no_repeat_ngram_size": 3
    }
})

# Processa o output
if 'error' in output:
    print(f"Erro no modelo: {output['error']}")
else:
    generated_text = output[0].get('generated_text', "Texto não gerado.")
    # Remove tokens indesejados do texto gerado
    cleaned_text = remove_token(generated_text)
    print("Texto gerado:", cleaned_text)
