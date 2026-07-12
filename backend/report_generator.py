# ─────────────────────────────────────────────
#  NIL Valuation Engine · Report Generator
# ─────────────────────────────────────────────

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

# ── Brand ─────────────────────────────────────
POSITION_COLORS = {
    "QB": HexColor("#0369a1"),
    "RB": HexColor("#16a34a"),
    "WR": HexColor("#c2410c"),
}
DARK   = HexColor("#0d0d0d")
MID    = HexColor("#4a4035")
LIGHT  = HexColor("#8b7f72")
BG     = HexColor("#f4f2ee")
BORDER = HexColor("#d0c8be")

TIER_COLORS = {
    "Elite":               HexColor("#0d0d0d"),
    "High-Level Starter":  HexColor("#1d4ed8"),
    "Starter":             HexColor("#16a34a"),
    "Contributor":         HexColor("#d97706"),
    "Below NIL Threshold": HexColor("#dc2626"),
}

LABEL_MAP = {
    "passing_yards":   "Passing Yards",
    "passing_tds":     "Passing TDs",
    "completion_pct":  "Completion %",
    "int_pct":         "INT % (inverted)",
    "rushing_yards":   "Rushing Yards",
    "rushing_tds":     "Rushing TDs",
    "ypc":             "Yards Per Carry",
    "receptions":      "Receptions",
    "receiving_yards": "Receiving Yards",
    "receiving_tds":   "Receiving TDs",
    "ypr":             "Yards Per Reception",
}

PAGE_W, PAGE_H = letter


def _styles(accent):
    """Return a dict of named ParagraphStyles."""
    return {
        "report_title": ParagraphStyle(
            "report_title",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=white,
            leading=13,
        ),
        "report_sub": ParagraphStyle(
            "report_sub",
            fontName="Helvetica",
            fontSize=8,
            textColor=HexColor("#cccccc"),
            leading=11,
        ),
        "section_label": ParagraphStyle(
            "section_label",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=accent,
            leading=10,
            spaceBefore=2,
        ),
        "player_name": ParagraphStyle(
            "player_name",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=DARK,
            leading=26,
            spaceBefore=4,
        ),
        "pvm_score": ParagraphStyle(
            "pvm_score",
            fontName="Helvetica-Bold",
            fontSize=32,
            textColor=accent,
            leading=36,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9,
            textColor=MID,
            leading=14,
            spaceAfter=2,
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=DARK,
            leading=14,
        ),
        "nil_value": ParagraphStyle(
            "nil_value",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=accent,
            leading=22,
            spaceBefore=2,
        ),
        "table_header": ParagraphStyle(
            "table_header",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=white,
            leading=11,
        ),
        "table_cell": ParagraphStyle(
            "table_cell",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=DARK,
            leading=12,
        ),
        "table_norm": ParagraphStyle(
            "table_norm",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=MID,
            leading=12,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=7,
            textColor=LIGHT,
            leading=10,
        ),
        "disclaimer": ParagraphStyle(
            "disclaimer",
            fontName="Helvetica",
            fontSize=7.5,
            textColor=LIGHT,
            leading=11,
            spaceBefore=4,
        ),
    }


