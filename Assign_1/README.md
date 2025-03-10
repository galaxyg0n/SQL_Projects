## Component layer - Assignment 1
### Guide to setup in vscode
1. Clone project
2. Open project folder in vscode
3. Create .vscode folder
4. Create settings.json in .vscode folder
5. Insert the following in the settings.json
```
{
    "python.defaultInterpreterPath": "[INSERT YOUR PATH]\\Assign_1\\env\\Scripts\\python.exe"
}
```

Note: This sets up the enviroment and should fix the missing dependencies



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