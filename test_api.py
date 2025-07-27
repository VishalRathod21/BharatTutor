from dotenv import load_dotenv; import os; load_dotenv(); print("API Key loaded successfully!" if os.getenv("GEMINI_API_KEY") else "API Key not found!")