def generate_pdf_report(result: dict) -> bytes:
    buffer   = BytesIO()
    name     = result.get("player_name", "Unknown Player")
    position = result.get("position", "QB")
    pvm      = result.get("pvm_score", 0.0)
    tier     = result.get("tier", "Contributor")
    nil_rec  = result.get("nil_rec", {})
    inputs   = result.get("inputs", {})
    norms    = result.get("normalized", {})
    accent   = POSITION_COLORS.get(position, HexColor("#0369a1"))
    tier_color = TIER_COLORS.get(tier, DARK)
    now      = datetime.now().strftime("%B %d, %Y")

    eligible  = nil_rec.get("eligible", False)
    estimated = nil_rec.get("estimated", 0) if eligible else None
    nil_range = nil_rec.get("range_display", "—") if eligible else "N/A"
    nil_desc  = nil_rec.get("description", "")

    S = _styles(accent)

    # ── Document ──────────────────────────────
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0,           # header drawn via onFirstPage
        bottomMargin=0.55 * inch,
        title="NIL Valuation Report",
        author="NIL Valuation Engine",
    )

    content_w = PAGE_W - 1.30 * inch

    # ── Header drawn on canvas ────────────────
    def on_first_page(canvas, doc):
        canvas.saveState()

        # Full-width dark header
        hdr_h = 0.80 * inch
        canvas.setFillColor(DARK)
        canvas.rect(0, PAGE_H - hdr_h, PAGE_W, hdr_h, fill=1, stroke=0)

        # Accent left bar
        canvas.setFillColor(accent)
        canvas.rect(0, PAGE_H - hdr_h, 5, hdr_h, fill=1, stroke=0)

        # Left: branding
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(white)
        canvas.drawString(0.65 * inch, PAGE_H - 0.32 * inch, "NIL VALUATION ENGINE")

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(HexColor("#9ca3af"))
        canvas.drawString(0.65 * inch, PAGE_H - 0.48 * inch,
                          "Performance-Based Athlete Valuation")

        # Right: date + position
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 0.32 * inch, now)
        canvas.setFillColor(accent)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawRightString(PAGE_W - 0.65 * inch, PAGE_H - 0.48 * inch,
                               f"{position} VALUATION REPORT")

        canvas.restoreState()

    # ── Story ─────────────────────────────────
    story = []

    # Spacer to clear the header
    story.append(Spacer(1, 0.95 * inch))

    # ── SECTION: Player Summary ───────────────
    story.append(Paragraph("PLAYER SUMMARY", S["section_label"]))
    story.append(HRFlowable(width=content_w, thickness=0.5,
                             color=accent, spaceAfter=8))

    # Two-column summary: name/position left | PVM score right
    summary_data = [[
        # Left cell
        Table(
            [
                [Paragraph(name, S["player_name"])],
                [Paragraph(f"{position}  ·  {tier}", S["body_bold"])],
            ],
            colWidths=[content_w * 0.65],
            style=TableStyle([
                ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING",   (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
            ]),
        ),
        # Right cell: PVM score
        Table(
            [
                [Paragraph("PVM SCORE", S["section_label"])],
                [Paragraph(f"{pvm:.3f}", S["pvm_score"])],
                [Paragraph("out of 1.000", S["disclaimer"])],
            ],
            colWidths=[content_w * 0.35],
            style=TableStyle([
                ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING",   (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
                ("ALIGN",        (0, 0), (-1, -1), "RIGHT"),
            ]),
        ),
    ]]

    summary_table = Table(
        summary_data,
        colWidths=[content_w * 0.65, content_w * 0.35],
        style=TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING",   (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ]),
    )
    story.append(summary_table)
    story.append(Spacer(1, 0.18 * inch))

    # ── SECTION: NIL Valuation ────────────────
    story.append(Paragraph("NIL VALUATION", S["section_label"]))
    story.append(HRFlowable(width=content_w, thickness=0.5,
                             color=accent, spaceAfter=8))

    if eligible:
        nil_left = [
            [Paragraph("ESTIMATED ANNUAL VALUE", S["section_label"])],
            [Paragraph(f"${estimated:,.0f}", S["nil_value"])],
            [Paragraph(f"Valuation Range:  {nil_range}", S["body_bold"])],
            [Spacer(1, 4)],
            [Paragraph(nil_desc, S["body"])],
        ]
    else:
        nil_left = [
            [Paragraph(
                "NO RECOMMENDED NIL ALLOCATION",
                ParagraphStyle("no_nil", fontName="Helvetica-Bold",
                               fontSize=10, textColor=HexColor("#dc2626"), leading=14),
            )],
            [Spacer(1, 4)],
            [Paragraph(nil_desc, S["body"])],
        ]

    nil_right = [
        [Paragraph("TIER", S["section_label"])],
        [Paragraph(
            tier,
            ParagraphStyle("tier_val", fontName="Helvetica-Bold",
                           fontSize=11, textColor=tier_color, leading=15),
        )],
        [Spacer(1, 8)],
        [Paragraph("ELIGIBILITY", S["section_label"])],
        [Paragraph(
            "Eligible" if eligible else "Not Eligible",
            ParagraphStyle("elig", fontName="Helvetica-Bold", fontSize=10,
                           textColor=accent if eligible else HexColor("#dc2626"),
                           leading=14),
        )],
    ]

    nil_table = Table(
        [[
            Table(nil_left,  colWidths=[content_w * 0.64],
                  style=TableStyle([
                      ("LEFTPADDING",  (0,0),(-1,-1), 0),
                      ("RIGHTPADDING", (0,0),(-1,-1), 0),
                      ("TOPPADDING",   (0,0),(-1,-1), 0),
                      ("BOTTOMPADDING",(0,0),(-1,-1), 2),
                  ])),
            Table(nil_right, colWidths=[content_w * 0.36],
                  style=TableStyle([
                      ("LEFTPADDING",  (0,0),(-1,-1), 8),
                      ("RIGHTPADDING", (0,0),(-1,-1), 0),
                      ("TOPPADDING",   (0,0),(-1,-1), 0),
                      ("BOTTOMPADDING",(0,0),(-1,-1), 2),
                      ("LINEBEFORE",   (0,0),(0,-1), 0.5, BORDER),
                  ])),
        ]],
        colWidths=[content_w * 0.64, content_w * 0.36],
        style=TableStyle([
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0),(-1,-1), 0),
            ("RIGHTPADDING", (0,0),(-1,-1), 0),
            ("TOPPADDING",   (0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ]),
    )
    story.append(nil_table)
    story.append(Spacer(1, 0.20 * inch))

    # ── SECTION: Statistics ───────────────────
    story.append(Paragraph("STATISTICAL BREAKDOWN", S["section_label"]))
    story.append(HRFlowable(width=content_w, thickness=0.5,
                             color=accent, spaceAfter=8))

    # Build table rows
    raw_vals  = list(inputs.values())
    norm_items = list(norms.items())

    col_w = [content_w * 0.44, content_w * 0.28, content_w * 0.28]

    stat_rows = [[
        Paragraph("METRIC",     S["table_header"]),
        Paragraph("VALUE",      S["table_header"]),
        Paragraph("NORMALIZED", S["table_header"]),
    ]]

    for idx, (nk, nv) in enumerate(norm_items):
        raw = raw_vals[idx] if idx < len(raw_vals) else "—"
        lbl = LABEL_MAP.get(nk, nk.replace("_", " ").title())
        stat_rows.append([
            Paragraph(lbl,       S["table_cell"]),
            Paragraph(str(raw),  S["table_cell"]),
            Paragraph(f"{nv:.3f}", S["table_norm"]),
        ])

    stat_table = Table(
        stat_rows,
        colWidths=col_w,
        repeatRows=1,
        style=TableStyle([
            # Header row
            ("BACKGROUND",   (0, 0), (-1, 0), accent),
            ("TEXTCOLOR",    (0, 0), (-1, 0), white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 8),
            ("TOPPADDING",   (0, 0), (-1, 0), 7),
            ("BOTTOMPADDING",(0, 0), (-1, 0), 7),
            ("LEFTPADDING",  (0, 0), (-1, 0), 10),
            # Data rows
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8.5),
            ("TOPPADDING",   (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING",(0, 1), (-1, -1), 6),
            ("LEFTPADDING",  (0, 1), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            # Alternating row shading
            *[("BACKGROUND", (0, i), (-1, i), HexColor("#f9f7f4"))
              for i in range(2, len(stat_rows), 2)],
            # Grid
            ("LINEBELOW",    (0, 0), (-1, -1), 0.3, BORDER),
            ("LINEAFTER",    (0, 0), (-1, -1), 0.3, BORDER),
            ("LINEBEFORE",   (0, 0), (0, -1),  0.3, BORDER),
            ("BOX",          (0, 0), (-1, -1), 0.5, BORDER),
            # Align value and normalized columns center
            ("ALIGN",        (1, 0), (-1, -1), "CENTER"),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]),
    )
    story.append(stat_table)
    story.append(Spacer(1, 0.22 * inch))

    # ── SECTION: Methodology note ─────────────
    story.append(HRFlowable(width=content_w, thickness=0.3,
                             color=BORDER, spaceAfter=6))
    story.append(Paragraph(
        "<b>Methodology:</b> PVM scores are calculated using a weighted composite of "
        "position-specific performance metrics normalized to [0, 1]. NIL valuations are "
        "estimates and do not constitute financial advice. School brand equity, social reach, "
        "and marketability are significant drivers not captured by this model.",
        S["disclaimer"],
    ))

    # ── Build ─────────────────────────────────
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_first_page)
    return buffer.getvalue()


# ── Plain-text fallback ───────────────────────

def generate_txt_report(result: dict) -> str:
    now     = datetime.now().strftime("%B %d, %Y  %I:%M %p")
    name    = result.get("player_name", "Unknown Player")
    pos     = result.get("position", "—")
    pvm     = result.get("pvm_score", 0.0)
    tier    = result.get("tier", "—")
    nil_rec = result.get("nil_rec", {})
    inputs  = result.get("inputs", {})
    norms   = result.get("normalized", {})

    nil_line  = nil_rec.get("display", "No Recommended NIL Allocation")
    nil_desc  = nil_rec.get("description", "")
    nil_range = nil_rec.get("range_display", "—") if nil_rec.get("eligible") else "N/A"

    lines = [
        "=" * 60,
        "  COLLEGE FOOTBALL NIL VALUATION ENGINE",
        "  Performance-Based Athlete Valuation Report",
        "=" * 60, "",
        f"  Report Generated: {now}", "",
        "-" * 60, "  PLAYER PROFILE", "-" * 60,
        f"  Name:      {name}",
        f"  Position:  {pos}",
        f"  PVM Score: {pvm:.4f}  ({pvm * 100:.1f} / 100)",
        f"  Tier:      {tier}", "",
        "-" * 60, "  NIL RECOMMENDATION", "-" * 60,
        f"  {nil_line}", f"  Range:     {nil_range}", "",
        f"  {nil_desc}", "",
        "-" * 60, "  INPUT STATISTICS", "-" * 60,
    ]
    for k, v in inputs.items():
        lines.append(f"  {str(k):<30} {v}")
    lines += ["", "-" * 60, "  NORMALIZED STATISTICS", "-" * 60]
    for k, v in norms.items():
        lines.append(f"  {k.replace('_', ' ').title():<30} {v:.4f}")
    lines += [
        "", "=" * 60,
        "  NIL Valuation Engine  |  Confidential",
        "=" * 60,
    ]
    return "\n".join(lines)