import os
from flask import Flask
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

app = Flask(__name__)

# إعداد المفاتيح بشكل آمن
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GBOOKING_API_KEY = os.getenv("GBOOKING_API_KEY")

# التحقق من تحميل المفاتيح بشكل صحيح
if not OPENAI_API_KEY or not GBOOKING_API_KEY:
    raise RuntimeError("❌ ERROR: API keys are missing! Please check your .env file.")

@app.route("/")
def home():
    return "API is Running!"
@app.route("/auth/login", methods=["POST"])
def login():
    return {"message": "Login endpoint is working!"}

if __name__ == "__main__":
    app.run(debug=True)
