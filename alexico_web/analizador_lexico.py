import re
from flask import Flask, render_template, request
from collections import defaultdict

app = Flask(__name__)

token_lexema = [
    ('PALABRA_RESERVADA', r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|null|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b'),
    ('NUMERO', r'\d+'),
    ('IDENTIFICADOR', r'[A-Za-z_]\w*'),
    ('SUMA', r'\+'),
    ('RESTA', r'-'),
    ('MULTIPLICACION', r'\*'),
    ('DIVISION', r'/'),
    ('PARENTESIS_IZQ', r'\('),
    ('PARENTESIS_DER', r'\)'),
    ('LLAVE_IZQ', r'\{'),
    ('LLAVE_DER', r'\}'),
    ('CORCHETE_IZQ', r'\['),
    ('CORCHETE_DER', r'\]'),
    ('COMA', r','),
    ('PUNTO_Y_COMA', r';'),
    ('DOS_PUNTOS', r':'),
    ('PUNTO', r'\.'),
    ('COMILLA_DOBLE', r'"'),
    ('IGUAL', r'='),
    ('MENOR_QUE', r'<'),
    ('MAYOR_QUE', r'>'),
    ('MENOR_IGUAL', r'<='),
    ('MAYOR_IGUAL', r'>='),
    ('IGUAL_IGUAL', r'=='),
    ('DIFERENTE', r'!='),
]

def tokenize(code):
    tokens = []
    position = 0
    line = 1
    token_count = defaultdict(int)  # Diccionario para contar tokens repetidos
    
    while position < len(code):
        match = None
        for token_type, pattern in token_lexema:
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                value = match.group(0)
                tokens.append((token_type, value, line))
                token_count[token_type] += 1  # Incrementa el contador del token
                position = match.end()
                break
        if not match:
            if code[position] == '\n':
                line += 1
                position += 1
            elif code[position].isspace():
                position += 1
            else:
                tokens.append(('DESCONOCIDO', code[position], line))
                token_count['DESCONOCIDO'] += 1  # Cuenta también tokens desconocidos
                position += 1
    
    return tokens, token_count

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('code', '')
        tokens, token_count = tokenize(content)  # Obtiene los tokens y el conteo
        return render_template('index.html', tokens=tokens, token_count=token_count, code=content)
    return render_template('index.html', tokens=None, token_count=None, code='')

if __name__ == "_main_":
    app.run(debug=True)