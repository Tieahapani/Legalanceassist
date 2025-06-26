from flask import Flask, request, jsonify 
from explain import simplify_with_claude 

app = Flask(__name__)

@app.route("/vapi-webhook", methods=["POST"])
def handle_voice():
    data = request.json
    user_input = data.get("transcript", "")
    
    if not user_input:
        return jsonify({"response": "Sorry, I did'nt catch that."})
    
    reply = simplify_with_claude(user_input)
    
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Claude: {reply}\n")
        f.write("-" * 40 + "\n")
    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Hello! Flask is working."

if __name__ == "__main__":
     app.run(debug=True)
    

