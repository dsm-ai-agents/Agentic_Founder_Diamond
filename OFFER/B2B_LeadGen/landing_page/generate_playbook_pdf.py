from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, ListFlowable, ListItem, KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
OUT = BASE / "b2b-lead-generation-playbook-designed.pdf"

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 19 * mm
MARGIN_BOTTOM = 17 * mm

NAVY = colors.HexColor("#081C2D")
INK = colors.HexColor("#122033")
MUTED = colors.HexColor("#64748B")
CYAN = colors.HexColor("#16C7D9")
GOLD = colors.HexColor("#FFB84D")
MINT = colors.HexColor("#DDFCF2")
PAPER = colors.HexColor("#F7FAFC")
LINE = colors.HexColor("#D7E2EA")
BLUE_SOFT = colors.HexColor("#EAF8FB")
ORANGE_SOFT = colors.HexColor("#FFF4E4")
GREEN_SOFT = colors.HexColor("#EAFBF2")

# Use available system fonts for a more premium look than default Helvetica.
FONT_DIRS = [Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/share/fonts/truetype/liberation2")]
try:
    pdfmetrics.registerFont(TTFont("DejaVuSerif", str(FONT_DIRS[0] / "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", str(FONT_DIRS[0] / "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSans", str(FONT_DIRS[0] / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(FONT_DIRS[0] / "DejaVuSans-Bold.ttf")))
    DISPLAY = "DejaVuSerif-Bold"
    BODY = "DejaVuSans"
    BODY_BOLD = "DejaVuSans-Bold"
except Exception:
    DISPLAY = "Times-Bold"
    BODY = "Helvetica"
    BODY_BOLD = "Helvetica-Bold"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="Kicker", fontName=BODY_BOLD, fontSize=8.5, leading=11,
    textColor=CYAN, uppercase=True, spaceAfter=7, tracking=1.3
))
styles.add(ParagraphStyle(
    name="CoverTitle", fontName=DISPLAY, fontSize=36, leading=40,
    textColor=colors.white, alignment=TA_LEFT, spaceAfter=14
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName=BODY, fontSize=13.5, leading=20,
    textColor=colors.HexColor("#DDEAF1"), spaceAfter=16
))
styles.add(ParagraphStyle(
    name="H1", fontName=DISPLAY, fontSize=22, leading=27,
    textColor=NAVY, spaceBefore=2, spaceAfter=12
))
styles.add(ParagraphStyle(
    name="H2", fontName=BODY_BOLD, fontSize=13.5, leading=17,
    textColor=NAVY, spaceBefore=8, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="Body", fontName=BODY, fontSize=10.2, leading=15.2,
    textColor=INK, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="Small", fontName=BODY, fontSize=8.2, leading=11.5,
    textColor=MUTED
))
styles.add(ParagraphStyle(
    name="Rule", fontName=BODY_BOLD, fontSize=10.5, leading=15,
    textColor=NAVY, backColor=ORANGE_SOFT, borderColor=GOLD,
    borderWidth=1, borderPadding=8, leftIndent=0, rightIndent=0,
    spaceBefore=8, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="Quote", fontName=BODY, fontSize=10, leading=15,
    textColor=INK, backColor=BLUE_SOFT, borderColor=CYAN,
    borderWidth=1, borderPadding=9, leftIndent=0, rightIndent=0,
    spaceBefore=6, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="TemplateBox", fontName=BODY, fontSize=9.2, leading=13.5,
    textColor=INK, backColor=colors.white, borderColor=LINE,
    borderWidth=0.8, borderPadding=9, spaceBefore=5, spaceAfter=9
))


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def p(text, style="Body"):
    # markdown-ish bold conversion
    text = esc(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    return Paragraph(text, styles[style])


def bullets(items, bullet_type="bullet"):
    flow = []
    for item in items:
        flow.append(ListItem(p(item), leftIndent=4, bulletColor=CYAN))
    return ListFlowable(flow, bulletType=bullet_type, start="1", leftIndent=15, bulletFontName=BODY_BOLD, bulletFontSize=8.5, bulletColor=CYAN)


def card(title, body_items=None, body_paras=None, bg=colors.white, accent=CYAN):
    content = [p(title, "H2")]
    if body_paras:
        for para in body_paras:
            content.append(p(para))
    if body_items:
        content.append(bullets(body_items))
    tbl = Table([[content]], colWidths=[PAGE_W - 2*MARGIN_X - 6*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.8, LINE),
        ("LINEBEFORE", (0,0), (0,-1), 4, accent),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    return KeepTogether([tbl, Spacer(1, 8)])


def header_footer(canv: canvas.Canvas, doc):
    page = canv.getPageNumber()
    canv.saveState()
    # Top hairline and running title after cover
    if page > 1:
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.6)
        canv.line(MARGIN_X, PAGE_H - 12*mm, PAGE_W - MARGIN_X, PAGE_H - 12*mm)
        canv.setFont(BODY_BOLD, 7.5)
        canv.setFillColor(MUTED)
        canv.drawString(MARGIN_X, PAGE_H - 9*mm, "THE B2B LEAD GENERATION PLAYBOOK")
        canv.setFont(BODY, 7.5)
        canv.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 9*mm, "14-day outbound execution system")
    # Footer
    if page > 1:
        canv.setStrokeColor(LINE)
        canv.line(MARGIN_X, 12*mm, PAGE_W - MARGIN_X, 12*mm)
        canv.setFont(BODY, 8)
        canv.setFillColor(MUTED)
        canv.drawString(MARGIN_X, 8*mm, "Target → Message → Follow-up")
        canv.drawRightString(PAGE_W - MARGIN_X, 8*mm, str(page-1))
    canv.restoreState()


def cover(canv: canvas.Canvas, doc):
    canv.saveState()
    # Background
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Decorative geometry
    canv.setFillColor(colors.HexColor("#0B3049"))
    canv.circle(PAGE_W-16*mm, PAGE_H-34*mm, 55*mm, fill=1, stroke=0)
    canv.setFillColor(colors.HexColor("#123B55"))
    canv.circle(PAGE_W-32*mm, 35*mm, 37*mm, fill=1, stroke=0)
    canv.setFillColor(CYAN)
    canv.rect(0, PAGE_H-24*mm, PAGE_W, 4*mm, fill=1, stroke=0)
    canv.setFillColor(GOLD)
    canv.rect(0, PAGE_H-30*mm, 78*mm, 4*mm, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont(BODY_BOLD, 9)
    canv.drawString(MARGIN_X, PAGE_H-48*mm, "FREE PDF PLAYBOOK")
    canv.setFont(DISPLAY, 38)
    y = PAGE_H-76*mm
    for line in ["The B2B Lead", "Generation", "Playbook"]:
        canv.drawString(MARGIN_X, y, line)
        y -= 15*mm
    canv.setFont(BODY, 13)
    canv.setFillColor(colors.HexColor("#DDEAF1"))
    canv.drawString(MARGIN_X, y-3*mm, "A practical, step-by-step system to book more")
    canv.drawString(MARGIN_X, y-10*mm, "meetings in the next 14 days.")

    # Promise panel
    panel_y = 52*mm
    canv.setFillColor(colors.HexColor("#FFFFFF"))
    canv.roundRect(MARGIN_X, panel_y, PAGE_W - 2*MARGIN_X, 42*mm, 4*mm, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.setFont(BODY_BOLD, 11)
    canv.drawString(MARGIN_X+8*mm, panel_y+28*mm, "Inside:")
    canv.setFont(BODY, 9.6)
    canv.drawString(MARGIN_X+8*mm, panel_y+20*mm, "ICP checklist • lead list setup • cold outreach templates")
    canv.drawString(MARGIN_X+8*mm, panel_y+13*mm, "follow-up sequence • simple KPI tracker")
    canv.setFillColor(CYAN)
    canv.roundRect(MARGIN_X+8*mm, panel_y+5*mm, 57*mm, 7*mm, 2*mm, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.setFont(BODY_BOLD, 7.8)
    canv.drawCentredString(MARGIN_X+36.5*mm, panel_y+7.1*mm, "TARGET → MESSAGE → FOLLOW-UP")
    canv.restoreState()


def build_story():
    story = []
    story.append(PageBreak())

    # Overview page
    story += [p("Page 1 — What this playbook helps you do", "H1")]
    story.append(p("If your outbound feels inconsistent, the issue is usually one of these:"))
    story.append(card("Common outbound failure points", [
        "Targeting is too broad",
        "Messaging is not specific enough",
        "Follow-ups stop too early",
        "There’s no simple tracking system",
    ], bg=BLUE_SOFT, accent=CYAN))
    story.append(p("This playbook gives you a lightweight system to fix all four—fast."))
    story.append(Spacer(1, 8))
    story.append(card("The practical promise", body_paras=["Use this as your 14-day operating system: define the right accounts, send messages that create replies, follow up with discipline, and track the metrics that matter."], bg=GREEN_SOFT, accent=colors.HexColor("#10B981")))
    story.append(PageBreak())

    story += [p("Page 2 — The 3-Step System", "H1")]
    data = [
        [p("01", "H2"), p("Target the right accounts", "H2"), p("Get ICP clarity before writing a single message.")],
        [p("02", "H2"), p("Send a reply-worthy message", "H2"), p("Use problem + outcome + proof to earn attention.")],
        [p("03", "H2"), p("Follow up like a system", "H2"), p("Stop ‘checking in.’ Add context, proof, assets, and clear next steps.")],
    ]
    tbl = Table(data, colWidths=[20*mm, 54*mm, 84*mm], rowHeights=[28*mm]*3)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
        ("BOX", (0,0), (-1,-1), 0.8, LINE),
        ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("BACKGROUND", (0,0), (0,-1), NAVY),
        ("TEXTCOLOR", (0,0), (0,-1), colors.white),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 12))
    story.append(card("Goal for the next 14 days", [
        "Build a clean list of 200–500 leads",
        "Send 20–50 messages per day depending on capacity",
        "Run a 4–6 touch follow-up sequence",
        "Track reply rate and meetings booked",
    ], bg=ORANGE_SOFT, accent=GOLD))
    story.append(PageBreak())

    story += [p("Page 3 — ICP Checklist", "H1"), p("Fill this before you write a single message.")]
    fields = ["Industry", "Company size (employees / revenue)", "Geography", "Job titles you target", "Current tools they use", "Top 3 pains you solve", "Top 3 outcomes you deliver", "What makes you different (1–2 lines)"]
    rows = [[p(f"<b>{f}</b>"), ""] for f in fields]
    form = Table(rows, colWidths=[58*mm, 100*mm], rowHeights=[11*mm]*len(rows))
    form.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, LINE), ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("BACKGROUND", (0,0), (0,-1), BLUE_SOFT), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(form)
    story.append(Spacer(1, 8))
    story.append(card("Trigger events: signals they might buy now", ["Hiring sales team", "Recently raised funding", "Launching a new product", "Expanding into a new region"], bg=colors.white, accent=CYAN))
    story.append(p("Rule: If you can’t describe “who + pain + outcome” in one sentence, your ICP is not ready.", "Rule"))
    story.append(PageBreak())

    story += [p("Page 4 — Lead List Setup", "H1")]
    story.append(card("Where to find leads", ["LinkedIn Sales Navigator", "Company directories and associations", "Industry newsletters and event attendee lists", "BuiltWith / similar tech lookup tools"], bg=BLUE_SOFT, accent=CYAN))
    story.append(card("Minimum fields to capture", ["First name, last name", "Title", "Company", "Website", "LinkedIn URL", "Work email", "Phone (optional but valuable)", "Notes: trigger, tool used, recent post, etc."], bg=colors.white, accent=GOLD))
    story.append(p("Quality filter: Don’t add leads unless you can answer: “Why them, why now?”", "Rule"))
    story.append(PageBreak())

    story += [p("Page 5 — Message Framework", "H1"), p("Use this structure as your base. It is simple enough to scale, but specific enough to avoid generic outreach.")]
    story.append(card("The only framework you need", ["Personalization: one relevant line", "Problem: what they likely face", "Outcome: what they want", "Proof: how you know / what you’ve done", "CTA: simple, low-friction"], bg=GREEN_SOFT, accent=colors.HexColor("#10B981")))
    story.append(p("Example", "H2"))
    story.append(p("“Hey {{Name}} — saw {{relevant trigger}}.<br/><br/>Many {{role}} teams struggle with {{pain}} which leads to {{cost}}.<br/><br/>We help {{ICP}} achieve {{outcome}} in {{timeframe}} using {{method}}.<br/><br/>Open to a quick 10-minute chat to see if this fits?”", "Quote"))
    story.append(PageBreak())

    story += [p("Page 6 — Cold Email Templates", "H1")]
    story.append(p("Template A — simple + direct", "H2"))
    story.append(p("<b>Subject:</b> Quick question about {{Company}}<br/><br/>Hi {{Name}},<br/><br/>Noticed {{trigger}} at {{Company}}.<br/><br/>Are you currently working on {{relevant initiative}}?<br/><br/>We help {{ICP}} get {{outcome}} by {{method}}.<br/><br/>If it’s useful, I can share a 1-page plan for {{Company}}.<br/><br/>Should I send it over?<br/><br/>Thanks,<br/>{{Your Name}}", "TemplateBox"))
    story.append(p("Template B — value first", "H2"))
    story.append(p("<b>Subject:</b> {{Outcome}} for {{Company}}?<br/><br/>Hi {{Name}},<br/><br/>I put together a quick checklist we use to help {{ICP}} improve {{outcome}}:<br/>• {{point 1}}<br/>• {{point 2}}<br/>• {{point 3}}<br/><br/>If you tell me what you’re using for {{tool/process}} today, I can tailor it to {{Company}}.<br/><br/>Worth sharing?<br/><br/>— {{Your Name}}", "TemplateBox"))
    story.append(PageBreak())

    story += [p("Page 7 — LinkedIn DM Templates", "H1")]
    story.append(card("Connection request — no pitch", body_paras=["“Hey {{Name}} — liked your post on {{topic}}. I work with {{ICP}} on {{outcome}}. Would love to connect.”"], bg=colors.white, accent=CYAN))
    story.append(card("After they accept", body_paras=["“Thanks for connecting, {{Name}}. Quick question—are you currently focused on {{initiative}} at {{Company}}?”"], bg=colors.white, accent=GOLD))
    story.append(card("If they reply “yes”", body_paras=["“Got it. We typically see {{pain}} show up when teams do {{context}}. If helpful, I can share the exact sequence we use to book meetings in {{industry}}. Want it?”"], bg=GREEN_SOFT, accent=colors.HexColor("#10B981")))
    story.append(PageBreak())

    story += [p("Page 8 — Follow-up Sequence", "H1"), p("Most meetings come from follow-ups. Use this sequence instead of vague ‘checking in’ messages.")]
    follow = [
        [p("Day 1", "H2"), p("Initial message")],
        [p("Day 2", "H2"), p("Quick add—recently helped {{similar company}} get {{result}} in {{timeframe}}. Worth exploring?")],
        [p("Day 4", "H2"), p("I can share a short checklist/template for {{outcome}}—want it?")],
        [p("Day 7", "H2"), p("Before I close this out—are you the right person for {{topic}}, or should I speak to someone else?")],
        [p("Day 10", "H2"), p("Looks like timing isn’t right. If you want, I can send the playbook and you can reach out when it’s a priority.")],
    ]
    ft = Table(follow, colWidths=[28*mm, 130*mm])
    ft.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, LINE), ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("BACKGROUND", (0,0), (0,-1), NAVY), ("TEXTCOLOR", (0,0), (0,-1), colors.white),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(ft)
    story.append(PageBreak())

    story += [p("Page 9 — KPI Tracker", "H1"), p("Keep it simple. Track only what helps you improve targeting, messaging, and meeting conversion.")]
    metrics = [[p("Metric", "H2"), p("Weekly count", "H2")]] + [[p(m), ""] for m in ["New leads added", "Messages sent", "Replies", "Positive replies", "Meetings booked", "Cost per meeting"]]
    mt = Table(metrics, colWidths=[78*mm, 80*mm], rowHeights=[12*mm]+[13*mm]*6)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BOX", (0,0), (-1,-1), 0.8, LINE), ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(mt)
    story.append(Spacer(1, 10))
    story.append(card("Benchmarks (guideline)", ["Cold outreach reply rate: 3–10%", "Positive reply rate: 1–5%", "Meetings booked depend on offer clarity + targeting"], bg=ORANGE_SOFT, accent=GOLD))
    story.append(PageBreak())

    story += [p("Page 10 — Your 14-Day Execution Plan", "H1")]
    plan = [
        [p("Day 1–2", "H2"), p("Finalize ICP + offer + messaging")],
        [p("Day 3–4", "H2"), p("Build list of 200–500 leads")],
        [p("Day 5–14", "H2"), p("Run daily outreach + follow-ups")],
    ]
    pt = Table(plan, colWidths=[36*mm, 122*mm], rowHeights=[22*mm]*3)
    pt.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, LINE), ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("BACKGROUND", (0,0), (0,-1), BLUE_SOFT), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(pt)
    story.append(Spacer(1, 10))
    story.append(card("Daily checklist", ["Add 20–50 leads", "Send 20–50 messages", "Follow up with yesterday’s non-responders", "Track replies + meetings booked"], bg=GREEN_SOFT, accent=colors.HexColor("#10B981")))
    story.append(PageBreak())

    story += [p("Final Page — Call to Action", "H1")]
    story.append(card("Want help implementing this system end-to-end?", body_paras=["Reply to our email or book a call from our website."], bg=NAVY, accent=GOLD))
    story.append(Spacer(1, 10))
    story.append(p("Use the playbook to create clarity. Get help if you want the targeting, list building, messaging, automation, and reporting implemented as a repeatable pipeline.", "Body"))
    return story


class PlaybookDoc(BaseDocTemplate):
    pass


def main():
    doc = PlaybookDoc(str(OUT), pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                      topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, PAGE_W-2*MARGIN_X, PAGE_H-MARGIN_TOP-MARGIN_BOTTOM, id="normal")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[frame], onPage=cover),
        PageTemplate(id="Body", frames=[frame], onPage=header_footer),
    ])
    story = build_story()
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
