## Instrucciones para instalar los paquetes:

---

**Nota:** El proyecto requiere un archivo `.env` donde se tiene que especificar las siguientes variables:

- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS
- SECRET_KEY
- UPLOAD*FOLDER=static/productos_imgs \_Se tiene que poner tal cual en el archivo .env*
- MAIL_SERVER
- MAIL_PORT
- MAIL_USERNAME
- MAIL_PASSWORD
- MAIL_USE_TLS

Primero se tiene que instalar el paquete `viertualenv`.

` pip install virtualenv`

Ya teniendo instalado `virtualenv` se tiene que crear un entorno virtual de la siguiente manera:

` virtualenv env`

Y activamos el entorno:

- Para Ubuntun `source env/bin/activate`

- Para Windows `.\env\Scripts\activate`

Ahora para instalar los paquetes listados en el archivo `requirements.txt` ejecutamos el siguiente comando:

` python -m pip install -r requirements.txt`

### Para correr el proyecto.

```
  set FLASK_APP=main:app
  set FLASK_ENV=development
  flask run
```
