from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os
import hashlib
import random


def _hex(h):
    return HexColor(h)


def generate_certificate_pdf(user_name: str, skill_name: str, date_str: str, output_path: str):
    """
    Generate a landscape certificate matching the provided IBM-style certificate layout.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Landscape A4 provides a better aspect ratio for this design
    W, H = landscape(A4)
    c = canvas.Canvas(output_path, pagesize=(W, H))

    # ══════════════════════════════════════════════════════════════════════════
    # LAYER 1 — BACKGROUND
    # White base with a prominent light grey center block
    # ══════════════════════════════════════════════════════════════════════════
    c.setFillColor(_hex("#FFFFFF"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Inner light grey box like the reference image
    bg_margin_top = 3.8 * cm
    bg_margin_bottom = 2.8 * cm
    c.setFillColor(_hex("#F3F3F3"))
    c.rect(0, bg_margin_bottom, W, H - bg_margin_top - bg_margin_bottom, fill=1, stroke=0)

    # ══════════════════════════════════════════════════════════════════════════
    # DECORATIVE BACKGROUND NETWORK (Subtle background tracks)
    # ══════════════════════════════════════════════════════════════════════════
    c.setLineWidth(25)
    c.setStrokeColor(HexColor("#EBEBEB"))
    c.setLineCap(1) # Round line caps
    c.setLineJoin(1)
    
    # Left bracket shape
    c.line(W/2 - 10*cm, H/2 - 3.5*cm, W/2 - 10*cm, H/2 + 4.5*cm)
    c.line(W/2 - 10*cm, H/2 - 3.5*cm, W/2 - 3*cm, H/2 - 3.5*cm)
    c.line(W/2 - 10*cm, H/2 + 4.5*cm, W/2 - 3*cm, H/2 + 4.5*cm)
    
    # Right bracket shape
    c.line(W/2 + 10*cm, H/2 - 3.5*cm, W/2 + 10*cm, H/2 + 4.5*cm)
    c.line(W/2 + 10*cm, H/2 - 3.5*cm, W/2 + 3*cm, H/2 - 3.5*cm)
    c.line(W/2 + 10*cm, H/2 + 4.5*cm, W/2 + 3*cm, H/2 + 4.5*cm)

    # ══════════════════════════════════════════════════════════════════════════
    # LOGOS OR TOP DECORATIONS
    # ══════════════════════════════════════════════════════════════════════════
    # Website logo
    # Resolve absolute path to the frontend/static/logo.png
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)
    logo_path = os.path.join(project_root, 'frontend', 'static', 'logo.png')
    
    if os.path.exists(logo_path):
        # Position logo towards the top left
        c.drawImage(logo_path, 1.5 * cm, H - 4.5 * cm, width=6*cm, height=3.5*cm, preserveAspectRatio=True, mask='auto')

    # Premium thick borders covering all four sides
    margin = 1.0 * cm
    
    # Very thick outer solid dark blue border
    c.setStrokeColor(_hex("#0D47A1"))
    c.setLineWidth(14.0)
    c.rect(margin, margin, W - 2*margin, H - 2*margin, fill=0, stroke=1)
    
    # Medium inner gold/grey accent line
    inner_m1 = margin + 0.35 * cm
    c.setStrokeColor(_hex("#A5A5A5"))
    c.setLineWidth(2.5)
    c.rect(inner_m1, inner_m1, W - 2*inner_m1, H - 2*inner_m1, fill=0, stroke=1)

    # Fine innermost blue line
    inner_m2 = margin + 0.50 * cm
    c.setStrokeColor(_hex("#0D47A1"))
    c.setLineWidth(1.0)
    c.rect(inner_m2, inner_m2, W - 2*inner_m2, H - 2*inner_m2, fill=0, stroke=1)

    # ══════════════════════════════════════════════════════════════════════════
    # TEXT CONTENT - Matching layout and fonts from the reference
    # ══════════════════════════════════════════════════════════════════════════
    light_text = _hex("#444444")
    dark_text  = _hex("#111111")
    blue_text  = _hex("#0D47A1") # Rich elegant blue requested by user

    # Name is not modified by Python string methods to keep exact capitalizations 
    # if provided, but let's standardise the case
    user_name = user_name.title()
    skill_name = skill_name.title()

    # 1. "This is to certify that"
    c.setFillColor(light_text)
    c.setFont("Times-Roman", 16)
    c.drawCentredString(W/2, H - 5.5*cm, "This is to certify that")

    # 2. Recipient Name
    c.setFont("Times-Bold", 35)
    c.setFillColor(blue_text)
    c.drawCentredString(W/2, H - 7.5*cm, user_name)

    # 3. "successfully completed and received a passing grade in"
    c.setFillColor(light_text)
    c.setFont("Times-Roman", 13)
    c.drawCentredString(W/2, H - 8.8*cm, "successfully completed and received a passing grade in")

    # 4. Course / Skill Name
    c.setFont("Times-Bold", 30)
    c.setFillColor(blue_text)
    c.drawCentredString(W/2, H - 10.4*cm, skill_name)

    # 5. Course Subtitle
    c.setFillColor(light_text)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W/2, H - 11.2*cm, "(SSEP, provided by Smart Skill-Exchange)")

    # 6. Additional Info
    c.setFillColor(light_text)
    c.setFont("Times-Roman", 12)
    c.drawCentredString(W/2, H - 12.3*cm, "A course on smartskill.exchange")
    c.drawCentredString(W/2, H - 12.8*cm, "Powered by Smart Skill-Exchange Network.")

    # 7. Issued By
    cert_y = H - 14.5 * cm
    c.setFont("Times-Roman", 13)
    c.drawCentredString(W/2, cert_y, "Issued by")
    c.setFont("Times-Bold", 13)
    c.setFillColor(dark_text)
    c.drawCentredString(W/2, cert_y - 0.6 * cm, "Smart Skill-Exchange Education Program")

    # 8. Date & Issue details
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(dark_text)
    c.drawCentredString(W/2, cert_y - 1.8 * cm, date_str)

    c.save()
