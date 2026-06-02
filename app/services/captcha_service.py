import random
import string
import html
def generate_captcha_svg(text: str, width: int = 150, height: int = 50) -> str:
    svg_elements = []
    bg_color = f"#{random.randint(230, 255):02x}{random.randint(230, 255):02x}{random.randint(230, 255):02x}"
    svg_elements.append(f'<rect width="100%" height="100%" fill="{bg_color}" />')
    for _ in range(7):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = f"#{random.randint(150, 200):02x}{random.randint(150, 200):02x}{random.randint(150, 200):02x}"
        stroke_width = random.randint(1, 3)
        svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{stroke_width}" />')
    for _ in range(20):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        r = random.randint(1, 4)
        color = f"#{random.randint(100, 200):02x}{random.randint(100, 200):02x}{random.randint(100, 200):02x}"
        svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.5" />')
    char_width = width / (len(text) + 1)
    for i, char in enumerate(text):
        x = int(char_width * (i + 0.8) + random.randint(-2, 2))
        y = int(height / 1.5 + random.randint(-5, 5))
        rotate = random.randint(-25, 25)
        color = f"#{random.randint(20, 80):02x}{random.randint(20, 80):02x}{random.randint(20, 80):02x}"
        font_size = random.randint(24, 30)
        safe_char = html.escape(char)
        svg_elements.append(
            f'<text x="{x}" y="{y}" font-family="monospace, sans-serif" font-weight="bold" font-size="{font_size}" '
            f'fill="{color}" transform="rotate({rotate}, {x}, {y})">{safe_char}</text>'
        )
    svg_content = "".join(svg_elements)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">{svg_content}</svg>'
def generate_captcha_text(length: int = 5) -> str:
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
    return "".join(random.choice(chars) for _ in range(length))
