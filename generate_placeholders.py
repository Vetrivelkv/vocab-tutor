import os
from PIL import Image, ImageDraw, ImageFont

def generate_placeholder(word, output_path):
    img = Image.new('RGB', (800, 600), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    # Just draw text in the middle
    d.text((350, 300), word, fill=(255, 255, 0))
    img.save(output_path)

words = ["am", "abandon", "abandoned", "aberrant", "aberration", "ability", "abjure", "able", "about", "above"]
os.makedirs("assets/images", exist_ok=True)

for word in words:
    generate_placeholder(word, f"assets/images/vocab_{word}.jpg")
