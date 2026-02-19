from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def Hello():
    return {"message": "Hello World I am Mudassar Gill"}
@app.get("/about")
def about():
    return {"message": "I am a student of Computer Science"}
@app.get("/contact")
def contact():
    return {"message": "You can contact me at [EMAIL_ADDRESS]"}