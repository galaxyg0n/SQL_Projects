## Component layer - Assignment 1
### Guide to setup in vscode
1. Clone project
2. Open project folder in vscode
3. Setup a python environment with
```
python -m venv venv
```
4. Activate the environment
```
./venv/Scripts/activate.ps1
```
5. Install the dependencies
```
pip install -r requirements.txt
```
Note: If you add more dependencies please update requirements.txt accordingly

6. To run flask app open terminal in vscode and type 
```
python app.py
```
Note: Website should now be running on http://localhost:8000/

### Writing css
1. Download "Live Sass Compiler" extension in vscode
2. Click CTRL + SHIFT + P and run
``` 
Live Sass: Watch Sass
```
Note: Please lookup how to use scss, but now it should be "compiling" automatically