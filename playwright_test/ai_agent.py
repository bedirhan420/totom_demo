import os
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr, ConfigDict

# API Anahtarı Kontrolü
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ HATA: GROQ_API_KEY bulunamadı! .env dosyasını kontrol et.")
    exit(1)

# --- NİHAİ DÜZELTME SINIFI ---
class ChatOpenAIFixed(ChatOpenAI):
    # Pydantic'e "Ekstra özellik eklememe izin ver" diyoruz.
    model_config = ConfigDict(extra='allow')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. browser-use'un "Sen kimsin?" sorusuna cevap:
        self.provider = "openai" 
        
        # 2. --- KRİTİK DÜZELTME ---
        # Hatanın sebebi burasıydı. Kütüphane .model arıyor, bizde .model_name var.
        # Bunları eşitliyoruz.
        self.model = self.model_name
# -----------------------------

async def main():
    print("🤖 Ajan Başlatılıyor... (Motor: Groq Llama 3.3 -> OpenAI Adapter)")

    # 1. Kendi oluşturduğumuz Fixed sınıfı kullanıyoruz
    llm = ChatOpenAIFixed(
        base_url="https://api.groq.com/openai/v1", # Adresi Groq'a yönlendir
        api_key=SecretStr(api_key),
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

    # 2. Görev Tanımı
    gorev = """
    Go to 'https://www.wikipedia.org'.
    Type 'Mustafa Kemal Atatürk' into the search input and press Enter.
    Wait for the result page to load.
    Find the 'Born' (Doğum) date in the text or infobox.
    Return ONLY the birth date string as the final result.
    """

    # 3. Ajanı Oluştur
    agent = Agent(
        task=gorev,
        llm=llm,
        use_vision=False, 
    )

    print("🚀 Tarayıcı (Headless) çalışıyor...")
    
    try:
        # Çalıştır
        history = await agent.run()
        
        print("\n" + "="*50)
        print("🏁 SONUÇ:")
        print(history.final_result())
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Bir hata oluştu:\n{e}")

if __name__ == "__main__":
    asyncio.run(main())