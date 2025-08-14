import vertexai
from vertexai.generative_models import GenerativeModel

# --- CONFIGURACIÓN ---
PROJECT_ID = "neurodiagnoses-cli-12345"
REGION = "us-central1"
MODEL_NAME = "gemini-1.5-flash-latest"

# --- LÓGICA DEL SCRIPT ---
def ask_gemini_about_code(file_to_analyze):
    """Lee un archivo, se lo pasa a Gemini y muestra la respuesta."""
    
    # Inicializa la conexión con Vertex AI
    vertexai.init(project=PROJECT_ID, location=REGION)
    
    # Carga el modelo Gemini que queremos usar
    model = GenerativeModel(model_name=MODEL_NAME)
    
    print(f"--- Leyendo el archivo: {file_to_analyze} ---")
    with open(file_to_analyze, 'r') as f:
        file_content = f.read()
    
    prompt = f"Explica el propósito de este script de Python en 3 puntos clave: {file_content}"
    
    print("--- Enviando la pregunta a Gemini... ---")
    response = model.generate_content(prompt)
    
    print("--- Respuesta de Gemini: ---")
    print(response.text)

if __name__ == '__main__':
    # Le pedimos que analice el script que creamos en nuestro proyecto
    ask_gemini_about_code('run_neurodiagnosis.py')
