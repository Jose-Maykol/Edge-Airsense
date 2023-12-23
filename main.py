from fastapi import FastAPI

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Ruta básica de prueba
@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}

# Ejecutar con uvicorn main:app --reload
# Otras rutas y lógica de tu aplicación FastAPI aquí...

# Si ejecutas este archivo directamente, se levantará el servidor
if __name__ == "__main__":
    import uvicorn

    # Iniciar el servidor usando Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
