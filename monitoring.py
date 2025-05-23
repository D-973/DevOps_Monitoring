import google.generativeai as genai
import datetime
import requests
import subprocess

# Konfigurasi API Gemini
genai.configure(api_key="AIzaSyDSILjc0WLk3FpLdpkmWvEbt1hZnuCQeo0")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_ssh_attempts():
    result = subprocess.check_output("grep 'Failed password' /var/log/auth.log | tail -n 10", shell=True)
    return result.decode()

def get_gemini_analysis(log_text):
    try:
        response = model.generate_content(f"Ambil percobaan login hanya hari ini dan 1 percobaan login terakhir saja. Ada percobaan login brute force:\n{log_text}\nApa yang sebaiknya saya lakukan?. responnya jangan terlalu panjang. Output deskripsi singkat percobaan login terakhir.")
        return response.text
    except Exception as e:
        return f"⚠️ Gagal mendapatkan analisis dari Gemini: {e}"

def send_whatsapp(message):
    token = "B9onMvcpADMhWgHXxjq9"
    payload = {
        "target": "628981659030",  # Add country code
        "message": message,
    }
    headers = {"Authorization": token}
    try:
        r = requests.post("https://api.fonnte.com/send", data=payload, headers=headers)
        print(f"WhatsApp API response status: {r.status_code}")
        print(f"Response content: {r.text}")
        return r.status_code
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None

# Eksekusi semua
log = get_ssh_attempts()
ai_response = get_gemini_analysis(log)
full_message = f"[{datetime.datetime.now()}] ⚠️ 🧠 Gemini says:\n{ai_response}"
send_whatsapp(full_message)