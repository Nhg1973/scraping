import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import re  # Importa el módulo de expresiones regulares

# Cargar el conjunto de datos
data = pd.read_csv('Emotion_classify_Data.csv')

# Preprocesamiento de texto
def preprocess(text):
    # Convertir texto a minúsculas
    text = text.lower()
    # Eliminar caracteres no alfabéticos
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Vectorización de texto utilizando TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Comment'])
y = data['Emotion']

# División del conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo SVM
model = SVC()
model.fit(X_train, y_train)

# Función para predecir la emoción a partir de una frase de entrada
def predict_emotion(input_text):
    # Preprocesamiento similar al usado en los datos de entrenamiento
    processed_text = preprocess(input_text)

    # Vectorización del texto preprocesado utilizando el mismo vectorizador
    vectorized_text = vectorizer.transform([processed_text])

    # Predicción utilizando el modelo entrenado
    predicted_emotion = model.predict(vectorized_text)
    return predicted_emotion[0]

# Ejemplo de uso de la función con una frase de entrada
input_text = "She trembled in fear as she heard footsteps approaching in the dark"
predicted_emotion = predict_emotion(input_text)
print("Emoción predicha para la frase:", predicted_emotion)
