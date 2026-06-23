#!/usr/bin/env python3
"""Generate a professional competitor analysis PDF report."""

import argparse
import json
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, Image, KeepTogether,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
)


def hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def make_color(hex_str: str):
    r, g, b = hex_to_rgb(hex_str)
    return colors.Color(r, g, b)


class NumberedCanvas:
    pass


def build_styles(primary_hex: str, accent_hex: str):
    primary = make_color(primary_hex)
    accent = make_color(accent_hex)
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"],
            textColor=primary, fontSize=26, spaceAfter=6, spaceBefore=0,
            fontName="Helvetica-Bold", alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"],
            textColor=accent, fontSize=13, spaceAfter=4,
            fontName="Helvetica", alignment=TA_LEFT,
        ),
        "section": ParagraphStyle(
            "SectionHead", parent=base["Heading1"],
            textColor=primary, fontSize=15, spaceBefore=18, spaceAfter=6,
            fontName="Helvetica-Bold", borderPad=0,
        ),
        "subsection": ParagraphStyle(
            "SubsectionHead", parent=base["Heading2"],
            textColor=accent, fontSize=12, spaceBefore=10, spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"],
            fontSize=10, leading=15, spaceAfter=6,
            fontName="Helvetica", alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"],
            fontSize=10, leading=14, spaceAfter=3, leftIndent=14,
            fontName="Helvetica", bulletIndent=4,
        ),
        "label": ParagraphStyle(
            "Label", parent=base["Normal"],
            fontSize=9, leading=12, textColor=colors.grey,
            fontName="Helvetica-Bold",
        ),
        "caption": ParagraphStyle(
            "Caption", parent=base["Normal"],
            fontSize=8, leading=11, textColor=colors.grey,
            fontName="Helvetica", alignment=TA_CENTER,
        ),
        "tag_high": ParagraphStyle(
            "TagHigh", parent=base["Normal"],
            fontSize=9, fontName="Helvetica-Bold",
            textColor=colors.white, backColor=colors.Color(0.8, 0.2, 0.2),
        ),
        "tag_medium": ParagraphStyle(
            "TagMedium", parent=base["Normal"],
            fontSize=9, fontName="Helvetica-Bold",
            textColor=colors.white, backColor=colors.Color(0.85, 0.55, 0.1),
        ),
        "tag_low": ParagraphStyle(
            "TagLow", parent=base["Normal"],
            fontSize=9, fontName="Helvetica-Bold",
            textColor=colors.white, backColor=colors.Color(0.25, 0.6, 0.3),
        ),
    }
    return styles, primary, accent


def priority_style(priority: str, styles):
    mapping = {"high": styles["tag_high"], "medium": styles["tag_medium"], "low": styles["tag_low"]}
    return mapping.get(priority.lower(), styles["body"])


def build_competitor_block(comp, styles, accent, primary):
    elements = []

    # Competitor header
    elements.append(Paragraph(comp["name"], styles["subsection"]))
    if comp.get("website"):
        elements.append(Paragraph(comp["website"], styles["label"]))
    elements.append(Spacer(1, 4))

    # Description
    elements.append(Paragraph(comp.get("description", ""), styles["body"]))
    elements.append(Spacer(1, 4))

    # Meta table: pricing + target market
    meta_data = [
        [Paragraph("<b>Pricing</b>", styles["label"]), Paragraph(comp.get("pricing", "N/A"), styles["body"])],
        [Paragraph("<b>Target Market</b>", styles["label"]), Paragraph(comp.get("target_market", "N/A"), styles["body"])],
    ]
    meta_table = Table(meta_data, colWidths=[1.2 * inch, 5.3 * inch])
    meta_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 6))

    # Strengths / Weaknesses / Notable Features table
    def make_bullets(items):
        return "\n".join(f"• {item}" for item in items)

    sw_data = [
        [
            Paragraph("<b>Strengths</b>", styles["label"]),
            Paragraph("<b>Weaknesses</b>", styles["label"]),
        ],
        [
            Paragraph(make_bullets(comp.get("strengths", [])), styles["bullet"]),
            Paragraph(make_bullets(comp.get("weaknesses", [])), styles["bullet"]),
        ],
    ]
    sw_table = Table(sw_data, colWidths=[3.25 * inch, 3.25 * inch])
    sw_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.Color(0.93, 0.97, 0.93)),
        ("BACKGROUND", (1, 0), (1, 0), colors.Color(0.98, 0.93, 0.93)),
        ("BACKGROUND", (0, 1), (0, 1), colors.Color(0.97, 1, 0.97)),
        ("BACKGROUND", (1, 1), (1, 1), colors.Color(1, 0.97, 0.97)),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(sw_table)

    if comp.get("notable_features"):
        elements.append(Spacer(1, 5))
        feats = "  ".join(f"▸ {f}" for f in comp["notable_features"])
        elements.append(Paragraph(f"<i>Notable: {feats}</i>", styles["caption"]))

    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=12, spaceBefore=10))
    return elements


