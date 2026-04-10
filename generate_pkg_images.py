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
            # Make the logo a bit prominent for packaging
            logo.thumbnail((200, 200))
            
            # Paste the logo right in the center to simulate printed branding
            x = (img.width - logo.width) // 2
            y = (img.height - logo.height) // 2
            img.paste(logo, (x, y))
        except Exception as e:
            print("Error pasting logo:", e)
            
        img.save(f'img/{filename}', quality=90)
        print(f"Successfully saved {filename}")
        
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Prompts for the packaging items described in id: 4 (Takeaway cup, coffee bean bag, tote bag, etc.)
prompts = {
    'pkg_1.jpg': 'A realistic mockup of a dark takeaway coffee paper cup on a clean cafe table, high resolution product photography',
    'pkg_2.jpg': 'A realistic mockup of a premium dark coffee bean bag package on a wooden surface, high resolution packaging photography',
    'pkg_3.jpg': 'A realistic mockup of a minimal dark paper tote shopping bag, clean background, high resolution packaging photography',
    'pkg_4.jpg': 'A realistic mockup of a coffee shop napkin and coaster set on a wooden table, high resolution photography'
}

for filename, prompt in prompts.items():
    generate_mockup(prompt, filename)
