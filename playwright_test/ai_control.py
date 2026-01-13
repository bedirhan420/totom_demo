from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from pydantic import SecretStr

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Farklı isimleri test et
models_to_test = [
    "gemini-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
]

for model_name in models_to_test:
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=SecretStr(api_key),
            temperature=0.0,
        )
        result = llm.invoke("Hi")
        print(f"✅ {model_name}: ÇALIŞIYOR")
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:80]}...")