para correr precisa-se de:
python 3.6
MySQL

---------------------------------------------------------------------------------------------

Comandos do projeto (nota: linha de comandos a apontar para a pasta do projeto "MaltaeC"):
 - Correr o website:
> python manage.py runserver


 - Popular BD com dados de teste:
> python DBinsertTestData.py



---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------

Setup MySQL:

 - Download MySQL community:
https://dev.mysql.com/downloads/windows/installer/5.7.html

 - Criar BD:
Abrir linha de comandos do MySQL e inserir:

> CREATE DATABASE MaltaC CHARACTER SET UTF8;
> CREATE USER mysqlDBUser@localhost IDENTIFIED BY 'maltaDBpassword';
> GRANT ALL PRIVILEGES ON MaltaC.* TO mysqlDBUser@localhost;
> FLUSH PRIVILEGES;
> exit

Nesta altura, terá criado uma BD de nome "MaltaC", com um utilizador "mysqlDBUser" e password "maltaDBpassword".

 - Nota: Pode-se mudar os parâmetros especificados atrás, é só substituir no sitio certo nos comandos atrás referidos
pelos nomes que queremos dar e Depois,
ir a "MaltaeC/MaltaCProject/settings.py"
substituir os parametros em "DATABASES", a que esta marcada com "#DB exemplo:" pelos novos parêmetros.





