from fastapi import FastAPI
import json
app=FastAPI()
def load_data():
   data= json.load(open("patients.json", "r"))
   return data 

@app.get("/")
def Hello():
    return {"message": "Hello World I am Mudassar Gill"}
@app.get("/about")
def about():
    return {"message": "I am a student of Computer Science"}
@app.get("/view")
def view():
    return load_data()

