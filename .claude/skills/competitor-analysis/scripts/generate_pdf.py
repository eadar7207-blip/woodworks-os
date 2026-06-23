#!/usr/bin/env python3
"""
Competitor Analysis PDF Generator
Usage: python3 generate_pdf.py --data data.json --logo logo.png --primary-color "#1A2B3C" --output report.pdf
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black, Color
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        HRFlowable, KeepTogether, Image as RLImage
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.platypus.flowables import Flowable
    from reportlab.pdfgen import canvas as rl_canvas
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab pillow")
    sys.exit(1)


def hex_to_color(hex_str):
    hex_str = hex_str.strip().lstrip("#")
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return Color(r, g, b)


def lighten(hex_str, factor=0.4):
    hex_str = hex_str.strip().lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"


class ColorBlock(Flowable):
    """Full-width colored rectangle for section headers."""
    def __init__(self, width, height, color, label="", label_color=white):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.label = label
        self.label_color = label_color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        if self.label:
            self.canv.setFillColor(self.label_color)
            self.canv.setFont("Helvetica-Bold", 11)
            self.canv.drawString(12, self.height / 2 - 5, self.label.upper())


def build_styles(primary_color, accent_color):
    base = getSampleStyleSheet()
    primary = hex_to_color(primary_color)
    accent = hex_to_color(accent_color)
    light_primary = hex_to_color(lighten(primary_color, 0.88))

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=white,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="Helvetica",
            fontSize=14,
            leading=18,
            textColor=white,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "cover_date": ParagraphStyle(
            "cover_date",
            fontName="Helvetica",
            fontSize=11,
            textColor=white,
            alignment=TA_LEFT,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=primary,
            spaceBefore=20,
            spaceAfter=10,
        ),
        "competitor_name": ParagraphStyle(
            "competitor_name",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=primary,
            spaceBefore=14,
            spaceAfter=4,
        ),
        "label": ParagraphStyle(
            "label",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=accent,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=black,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=black,
            leftIndent=14,
            spaceAfter=2,
            bulletIndent=4,
        ),
        "small_muted": ParagraphStyle(
            "small_muted",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=HexColor("#888888"),
            spaceAfter=2,
        ),
    }
    return styles, primary, accent, light_primary


def cover_page(c, width, height, data, primary_color, accent_color, logo_path):
    primary = hex_to_color(primary_color)
    accent = hex_to_color(accent_color)

    # Full-page primary color background
    c.setFillColor(primary)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Accent stripe on the right
    stripe_w = 0.35 * inch
    c.setFillColor(accent)
    c.rect(width - stripe_w, 0, stripe_w, height, fill=1, stroke=0)

    # Logo top-left
    if logo_path and os.path.isfile(logo_path):
        try:
            logo_max_w = 2.2 * inch
            logo_max_h = 0.9 * inch
            from PIL import Image as PILImage
            img = PILImage.open(logo_path)
            orig_w, orig_h = img.size
            ratio = min(logo_max_w / orig_w, logo_max_h / orig_h)
            logo_w = orig_w * ratio
            logo_h = orig_h * ratio
            c.drawImage(
                logo_path,
                0.55 * inch,
                height - 1.2 * inch - logo_h,
                width=logo_w,
                height=logo_h,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass  # Skip logo if PIL unavailable or image broken

    # Report title
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(white)
    c.drawString(0.55 * inch, height * 0.52, "Competitor Intelligence")
    c.drawString(0.55 * inch, height * 0.52 - 38, "Report")

    # Business name
    c.setFont("Helvetica", 15)
    c.setFillColor(white)
    c.drawString(0.55 * inch, height * 0.52 - 75, data.get("business_name", ""))

    # Industry + date
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor("#CCCCCC"))
    industry = data.get("industry", "")
    date_str = data.get("generated_date", datetime.today().strftime("%Y-%m-%d"))
    c.drawString(0.55 * inch, 1.1 * inch, f"{industry}  |  {date_str}")

    # Bottom tagline
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(0.55 * inch, 0.65 * inch, "Prepared by AI Competitor Analysis Workflow")

    c.showPage()


def header_footer(canvas_obj, doc, data, primary_color, logo_path, primary):
    width, height = letter
    canvas_obj.saveState()

    # Top bar
    canvas_obj.setFillColor(primary)
    canvas_obj.rect(0, height - 0.45 * inch, width, 0.45 * inch, fill=1, stroke=0)

    # Business name in header
    canvas_obj.setFont("Helvetica-Bold", 9)
    canvas_obj.setFillColor(white)
    canvas_obj.drawString(0.5 * inch, height - 0.3 * inch, data.get("business_name", ""))

    # Report title in header right
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(HexColor("#CCCCCC"))
    canvas_obj.drawRightString(width - 0.5 * inch, height - 0.3 * inch, "Competitor Intelligence Report")

    # Footer line
    canvas_obj.setStrokeColor(HexColor("#DDDDDD"))
    canvas_obj.line(0.5 * inch, 0.45 * inch, width - 0.5 * inch, 0.45 * inch)

    # Page number
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(HexColor("#999999"))
    canvas_obj.drawCentredString(width / 2, 0.28 * inch, f"Page {doc.page}")

    canvas_obj.restoreState()


def build_story(data, styles, primary, accent, light_primary, page_width):
    story = []
    body_width = page_width - 1.1 * inch  # account for margins

    def rule():
        return HRFlowable(width="100%", thickness=0.5, color=HexColor("#E0E0E0"), spaceAfter=8, spaceBefore=4)

    def section_header(title):
        return [
            Spacer(1, 0.15 * inch),
            Paragraph(title, styles["section_heading"]),
            rule(),
        ]

    def bullet_item(text):
        return Paragraph(f"<bullet>•</bullet> {text}", styles["bullet"])

    # --- Executive Summary ---
    story += section_header("Executive Summary")
    for item in data.get("executive_summary", []):
        story.append(bullet_item(item))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # --- Competitor Profiles ---
    story += section_header("Competitor Profiles")
    story.append(Paragraph(
        f"Analysis of {len(data.get('competitors', []))} competitors in the {data.get('industry', '')} space.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.1 * inch))

    for comp in data.get("competitors", []):
        block = []
        block.append(Paragraph(comp.get("name", ""), styles["competitor_name"]))

        website = comp.get("website", "")
        if website:
            block.append(Paragraph(website, styles["small_muted"]))

        block.append(Paragraph(comp.get("what_they_do", ""), styles["body"]))

        if comp.get("pricing"):
            block.append(Paragraph("Pricing", styles["label"]))
            block.append(Paragraph(comp["pricing"], styles["body"]))

        if comp.get("target_market"):
            block.append(Paragraph("Target Market", styles["label"]))
            block.append(Paragraph(comp["target_market"], styles["body"]))

        strengths = comp.get("strengths", [])
        if strengths:
            block.append(Paragraph("Strengths", styles["label"]))
            for s in strengths:
                block.append(bullet_item(s))

        weaknesses = comp.get("weaknesses", [])
        if weaknesses:
            block.append(Paragraph("Weaknesses / Gaps", styles["label"]))
            for w in weaknesses:
                block.append(bullet_item(w))

        block.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#EEEEEE"), spaceAfter=6, spaceBefore=10))
        story.append(KeepTogether(block))

    story.append(PageBreak())

    # --- Gap Analysis ---
    story += section_header("Competitive Gap Analysis")

    gap = data.get("gap_analysis", {})

    if gap.get("where_you_win"):
        story.append(Paragraph("Where You Win", styles["label"]))
        for item in gap["where_you_win"]:
            story.append(bullet_item(item))
        story.append(Spacer(1, 6))

    if gap.get("underserved_needs"):
        story.append(Paragraph("Underserved Market Needs", styles["label"]))
        for item in gap["underserved_needs"]:
            story.append(bullet_item(item))
        story.append(Spacer(1, 6))

    if gap.get("market_trends"):
        story.append(Paragraph("Emerging Trends", styles["label"]))
        for item in gap["market_trends"]:
            story.append(bullet_item(item))

    story.append(Spacer(1, 0.2 * inch))

    # --- Recommended Actions ---
    story += section_header("Recommended Actions")
    for i, action in enumerate(data.get("recommended_actions", []), 1):
        story.append(Paragraph(f"{i}.  {action}", styles["body"]))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # --- Sources ---
    story += section_header("Sources")
    for url in data.get("sources", []):
        story.append(Paragraph(url, styles["small_muted"]))
        story.append(Spacer(1, 2))

    return story


def main():
    parser = argparse.ArgumentParser(description="Generate branded competitor analysis PDF")
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    parser.add_argument("--logo", default=None, help="Path to logo PNG")
    parser.add_argument("--primary-color", default="#1A2B3C", help="Primary brand hex color")
    parser.add_argument("--accent-color", default=None, help="Accent brand hex color (optional)")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    args = parser.parse_args()

    # Load data
    with open(args.data, "r") as f:
        data = json.load(f)

    primary_color = args.primary_color.strip()
    accent_color = args.accent_color.strip() if args.accent_color else lighten(primary_color, 0.35)

    output_path = os.path.expanduser(args.output)
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    width, height = letter
    styles, primary, accent, light_primary = build_styles(primary_color, accent_color)

    # Draw cover page manually first, then build the body doc
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

    # We'll use a two-pass approach: cover canvas + platypus body merged via pypdf
    import tempfile

    cover_path = tempfile.mktemp(suffix="_cover.pdf")
    body_path = tempfile.mktemp(suffix="_body.pdf")

    # Cover
    c = pdf_canvas.Canvas(cover_path, pagesize=letter)
    cover_page(c, width, height, data, primary_color, accent_color, args.logo)
    c.save()

    # Body
    logo_path = args.logo

    def on_page(canvas_obj, doc):
        header_footer(canvas_obj, doc, data, primary_color, logo_path, primary)

    doc = SimpleDocTemplate(
        body_path,
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    story = build_story(data, styles, primary, accent, light_primary, width)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

    # Merge cover + body
    try:
        from pypdf import PdfReader, PdfWriter
        writer = PdfWriter()
        for path in [cover_path, body_path]:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_path, "wb") as out:
            writer.write(out)
    except ImportError:
        # Fallback: just use body (no cover merge)
        import shutil
        shutil.copy(body_path, output_path)
        print("Note: pypdf not installed — cover page omitted. Run: pip install pypdf")

    # Cleanup temps
    for p in [cover_path, body_path]:
        try:
            os.remove(p)
        except OSError:
            pass

    print(f"PDF saved to: {output_path}")


if __name__ == "__main__":
    main()
