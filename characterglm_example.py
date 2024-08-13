import time
from dotenv import load_dotenv
from requests.exceptions import ConnectionError
from api import get_characterglm_response

load_dotenv()

def create_character_profile(text):
    return {
        "user_info": "阿南，性别男，18岁，孤儿院中的大哥哥。",
        "bot_info": "小白，性别女，17岁，患有先天白血病。",
        "user_name": "阿南",
        "bot_name": "小白"
    }

def append_to_file(line, filename="dialogue.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(line)

def fetch_responses(messages, meta, retries=10, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = list(get_characterglm_response(messages, meta=meta))
            if response:
                return response
        except ConnectionError as e:
            print(f"Connection error: {e}. Retrying {attempt + 1}/{retries}...")
        attempt += 1
        time.sleep(delay)
    raise ConnectionError("Max retries exceeded.")

def characterglm_example():
    text = """
    在漫天大雪中，小白被孤儿院院长捡到。她身穿红裙子，脸色苍白。
    阿南是她的好朋友，总是陪伴在她身边。
    """
    character_meta = create_character_profile(text)
    messages = [
        {"role": "assistant", "content": "哥哥，我会死吗？"},
        {"role": "user", "content": "怎么会呢？医生说你的病情已经好转了"}
    ]
    
    reply = 0
    for _ in range(3):  # 进行3轮对话
        responses = fetch_responses(messages, meta=character_meta)
        if not responses:
            print("No response received. Ending dialogue.")
            break
        else:
            reply = reply + 1
        for i, chunk in enumerate(responses):
            role = "小白" if reply % 2 == 0 else "阿南"
            line = f"{role}: {chunk}\n"
            print(line.strip())
            append_to_file(line)
        last_message = responses[-1]
        messages.append({
            "role": "assistant" if len(messages) % 2 == 1 else "user",
            "content": last_message
        })

if __name__ == "__main__":
    characterglm_example()