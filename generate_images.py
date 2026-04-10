import urllib.request
import urllib.parse
from PIL import Image
import io
import os

def generate_mockup(prompt, filename):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
    
    print(f"Generating image for prompt: {prompt}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
            
        img = Image.open(io.BytesIO(img_data)).convert('RGB')
        
        # Load and paste logo
        try:
            logo = Image.open('img/logo.jpg').convert('RGBA')
            logo.thumbnail((150, 150))
            
            x = img.width - logo.width - 30
            y = img.height - logo.height - 30
            img.paste(logo, (x, y))
        except Exception as e:
            print("Error pasting logo:", e)
            
        img.save(f'img/{filename}', quality=90)
        print(f"Successfully saved {filename}")
        
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Prompts for the specific items described in id: 6
prompts = {
    'id6_ethiopia.jpg': 'A professional photo of a cup of hot latte coffee with beautiful latte art on a wooden cafe table, warm lighting, high resolution food photography',
    'id6_colombia.jpg': 'A professional photo of a glass of iced pour-over coffee with condensation, light and refreshing, bright cafe setting, high resolution',
    'id6_finedining.jpg': 'A gourmet fine dining dish with a delicious steak and roasted vegetables on a ceramic plate, restaurant setting, high resolution food photography',
    'id6_pasta.jpg': 'A beautifully plated gourmet pasta dish with fresh herbs and a side of light salad, restaurant setting, high resolution food photography'
}

for filename, prompt in prompts.items():
    generate_mockup(prompt, filename)
