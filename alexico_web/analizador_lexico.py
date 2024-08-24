import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

reserved = {
    'for' : 'FOR',
    'do'  : 'DO',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE'
}

tokens = ['PABIERTO','PCERRADO'] + list(reserved.values())

t_FOR = r'for'
t_DO = r'do'
t_WHILE = r'while'
t_IF = r'if'
t_ELSE = 'else'
t_ignore = ' \t\n\r'

t_PABIERTO = r'\('
t_PCERRADO = r'\)'

def t_error(t): 
    print('Caracter no valido',t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

@app.route('/', methods = ['GET','POST'])

def index():
    if request.method == 'POST':
        content = request.form.get('code','')
        lexer.input(content)
 
        result_lexema = [
            (f"Reservada {token.type.capitalize()}" if token.type in reserved.values() else "Parentesis de apertura" if token.type == "ABIERTO" else "Parentesis de cierre", token.value)
            for token in lexer
        ]
        return render_template('index.html', tokens=result_lexema)
    return render_template('index.html', tokens=None)
 
if __name__ == "main":
    app.run(debug=True)