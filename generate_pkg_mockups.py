import urllib.request
import urllib.parse
from PIL import Image, ImageChops, ImageFilter, ImageEnhance
import io
import os

def generate_mockup(prompt, filename, logo_position_scale=(0.5, 0.5), logo_size_ratio=0.3):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed=42"
    
    print(f"Generating image for prompt: {prompt}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
            
        base_img = Image.open(io.BytesIO(img_data)).convert('RGB')
        
        # Load logo
        try:
            logo = Image.open('img/logo.jpg').convert('RGB')
            
            # Target width based on ratio
            target_width = int(base_img.width * logo_size_ratio)
            target_height = int(logo.height * (target_width / logo.width))
            
            logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Slightly blur the logo to match photographic depth of field
            logo = logo.filter(ImageFilter.GaussianBlur(0.5))
            
            # Create a white canvas the size of the base image
            canvas = Image.new('RGB', base_img.size, (255, 255, 255))
            
            # Calculate placement
            x = int(base_img.width * logo_position_scale[0] - target_width / 2)
            y = int(base_img.height * logo_position_scale[1] - target_height / 2)
            
            canvas.paste(logo, (x, y))
            
            # Blend using Multiply to make the logo look printed on the surface
            # This makes the white background disappear and the dark parts blend with the texture
            blended = ImageChops.multiply(base_img, canvas)
            
            # Optional: slightly reduce contrast of the final image to make it look cohesive
            # enhancer = ImageEnhance.Contrast(blended)
            # final_img = enhancer.enhance(0.95)
            final_img = blended
            
            final_img.save(f'img/{filename}', quality=90)
            print(f"Successfully saved {filename} with realistic multiply blending")
            
        except Exception as e:
            print("Error pasting logo:", e)
            base_img.save(f'img/{filename}', quality=90)
            
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Prompts for the packaging items. Using lighter materials (kraft, beige) so the dark logo shows up perfectly.
prompts = {
    'pkg_1.jpg': ('A realistic clean blank kraft paper takeaway coffee cup mockup on a wooden cafe table, natural lighting, high resolution product photography, center focus', (0.5, 0.55), 0.2),
    'pkg_2.jpg': ('A realistic clean blank light beige coffee bean bag package on a marble surface, high resolution packaging photography, flat lay', (0.5, 0.5), 0.25),
    'pkg_3.jpg': ('A realistic clean blank white paper tote shopping bag mockup standing, bright cafe background, high resolution packaging photography', (0.5, 0.6), 0.35),
    'pkg_4.jpg': ('A realistic blank light grey square coaster mockup next to a coffee cup on a wooden table, top down view, high resolution photography', (0.5, 0.5), 0.15)
}

for filename, (prompt, pos, size) in prompts.items():
    generate_mockup(prompt, filename, pos, size)
