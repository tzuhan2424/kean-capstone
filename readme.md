# Project Introduction

Algae bloom map


## Backend env set up

### env solution1
```bash
conda env create -f environment.yml
```

### env solution2
```bash
conda create -n cap python=3.9.18
pip install -r requirements.txt
```
If you need install more package for backend service, please add into package.md
what package you install, and what service it provide



## Frontend env set up 
```bash
npm install
npm start
```


## Frontend ENV
create a .env file at backend/
<br>
DB_NAME = XXX
DB_USER = XXX
DB_PASSWORD = XXXXX
HOST = XXXX



## Backend ENV
create a .env.local file at frontend/
<br>
REACT_APP_ARCGIS_API_KEY="XXXXX"

