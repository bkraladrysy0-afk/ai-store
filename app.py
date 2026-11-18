
from flask import Flask, request, jsonify, render_template_string
import random, requests

app = Flask(__name__)
ID = "710722794695"
TOKEN = "9d626941d9704b22bd7d3ac109f24fe26b3e6b7eacbb4251b5"
codes = {}

HTML = """
<!DOCTYPE html><html dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>متجر الذكاء الاصطناعي</title><style>body{font-family:sans-serif;background:#0f0f1a;color:white;padding:20px;text-align:center}input{width:100%;padding:13px;border-radius:10px;border:none;margin:8px 0;font-size:16px;box-sizing:border-box}button{width:100%;padding:13px;background:#25d366;color:white;border:none;border-radius:10px;font-size:17px;cursor:pointer}.box{background:#1e1e2e;padding:20px;border-radius:15px;margin-top:20px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}.card{background:#1e1e2e;padding:18px 10px;border-radius:15px;text-decoration:none;color:white;display:block}.card span{font-size:35px;display:block}.card b{font-size:15px}</style></head><body>
<h2>🤖 متجر الذكاء الاصطناعي</h2><p>أدخل رقمك، وصلك الكود، وافتح أي موقع</p>
<div class="box">
<input id="phone" placeholder="مثال: 967777123456">
<button onclick="sendCode()">📩 ارسل لي الكود واتساب</button>
<input id="code" placeholder="اكتب الكود اللي وصلك" style="margin-top:15px">
<button onclick="verify()" style="background:#a855f7">تحقق ✅</button>
<p id="msg"></p>
</div>
<div class="grid" id="apps"></div>
<script>
let apps=[
 {n:'Sora',e:'🎬',l:'https://openai.com/sora'},
 {n:'Suno',e:'🎵',l:'https://suno.com'},
 {n:'ChatGPT',e:'💬',l:'https://chatgpt.com'},
 {n:'Gemini',e:'✨',l:'https://gemini.google.com'},
 {n:'Claude',e:'🧠',l:'https://claude.ai'},
 {n:'Midjourney',e:'🎨',l:'https://midjourney.com'},
 {n:'Canva AI',e:'🖼️',l:'https://canva.com'},
 {n:'CapCut',e:'✂️',l:'https://capcut.com'},
 {n:'Copilot',e:'🤖',l:'https://copilot.microsoft.com'},
 {n:'Leonardo',e:'🦁',l:'https://leonardo.ai'},
];
let h='';
apps.forEach(a=>{h+=`<a class="card" href="${a.l}" target="_blank"><span>${a.e}</span><b>${a.n}</b></a>`});
document.getElementById('apps').innerHTML=h;
async function sendCode(){
 let phone=document.getElementById('phone').value;
 let r=await fetch('/send-code',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone})});
 let d=await r.json();
 document.getElementById('msg').innerText=d.msg;
}
async function verify(){
 let phone=document.getElementById('phone').value;
 let code=document.getElementById('code').value;
 let r=await fetch('/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone,code})});
 let d=await r.json();
 if(d.ok){document.getElementById('msg').innerText='✅ تم التحقق! الآن اضغط على أي أيقونة';}
 else{document.getElementById('msg').innerText='الكود غلط، حاول مرة ثانية';}
}
</script></body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/send-code', methods=['POST'])
def send_code():
    phone = request.json.get('phone')
    code = str(random.randint(100000, 999999))
    codes[phone] = code
    url = f"https://7107.api.green-api.com/waInstance{ID}/sendMessage/{TOKEN}"
    msg = f"كود التحقق لموقعك هو: {code} 🔐 لا تشاركه مع احد"
    r = requests.post(url, json={"chatId": f"{phone}@c.us", "message": msg})
    print("Green-API:", r.text)
    return jsonify({"msg": "تم ارسال الكود لواتسابك ✅"})
@app.route('/verify', methods=['POST'])
def verify():
    phone = request.json.get('phone')
    code = request.json.get('code')
    if codes.get(phone) == code:
        return jsonify({"ok": True})
    return jsonify({"ok": False})
if __name__ == '__main__':
    app.run
