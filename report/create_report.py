from pathlib import Path
from xml.sax.saxutils import escape
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)

BASE = Path.home() / "FUTURE_CS_03"
SOURCE = BASE / "report" / "report_content.md"
OUTPUT = BASE / "report" / "FUTURE_CS_03_API_Security_Risk_Analysis.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=25, leading=31, textColor=colors.HexColor("#15345B"),
    alignment=TA_CENTER, spaceAfter=14
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontSize=12,
    leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#526579")
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontSize=16, leading=20,
    textColor=colors.HexColor("#15345B"), spaceBefore=12, spaceAfter=8,
    keepWithNext=True
))
styles.add(ParagraphStyle(
    name="SubSection", parent=styles["Heading2"], fontSize=12, leading=15,
    textColor=colors.HexColor("#176B87"), spaceBefore=10, spaceAfter=5,
    keepWithNext=True
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontSize=9.5,
    leading=14, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="BulletCustom", parent=styles["BodyText"], fontSize=9.5,
    leading=13, leftIndent=14, firstLineIndent=-8, spaceAfter=4
))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5DEE8"))
    canvas.line(18 * mm, 15 * mm, 192 * mm, 15 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526579"))
    canvas.drawString(18 * mm, 10 * mm, "FUTURE_CS_03 | API Security Risk Analysis")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()

def inline_markup(text):
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text

if not SOURCE.exists():
    raise SystemExit(f"Report source not found: {SOURCE}")

lines = SOURCE.read_text(encoding="utf-8").splitlines()

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=20 * mm, leftMargin=20 * mm,
    topMargin=20 * mm, bottomMargin=22 * mm,
    title="API Security Risk Analysis Report",
    author="Aditya Ashok Jondhale"
)

story = [
    Spacer(1, 35 * mm),
    Paragraph("API SECURITY<br/>RISK ANALYSIS", styles["CoverTitle"]),
    HRFlowable(width="65%", thickness=2, color=colors.HexColor("#176B87")),
    Spacer(1, 10 * mm),
    Paragraph("Future Interns Cyber Security Internship", styles["CoverSub"]),
    Spacer(1, 4 * mm),
    Paragraph("Task 3 — FUTURE_CS_03", styles["CoverSub"]),
    Spacer(1, 12 * mm),
]

cover_data = [
    ["Assessment target", "OWASP crAPI — local training environment"],
    ["Target URL", "http://127.0.0.1:8888"],
    ["Assessment type", "Authorized API security testing"],
    ["Report status", "Preliminary findings; validation required"],
]
cover_table = Table(cover_data, colWidths=[42 * mm, 105 * mm])
cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F6")),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#15345B")),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DEE8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [cover_table, Spacer(1, 20 * mm),
          Paragraph("Prepared by: Aditya Ashok Jondhale", styles["CoverSub"]),
          PageBreak()]

for line in lines:
    line = line.strip()
    if not line:
        story.append(Spacer(1, 2))
    elif line.startswith("# "):
        # Skip the document title because the cover already contains it.
        if "API Security Risk Analysis Report" not in line:
            story.append(Paragraph(inline_markup(line[2:]), styles["Section"]))
    elif line.startswith("## "):
        story.append(Paragraph(inline_markup(line[3:]), styles["Section"]))
    elif line.startswith("### "):
        story.append(Paragraph(inline_markup(line[4:]), styles["SubSection"]))
    elif line.startswith("- "):
        story.append(Paragraph("• " + inline_markup(line[2:]), styles["BulletCustom"]))
    elif re.match(r"^\d+\.\s", line):
        story.append(Paragraph(inline_markup(line), styles["BulletCustom"]))
    else:
        story.append(Paragraph(inline_markup(line), styles["BodyCustom"]))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF created: {OUTPUT}")
