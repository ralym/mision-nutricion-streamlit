Mision Nutricion - Streamlit
============================

Juego educativo hecho con Streamlit.

La version web toma como base el flujo del archivo local `mision_nutricion.py`,
pero ahora funciona como formulario por pasos.

Cada grupo puede entrar al mismo link al mismo tiempo desde su propia computadora
o celular. El grupo escribe su nombre, recibe un paciente al azar, completa las
misiones y envia su resultado. El ranking se guarda en `resultados.json` y todos
pueden verlo desde el boton "Ver ranking en vivo".

Archivos principales
--------------------

- `mision_nutricion.py`: version local original con Tkinter.
- `app.py`: version web para Streamlit.
- `iniciar.bat`: arranque rapido en Windows.
- `resultados.json`: ranking compartido, se crea automaticamente cuando un grupo
  envia su resultado.

Como ejecutarla en Windows
--------------------------

1. Abrir PowerShell en esta carpeta:

   C:\Users\RAUL\Downloads\mision_nutricion_streamlit

2. Crear el entorno virtual, si todavia no existe:

   py -3.12 -m venv .venv

3. Instalar dependencias:

   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

4. Arrancar la app:

   .\.venv\Scripts\python.exe -m streamlit run app.py

5. Abrir en el navegador:

   http://localhost:8501

Forma facil
-----------

Tambien puedes ejecutar:

.\iniciar.bat

Nota
----

En esta computadora el comando `python` puede abrir el lanzador de Windows o usar
Python 3.14 beta. Por eso es mejor usar `py -3.12` para crear el entorno y luego
ejecutar Streamlit con:

.\.venv\Scripts\python.exe -m streamlit run app.py

Publicar en Streamlit Community Cloud
-------------------------------------

1. Subir a GitHub estos archivos principales:

   app.py
   requirements.txt
   README.txt

2. No subir la carpeta `.venv`, `__pycache__` ni `resultados.json`.

3. En Streamlit Community Cloud crear una app nueva desde el repositorio de
   GitHub.

4. Configurar:

   Main file path: app.py

5. Deploy.

Nota sobre el ranking
---------------------

El ranking se guarda en `resultados.json`. En local funciona bien. En Streamlit
Community Cloud puede funcionar durante la sesion de la app, pero no debe
considerarse almacenamiento permanente: si la app se reinicia, se redeploya o se
duerme, los resultados pueden perderse. Para un ranking permanente haria falta
conectarlo a una base de datos o a Google Sheets.

Ranking permanente con Google Sheets
------------------------------------

La app ya soporta Google Sheets de forma opcional.

Si no configuras Google Sheets, usa `resultados.json` en local.
Si configuras Google Sheets en Streamlit Secrets, el ranking se guarda en la hoja.

Pasos generales:

1. Crear una hoja de Google Sheets.

2. Copiar el ID de la hoja. Es la parte de la URL entre `/d/` y `/edit`.

3. En Google Cloud, crear un service account y descargar su clave JSON.

4. Compartir la hoja de Google Sheets con el correo `client_email` del JSON.
   Dale permiso de editor.

5. En Streamlit Community Cloud ir a:

   App settings > Secrets

6. Pegar los secretos con esta estructura:

   google_sheet_id = "ID_DE_TU_GOOGLE_SHEET"
   google_worksheet = "ranking"

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "..."
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."

7. Hacer redeploy.

Tambien puedes ver el archivo `.streamlit/secrets.toml.example`.

Importante: nunca subas `.streamlit/secrets.toml` real a GitHub.
