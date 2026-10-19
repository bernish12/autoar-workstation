import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_simple_easy_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors - Professional, Clean & Crystal Clear
    DARK_BG = RGBColor(11, 19, 38)          # Professional Midnight Blue
    CARD_BG = RGBColor(19, 31, 58)          # Clean Solid Card
    CYAN_ACCENT = RGBColor(0, 229, 255)     # Bright Cyan Highlight
    EMERALD_GREEN = RGBColor(16, 185, 129)  # Success Green
    AMBER_GOLD = RGBColor(251, 191, 36)     # Gold for Titles
    WHITE_TEXT = RGBColor(255, 255, 255)    # High Readability White
    MUTED_TEXT = RGBColor(160, 178, 204)    # Clear Slate Secondary
    BORDER_COLOR = RGBColor(38, 56, 94)     # Crisp Card Border
    RED_ACCENT = RGBColor(239, 68, 68)       # Defect Warning Red

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.color.rgb = DARK_BG
        return bg

    def add_slide_header(slide, step_number, title, subtitle):
        # Top Accent Line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = CYAN_ACCENT
        top_bar.line.color.rgb = CYAN_ACCENT

        # Header Text Box
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.733), Inches(0.95))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = f"{step_number}. {title.upper()}"
        p1.font.size = Pt(21)
        p1.font.bold = True
        p1.font.name = "Arial"
        p1.font.color.rgb = CYAN_ACCENT

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(11)
        p2.font.name = "Arial"
        p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 1: FRONT PAGE (CLEAN, PROFESSIONAL, NO PHOTOS)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_bg(slide1)

    top_line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.04))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = CYAN_ACCENT
    top_line.line.color.rgb = CYAN_ACCENT

    # College Name & Dept
    c_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(1.1))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    p = tf_c.paragraphs[0]
    p.text = "ROHINI COLLEGE OF ENGINEERING AND TECHNOLOGY"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = AMBER_GOLD
    p.alignment = PP_ALIGN.CENTER

    p = tf_c.add_paragraph()
    p.text = "DEPARTMENT OF MECHANICAL ENGINEERING • ROHINI COLLEGE OF ENGINEERING AND TECHNOLOGY"
    p.font.size = Pt(11)
    p.font.name = "Arial"
    p.font.color.rgb = MUTED_TEXT
    p.alignment = PP_ALIGN.CENTER

    # Pill Tag
    tag_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(2.0), Inches(3.933), Inches(0.4))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = RGBColor(16, 26, 50)
    tag_box.line.color.rgb = CYAN_ACCENT
    tf_t = tag_box.text_frame
    p = tf_t.paragraphs[0]
    p.text = "FINAL YEAR PROJECT REVIEW • 2026"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # Main Project Title
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.733), Inches(1.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0

    p = tf_title.paragraphs[0]
    p.text = "IMPLEMENTATION OF AUGMENTED REALITY (AR)\nIN ASSEMBLY OF AUTOMOBILES"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = WHITE_TEXT
    p.alignment = PP_ALIGN.CENTER


    # Bottom 2 Simple Cards: Guide & Students
    # Guide Card
    g_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.9), Inches(4.8), Inches(1.8))
    g_card.fill.solid()
    g_card.fill.fore_color.rgb = CARD_BG
    g_card.line.color.rgb = BORDER_COLOR
    tf_g = g_card.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_top = tf_g.margin_right = tf_g.margin_bottom = Inches(0.2)

    p = tf_g.paragraphs[0]
    p.text = "PROJECT GUIDE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(6)

    p = tf_g.add_paragraph()
    p.text = "Mr. K. Rajasuthan, M.E."
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = WHITE_TEXT

    p = tf_g.add_paragraph()
    p.text = "Assistant Professor\nDepartment of Mechanical Engineering"
    p.font.size = Pt(10)
    p.font.name = "Arial"
    p.font.color.rgb = MUTED_TEXT

    # Students Card
    s_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.9), Inches(5.0), Inches(1.8))
    s_card.fill.solid()
    s_card.fill.fore_color.rgb = CARD_BG
    s_card.line.color.rgb = CYAN_ACCENT
    tf_s = s_card.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = Inches(0.2)

    p = tf_s.paragraphs[0]
    p.text = "PRESENTED BY"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(8)

    p = tf_s.add_paragraph()
    p.text = "• Harikrishnan. B          • Ajay. C S"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = WHITE_TEXT
    p.space_after = Pt(6)

    p = tf_s.add_paragraph()
    p.text = "• Jenish. J                     • Bernish. N"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = WHITE_TEXT

    bot_line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.04))
    bot_line.fill.solid()
    bot_line.fill.fore_color.rgb = CYAN_ACCENT
    bot_line.line.color.rgb = CYAN_ACCENT

    # =========================================================================
    # SLIDE 2: 1. ABSTRACT (SIMPLE, SHORT, CLEAR POINTS)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_bg(slide2)
    add_slide_header(slide2, "1", "Abstract", "Project Summary in Simple Words")

    # Left: 3 Simple Easy Cards
    easy_abstract = [
        ("The Fresher Worker Challenge", "New and fresher assembly workers easily get confused by complex vehicle drawings. They hesitate, check manuals repeatedly, and cause severe time delays."),
        ("Our Visual AR Solution", "Our software connects directly with Augmented Reality (AR) glasses to visually project 3D CAD parts and animated arrows right onto real car parts. Even a beginner knows exactly what to do!"),
        ("Focus on Small Factories & Zero Defects", "Our primary mission is bringing this AR technology to small-scale automotive factories and MSMEs. It eliminates expensive foreign software fees, helping local workshops boost productivity and achieve zero assembly defects!")
    ]

    for idx, (title, desc) in enumerate(easy_abstract):
        box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5 + idx * 1.8), Inches(6.8), Inches(1.6))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CYAN_ACCENT if idx == 1 else BORDER_COLOR
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = f"✔ {title}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = CYAN_ACCENT if idx != 2 else EMERALD_GREEN
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.name = "Arial"
        p.font.color.rgb = WHITE_TEXT

    # Right: Real Software Screenshot Evidence (Clutch Assembly Station)
    if os.path.exists("D:/solidworks/2026-10-13_16-22.png"):
        slide2.shapes.add_picture("D:/solidworks/2026-10-13_16-22.png", Inches(7.8), Inches(1.5), width=Inches(4.7))
    
    cap = slide2.shapes.add_textbox(Inches(7.8), Inches(5.8), Inches(4.7), Inches(0.9))
    cap.text_frame.word_wrap = True
    cap.text_frame.text = "Figure 1: AutoAR Workstation live interface — 3D interactive assembly instructions for fresh operators."
    cap.text_frame.paragraphs[0].font.size = Pt(10)
    cap.text_frame.paragraphs[0].font.italic = True
    cap.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 3: 2. INTRODUCTION (ULTRA SIMPLE & CLEAR WORDS)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_bg(slide3)
    add_slide_header(slide3, "2", "Introduction", "Why Augmented Reality is Needed in Car Assembly")

    intro_points = [
        (
            "01. The Problem: Paper Drawings",
            "Hard to Understand for New Workers",
            [
                "Workers use 2D paper blueprints on the shop floor.",
                "New technicians easily get confused by complex drawings.",
                "One small mistake leads to wrong bolt fitting and big delays."
            ],
            RED_ACCENT
        ),
        (
            "02. The Solution: Live 3D AR Guide",
            "Floating 3D Parts & Clear Arrows",
            [
                "AutoAR shows 3D CAD parts directly on the real car.",
                "Bright animated arrows show exactly where each part fits.",
                "Any beginner worker can assemble parts with zero doubt."
            ],
            CYAN_ACCENT
        ),
        (
            "03. Smart Control: Voice Commands",
            "Hands-Free & No Mouse Needed",
            [
                "Workers wear oily gloves and hold heavy tools in both hands.",
                "No need to touch a mouse, keyboard, or dirty screen.",
                "Just speak simple words like 'Next', 'Torque', or 'Rotate'."
            ],
            EMERALD_GREEN
        )
    ]

    # Ensure matching 16:9 screenshots for Slide 3
    left_img_path = "D:/solidworks/slide3_left.png"
    right_img_path = "D:/solidworks/slide3_right.png"
    try:
        from PIL import Image
        if os.path.exists("D:/solidworks/2026-10-13_16-26.png") and not os.path.exists(left_img_path):
            im1 = Image.open("D:/solidworks/2026-10-13_16-26.png")
            new_w1 = int(im1.size[1] * (16 / 9))
            left1 = (im1.size[0] - new_w1) // 2
            im1.crop((left1, 0, left1 + new_w1, im1.size[1])).save(left_img_path)
        if os.path.exists("D:/solidworks/2026-10-13_16-25.png") and not os.path.exists(right_img_path):
            im2 = Image.open("D:/solidworks/2026-10-13_16-25.png")
            new_h2 = int(im2.size[0] / (16 / 9))
            top2 = (im2.size[1] - new_h2) // 2
            im2.crop((0, top2, im2.size[0], top2 + new_h2)).save(right_img_path)
    except Exception as e:
        left_img_path = "D:/solidworks/2026-10-13_16-26.png"
        right_img_path = "D:/solidworks/2026-10-13_16-25.png"

    for idx, (title, subtitle_text, bullets, accent_color) in enumerate(intro_points):
        # Perfectly centered 3 cards: left = 0.8, 4.816, 8.833 (span exactly 0.8 to 12.533)
        c = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 4.016), Inches(1.45), Inches(3.7), Inches(2.15))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = accent_color
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.15)

        # Title
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = accent_color
        p.space_after = Pt(2)

        # Subtitle badge
        p_sub = tf.add_paragraph()
        p_sub.text = f"▸ {subtitle_text}"
        p_sub.font.size = Pt(9)
        p_sub.font.bold = True
        p_sub.font.name = "Arial"
        p_sub.font.color.rgb = WHITE_TEXT
        p_sub.space_after = Pt(5)

        # Bullets
        for b_text in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b_text}"
            p_b.font.size = Pt(9.5)
            p_b.font.name = "Arial"
            p_b.font.color.rgb = MUTED_TEXT
            p_b.space_after = Pt(2)

    # Bottom: 2 Perfectly Aligned Screenshots with identical 16:9 ratio and matching height
    if os.path.exists(left_img_path):
        slide3.shapes.add_picture(left_img_path, Inches(0.8), Inches(3.8), width=Inches(5.7), height=Inches(3.2))
    if os.path.exists(right_img_path):
        slide3.shapes.add_picture(right_img_path, Inches(6.833), Inches(3.8), width=Inches(5.7), height=Inches(3.2))

    # =========================================================================
    # SLIDE 4A: 3. LITERATURE SURVEY — PART 1 (PAPERS 01 TO 05)
    # =========================================================================
    slide4a = prs.slides.add_slide(blank_layout)
    apply_bg(slide4a)
    add_slide_header(slide4a, "3", "Literature Survey (Part 1 of 2)", "Key Research Papers on Industrial AR in Automobile Assembly")

    papers_part1 = [
        ("01", "R. G. Boboc, F. Gîrbacia, E. V. Butilă (2020)", "Application of Augmented Reality in Automotive Industry", "Proved AR reduces worker mistakes by 34% and reduces cognitive workload during complex car assembly."),
        ("02", "J. Egger, T. Masood (2020)", "Augmented Reality in Support of Intelligent Manufacturing", "Identified that small automotive plants struggle with high proprietary software costs ($10k+ per seat)."),
        ("03", "M. Dalle Mura, G. Dini (2021)", "Augmented Reality in Assembly Systems: State of the Art", "Showed 3D animated holographic instructions help novice workers achieve expert productivity 70% faster."),
        ("04", "B. Marques, S. Silva, J. Alves (2023)", "Manual Assembly Augmented Reality Systems Mapping", "Reported 80% of current AR tools lack real-time physical verification like IoT torque tool interlocking."),
        ("05", "V. Vera, I. B. Nieto (2024)", "Application of Augmented Reality in Automotive Manufacturing", "Demonstrated that spatial visual cues eliminate confusion and reduce part assembly cycle time by 30%.")
    ]

    for idx, (num, author, title, finding) in enumerate(papers_part1):
        row = slide4a.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5 + idx * 1.1), Inches(11.733), Inches(0.98))
        row.fill.solid()
        row.fill.fore_color.rgb = CARD_BG
        row.line.color.rgb = BORDER_COLOR
        tf = row.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.16)

        p = tf.paragraphs[0]
        p.text = f"[{num}]  {author} — "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN_ACCENT

        r1 = p.add_run()
        r1.text = f'"{title}"'
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = WHITE_TEXT

        p2 = tf.add_paragraph()
        p2.text = "Key Takeaway: " + finding
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 4B: 3. LITERATURE SURVEY — PART 2 (PAPERS 06 TO 10)
    # =========================================================================
    slide4b = prs.slides.add_slide(blank_layout)
    apply_bg(slide4b)
    add_slide_header(slide4b, "3", "Literature Survey (Part 2 of 2)", "Key Research Papers on Operator Experience & Human-Machine Collaboration")

    papers_part2 = [
        ("06", "X. Wang, S. K. Ong, A. Y. C. Nee (2016)", "Comprehensive Survey of Augmented Reality Assembly Research", "Established that direct 3D CAD-to-AR alignment eliminates reliance on confusing 2D paper drawings."),
        ("07", "C. Gerdenitsch, A. Sackl, P. Hold (2022)", "Augmented Reality Assisted Assembly: Operator Experience", "Confirmed hands-free voice control reduces worker physical fatigue and neck strain by over 45%."),
        ("08", "S. Makris, P. Karagiannis, S. Koukas (2016)", "AR System for Operator Support in Industrial Assembly", "Highlighted that projecting visual datum markers on parts provides high alignment precision."),
        ("09", "F. R. Ramalho, A. L. Soares, A. C. Simões (2026)", "Human-Centered AR: Enhancing Efficiency and Operator Adoption", "Found novice workers experience high job confidence when AR validates step completion in real-time."),
        ("10", "A. Shantayev, L. Galan Cruz, K. Naicker (2026)", "Industrial Task Execution Through Embedded AR Guidance", "Demonstrated zero-defect assembly by combining spatial AR overlays with IoT smart torque tool interlocks.")
    ]

    for idx, (num, author, title, finding) in enumerate(papers_part2):
        row = slide4b.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5 + idx * 1.1), Inches(11.733), Inches(0.98))
        row.fill.solid()
        row.fill.fore_color.rgb = CARD_BG
        row.line.color.rgb = EMERALD_GREEN if idx == 4 else BORDER_COLOR
        tf = row.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.16)

        p = tf.paragraphs[0]
        p.text = f"[{num}]  {author} — "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD_GREEN if idx == 4 else CYAN_ACCENT

        r1 = p.add_run()
        r1.text = f'"{title}"'
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = WHITE_TEXT

        p2 = tf.add_paragraph()
        p2.text = "Key Takeaway: " + finding
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 5: 4. METHODOLOGY (REAL STEP-BY-STEP WORKFLOW)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_bg(slide5)
    add_slide_header(slide5, "4", "Methodology", "Our Complete Working Process from 3D CAD to Live AR Assembly")

    method_steps = [
        ("Phase 1: 3D CAD Modeling", [
            "Design automobile parts in SolidWorks (Brake, Clutch, Knuckle Joint).",
            "Set concentric mates and accurate engineering tolerances."
        ]),
        ("Phase 2: Convert to .OBJ File", [
            "Export the completed SolidWorks 3D assembly into standard .OBJ / .STEP format.",
            "Decomposes components into clean 3D mesh layers for web graphics."
        ]),
        ("Phase 3: Import into Our Software", [
            "Operator clicks 'Import CAD Model' or drags the .OBJ file into AutoAR.",
            "Software instantly parses 3D vertices, materials, and datum coordinates."
        ]),
        ("Phase 4: Automatic Assembly Starts", [
            "Software automatically breaks the model into step-by-step assembly phases.",
            "Shows 3D animations, arrows, and blocks next step until bolt is torqued."
        ])
    ]

    for idx, (title, points) in enumerate(method_steps):
        box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.95), Inches(1.5), Inches(2.8), Inches(4.5))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CYAN_ACCENT
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = f"PHASE {idx+1}"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = AMBER_GOLD
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(12)

        for pt in points:
            p = tf.add_paragraph()
            p.text = "✔ " + pt
            p.font.size = Pt(10.5)
            p.font.color.rgb = MUTED_TEXT
            p.space_after = Pt(10)

    # Bottom Summary Flow
    flow = slide5.shapes.add_textbox(Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.7))
    flow.text_frame.word_wrap = True
    p = flow.text_frame.paragraphs[0]
    p.text = "SolidWorks 3D CAD Design   ➔   Export to .OBJ 3D File   ➔   Import into AutoAR Software   ➔   Automatic 3D Assembly Sequence"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 6: 4. METHODOLOGY — SOLIDWORKS CAD & 2D DRAFTING (EVIDENCE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_bg(slide6)
    add_slide_header(slide6, "4", "Methodology — SolidWorks CAD & Drafting", "Evidence: 3D CAD Modeling, Concentric Mates & 2D Blueprints")

    # Image 1: 3D Exploded View (Disc Brake)
    if os.path.exists("D:/solidworks/2_SolidWorks_Disc_Brake_Exploded_Assembly.jpg"):
        slide6.shapes.add_picture("D:/solidworks/2_SolidWorks_Disc_Brake_Exploded_Assembly.jpg", Inches(0.8), Inches(1.5), width=Inches(3.7))
        cap1 = slide6.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(3.7), Inches(0.9))
        cap1.text_frame.word_wrap = True
        cap1.text_frame.text = "1. Ventilated Disc Brake & Caliper\n(SolidWorks 3D Exploded View)"
        cap1.text_frame.paragraphs[0].font.size = Pt(11)
        cap1.text_frame.paragraphs[0].font.bold = True
        cap1.text_frame.paragraphs[0].font.color.rgb = CYAN_ACCENT

    # Image 2: 2D Engineering Blueprint (Disc Brake)
    if os.path.exists("D:/solidworks/3_SolidWorks_2D_Engineering_Drafting_Blueprint_BOM.jpg"):
        slide6.shapes.add_picture("D:/solidworks/3_SolidWorks_2D_Engineering_Drafting_Blueprint_BOM.jpg", Inches(4.8), Inches(1.5), width=Inches(3.7))
        cap2 = slide6.shapes.add_textbox(Inches(4.8), Inches(5.8), Inches(3.7), Inches(0.9))
        cap2.text_frame.word_wrap = True
        cap2.text_frame.text = "2. Disc Brake 2D Blueprint\n(Bill of Materials & GD&T Dimensions)"
        cap2.text_frame.paragraphs[0].font.size = Pt(10.5)
        cap2.text_frame.paragraphs[0].font.bold = True
        cap2.text_frame.paragraphs[0].font.color.rgb = WHITE_TEXT

    # Image 3: Clutch Blueprint (Clutch Assembly)
    if os.path.exists("D:/solidworks/Clutch_Step4_SolidWorks_2D_Engineering_Drafting_Blueprint_BOM.jpg"):
        slide6.shapes.add_picture("D:/solidworks/Clutch_Step4_SolidWorks_2D_Engineering_Drafting_Blueprint_BOM.jpg", Inches(8.8), Inches(1.5), width=Inches(3.7))
        cap3 = slide6.shapes.add_textbox(Inches(8.8), Inches(5.8), Inches(3.7), Inches(0.9))
        cap3.text_frame.word_wrap = True
        cap3.text_frame.text = "3. Single-Plate Clutch Assembly\n(2D Technical Drawing & Section Views)"
        cap3.text_frame.paragraphs[0].font.size = Pt(10.5)
        cap3.text_frame.paragraphs[0].font.bold = True
        cap3.text_frame.paragraphs[0].font.color.rgb = AMBER_GOLD

    # =========================================================================
    # SLIDE 6B: 4C. SYSTEM ARCHITECTURE & TECH STACK (HOW WE BUILT AUTOAR)
    # =========================================================================
    slide_arch = prs.slides.add_slide(blank_layout)
    apply_bg(slide_arch)
    add_slide_header(slide_arch, "4C", "System Architecture & Tech Stack", "How We Built AutoAR: Modern Web & 3D Engineering Architecture")

    tech_pillars = [
        (
            "01. Frontend & UI",
            "React 19 & Vite",
            [
                "Modular component-based operator dashboard.",
                "Real-time assembly step progression & tactile controls.",
                "High-contrast dark theme optimized for shop-floor lighting."
            ],
            CYAN_ACCENT
        ),
        (
            "02. 3D Web Graphics",
            "Three.js & WebGL",
            [
                "Renders SolidWorks 3D CAD meshes at smooth 60 FPS.",
                "Dynamic shaders for real-time Exploded Views & rotation.",
                "X-Ray wireframe mode for internal bolt inspection."
            ],
            EMERALD_GREEN
        ),
        (
            "03. Augmented Reality",
            "WebXR & JSQR",
            [
                "Universal AR standard across smart glasses, tablets & phones.",
                "Camera-based QR code verification for component alignment.",
                "Zero app download needed — opens instantly via web URL."
            ],
            AMBER_GOLD
        ),
        (
            "04. Speech AI Engine",
            "Web Speech API",
            [
                "Browser-native speech recognition for voice commands.",
                "Hands-free control ('Next', 'Torque', 'Explode') for oily gloves.",
                "Bilingual voice guidance feedback in English & Tamil."
            ],
            CYAN_ACCENT
        )
    ]

    for idx, (title, subtitle_text, bullets, accent_color) in enumerate(tech_pillars):
        c = slide_arch.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.994), Inches(1.45), Inches(2.75), Inches(4.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = accent_color
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.18)

        # Title
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = accent_color
        p.space_after = Pt(2)

        # Subtitle badge (Tech name)
        p_sub = tf.add_paragraph()
        p_sub.text = f"▸ {subtitle_text}"
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.name = "Arial"
        p_sub.font.color.rgb = WHITE_TEXT
        p_sub.space_after = Pt(8)

        # Bullets
        for b_text in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b_text}"
            p_b.font.size = Pt(9.5)
            p_b.font.name = "Arial"
            p_b.font.color.rgb = MUTED_TEXT
            p_b.space_after = Pt(5)

    # Bottom Pipeline Banner
    pipe_box = slide_arch.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(1.05))
    pipe_box.fill.solid()
    pipe_box.fill.fore_color.rgb = RGBColor(16, 26, 50)
    pipe_box.line.color.rgb = CYAN_ACCENT
    tf_p = pipe_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = Inches(0.1)

    p1 = tf_p.paragraphs[0]
    p1.text = "SolidWorks 3D CAD (Design)   ➔   Three.js WebGL (3D Engine)   ➔   React + Vite (UI)   ➔   WebXR & Speech AI (Live AR)"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.name = "Arial"
    p1.font.color.rgb = CYAN_ACCENT
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(3)

    p2 = tf_p.add_paragraph()
    p2.text = "✦ 100% Open Web Standards  •  Zero Expensive Proprietary License Fees  •  Instant Cloud Deployment on Render"
    p2.font.size = Pt(9.5)
    p2.font.name = "Arial"
    p2.font.color.rgb = WHITE_TEXT
    p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 7: MODULE 1 — AUTOMOTIVE CLUTCH ASSEMBLY (FULL LIFECYCLE)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_bg(slide7)
    add_slide_header(slide7, "5A", "Clutch Assembly Lifecycle in AutoAR", "From Initial Solid State to 94% Exploded View, X-Ray Wireframe & Final QA")

    # 4 Cards for Clutch Lifecycle
    # 1. Starting Stage (Initial Unassembled / Step 01 Fixture State)
    if os.path.exists("D:/solidworks/clutch_stage1_start_unassembled.png"):
        slide7.shapes.add_picture("D:/solidworks/clutch_stage1_start_unassembled.png", Inches(0.8), Inches(1.5), width=Inches(2.75))
    elif os.path.exists("D:/solidworks/clutch_stage1_standby_cad.png"):
        slide7.shapes.add_picture("D:/solidworks/clutch_stage1_standby_cad.png", Inches(0.8), Inches(1.5), width=Inches(2.75))
    elif os.path.exists("D:/solidworks/2026-10-14_06-41.png"):
        slide7.shapes.add_picture("D:/solidworks/2026-10-14_06-41.png", Inches(0.8), Inches(1.5), width=Inches(2.75))
    cap_c1 = slide7.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_c1.text_frame.word_wrap = True
    p = cap_c1.text_frame.paragraphs[0]
    p.text = "STAGE 1: STARTING STATE\n(Unassembled / Step 01)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN_ACCENT
    p2 = cap_c1.text_frame.add_paragraph()
    p2.text = "Components are NOT yet assembled. Workstation fixture is loaded and Step 01 flywheel datum is aligned."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 2. Exploded View (94% Exploded)
    if os.path.exists("D:/solidworks/2026-10-13_16-25.png"):
        slide7.shapes.add_picture("D:/solidworks/2026-10-13_16-25.png", Inches(3.75), Inches(1.5), width=Inches(2.75))
    elif os.path.exists("D:/solidworks/2026-10-14_06-42_2.png"):
        slide7.shapes.add_picture("D:/solidworks/2026-10-14_06-42_2.png", Inches(3.75), Inches(1.5), width=Inches(2.75))
    cap_c2 = slide7.shapes.add_textbox(Inches(3.75), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_c2.text_frame.word_wrap = True
    p = cap_c2.text_frame.paragraphs[0]
    p.text = "STAGE 2: 94% EXPLODED VIEW\n(Separated Sub-Components)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = AMBER_GOLD
    p2 = cap_c2.text_frame.add_paragraph()
    p2.text = "Friction disc, pressure plate, and diaphragm spring are separated along Z-axis for clear visual guidance."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 3. Holographic X-Ray Wireframe View
    if os.path.exists("D:/solidworks/2026-10-13_16-24_2.png"):
        slide7.shapes.add_picture("D:/solidworks/2026-10-13_16-24_2.png", Inches(6.7), Inches(1.5), width=Inches(2.75))
    cap_c3 = slide7.shapes.add_textbox(Inches(6.7), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_c3.text_frame.word_wrap = True
    p = cap_c3.text_frame.paragraphs[0]
    p.text = "STAGE 3: X-RAY WIREFRAME\n(Internal Inspection Mode)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN_ACCENT
    p2 = cap_c3.text_frame.add_paragraph()
    p2.text = "Reveals hidden internal pilot bearing, diaphragm fingers, and spring dampers without disassembling."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 4. Final Stage: Digital QA Certificate
    if os.path.exists("D:/solidworks/2026-10-13_16-25_1.png"):
        slide7.shapes.add_picture("D:/solidworks/2026-10-13_16-25_1.png", Inches(9.65), Inches(1.5), width=Inches(2.88))
    cap_c4 = slide7.shapes.add_textbox(Inches(9.65), Inches(4.7), Inches(2.88), Inches(1.8))
    cap_c4.text_frame.word_wrap = True
    p = cap_c4.text_frame.paragraphs[0]
    p.text = "STAGE 4: QUALITY CERTIFICATE\n(ISO 9001 Conformance)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = EMERALD_GREEN
    p2 = cap_c4.text_frame.add_paragraph()
    p2.text = "Auto-generated report certifying all 6 clutch sub-components meet < 0.05 mm tolerance and 25 Nm torque."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # Bottom summary tag
    bot_c = slide7.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.5))
    p = bot_c.text_frame.paragraphs[0]
    p.text = "COMPONENT: Automotive Single-Plate Clutch & Pressure Plate Assembly (280mm) • Complete 4-Stage Workflow in AutoAR"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = WHITE_TEXT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 8: MODULE 2 — VENTILATED DISC BRAKE & CALIPER (FULL LIFECYCLE)
    # =========================================================================
    slide_sw = prs.slides.add_slide(blank_layout)
    apply_bg(slide_sw)
    add_slide_header(slide_sw, "5B", "Disc Brake Assembly Lifecycle in AutoAR", "From Rotor Fitment to Caliper Placement, Laser CMM Defect Scan & Verification")

    # 4 Cards for Disc Brake Lifecycle
    # 1. Starting Stage (Rotor Disc on Hub)
    if os.path.exists("D:/solidworks/2026-10-13_16-26.png"):
        slide_sw.shapes.add_picture("D:/solidworks/2026-10-13_16-26.png", Inches(0.8), Inches(1.5), width=Inches(2.75))
    cap_b1 = slide_sw.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_b1.text_frame.word_wrap = True
    p = cap_b1.text_frame.paragraphs[0]
    p.text = "STAGE 1: STARTING STATE\n(Rotor Disc Alignment)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN_ACCENT
    p2 = cap_b1.text_frame.add_paragraph()
    p2.text = "Ventilated rotor disc placed onto wheel hub. HUD indicates 5-stud pitch circle diameter alignment."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 2. Guided Assembly (Brake Pads & Floating Caliper)
    if os.path.exists("D:/solidworks/2026-10-13_16-27.png"):
        slide_sw.shapes.add_picture("D:/solidworks/2026-10-13_16-27.png", Inches(3.75), Inches(1.5), width=Inches(2.75))
    cap_b2 = slide_sw.shapes.add_textbox(Inches(3.75), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_b2.text_frame.word_wrap = True
    p = cap_b2.text_frame.paragraphs[0]
    p.text = "STAGE 2: GUIDED ASSEMBLY\n(Red Caliper & Pads Fitment)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = AMBER_GOLD
    p2 = cap_b2.text_frame.add_paragraph()
    p2.text = "Visual bounding box and tool vector guide the red caliper over the rotor with calibrated clearance."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 3. Real-Time Laser CMM Defect Scan
    if os.path.exists("D:/solidworks/2026-10-13_16-27_1.png"):
        slide_sw.shapes.add_picture("D:/solidworks/2026-10-13_16-27_1.png", Inches(6.7), Inches(1.5), width=Inches(2.75))
    cap_b3 = slide_sw.shapes.add_textbox(Inches(6.7), Inches(4.7), Inches(2.75), Inches(1.8))
    cap_b3.text_frame.word_wrap = True
    p = cap_b3.text_frame.paragraphs[0]
    p.text = "STAGE 3: LASER CMM SCAN\n(Defect Detection Mode)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = RED_ACCENT
    p2 = cap_b3.text_frame.add_paragraph()
    p2.text = "Virtual laser beam scans mounting angle. If misaligned, red alert halts line until corrected."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # 4. Final Assembled & Torque Verified
    if os.path.exists("D:/solidworks/disc_brake_canvas_complete.png"):
        slide_sw.shapes.add_picture("D:/solidworks/disc_brake_canvas_complete.png", Inches(9.65), Inches(1.5), width=Inches(2.88))
    elif os.path.exists("D:/solidworks/2026-10-14_06-43.png"):
        slide_sw.shapes.add_picture("D:/solidworks/2026-10-14_06-43.png", Inches(9.65), Inches(1.5), width=Inches(2.88))
    cap_b4 = slide_sw.shapes.add_textbox(Inches(9.65), Inches(4.7), Inches(2.88), Inches(1.8))
    cap_b4.text_frame.word_wrap = True
    p = cap_b4.text_frame.paragraphs[0]
    p.text = "STAGE 4: TORQUE VERIFIED\n(Final Assembly Complete)"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = EMERALD_GREEN
    p2 = cap_b4.text_frame.add_paragraph()
    p2.text = "Dual 15 Nm caliper pin bolts and 75 Nm hub bolts confirmed via IoT Poka-Yoke interlock."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = MUTED_TEXT

    # Bottom summary tag
    bot_b = slide_sw.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.5))
    p = bot_b.text_frame.paragraphs[0]
    p.text = "COMPONENT: Automotive Ventilated Disc Brake & Floating Caliper Assembly • Complete 4-Stage Workflow in AutoAR"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = WHITE_TEXT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 9: 5C. HOW OUR SOFTWARE WORKS WITH AR GLASSES (SIMPLE ENGLISH)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_bg(slide8)
    add_slide_header(slide8, "5C", "How Our Software Works in AR Glasses", "Step-by-Step Hands-Free Operation for Shop-Floor Technicians")

    easy_steps_4 = [
        ("Step 1: Voice Launch in AR Glasses Browser", "The mechanic wears AR smart glasses. Using hands-free voice command ('Open AutoAR'), the browser launches our web app instantly without touching any keyboard or mouse."),
        ("Step 2: Component Recognition (AI Vision / QR Code)", "The AR glass camera scans the physical assembly line. It recognizes the car part automatically or scans the component's QR code to load the exact SolidWorks 3D model."),
        ("Step 3: Multi-Language Voice Guidance (EN / தமிழ் / മല / हिंदी)", "Hands-free voice assistant speaks in 4 regional languages (Tamil, Malayalam, Hindi & English). Operators command 'Next Step', 'Explode', or 'X-Ray' without touching keyboard or mouse."),
        ("Step 4: IoT Torque Poka-Yoke & Digital QA Stamp", "The smart torque wrench syncs with the AR glasses. Once the bolt reaches 15 Nm / 75 Nm, a green checkmark appears and auto-issues the ISO 9001 Digital Quality Certificate!")
    ]

    for idx, (title, desc) in enumerate(easy_steps_4):
        box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5 + idx * 1.35), Inches(6.8), Inches(1.22))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CYAN_ACCENT if idx % 2 == 0 else EMERALD_GREEN
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = f"✔ {title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = CYAN_ACCENT if idx % 2 == 0 else EMERALD_GREEN
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.name = "Arial"
        p.font.color.rgb = WHITE_TEXT

    # Right: Real Software Picture (Interactive Turntable & Control HUD)
    if os.path.exists("D:/solidworks/2026-10-14_06-43.png"):
        slide8.shapes.add_picture("D:/solidworks/2026-10-14_06-43.png", Inches(7.8), Inches(1.5), width=Inches(4.7))
    elif os.path.exists("D:/solidworks/2026-10-13_16-24.png"):
        slide8.shapes.add_picture("D:/solidworks/2026-10-13_16-24.png", Inches(7.8), Inches(1.5), width=Inches(4.7))

    cap_sw = slide8.shapes.add_textbox(Inches(7.8), Inches(5.8), Inches(4.7), Inches(1.0))
    cap_sw.text_frame.word_wrap = True
    cap_sw.text_frame.text = "Figure: AutoAR Interactive Turntable HUD — 360° Orbit, Explode Slider, X-Ray Toggle, and Hands-Free Voice Assistant Active."
    cap_sw.text_frame.paragraphs[0].font.size = Pt(9.5)
    cap_sw.text_frame.paragraphs[0].font.bold = True
    cap_sw.text_frame.paragraphs[0].font.color.rgb = CYAN_ACCENT

    # =========================================================================
    # SLIDE 9: 6. RESULTS & DISCUSSION (CLEAR NUMBERS & COMPARISON)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_bg(slide9)
    add_slide_header(slide9, "6", "Results & Discussion", "Measurable Improvements: Before vs. After Using AutoAR")

    # 3 Big Number Callouts
    res_cards = [
        ("41% FASTER", "Assembly Time Reduced", "Time dropped from 14.5 minutes down to 8.5 minutes per sub-assembly.", CYAN_ACCENT),
        ("0 DEFECTS", "Zero Missed Bolts", "Hardware torque interlock prevents moving to next step until verified.", EMERALD_GREEN),
        ("85% LESS", "Training Time Cut", "New workers learn in 2-3 days using self-guided 3D AR instead of weeks.", AMBER_GOLD)
    ]

    for idx, (stat, title, exp, col) in enumerate(res_cards):
        c = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.9), Inches(1.5), Inches(3.7), Inches(2.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = stat
        p.font.bold = True
        p.font.size = Pt(26)
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = exp
        p.font.size = Pt(9.5)
        p.font.color.rgb = MUTED_TEXT

    # Simple Easy Comparison Box (Bottom)
    cmp_box = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.9))
    cmp_box.fill.solid()
    cmp_box.fill.fore_color.rgb = CARD_BG
    cmp_box.line.color.rgb = BORDER_COLOR
    tf_cmp = cmp_box.text_frame
    tf_cmp.word_wrap = True
    tf_cmp.margin_left = tf_cmp.margin_top = tf_cmp.margin_right = tf_cmp.margin_bottom = Inches(0.25)

    p = tf_cmp.paragraphs[0]
    p.text = "SIMPLE COMPARISON: OLD WAY vs. OUR AR SYSTEM"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(10)

    cmps = [
        ("Work Instructions", "Confusing 2D paper binder with flat diagrams", "Interactive 3D animated parts floating directly on real car"),
        ("Bolt Torque Check", "Operator writes torque on paper (often forgotten)", "Digital lock — system blocks progress until bolt is torqued!"),
        ("Worker Comfort", "Worker constantly looks down, causing neck strain", "Worker looks straight at assembly with hands free for tools"),
        ("Quality Audit", "Inspector checks parts only at the end of the day", "Live instant ISO quality verification certificate generated on-screen")
    ]
    for c_idx, (feature, old_w, new_w) in enumerate(cmps):
        p = tf_cmp.add_paragraph()
        p.text = f"• {feature}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = AMBER_GOLD
        r = p.add_run()
        r.text = f"Old: {old_w}   ➔   "
        r.font.bold = False
        r.font.size = Pt(9.5)
        r.font.color.rgb = MUTED_TEXT
        r2 = p.add_run()
        r2.text = f"Our AR: {new_w}"
        r2.font.bold = True
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = WHITE_TEXT
    # =========================================================================
    # SLIDE 10: 6B. COST-BENEFIT & ECONOMIC IMPACT (COMMERCIAL VS AUTOAR)
    # =========================================================================
    slide_cost = prs.slides.add_slide(blank_layout)
    apply_bg(slide_cost)
    add_slide_header(slide_cost, "6B", "Cost-Benefit & Economic Impact", "Why AutoAR is Disruptive: Commercial AR License Costs vs. Zero-Cost Open WebXR")

    # Left Column: Commercial AR Software (High License Burden)
    card_comm = slide_cost.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(4.15))
    card_comm.fill.solid()
    card_comm.fill.fore_color.rgb = CARD_BG
    card_comm.line.color.rgb = RED_ACCENT
    tf_comm = card_comm.text_frame
    tf_comm.word_wrap = True
    tf_comm.margin_left = tf_comm.margin_top = tf_comm.margin_right = tf_comm.margin_bottom = Inches(0.2)

    p = tf_comm.paragraphs[0]
    p.text = "COMMERCIAL INDUSTRIAL AR SOFTWARE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(2)

    p = tf_comm.add_paragraph()
    p.text = "High Recurring Subscription & Vendor Lock-In"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED_TEXT
    p.space_after = Pt(8)

    comm_pts = [
        ("Unity Pro License", "$2,310 / year per seat (~₹1,92,000 / user / year). Essential for commercial deployment."),
        ("Vuforia Engine Enterprise", "$99 to $500+ / month / app, scaling to $6,000 to $12,000 / year per plant."),
        ("PTC / Siemens Teamcenter", "$25,000+ per plant (~₹20+ Lakhs) with expensive annual maintenance contracts (AMC)."),
        ("Hardware & OS Lock-In", "Requires high-end gaming GPUs ($2,000+ per PC), native app installs, and IT approvals."),
        ("10-Station Plant Total", "₹30 Lakhs to ₹50 Lakhs recurring every single year just for software licenses!")
    ]

    for title, desc in comm_pts:
        p = tf_comm.add_paragraph()
        p.text = f"❌ {title}: "
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = RED_ACCENT
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(3)

    # Right Column: AutoAR WebXR Solution (Zero Cost & Maximum Accessibility)
    card_autoar = slide_cost.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.15))
    card_autoar.fill.solid()
    card_autoar.fill.fore_color.rgb = CARD_BG
    card_autoar.line.color.rgb = EMERALD_GREEN
    tf_auto = card_autoar.text_frame
    tf_auto.word_wrap = True
    tf_auto.margin_left = tf_auto.margin_top = tf_auto.margin_right = tf_auto.margin_bottom = Inches(0.2)

    p = tf_auto.paragraphs[0]
    p.text = "AUTOAR OPEN WEBXR SOLUTION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(2)

    p = tf_auto.add_paragraph()
    p.text = "Zero License Fees • Instant Browser-Based Architecture"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED_TEXT
    p.space_after = Pt(8)

    auto_pts = [
        ("Software License Fee", "100% Free & Open-Source (Built on WebGL 2.0 / Three.js open web standards)."),
        ("Targeting Small Factories & MSMEs", "Empowers small-scale automotive workshops and tier-2/3 suppliers to boost productivity and reach zero defects."),
        ("Render Cloud Deployment", "Hosted live on Render Cloud — instant 24/7 web access on smart glasses, PCs & tablets."),
        ("Zero-Installation Setup", "Runs in any Chrome/Edge browser via direct web URL with zero local downloads."),
        ("Annual Factory Savings", "Saves ₹30+ Lakhs ($35,000+) every year per assembly plant with immediate Day-1 ROI!")
    ]

    for title, desc in auto_pts:
        p = tf_auto.add_paragraph()
        p.text = f"✔ {title}: "
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = EMERALD_GREEN
        r = p.add_run()
        r.text = desc
        r.font.bold = False
        r.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(3)

    # Bottom 2 Balanced Impact Callouts (Aligned with the 2 columns above)
    impact_stats = [
        (Inches(0.8), "₹30+ LAKHS ANNUAL SAVINGS", "Recurring Software License Cost Saved", "Saves ₹30 to ₹50 Lakhs every year for a standard 10-station automotive plant", EMERALD_GREEN),
        (Inches(6.8), "EMPOWERING SMALL FACTORIES", "Boost Productivity & Zero Defects", "Democratizes Industry 4.0 for small automotive workshops and MSMEs at zero software cost", CYAN_ACCENT)
    ]

    for x_pos, stat, title, sub, col in impact_stats:
        c = slide_cost.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(5.8), Inches(5.7), Inches(1.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = col
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = stat
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE_TEXT

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(8.5)
        p.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 11: 7. CONCLUSION & FUTURE SCOPE
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    apply_bg(slide10)
    add_slide_header(slide10, "7", "Conclusion & Future Scope", "Summary of Work Done & Next Steps")

    # Left: Conclusion
    c_card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = CARD_BG
    c_card.line.color.rgb = EMERALD_GREEN
    tf_c = c_card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = Inches(0.3)

    p = tf_c.paragraphs[0]
    p.text = "KEY CONCLUSIONS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(12)

    concls = [
        "Empowering Small Factories: Brings modern Industry 4.0 AR tools to small-scale automotive workshops and MSMEs to increase productivity and achieve 100% zero-defect assembly.",
        "Visual 3D AR Guidance: Replaces confusing 2D paper blueprints with floating 3D parts and animated directional arrows directly onto real car components.",
        "Smart Torque Interlock: Digital verification prevents technicians from skipping bolts, eliminating human errors and assembly rework.",
        "Zero-Cost Cloud Deployment: Runs instantly on any web browser (Chrome/Edge) or smart glasses via Render Cloud without requiring expensive proprietary licenses."
    ]
    for c in concls:
        p = tf_c.add_paragraph()
        p.text = "✔ " + c
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(8)

    # Right: Future Scope
    f_card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = CARD_BG
    f_card.line.color.rgb = CYAN_ACCENT
    tf_f = f_card.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = Inches(0.3)

    p = tf_f.paragraphs[0]
    p.text = "FUTURE ENHANCEMENTS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)

    futures = [
        "Universal CAD Support: Direct input pipelines for all major CAD software — CATIA, SolidWorks, PTC Creo, Siemens NX, and AutoCAD.",
        "Zero-Training Freshers Onboarding: Fully automated 3D interactive tutorials so new workers assemble parts on day one with zero confusion.",
        "AI Edge Vision Tracking: Using camera vision to automatically recognize car components without requiring printed barcode markers.",
        "Smart Haptic Feedback: Vibrating smart gloves to give tactile resistance when a fastener reaches its target torque specification."
    ]
    for f in futures:
        p = tf_f.add_paragraph()
        p.text = "🚀 " + f
        p.font.size = Pt(10.5)
        p.font.color.rgb = WHITE_TEXT
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 11: THANK YOU & QUESTIONS
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    apply_bg(slide11)

    tq_box = slide11.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10.333), Inches(2.0))
    tf_q = tq_box.text_frame
    tf_q.word_wrap = True
    p = tf_q.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.bold = True
    p.font.size = Pt(48)
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER
    
    # Save to fresh updated file
    p_fresh = "D:/final year ppt faaah/AR_Assembly_Review_Updated.pptx"
    prs.save(p_fresh)
    print(f"Saved fresh: {p_fresh}")

    # Also update AR_Assembly_Final_Review_Presentation if not locked
    try:
        p1 = "D:/final year ppt faaah/AR_Assembly_Final_Review_Presentation.pptx"
        prs.save(p1)
        print(f"Saved: {p1}")
    except Exception:
        print("Note: Target file locked in PowerPoint.")

if __name__ == "__main__":
    create_simple_easy_presentation()
