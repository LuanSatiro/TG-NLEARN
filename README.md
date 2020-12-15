# TG-NLEARN


### Requisitos:

```
Python 3.9
Mysql
git

```

### Primeiros passos:

```
Navegue até a pasta onde quer clonar o projeto pelo cmd
execute: git clone https://github.com/LuanSatiro/TG-NLEARN
execute: pip install -r requirements.txt
```

### Segunda etapa: 

```
Na pasta raiz abra o arquivo config.py onde encontrará uma linha como está SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:@maxter@m4@localhost/nlearn'
altere o usuário e a senha para as credenciais do seu banco Mysql
Crie um schema em seu banco no qual inseriu as credenciais, utilize o nome de nlearn.


```
### Terceira etapa(popular o schema com tables e column): 

```
Na pasta raiz execute o comando: python run.py db stamp head
e depois: python run.py db migrate
e por fim: python run.py db upgrade

```

### Quarta etapa: 

```
Entre no seu banco Mysql pelo workbench e adicione um usuário e senha e no campo flag utilize "king" na table Users para poder fazer login na plataforma

```
### Etapa final: 

```
Execute: python run.py runserver
Após isso navegue até o localhost pelo navegador na página index: http://localhost:5000/index

```

### Demonstrando o funcionamento parcial da aplicação: https://www.youtube.com/watch?v=n51UwHDRNfo&feature=youtu.be
### Demonstrando o funcionamento completo da aplicação: https://www.youtube.com/watch?v=XuhpMKGNcz4&feature=youtu.be
