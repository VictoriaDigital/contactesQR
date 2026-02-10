#!/usr/bin/env python3
"""Create a one-page Mental Health Supports leaflet PDF for ED printing."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import urllib.request
import os

# Colors
BLUE_DARK = HexColor('#1a5276')
BLUE_LIGHT = HexColor('#2980b9')
GREEN = HexColor('#27ae60')
RED = HexColor('#e74c3c')
GRAY = HexColor('#5d6d7e')
LIGHT_BG = HexColor('#f8f9fa')
GREEN_BG = HexColor('#f0fdf4')
RED_BG = HexColor('#fef2f2')

def draw_rounded_rect(c, x, y, width, height, radius, fill_color=None, stroke_color=None, left_border_color=None, left_border_width=3):
    """Draw a rounded rectangle with optional left border accent."""
    c.saveState()
    
    if fill_color:
        c.setFillColor(fill_color)
        c.roundRect(x, y, width, height, radius, fill=1, stroke=0)
    
    if left_border_color:
        c.setStrokeColor(left_border_color)
        c.setLineWidth(left_border_width)
        c.line(x + 2, y + radius, x + 2, y + height - radius)
    
    c.restoreState()

def create_leaflet():
    output_path = "/root/clawd/projects/contactesQR/mental-health-supports-leaflet.pdf"
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    margin = 15 * mm
    content_width = width - 2 * margin
    y = height - margin
    
    # === HEADER ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, y - 10, "🏥 Mental Health Supports")
    y -= 25
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y - 5, "University Hospital Limerick – Liaison Psychiatry Team")
    y -= 20
    
    # Divider line
    c.setStrokeColor(BLUE_DARK)
    c.setLineWidth(2)
    c.line(margin, y, width - margin, y)
    y -= 15
    
    # === SOLACE CAFÉ ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "☕ Community Support (Limerick)")
    y -= 18
    
    box_height = 85
    draw_rounded_rect(c, margin, y - box_height, content_width, box_height, 4, fill_color=GREEN_BG, left_border_color=GREEN, left_border_width=4)
    
    # Content inside box
    tx = margin + 10
    ty = y - 12
    
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(tx, ty, "Solace Café")
    
    # Free badge
    c.setFillColor(GREEN)
    c.roundRect(tx + 70, ty - 3, 30, 14, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(tx + 75, ty, "FREE")
    
    # Hours badge
    c.setFillColor(HexColor('#e8f4fd'))
    c.roundRect(tx + 110, ty - 3, 130, 14, 5, fill=1, stroke=0)
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(tx + 115, ty, "🕕 Thu–Sun, 6pm – Midnight")
    
    ty -= 15
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "Confidential, non-clinical mental health support for adults experiencing emotional distress.")
    ty -= 10
    c.drawString(tx, ty, "Book a 1-hour session with trained support workers and peer connectors.")
    
    ty -= 12
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(tx, ty, "📍 Limerick Mental Health Association, Sarsfield Bridge (Former Pier One Hotel)")
    
    ty -= 15
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(tx, ty, "📞 061 446 786    💬 Text/WhatsApp: 085 261 2025    ✉️ solace@limerickmentalhealth.ie")
    
    y -= box_height + 12
    
    # === TEXT ABOUT IT ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "💬 Text Support")
    y -= 18
    
    box_height = 55
    draw_rounded_rect(c, margin, y - box_height, content_width, box_height, 4, fill_color=LIGHT_BG, left_border_color=BLUE_LIGHT, left_border_width=4)
    
    tx = margin + 10
    ty = y - 12
    
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(tx, ty, "Text About It")
    
    # Free badge
    c.setFillColor(GREEN)
    c.roundRect(tx + 80, ty - 3, 30, 14, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(tx + 85, ty, "FREE")
    
    # 24/7 badge
    c.setFillColor(GREEN)
    c.roundRect(tx + 115, ty - 3, 30, 14, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(tx + 121, ty, "24/7")
    
    ty -= 15
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(tx, ty, "24/7 anonymous text-based support. Text the word HELLO to start.")
    
    ty -= 15
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(tx, ty, "💬 Text 50808    •    WhatsApp: 086 180 4253")
    
    ty -= 10
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(tx, ty, "48, An Post & Clear Mobile users: Use WhatsApp or text 086 180 0280 (standard SMS rates)")
    
    y -= box_height + 12
    
    # === CRISIS HELPLINES ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "📞 Crisis Helplines")
    y -= 18
    
    # Two column layout for helplines
    col_width = (content_width - 10) / 2
    
    # Samaritans
    box_height = 50
    draw_rounded_rect(c, margin, y - box_height, col_width, box_height, 4, fill_color=LIGHT_BG)
    
    tx = margin + 10
    ty = y - 14
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(tx, ty, "Samaritans")
    
    # Badges
    c.setFillColor(GREEN)
    c.roundRect(tx + 70, ty - 3, 30, 12, 4, fill=1, stroke=0)
    c.roundRect(tx + 103, ty - 3, 28, 12, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(tx + 76, ty - 1, "FREE")
    c.drawString(tx + 109, ty - 1, "24/7")
    
    ty -= 25
    c.setFillColor(HexColor('#3498db'))
    c.roundRect(tx, ty - 5, col_width - 20, 22, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(tx + (col_width - 20) / 2, ty + 2, "📞 116 123")
    
    # Pieta House
    draw_rounded_rect(c, margin + col_width + 10, y - box_height, col_width, box_height, 4, fill_color=LIGHT_BG)
    
    tx = margin + col_width + 20
    ty = y - 14
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(tx, ty, "Pieta House")
    
    # Badges
    c.setFillColor(GREEN)
    c.roundRect(tx + 70, ty - 3, 30, 12, 4, fill=1, stroke=0)
    c.roundRect(tx + 103, ty - 3, 28, 12, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(tx + 76, ty - 1, "FREE")
    c.drawString(tx + 109, ty - 1, "24/7")
    
    ty -= 25
    c.setFillColor(HexColor('#3498db'))
    c.roundRect(tx, ty - 5, col_width - 20, 22, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(tx + (col_width - 20) / 2, ty + 2, "📞 1800 247 247")
    
    y -= box_height + 5
    
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, y, "These are Irish freephone numbers. Calls are free from any phone.")
    y -= 18
    
    # === EMERGENCY ===
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "🚨 Emergency")
    y -= 18
    
    box_height = 60
    draw_rounded_rect(c, margin, y - box_height, content_width, box_height, 4, fill_color=RED_BG, left_border_color=RED, left_border_width=4)
    
    tx = margin + 10
    ty = y - 14
    
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(tx, ty, "Emergency Department")
    
    # 24/7 badge
    c.setFillColor(RED)
    c.roundRect(tx + 130, ty - 3, 70, 14, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(tx + 138, ty, "Available 24/7")
    
    ty -= 15
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(tx, ty, "For mental health crisis assessment. If you or someone is at immediate risk of harm")
    ty -= 11
    c.drawString(tx, ty, "or needs urgent medical treatment, call emergency services.")
    
    ty -= 18
    # Emergency buttons
    c.setFillColor(RED)
    c.roundRect(tx + 50, ty - 5, 80, 25, 5, fill=1, stroke=0)
    c.roundRect(tx + 150, ty - 5, 80, 25, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(tx + 90, ty + 3, "📞 999")
    c.drawCentredString(tx + 190, ty + 3, "📞 112")
    
    y -= box_height + 15
    
    # === QR CODE & FOOTER ===
    # Divider
    c.setStrokeColor(HexColor('#e0e0e0'))
    c.setLineWidth(0.5)
    c.line(margin, y, width - margin, y)
    y -= 15
    
    # Download QR code
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=https://victoriadigital.github.io/contactesQR/"
    qr_path = "/tmp/leaflet_qr.png"
    try:
        urllib.request.urlretrieve(qr_url, qr_path)
        c.drawImage(qr_path, margin + 5, y - 75, width=70, height=70)
    except:
        pass
    
    # QR label and footer text
    tx = margin + 85
    ty = y - 20
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(tx, ty, "Scan for digital version")
    ty -= 12
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(tx, ty, "victoriadigital.github.io/contactesQR")
    
    ty -= 25
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
