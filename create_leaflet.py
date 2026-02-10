#!/usr/bin/env python3
"""Create a one-page Mental Health Supports leaflet PDF for ED printing."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import urllib.request
import os

# Colors
BLUE_DARK = HexColor('#1a5276')
BLUE_LIGHT = HexColor('#2980b9')
GREEN = HexColor('#27ae60')
RED = HexColor('#c0392b')
GRAY = HexColor('#5d6d7e')
LIGHT_BG = HexColor('#f8f9fa')
GREEN_BG = HexColor('#e8f6e9')
RED_BG = HexColor('#fdeaea')
BLUE_BG = HexColor('#e8f4fd')

# Emoji image cache
EMOJI_CACHE_DIR = "/tmp/emoji_cache"
os.makedirs(EMOJI_CACHE_DIR, exist_ok=True)

def get_emoji_image(emoji_char, size=16):
    """Download emoji image from Twemoji CDN."""
    codepoints = '-'.join(f'{ord(c):x}' for c in emoji_char if ord(c) > 255)
    if not codepoints:
        return None
    
    cache_path = os.path.join(EMOJI_CACHE_DIR, f"{codepoints}.png")
    
    if not os.path.exists(cache_path):
        url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/{codepoints}.png"
        try:
            urllib.request.urlretrieve(url, cache_path)
        except Exception as e:
            print(f"Could not download emoji {emoji_char}: {e}")
            return None
    
    return cache_path

def draw_section_box(c, x, y, width, height, fill_color, border_color=None):
    """Draw a simple section box with optional left border."""
    c.saveState()
    c.setFillColor(fill_color)
    c.roundRect(x, y, width, height, 5, fill=1, stroke=0)
    
    if border_color:
        c.setStrokeColor(border_color)
        c.setLineWidth(4)
        c.line(x + 2, y + 5, x + 2, y + height - 5)
    
    c.restoreState()

def draw_badge(c, x, y, text, bg_color, text_color=HexColor('#ffffff')):
    """Draw a small badge."""
    text_width = c.stringWidth(text, "Helvetica-Bold", 7) + 8
    c.setFillColor(bg_color)
    c.roundRect(x, y, text_width, 12, 4, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 4, y + 3, text)
    return text_width + 5

def create_leaflet():
    output_path = "/root/clawd/projects/contactesQR/mental-health-supports-leaflet.pdf"
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    margin = 15 * mm
    content_width = width - 2 * margin
    y = height - margin
    
    # === HEADER ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 20)
    emoji_path = get_emoji_image("🏥", 22)
    if emoji_path:
        c.drawImage(emoji_path, margin, y - 12, width=22, height=22, mask='auto')
    c.drawString(margin + 28, y - 8, "Mental Health Supports")
    y -= 22
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "University Hospital Limerick – Liaison Psychiatry Team")
    y -= 15
    
    # Header divider
    c.setStrokeColor(BLUE_DARK)
    c.setLineWidth(2)
    c.line(margin, y, width - margin, y)
    y -= 20
    
    # ============================================
    # === SECTION 1: SOLACE CAFÉ ===
    # ============================================
    section_height = 115
    draw_section_box(c, margin, y - section_height, content_width, section_height, GREEN_BG, GREEN)
    
    tx = margin + 15
    ty = y - 22
    
    # Title row
    emoji_path = get_emoji_image("☕", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 3, width=16, height=16, mask='auto')
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(tx + 20, ty, "Solace Café")
    
    # Badges
    badge_x = tx + 95
    badge_x += draw_badge(c, badge_x, ty - 2, "FREE", GREEN)
    badge_x += draw_badge(c, badge_x, ty - 2, "Thu–Sun 6pm–12am", HexColor('#5dade2'), HexColor('#1a5276'))
    
    # Description - MUST match website exactly
    ty -= 18
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "Confidential, non-clinical mental health support for adults experiencing emotional distress,")
    ty -= 10
    c.drawString(tx, ty, "anxiety, or feeling overwhelmed. Book a 1-hour session with trained support workers and")
    ty -= 10
    c.drawString(tx, ty, "peer connectors. Access coping strategies, one-to-one support, and sign-posting to local services.")
    
    # Divider inside box
    ty -= 10
    c.setStrokeColor(HexColor('#b8e0b8'))
    c.setLineWidth(0.5)
    c.line(tx, ty, tx + content_width - 30, ty)
    ty -= 12
    
    # Location
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 8)
    emoji_path = get_emoji_image("📍", 10)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 2, width=10, height=10, mask='auto')
    c.drawString(tx + 13, ty, "Limerick Mental Health Assoc., Sarsfield Bridge (Former Pier One Hotel)")
    
    # Contact info
    ty -= 14
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 9)
    emoji_path = get_emoji_image("📞", 10)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 2, width=10, height=10, mask='auto')
    c.drawString(tx + 13, ty, "061 446 786")
    
    emoji_path = get_emoji_image("💬", 10)
    if emoji_path:
        c.drawImage(emoji_path, tx + 85, ty - 2, width=10, height=10, mask='auto')
    c.drawString(tx + 98, ty, "085 261 2025")
    
    emoji_path = get_emoji_image("📧", 10)
    if emoji_path:
        c.drawImage(emoji_path, tx + 180, ty - 2, width=10, height=10, mask='auto')
    c.drawString(tx + 193, ty, "solace@limerickmentalhealth.ie")
    
    y -= section_height + 12
    
    # ============================================
    # === SECTION 2: TEXT ABOUT IT ===
    # ============================================
    section_height = 75
    draw_section_box(c, margin, y - section_height, content_width, section_height, BLUE_BG, BLUE_LIGHT)
    
    tx = margin + 15
    ty = y - 22
    
    # Title row
    emoji_path = get_emoji_image("💬", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 3, width=16, height=16, mask='auto')
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(tx + 20, ty, "Text About It")
    
    # Badges
    badge_x = tx + 105
    badge_x += draw_badge(c, badge_x, ty - 2, "FREE", GREEN)
    badge_x += draw_badge(c, badge_x, ty - 2, "24/7", GREEN)
    
    # Description - MUST match website exactly
    ty -= 18
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica", 9)
    c.drawString(tx, ty, "24/7 anonymous text-based support service. Text the word HELLO to start.")
    
    # Contact
    ty -= 16
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(BLUE_DARK)
    c.drawString(tx, ty, "Text 50808")
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(tx + 70, ty, "or WhatsApp")
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(tx + 135, ty, "086 180 4253")
    
    ty -= 12
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(tx, ty, "48/An Post/Clear Mobile users: WhatsApp or text 086 180 0280 (standard rates)")
    
    y -= section_height + 35
    
    # ============================================
    # === SECTION 3: CRISIS HELPLINES ===
    # ============================================
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    emoji_path = get_emoji_image("📞", 14)
    if emoji_path:
        c.drawImage(emoji_path, margin, y - 3, width=14, height=14, mask='auto')
    c.drawString(margin + 18, y, "Crisis Helplines")
    
    # Badges next to title
    badge_x = margin + 120
    draw_badge(c, badge_x, y - 3, "FREE", GREEN)
    draw_badge(c, badge_x + 40, y - 3, "24/7", GREEN)
    
    y -= 20
    
    # Two boxes side by side
    col_width = (content_width - 10) / 2
    box_height = 65
    
    # --- Samaritans ---
    draw_section_box(c, margin, y - box_height, col_width, box_height, LIGHT_BG)
    
    tx = margin + 15
    ty = y - 20
    
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(tx, ty, "Samaritans")
    
    # Phone number - simple text, not a button
    ty -= 22
    c.setFillColor(BLUE_LIGHT)
    c.setFont("Helvetica-Bold", 18)
    emoji_path = get_emoji_image("📞", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx + 20, ty - 3, width=16, height=16, mask='auto')
    c.drawString(tx + 40, ty, "116 123")
    
    ty -= 14
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "Listening support, any time")
    
    # --- Pieta House ---
    draw_section_box(c, margin + col_width + 10, y - box_height, col_width, box_height, LIGHT_BG)
    
    tx = margin + col_width + 25
    ty = y - 20
    
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(tx, ty, "Pieta House")
    
    # Phone number
    ty -= 22
    c.setFillColor(BLUE_LIGHT)
    c.setFont("Helvetica-Bold", 18)
    emoji_path = get_emoji_image("📞", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx + 5, ty - 3, width=16, height=16, mask='auto')
    c.drawString(tx + 25, ty, "1800 247 247")
    
    ty -= 14
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "Suicide & self-harm crisis support")
    
    y -= box_height + 8
    
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, y, "These are Irish freephone numbers – free from any phone.")
    y -= 18
    
    # ============================================
    # === SECTION 4: EMERGENCY ===
    # ============================================
    section_height = 90
    draw_section_box(c, margin, y - section_height, content_width, section_height, RED_BG, RED)
    
    tx = margin + 15
    ty = y - 22
    
    # Title row
    emoji_path = get_emoji_image("🚨", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 3, width=16, height=16, mask='auto')
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(tx + 20, ty, "Emergency")
    
    # 24/7 badge
    draw_badge(c, tx + 100, ty - 2, "24/7", RED)
    
    # Description - MUST match website exactly
    ty -= 18
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "For mental health crisis assessment. If you or someone is at immediate risk of harm or needs")
    ty -= 10
    c.drawString(tx, ty, "urgent medical treatment, always call emergency services.")
    
    # Divider inside box
    ty -= 10
    c.setStrokeColor(HexColor('#e0b8b8'))
    c.setLineWidth(0.5)
    c.line(tx, ty, tx + content_width - 30, ty)
    ty -= 16
    
    # Emergency numbers - simple layout, no overlapping buttons
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 18)
    emoji_path = get_emoji_image("📞", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx + 40, ty - 3, width=16, height=16, mask='auto')
    c.drawString(tx + 60, ty, "999")
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 12)
    c.drawString(tx + 110, ty, "or")
    
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 18)
    emoji_path = get_emoji_image("📞", 16)
    if emoji_path:
        c.drawImage(emoji_path, tx + 140, ty - 3, width=16, height=16, mask='auto')
    c.drawString(tx + 160, ty, "112")
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(tx + 220, ty, "(Emergency Services)")
    
    y -= section_height + 18
    
    # ============================================
    # === FOOTER: QR CODE ===
    # ============================================
    c.setStrokeColor(HexColor('#e0e0e0'))
    c.setLineWidth(0.5)
    c.line(margin, y, width - margin, y)
    y -= 12
    
    # QR code - points to GitHub Pages
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=https://victoriadigital.github.io/contactesQR/"
    qr_path = "/tmp/leaflet_qr.png"
    try:
        urllib.request.urlretrieve(qr_url, qr_path)
        c.drawImage(qr_path, margin + 5, y - 65, width=60, height=60)
    except:
        pass
    
    # QR label
    tx = margin + 75
    ty = y - 20
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 10)
    emoji_path = get_emoji_image("📱", 12)
    if emoji_path:
        c.drawImage(emoji_path, tx, ty - 2, width=12, height=12, mask='auto')
    c.drawString(tx + 15, ty, "Scan for digital version")
    
    ty -= 14
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "victoriadigital.github.io/contactesQR")
    
    ty -= 20
    c.setFillColor(HexColor('#95a5a6'))
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "Keep this leaflet. These services are confidential and here to help.")
    
    # Hospital footer
    c.setFillColor(HexColor('#95a5a6'))
    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, margin, "Liaison Psychiatry Team – University Hospital Limerick")
    
    c.save()
    print(f"✅ Created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_leaflet()
