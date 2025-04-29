## Component layer MySQL project
### Running the project
1. Clone the repo
2. Open the folder in a terminal (commandprompt, powershell, WSL, ...)
3. Download the dependencies
```
pip install -r requirements.txt 
``` 

<br>

4. Setup the MySQL database using the **createTables.sql** and fill it with **dummyData.sql**
```
This is done by using a database interface of your choice (MySQL Workbench, XAMPP + phpmyadmin, ...)
It is important that the schema is called "componentlayer_db" and the credentials should be:
User: "root" 
Pass: "toor"
The MySQL server should also run on the default port: 3306
``` 

<br>

5. Run the flask server
```
python app.py
``` 
The website should now be live on http://localhost:8000/

Feel free to contact the authors in case of confusion or errors :)

---

### Guide to setup in vscode
1. Clone project
2. Open project folder in vscode
3. Setup a python environment with
```
python -m venv .venv
```

4. Activate the environment
```
./.venv/Scripts/activate.ps1
```
This step requires that **powershell execution policy** is set as unrestricted
See [Microsoft docs](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.5) for guide


5. Install the dependencies
```
pip install -r requirements.txt
```
Note: If you add more dependencies please update requirements.txt accordingly
```
pip freeze > requirements.txt
```

<br>

6. To run flask app open terminal in vscode and type 
```
python app.py
```
Note: Website should now be running on http://localhost:8000/
 
---

### Writing css
1. Download "Live Sass Compiler" extension in vscode
2. Click CTRL + SHIFT + P and run
``` 
Live Sass: Watch Sass
```
Note: Please lookup how to use scss, but now it should be "compiling" automatically
