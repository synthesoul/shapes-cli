import json
import datetime
import os
import re
import subprocess
import urllib.request
from openai import OpenAI

# --- Initial Setup ---
api_key = input("Enter your Shapes API Key: ").strip()
model_name = input("Enter your Shape Model (default: shapesinc/chatgpt-0sob): ").strip()
if not model_name:
    model_name = "shapesinc/chatgpt-0sob"

shape_id = model_name.split("/")[-1]
log_dir = os.path.join("chatlogs", shape_id)
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_txt = os.path.join(log_dir, f"{timestamp}_{shape_id}.txt")
log_json = os.path.join(log_dir, f"{timestamp}_{shape_id}.json")
play_audio = False
context_mode = "nonintrusive"  # Options: nonintrusive, intrusive, incognito

shapes_client = OpenAI(
    api_key=api_key,
    base_url="https://api.shapes.inc/v1/",
)

# --- Load Context Logs Based on Mode ---
def load_context():
    convo = [{"role": "user", "content": "Hello"}]
    if context_mode == "incognito":
        return convo

    base_dir = "chatlogs" if context_mode == "intrusive" else log_dir
    for root, _, files in os.walk(base_dir):
        for f in sorted(files):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(root, f), "r") as file:
                        data = json.load(file)
                        convo.extend(data[-4:])
                except:
                    continue
    return convo

# --- Chat Handler ---
def chat_with_model(convo, model):
    try:
        response = shapes_client.chat.completions.create(
            model=model,
            messages=convo
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] {str(e)}"

# --- Play Audio from MP3 URL ---
def play_mp3_from_url(text):
    if not play_audio:
        return
    match = re.search(r'https://files\.shapes\.inc/[^\s]+\.mp3', text)
    if match:
        url = match.group(0)
        local_file = "/tmp/shape_speech.mp3"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response, open(local_file, 'wb') as out_file:
                out_file.write(response.read())
            subprocess.run(["mpg123", local_file], check=False)
        except Exception as e:
            print(f"[!] Could not play audio: {e}")

# --- Save Logs ---
def save_logs():
    if context_mode == "incognito":
        return
    with open(log_txt, "w") as f:
        for msg in conversation:
            f.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
    with open(log_json, "w") as f:
        json.dump(conversation, f, indent=2)

# --- History Functions ---
def list_logs():
    if not os.path.isdir(log_dir):
        print("[No logs directory found]")
        return []
    files = sorted([f for f in os.listdir(log_dir) if f.endswith(".txt")])
    if not files:
        print("[No saved chats found]")
        return []
    for i, file in enumerate(files):
        print(f"{i}: {file}")
    return files

def read_log(index):
    files = list_logs()
    if 0 <= index < len(files):
        with open(os.path.join(log_dir, files[index]), "r") as f:
            print(f"\n--- {files[index]} ---")
            print(f.read())
            print("------")
    else:
        print("[!] Invalid index.")

def load_json_log(index):
    files = sorted([f for f in os.listdir(log_dir) if f.endswith(".json")])
    if 0 <= index < len(files):
        with open(os.path.join(log_dir, files[index]), "r") as f:
            return json.load(f)
    else:
        print("[!] Invalid index.")
        return None

# --- Load and Respond ---
conversation = load_context()
print("\n[Assistant is loading...]\n")
initial_reply = chat_with_model(conversation, model_name)
print("AI:", initial_reply)
play_mp3_from_url(initial_reply)
conversation.append({"role": "assistant", "content": initial_reply})

# --- Help Message ---
help_text = """
[COMMANDS]
/exit                  → Exit the chat
/change <model>        → Change to a new character model
/save                  → Save chat to log files now
/audio on              → Turn ON voice playback
/audio off             → Turn OFF voice playback
/context <mode>        → Set context mode: intrusive, nonintrusive, incognito
/history               → List saved chats for this character
/history read <index>  → Read a saved chat
/history load <index>  → Resume a saved chat
/help                  → Show this help message
"""
print(help_text)

# --- Main Loop ---
while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["/exit", "exit", "quit"]:
        print("Exiting and saving chat history...")
        save_logs()
        break

    elif user_input.lower().startswith("/change "):
        new_model = user_input[8:].strip()
        if new_model:
            model_name = new_model
            shape_id = model_name.split("/")[-1]
            log_dir = os.path.join("chatlogs", shape_id)
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_txt = os.path.join(log_dir, f"{timestamp}_{shape_id}.txt")
            log_json = os.path.join(log_dir, f"{timestamp}_{shape_id}.json")
            print(f"✔ Model changed to: {model_name}")
        else:
            print("[!] No model specified.")
        continue

    elif user_input.lower() == "/audio on":
        play_audio = True
        print("🔊 Audio playback is now ON.")
        continue

    elif user_input.lower() == "/audio off":
        play_audio = False
        print("🔇 Audio playback is now OFF.")
        continue

    elif user_input.lower().startswith("/context "):
        mode = user_input.split()[1].lower()
        if mode in ["intrusive", "nonintrusive", "incognito"]:
            context_mode = mode
            print(f"🧠 Context mode set to: {context_mode}")
        else:
            print("[!] Invalid context mode. Choose: intrusive, nonintrusive, incognito.")
        continue

    elif user_input.lower() == "/help":
        print(help_text)
        continue

    elif user_input.lower() == "/save":
        save_logs()
        print(f"✔ Conversation saved to {log_txt} and {log_json}")
        continue

    elif user_input.lower() == "/history":
        list_logs()
        continue

    elif user_input.lower().startswith("/history read "):
        try:
            index = int(user_input.split()[2])
            read_log(index)
        except:
            print("[!] Usage: /history read <index>")
        continue

    elif user_input.lower().startswith("/history load "):
        try:
            index = int(user_input.split()[2])
            loaded = load_json_log(index)
            if loaded:
                conversation.clear()
                conversation.extend(loaded)
                print("✔ Chat history loaded. You can now continue this session.")
        except:
            print("[!] Usage: /history load <index>")
        continue

    # --- Normal Chat Message ---
    conversation.append({"role": "user", "content": user_input})
    ai_reply = chat_with_model(conversation, model_name)
    print("AI:", ai_reply)
    play_mp3_from_url(ai_reply)
    conversation.append({"role": "assistant", "content": ai_reply})