def generate_pdf(data_path: str, logo_path: str, primary_hex: str, accent_hex: str, output_path: str):
    with open(data_path) as f:
        data = json.load(f)

    styles, primary, accent = build_styles(primary_hex, accent_hex)

    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")

    def header_footer(canvas, doc):
        canvas.saveState()
        # Header bar
        canvas.setFillColor(primary)
        canvas.rect(0, letter[1] - 0.35 * inch, letter[0], 0.35 * inch, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(0.75 * inch, letter[1] - 0.23 * inch, data.get("business_name", ""))
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(letter[0] - 0.75 * inch, letter[1] - 0.23 * inch,
                               f"Competitor Analysis — {data.get('report_period', '')}")
        # Footer
        canvas.setFillColor(primary)
        canvas.rect(0, 0, letter[0], 0.3 * inch, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.75 * inch, 0.1 * inch, f"Generated {data.get('generated_date', '')}")
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.1 * inch, f"Page {doc.page}")
        canvas.restoreState()

    template = PageTemplate(id="main", frames=[frame], onPage=header_footer)
    doc.addPageTemplates([template])

    story = []

    # Cover page
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=4 * inch, height=1.1 * inch)
            story.append(img)
        except Exception:
            pass

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Competitor Analysis Report", styles["title"]))
    story.append(Paragraph(data.get("industry", "").title(), styles["subtitle"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Report Period: <b>{data.get('report_period', '')}</b> &nbsp;|&nbsp; "
        f"Generated: <b>{data.get('generated_date', '')}</b>",
        styles["label"],
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=accent, spaceAfter=14, spaceBefore=10))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles["section"]))
    story.append(Paragraph(data.get("executive_summary", ""), styles["body"]))

    # Market Overview
    story.append(Paragraph("Market Overview", styles["section"]))
    story.append(Paragraph(data.get("market_overview", ""), styles["body"]))

    # Competitor Profiles
    story.append(PageBreak())
    story.append(Paragraph("Competitor Profiles", styles["section"]))
    story.append(Spacer(1, 6))

    for comp in data.get("competitors", []):
        story.extend(build_competitor_block(comp, styles, accent, primary))

    # Gap Analysis
    story.append(PageBreak())
    story.append(Paragraph("Gap Analysis", styles["section"]))

    gap = data.get("gap_analysis", {})
    for section_key, section_label, bg in [
        ("market_gaps", "Market Gaps", colors.Color(0.95, 0.97, 1.0)),
        ("opportunities", "Opportunities", colors.Color(0.93, 1.0, 0.93)),
        ("threats", "Threats", colors.Color(1.0, 0.95, 0.93)),
    ]:
        items = gap.get(section_key, [])
        if not items:
            continue
        story.append(Paragraph(section_label, styles["subsection"]))
        rows = [[Paragraph(f"• {item}", styles["bullet"])] for item in items]
        tbl = Table(rows, colWidths=[6.5 * inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 10))

    # Recommended Actions
    story.append(PageBreak())
    story.append(Paragraph("Recommended Actions", styles["section"]))
    story.append(Spacer(1, 6))

    priority_colors = {
        "high": colors.Color(0.85, 0.15, 0.15),
        "medium": colors.Color(0.85, 0.5, 0.05),
        "low": colors.Color(0.2, 0.55, 0.25),
    }

    for i, action in enumerate(data.get("recommended_actions", []), 1):
        p = action.get("priority", "medium").lower()
        p_color = priority_colors.get(p, colors.grey)
        label = f"{i}. [{action.get('priority', '').upper()}]"
        row_data = [
            [
                Paragraph(f'<font color="white"><b>{label}</b></font>', styles["body"]),
                Paragraph(f"<b>{action.get('action', '')}</b>", styles["body"]),
            ],
            [
                Paragraph("Rationale:", styles["label"]),
                Paragraph(action.get("rationale", ""), styles["body"]),
            ],
        ]
        tbl = Table(row_data, colWidths=[1.0 * inch, 5.5 * inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), p_color),
            ("BACKGROUND", (0, 1), (-1, 1), colors.Color(0.97, 0.97, 0.97)),
            ("BACKGROUND", (1, 0), (1, 0), colors.Color(0.93, 0.95, 1.0)),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("SPAN", (0, 0), (0, 0)),
        ]))
        story.append(KeepTogether([tbl, Spacer(1, 8)]))

    doc.build(story)
    print(f"PDF saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to competitor_data.json")
    parser.add_argument("--logo", required=True, help="Path to logo PNG")
    parser.add_argument("--primary-color", default="#1B3A6B")
    parser.add_argument("--accent-color", default="#4A9EDB")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()
    generate_pdf(args.data, args.logo, args.primary_color, args.accent_color, args.output)
