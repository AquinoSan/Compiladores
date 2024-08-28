import re
from flask import Flask, render_template, request

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
    ('COMA', r','),
    ('PUNTO_Y_COMA', r';'),
    ('DOS_PUNTOS', r':'),
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
    while position < len(code):
        match = None
        for token_type, pattern in token_lexema:
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                value = match.group(0)
                tokens.append((token_type, value, line))
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
                position += 1
    return tokens

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('code', '')
        tokens = tokenize(content)
        return render_template('index.html', tokens=tokens, code=content)
    return render_template('index.html', tokens=None, code='')

if __name__ == "_main_":
    app.run(debug=True)