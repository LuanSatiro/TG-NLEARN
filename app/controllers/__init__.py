from app import app


@app.route("/")
def default():
    return "Hello World eu sou o Luan e esse será meu TG e o tema da disciplina laboratório de engenharia de software 2020-02 "
