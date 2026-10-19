import os
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"D:\seminar iot\Industrial_Visit_Report_Hatsun_STEPHY_BELCITTA.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # We don't draw running header/footer on page 1 (Front Cover Page)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))

        # Header Text & Rule
        self.drawString(54, 795, "INDUSTRIAL VISIT REPORT — HATSUN AGRO PRODUCT (NANGUNERI)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(541, 795, "STEPHY BELCITTA P (Roll No: 878)")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 788, 541, 788)

        # Footer Text & Rule
        self.line(54, 45, 541, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 32, "Department of Microbiology | Scott Christian College (Autonomous), Nagercoil")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()

def build_pdf():
    # A4: 595.27 x 841.89 points
    # Margins: 54 pt (0.75 in) Left/Right, 58 pt Top, 54 pt Bottom
    # Usable width: 487.27 pt
    # Usable height: 729.89 pt
    
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=58,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom styles
    title_cover = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        alignment=1, # Center
        textColor=colors.HexColor('#0F294A')
    )

    date_cover = ParagraphStyle(
        'CoverDate',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#334155')
    )

    meta_cover = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        alignment=1,
        textColor=colors.HexColor('#1E293B')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F294A'),
        spaceBefore=0,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.2,
        leading=13.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        alignment=4, # Justified
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12.2,
        alignment=4,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3.5
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=colors.white
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )

    story = []

    # =========================================================================
    # PAGE 1: FRONT COVER PAGE (EXACT TEMPLATE MATCH)
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("INDUSTRIAL VISIT TO HATSUN<br/>AGRO PRODUCT NANGUNERI", title_cover))
    story.append(Spacer(1, 28))
    story.append(Paragraph("22 September 2026", date_cover))
    story.append(Spacer(1, 45))
    story.append(Paragraph("A REPORT", ParagraphStyle('ReportHeader', parent=title_cover, fontSize=18, leading=22, textColor=colors.HexColor('#0F294A'))))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Submitted by", ParagraphStyle('SubBy', parent=meta_cover, fontName='Helvetica-Oblique', fontSize=12, leading=16)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>STEPHY BELCITTA P</b>", ParagraphStyle('StudentName', parent=meta_cover, fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#0F294A'))))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>I B.Sc. Microbiology</b>", meta_cover))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Class No: 878</b>", ParagraphStyle('ClassNo', parent=meta_cover, fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#1E3A8A'))))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Department of Microbiology<br/><b>Scott Christian College (Autonomous)</b><br/>Nagercoil – 629 003, Tamil Nadu", meta_cover))
    
    story.append(Spacer(1, 45))
    # Elegant decorative box for Cover Page Footer
    cover_box_data = [[
        Paragraph("<para align='center'><b>Educational Industrial Visit Record</b><br/><font size='8' color='#475569'>Comprehensive Study of Modern Dairy Processing, Cold Chain Logistics, Industrial Microbiology, and Quality Assurance Protocols at Hatsun Agro Product Ltd., Nanguneri Plant.</font></para>", table_cell)
    ]]
    t_cover_box = Table(cover_box_data, colWidths=[460])
    t_cover_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(t_cover_box)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & TABLE OF CONTENTS (NO CERTIFICATE)
    # =========================================================================
    story.append(Paragraph("EXECUTIVE SUMMARY & REPORT PREAMBLE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p2_preamble = (
        "This industrial visit report documents the academic study and technical observations conducted during an on-site visit to the "
        "<b>Hatsun Agro Product Limited</b> dairy processing plant situated at Nanguneri, Tirunelveli District, Tamil Nadu, on "
        "<b>22 September 2026</b>. As part of the undergraduate curriculum in Microbiology at <b>Scott Christian College (Autonomous)</b>, "
        "this investigation bridges theoretical classroom concepts—such as microbial thermal kinetics, pasteurization verification assays, "
        "and pathogen control—with modern automated dairy engineering practices.<br/><br/>"
        "The report follows the complete dairy value chain from decentralized village milk collection and rapid bulk chilling, "
        "through raw intake platform diagnostics, high-temperature short-time (HTST) pasteurization, pressure homogenization, "
        "and automated Form-Fill-Seal (FFS) packaging, to refrigerated cold chain logistics and Clean-in-Place (CIP) sanitation engineering."
    )
    story.append(Paragraph(p2_preamble, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceAfter=6))

    toc_data = [
        [Paragraph("<b>Sec</b>", table_header), Paragraph("<b>Chapter / Section Title</b>", table_header), Paragraph("<b>Page</b>", table_header)],
        [Paragraph("—", table_cell), Paragraph("Title Cover Page (Industrial Visit Record Particulars)", table_cell), Paragraph("1", table_cell)],
        [Paragraph("—", table_cell), Paragraph("Executive Summary & Comprehensive Table of Contents", table_cell), Paragraph("2", table_cell)],
        [Paragraph("1.0", table_cell), Paragraph("Introduction, Objectives & Indian Dairy Sector Context", table_cell), Paragraph("3", table_cell)],
        [Paragraph("2.0", table_cell), Paragraph("Company Profile: Hatsun Agro Product Limited (HAP)", table_cell), Paragraph("4", table_cell)],
        [Paragraph("3.0", table_cell), Paragraph("The Nanguneri Processing Plant: Infrastructure & Zonal Layout", table_cell), Paragraph("5", table_cell)],
        [Paragraph("4.0", table_cell), Paragraph("Grassroots Procurement: Village Collection & Cold Chain Initiation", table_cell), Paragraph("6", table_cell)],
        [Paragraph("5.0", table_cell), Paragraph("Raw Milk Reception & Pre-Processing Clarification", table_cell), Paragraph("7", table_cell)],
        [Paragraph("6.0", table_cell), Paragraph("Core Dairy Thermal Processing: HTST Pasteurization & Homogenization", table_cell), Paragraph("8", table_cell)],
        [Paragraph("7.0", table_cell), Paragraph("Manufacturing of Value-Added Dairy Products", table_cell), Paragraph("9", table_cell)],
        [Paragraph("8.0", table_cell), Paragraph("Automated Packaging, UV Sterilization & Date-Coding", table_cell), Paragraph("10", table_cell)],
        [Paragraph("9.0", table_cell), Paragraph("Refrigerated Cold Chain & Multi-Tier Distribution Architecture", table_cell), Paragraph("11", table_cell)],
        [Paragraph("10.0", table_cell), Paragraph("Industrial Microbiology & Multi-Stage Quality Assurance Protocols", table_cell), Paragraph("12", table_cell)],
        [Paragraph("11.0", table_cell), Paragraph("Sanitation Engineering, Clean-in-Place (CIP) & FSSAI / HACCP Compliance", table_cell), Paragraph("13", table_cell)],
        [Paragraph("12.0", table_cell), Paragraph("Socio-Economic Impact, Automation, Effluent Treatment (ETP) & Green Initiatives", table_cell), Paragraph("14", table_cell)],
        [Paragraph("13.0", table_cell), Paragraph("Key Student Learning Outcomes, Recommendations & Formal Conclusion", table_cell), Paragraph("15", table_cell)],
    ]
    t_toc = Table(toc_data, colWidths=[35, 410, 35])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F294A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: INTRODUCTION, OBJECTIVES & INDUSTRY CONTEXT
    # =========================================================================
    story.append(Paragraph("1.0 INTRODUCTION & CONTEXTUAL OVERVIEW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p3_intro = (
        "Milk represents one of nature’s most complete and nutritionally dense liquid biological foods, comprising "
        "essential proteins (casein, lactalbumin, lactoglobulin), emulsified butterfats, bioavailable lactose carbohydrates, "
        "and critical micronutrients including calcium, potassium, and vitamins. However, its high water activity (aw ≈ 0.99) "
        "and near-neutral pH (6.6 – 6.8) render fresh bovine milk exceptionally vulnerable to rapid microbial spoilage "
        "and enzymatic deterioration when exposed to ambient tropical temperatures. India stands as the world's undisputed "
        "leader in raw milk production, yet over 75% of milk originates from millions of small and marginal farmers owning "
        "only 2 to 5 milch animals. The foundational success of modern organized dairying lies in engineering a seamless, "
        "unbroken cold chain that captures raw milk within minutes of harvest, prevents bacterial proliferation, and transforms "
        "it into pathogen-free, long-life consumer commodities. The Nanguneri facility of Hatsun Agro Product Limited serves as a "
        "world-class operational benchmark for this end-to-end industrial model."
    )
    story.append(Paragraph(p3_intro, body_style))

    story.append(Paragraph("1.1 Specific Objectives of the Industrial Study", h2_style))
    objs = [
        "<b>Investigate Industrial Milk Processing:</b> To examine each physical and thermodynamic transformation of milk, including centrifugation, homogenization, high-temperature short-time (HTST) pasteurization, and aseptic packaging.",
        "<b>Analyze Grassroots Procurement Architecture:</b> To evaluate how rural Automatic Milk Collection Units (AMCUs) and Bulk Milk Coolers (BMCs) maintain microbial stability across thousands of decentralized village supply points.",
        "<b>Correlate Theoretical Microbiology with Plant Practice:</b> To bridge academic knowledge of dairy bacteriology, pathogen kinetics (<i>Salmonella</i>, <i>Listeria</i>, <i>E. coli</i>), and thermal death time (D & z values) with plant operations.",
        "<b>Observe Analytical Laboratory Quality Gates:</b> To document raw intake platform testing, adulteration screening, antibiotic residue detection, somatic cell quantification, and finished-product organoleptic evaluations.",
        "<b>Examine Cold Chain Logistics & Regulatory Standards:</b> To study insulated bulk transport logistics, HACCP (Hazard Analysis Critical Control Point) execution, and adherence to statutory FSSAI and ISO 22000 mandates."
    ]
    for obj in objs:
        story.append(Paragraph(f"• {obj}", bullet_style))

    story.append(Paragraph("1.2 Study Methodology & Observational Scope", h2_style))
    p3_meth = (
        "The observational methodology for this industrial report combined guided walk-throughs of plant operational units, "
        "demonstrations by senior production executives and dairy microbiologists, inspection of on-site central analytical "
        "laboratories, and review of secondary data from Hatsun Agro Product's technical manuals and FSSAI regulatory compendiums. "
        "This multi-disciplinary analysis places special emphasis on food safety, microbial quality gates, and process hygiene."
    )
    story.append(Paragraph(p3_meth, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: COMPANY PROFILE: HATSUN AGRO PRODUCT LIMITED
    # =========================================================================
    story.append(Paragraph("2.0 COMPANY PROFILE: HATSUN AGRO PRODUCT LIMITED (HAP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p4_comp = (
        "Hatsun Agro Product Limited (HAP) is recognized as India's largest private-sector dairy corporation, headquartered "
        "in Chennai, Tamil Nadu. Established in 1970 by visionary industrialist Mr. R. G. Chandramogan as a modest ice cream "
        "enterprise, the company underwent strategic vertical integration to evolve into an agricultural dairy powerhouse. "
        "Today, HAP procures milk directly from over 400,000 enrolled dairy farmers daily across Tamil Nadu, Andhra Pradesh, "
        "Karnataka, Telangana, and Maharashtra, operating entirely without middle-tier commission agents."
    )
    story.append(Paragraph(p4_comp, body_style))

    story.append(Paragraph("2.1 Strategic Brand Portfolio & Product Architecture", h2_style))
    brands = [
        "<b>Arokya Milk & Curd:</b> The flagship household brand across South India, renowned for stringent purity benchmarks, natural nutrient retention, and standardized fat content customized for family nutrition.",
        "<b>Hatsun Dairy Range:</b> Premium table butter, pure clarified cow ghee, dairy whitener, standardized curd, paneer, and cooking ingredients produced via automated continuous lines.",
        "<b>Arun Icecreams:</b> One of South India's pioneer commercial ice cream brands, supported by extensive deep-freeze retail distribution networks in urban and rural sectors.",
        "<b>ibaco:</b> High-end artisanal scoop ice cream parlours offering customized frozen yogurt, fruit-infused desserts, and premium dairy confectionery across metro hubs.",
        "<b>Oyalo:</b> Ready-to-eat culinary snacks and nutritional grain-dairy preparations leveraging modern thermal preservation packaging."
    ]
    for b in brands:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(Spacer(1, 4))
    if os.path.exists("d:/seminar iot/assets/product_portfolio.png"):
        story.append(Image("d:/seminar iot/assets/product_portfolio.png", width=460, height=140))
        story.append(Paragraph("Figure 2.1: Estimated Product Volume Processing Share across Primary Manufacturing Lines.", caption_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.2 Integrated Direct-to-Farmer Procurement Ecosystem", h2_style))
    p4_farm = (
        "Unlike conventional cooperative or contractor-driven dairy procurement systems, Hatsun's direct procurement model "
        "disburses bi-monthly payments directly into individual farmer bank accounts based upon digital milk analyzer readouts. "
        "This transparent ecosystem eliminates middleman deductions, provides free veterinary clinical care, animal feed supplements "
        "(Santosa Cattle Feed), and artificial insemination services, securing unmatched supply chain resilience."
    )
    story.append(Paragraph(p4_farm, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: THE NANGUNERI PROCESSING PLANT
    # =========================================================================
    story.append(Paragraph("3.0 THE NANGUNERI PROCESSING PLANT: ARCHITECTURE & ROLE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p5_nang = (
        "The Hatsun Agro Product milk processing facility located at Nanguneri in Tirunelveli district, Tamil Nadu, represents "
        "a critical strategic node in South India's dairy infrastructure. Situated within an agrarian livestock heartland, the plant "
        "acts as a high-throughput processing terminal converting milk harvested from thousands of village households into pasteurized "
        "liquid pouch milk and commercial dairy products. Operating on the principle of hygienic zonal separation, the architectural "
        "design guarantees that raw milk intake, chemical processing halls, aseptic packaging bays, and finished-product cold stores "
        "never share intersecting air currents or manual traffic routes, thereby eliminating cross-contamination risks."
    )
    story.append(Paragraph(p5_nang, body_style))

    story.append(Paragraph("3.1 Plant Functional Zones & Technical Layout", h2_style))
    
    zone_data = [
        [Paragraph("<b>Zone Code</b>", table_header), Paragraph("<b>Plant Department / Operational Sector</b>", table_header), Paragraph("<b>Key Functions & Equipment Installed</b>", table_header)],
        [Paragraph("<b>Zone A</b>", table_cell), Paragraph("<b>Raw Milk Reception Dock (RMRD)</b>", table_cell), Paragraph("Tanker unloading bays, flow meters, deaerators, reception chillers, CIP stations, laboratory intake sampling port.", table_cell)],
        [Paragraph("<b>Zone B</b>", table_cell), Paragraph("<b>Silo Storage Yard</b>", table_cell), Paragraph("Vertical insulated stainless steel silos (AISI 316) maintaining raw and pasteurized milk reserves at 3°C – 4°C.", table_cell)],
        [Paragraph("<b>Zone C</b>", table_cell), Paragraph("<b>Core Processing Hall</b>", table_cell), Paragraph("Centrifugal clarifiers, cream separators, continuous HTST plate pasteurizers, high-pressure homogenizers.", table_cell)],
        [Paragraph("<b>Zone D</b>", table_cell), Paragraph("<b>Aseptic Packaging Hall</b>", table_cell), Paragraph("Automated Form-Fill-Seal (FFS) multi-track pouch packing machines operating under HEPA-filtered clean air.", table_cell)],
        [Paragraph("<b>Zone E</b>", table_cell), Paragraph("<b>Finished Cold Storage</b>", table_cell), Paragraph("Heavy-duty blast-cooled dispatch chambers held at 2°C – 4°C with FIFO motorized roller crate handling.", table_cell)],
        [Paragraph("<b>Zone F</b>", table_cell), Paragraph("<b>Central Quality Control Laboratory</b>", table_cell), Paragraph("Microbiology culture hoods, Gerber centrifuges, spectrophotometers, FTIR milk analyzers, incubator suites.", table_cell)],
        [Paragraph("<b>Zone G</b>", table_cell), Paragraph("<b>Utilities & Environmental Station</b>", table_cell), Paragraph("Steam boilers, ammonia refrigeration compressors, RO water plants, Effluent Treatment Plant (ETP).", table_cell)],
    ]
    t_zone = Table(zone_data, colWidths=[55, 140, 290])
    t_zone.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F294A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ]))
    story.append(t_zone)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Strategic Geographical Advantages of Nanguneri", h2_style))
    p5_geo = (
        "<b>Proximity to Cattle Husbandry Belts:</b> Nanguneri is surrounded by intensive pastoral communities across Tirunelveli, "
        "Tenkasi, and Kanyakumari districts, minimizing average farm-to-chiller transit to under 45 minutes.<br/>"
        "<b>Multi-District Logistics Corridor:</b> Immediate connectivity to National Highway 44 (NH-44) facilitates rapid dispatch "
        "of night delivery reefer trucks to Madurai, Thoothukudi, Nagercoil, and southern Kerala markets before daybreak.<br/>"
        "<b>Regional Employment & Rural Industrialization:</b> The plant generates hundreds of skilled technician, laboratory analyst, "
        "and logistics jobs while sustaining over 20,000 smallholder farming incomes."
    )
    story.append(Paragraph(p5_geo, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MILK COLLECTION FROM THOUSANDS OF FARMERS
    # =========================================================================
    story.append(Paragraph("4.0 GRASSROOTS PROCUREMENT & COLD CHAIN INITIATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p6_coll = (
        "The collection stage constitutes the single most vulnerable link in the dairy supply chain. Fresh raw milk exits the "
        "bovine udder at approximately 37°C — a temperature ideal for rapid bacterial reproduction. Under ambient conditions, "
        "mesophilic bacteria double in population every 20 minutes, converting lactose into lactic acid, triggering enzymatic "
        "spoilage, and precipitating casein curdling. To prevent this deterioration, Hatsun has engineered a rigorous two-tier "
        "procurement model: Village Milk Collection Centers (MCCs) paired with Bulk Milk Chilling Centers (BMCs)."
    )
    story.append(Paragraph(p6_coll, body_style))

    story.append(Paragraph("4.1 Operational Architecture of Village Collection Centers", h2_style))
    p6_steps = [
        "<b>Morning & Evening Delivery:</b> Farmers deliver freshly drawn milk within 60 minutes of milking in food-grade aluminum or stainless steel cans.",
        "<b>Automated Milk Collection Units (AMCU):</b> Milk is poured into an electronic weigh-pan. A motorized stirrer homogenizes the can, and an ultrasonic/infrared milk analyzer measures Fat% and Solids-Not-Fat (SNF)% within 15 seconds.",
        "<b>Instant Digital Accounting:</b> Data is logged into the farmer's unique RFID card, printing a transaction slip displaying weight, quality readings, and purchase value, which is deposited bi-weekly via direct bank transfer.",
        "<b>Organoleptic Screening:</b> Trained center personnel inspect each batch for abnormal color, colostrum traits, foreign odors, or visible particulates before acceptance."
    ]
    for s in p6_steps:
        story.append(Paragraph(f"• {s}", bullet_style))

    story.append(Paragraph("4.2 Bulk Milk Coolers (BMCs) & The 4°C Cold Chain Threshold", h2_style))
    p6_bmc = (
        "Accepted milk is immediately transferred into Bulk Milk Coolers (BMCs) — stainless steel jacketed tanks equipped with "
        "direct-expansion refrigerant coils and low-shear mechanical agitators. The system rapidly drops milk temperature from 37°C "
        "to below 4°C within 90 minutes. At 4°C, bacterial metabolic activity enters a bacteriostatic dormant state, inhibiting "
        "spoilage organisms (e.g., <i>Streptococcus lactis</i>, <i>Pseudomonas</i> species) and preserving raw milk quality for up to 48 hours."
    )
    story.append(Paragraph(p6_bmc, body_style))

    story.append(Paragraph("4.3 Insulated Road Tanker Transportation", h2_style))
    p6_trans = (
        "Chilled milk is collected by fleet road tankers featuring twin-wall polyurethane foam (PUF) insulation. These tankers "
        "maintain internal temperatures with less than a 1°C gain over a 12-hour journey. Strict regulatory protocols dictate tamper-evident "
        "digital seals on all manholes and discharge valves, digital temperature data loggers tracking real-time transit thermals, and "
        "mandatory CIP chemical sanitization of tanker interiors prior to dispatch."
    )
    story.append(Paragraph(p6_trans, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: RAW MILK RECEPTION & PURIFICATION
    # =========================================================================
    story.append(Paragraph("5.0 RAW MILK RECEPTION & PRE-PROCESSING PURIFICATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p7_rmrd = (
        "Upon tanker arrival at the Nanguneri Raw Milk Reception Dock (RMRD), the shipment remains strictly locked until quality "
        "assurance microbiologists execute a series of rapid 'Platform Tests'. If any single parameter violates statutory thresholds, "
        "the entire tanker volume (ranging from 10,000 to 25,000 liters) is instantly rejected, preventing contamination of central silos."
    )
    story.append(Paragraph(p7_rmrd, body_style))

    story.append(Paragraph("5.1 Intake Platform Quality Tests at RMRD", h2_style))
    plat_tests = [
        "<b>Temperature Verification:</b> Infrared probe immersion ensures intake temperature is strictly ≤ 4.0°C.",
        "<b>Clot-on-Boiling (COB) Test:</b> Rapid heating of 5 mL milk in a test tube. Any visible curdling indicates developed titratable acidity (> 0.18% lactic acid) and high microbial load, warranting immediate rejection.",
        "<b>Alcohol Stability Test:</b> Equal volumes of milk and 68% neutral ethanol are mixed. Coagulation signifies mineral instability, elevated calcium ions, or bacterial acid development.",
        "<b>Adulteration Screening Strip:</b> High-sensitivity chemical dipsticks screen for neutralizers (sodium hydroxide/carbonate), added urea, ammonium salts, starch, detergent, or commercial hydrogen peroxide preservatives.",
        "<b>Beta-Lactam Antibiotic Assay:</b> Lateral flow test kits confirm the total absence of veterinary antibiotic residues."
    ]
    for pt in plat_tests:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(Paragraph("5.2 Physical Clarification & Centrifugal Separation", h2_style))
    p7_clar = (
        "Once cleared by platform testing, milk is unloaded via flexible food-grade sanitary hoses through inline duplex stainless steel "
        "mesh strainers (removing foreign straw, hairs, or environmental particles). It then enters high-speed centrifugal clarifiers.<br/>"
        "<b>Centrifugal Clarification Mechanism:</b> Operating at 5,000 to 6,000 RPM, the centrifugal force generates intense radial "
        "acceleration. Denser microscopic contaminants — including somatic cells (epithelial and leucocyte cells from bovine udders), "
        "spores, and cellular debris — are forced outward and collected as 'clarifier sludge' for hygienic disposal, leaving pure liquid milk."
    )
    story.append(Paragraph(p7_clar, body_style))

    story.append(Paragraph("5.3 Centrifugal Standardization of Fat & SNF", h2_style))
    p7_std = (
        "Raw milk arrives with variable fat content (3.5% to 6.5%). To manufacture consistent commercial variants, milk passes through "
        "a centrifugal cream separator equipped with conical disc stacks. The unit separates dense skim milk from lighter milk fat (cream). "
        "Automated inline density transmitters continuously blend precise cream proportions back into the skim flow, standardizing the stream "
        "to exact FSSAI statutory formulations before thermal treatment."
    )
    story.append(Paragraph(p7_std, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CORE THERMAL PROCESSING & HOMOGENIZATION
    # =========================================================================
    story.append(Paragraph("6.0 CORE THERMAL PROCESSING: HTST PASTEURIZATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p8_past = (
        "Pasteurization represents the central thermal preservation benchmark in commercial dairy processing. Named in honor of "
        "Louis Pasteur, the process is engineered to destroy 100% of non-spore-forming pathogenic microorganisms (notably "
        "<i>Mycobacterium tuberculosis</i>, <i>Coxiella burnetii</i>, <i>Salmonella enterica</i>, <i>Listeria monocytogenes</i>, and pathogenic "
        "<i>Escherichia coli</i>) while preserving the natural organoleptic, enzymatic, and nutritional qualities of fresh milk."
    )
    story.append(Paragraph(p8_past, body_style))

    story.append(Paragraph("6.1 High-Temperature Short-Time (HTST) Engineering Architecture", h2_style))
    p8_htst = (
        "The Nanguneri plant employs state-of-the-art continuous High-Temperature Short-Time (HTST) Plate Heat Exchangers (PHE). "
        "The operational cycle operates through four synchronized thermodynamic phases:<br/>"
        "<b>1. Regenerative Pre-Heating:</b> Cold incoming raw milk (4°C) is counter-currently heated against outgoing hot pasteurized milk, "
        "recovering over 90% of thermal energy and elevating incoming milk to ~58°C without external steam expenditure.<br/>"
        "<b>2. Final Heating Section:</b> Pressurized hot water/steam raises milk temperature to <b>72°C – 75°C</b>.<br/>"
        "<b>3. Precision Holding Tube:</b> The milk traverses a serpentine stainless steel holding tube calibrated to ensure every particle "
        "remains exposed to 72°C for exactly <b>15 seconds</b>.<br/>"
        "<b>4. Flow Diversion Valve (FDV):</b> A critical safety mechanism monitored by microprocessor controllers. If the holding tube "
        "temperature drops below 72°C by even 0.1°C, the FDV instantly diverts milk back to the raw balance tank for re-processing.<br/>"
        "<b>5. Chilled Regeneration & Final Cooling:</b> Pasteurized milk transfers its heat to incoming raw milk and is chilled via ice-water "
        "circulators to ≤ 4°C, preventing spore germination and entering insulated storage silos."
    )
    story.append(Paragraph(p8_htst, body_style))

    story.append(Paragraph("6.2 High-Pressure Mechanical Homogenization", h2_style))
    p8_homo = (
        "In unhomogenized milk, natural butterfat globules have large diameters (1 to 10 microns). Because fat has a lower density than water, "
        "globules cluster and rise to form an undesirable cream layer according to Stokes' Law.<br/>"
        "<b>Homogenization Mechanics:</b> Milk is forced through a microscopic carbide homogenization orifice at enormous hydraulic pressures "
        "(150 to 200 bar, followed by a second stage of 50 bar). The intense cavitation, turbulence, and shear forces shatter fat globules "
        "down to sub-micron dimensions (< 1.5 microns). Adsorbed casein micelles surround the new fat surfaces, ensuring uniform emulsion "
        "stability, preventing cream separation, enhancing dairy whiteness, and imparting a rich, smooth mouthfeel."
    )
    story.append(Paragraph(p8_homo, body_style))

    story.append(Spacer(1, 4))
    if os.path.exists("d:/seminar iot/assets/flow_diagram.png"):
        story.append(Image("d:/seminar iot/assets/flow_diagram.png", width=460, height=135))
        story.append(Paragraph("Figure 6.1: Industrial Flow Schematic of Milk Processing and Quality Gates at Hatsun Dairy.", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: MANUFACTURING OF VALUE-ADDED DAIRY PRODUCTS
    # =========================================================================
    story.append(Paragraph("7.0 VALUE-ADDED DAIRY PRODUCT PROCESSING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p9_prod = (
        "While fluid pouch milk forms the primary production volume, converting standardized milk and surplus cream into value-added "
        "dairy commodities enables plant optimization, absorbs seasonal flush milk surpluses, and yields higher profit margins. "
        "The Nanguneri plant houses dedicated hygienic production sections for cultured and concentrated dairy derivatives."
    )
    story.append(Paragraph(p9_prod, body_style))

    story.append(Paragraph("7.1 Product Manufacturing Highlights & Process Flow", h2_style))

    prod_table_data = [
        [Paragraph("<b>Dairy Product</b>", table_header), Paragraph("<b>Key Raw Material</b>", table_header), Paragraph("<b>Industrial Process Summary & Biological Mechanisms</b>", table_header)],
        [
            Paragraph("<b>Standardized Pouch Milk</b>", table_cell),
            Paragraph("Pasteurized milk standardized for Fat & SNF", table_cell),
            Paragraph("Separation, fat blending to specifications (Toned: 3.0% Fat / 8.5% SNF; Full Cream: 6.0% Fat / 9.0% SNF), HTST pasteurized, homogenized, chilled to 4°C, routed directly to FFS packaging lines.", table_cell)
        ],
        [
            Paragraph("<b>Cultured Curd (Dahi)</b>", table_cell),
            Paragraph("Pasteurized milk, starter bacterial cultures", table_cell),
            Paragraph("Milk is pasteurized at 85°C – 90°C (denaturing whey proteins for firmer curd texture), cooled to 42°C, inoculated with defined lactic starter culture (<i>Lactobacillus bulgaricus</i>, <i>Streptococcus thermophilus</i>), packed into retail cups/pouches, and incubated at 40°C – 42°C for 4–5 hours until pH hits 4.5. Blast-chilled to 4°C to arrest fermentation.", table_cell)
        ],
        [
            Paragraph("<b>Clarified Butter (Ghee)</b>", table_cell),
            Paragraph("Cream / Churned unsalted butter", table_cell),
            Paragraph("Cream is aged, churned into butter, and heated in stainless steel steam-jacketed ghee kettles at 110°C – 120°C. Moisture evaporates entirely (< 0.5%), milk solids precipitate, and Maillard browning generates characteristic aroma and granular crystalline texture. Filtered, cooled, and hermetically sealed.", table_cell)
        ],
        [
            Paragraph("<b>Table Butter</b>", table_cell),
            Paragraph("Standardized cream (38–40% fat)", table_cell),
            Paragraph("Cream pasteurized, aged at 5°C to crystallize butterfat, churned in continuous butter makers (phase inversion from oil-in-water to water-in-oil emulsion). Buttermilk drained, butter granules washed, salted (optional 2%), vacuum-worked to uniform moisture (< 16%), and packaged.", table_cell)
        ],
        [
            Paragraph("<b>Paneer (Cottage Cheese)</b>", table_cell),
            Paragraph("Standardized high-fat milk (5.8% fat)", table_cell),
            Paragraph("Heated to 85°C, direct acidified with food-grade citric acid or lactic acid (pH 5.3). Whey separates from coagulated casein-fat curds; curds collected in perforated hoops, mechanically pressed under pneumatic weight to express whey, and chilled in chilled-water brine vats at 4°C.", table_cell)
        ],
        [
            Paragraph("<b>Spray-Dried Milk Powder</b>", table_cell),
            Paragraph("Surplus skimmed milk", table_cell),
            Paragraph("Skim milk concentrated in multi-effect falling-film evaporators to 48% total solids. Atomized through high-speed rotary disks into hot air drying chambers (180°C – 200°C). Instant flash-evaporation produces fine milk powder (< 4% moisture), cyclonically separated, cooled, and gas-flushed into bulk bags.", table_cell)
        ],
    ]

    t_prod = Table(prod_table_data, colWidths=[90, 105, 290])
    t_prod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F294A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_prod)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 By-Product Recovery & Circular Utilization", h2_style))
    p9_by = (
        "Sustainable dairy engineering requires full valorization of processing by-products. Acid whey recovered from paneer "
        "coagulation is neutral-treated and processed into nutritional whey drinks or animal feedstock supplements. Sweet buttermilk "
        "from butter churning is chilled, pasteurized, seasoned with salt and spices (curry leaf, mustard, ginger), and packaged as "
        "refreshing ready-to-drink spiced buttermilk, minimizing biological oxygen demand (BOD) loads on effluent treatment plants."
    )
    story.append(Paragraph(p9_by, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: AUTOMATED PACKAGING & CODING
    # =========================================================================
    story.append(Paragraph("8.0 AUTOMATED PACKAGING & ASEPTIC FILLING SYSTEMS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p10_pack = (
        "Packaging represents the critical barrier preserving pasteurized milk quality between factory gate and domestic consumption. "
        "Because milk is vulnerable to photo-oxidation, microbial re-contamination, and foreign flavor absorption, the packaging "
        "operation must function with high speed, hermetic sealing integrity, and complete environmental sterility."
    )
    story.append(Paragraph(p10_pack, body_style))

    story.append(Paragraph("8.1 Form-Fill-Seal (FFS) High-Speed Machinery Operations", h2_style))
    p10_ffs = (
        "Liquid milk packaging at Nanguneri is executed by automated high-speed vertical Form-Fill-Seal (FFS) machines capable of packaging "
        "over 5,000 pouches per hour per filling head under largely touch-free conditions:<br/>"
        "<b>1. Multi-Layer Co-Extruded Film Uncoiling:</b> Packaging film consists of 3-layer or 5-layer virgin polyethylene (LDPE/LLDPE). "
        "The black inner layer blocks UV/visible light (preventing riboflavin vitamin breakdown and oxidized off-flavors), while the white outer layer "
        "provides clean printability, chemical barrier properties, and tensile drop resistance.<br/>"
        "<b>2. Inline Germicidal UV Irradiation:</b> Prior to forming the tube, the inner food-contact surface of the uncoiling film passes beneath "
        "high-intensity germicidal ultraviolet (UV-C, 254 nm) lamps, eradicating surface bacteria and fungal spores.<br/>"
        "<b>3. Precision Volumetric Dosing:</b> Piston dosers or magnetic induction flow meters inject exact volumes (500 mL or 1,000 mL) "
        "into the film tube formed over a cylindrical mandrel.<br/>"
        "<b>4. Pneumatic Thermal Jaw Sealing:</b> Impulse thermal jaws simultaneously melt-fuse the horizontal pouch seal and sever the completed pack, "
        "forming a hermetic, leak-proof barrier without manual operator contact."
    )
    story.append(Paragraph(p10_ffs, body_style))

    story.append(Paragraph("8.2 Continuous Laser Batch Coding & Regulatory Traceability", h2_style))
    p10_code = (
        "Every single pouch exiting the sealing jaw passes beneath an automated continuous ink-jet or laser coding station. "
        "In accordance with statutory FSSAI and Legal Metrology mandates, each pack is indelibly printed with:<br/>"
        "• Batch Identification Code (linking back to specific raw silo, processing time, and HTST operator run)<br/>"
        "• Date of Packaging & Precise Timestamp (DD/MM/YYYY HH:MM)<br/>"
        "• 'Use By' Expiry Date (calculated under recommended 4°C storage conditions)<br/>"
        "• Maximum Retail Price (MRP inclusive of all taxes), Net Volume, and FSSAI Central License Number.<br/>"
        "This granular digital traceability ensures that in the event of an adulteration query or cold chain break, the exact source "
        "can be isolated within minutes."
    )
    story.append(Paragraph(p10_code, body_style))

    story.append(Paragraph("8.3 Secondary Boxing, Crating & Conveyance", h2_style))
    p10_crate = (
        "Sealed pouches drop onto motorized conveyor belts where inline weight checkers automatically reject underfilled or leaking units. "
        "Pouches are packed into standardized, sanitized food-grade high-density polyethylene (HDPE) crates (typically 20 pouches per crate). "
        "Automated crate stackers stack crates 5-high and transfer them immediately along low-friction roller conveyors into the blast cold room."
    )
    story.append(Paragraph(p10_crate, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: DISTRIBUTION & COLD CHAIN ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("9.0 REFRIGERATED COLD CHAIN & DISTRIBUTION LOGISTICS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p11_dist = (
        "Pasteurized pouch milk is a highly perishable living biological commodity with an active shelf life of 48 to 72 hours under strict "
        "refrigeration. The cold chain constitutes an unbroken thermal link from the factory cooling exchanger through transport, wholesale "
        "depots, retail dairy booths, and domestic household storage. A temperature increase to just 10°C accelerates psychrotrophic bacterial "
        "growth exponentially, cutting commercial shelf life in half."
    )
    story.append(Paragraph(p11_dist, body_style))

    story.append(Paragraph("9.1 Multi-Tier Distribution Network Architecture", h2_style))
    dist_tiers = [
        "<b>1. Plant Holding Cold Chambers (2°C – 4°C):</b> Crates are palletized in high-capacity air-blast cold rooms maintaining 2°C to 4°C. Inventory follows strict First-In, First-Out (FIFO) stock rotation schedules.",
        "<b>2. Primary Insulated Reefer Transport Fleet:</b> Specialized heavy-duty reefer trucks featuring active mechanical refrigeration units and multi-temperature partitions transport crates from Nanguneri to regional distribution hubs across Tamil Nadu and Kerala.",
        "<b>3. Regional Depots & Cold Buffers:</b> Urban distribution centers receive bulk nightly shipments, cross-docking crates into designated route vans and three-wheeler distribution carriers.",
        "<b>4. Dedicated Retail Touchpoints & Hatsun Daily Outlets:</b> Products reach thousands of retail kirana shops, authorized milk booths, and company-owned 'Hatsun Daily' cold outlets equipped with commercial visi-coolers and deep freezers.",
        "<b>5. Pre-Dawn Doorstep Delivery Network:</b> Local delivery agents dispatch milk pouches to residential households between 4:30 AM and 6:30 AM before daily ambient temperatures rise."
    ]
    for dt in dist_tiers:
        story.append(Paragraph(f"• {dt}", bullet_style))

    story.append(Spacer(1, 4))
    if os.path.exists("d:/seminar iot/assets/cold_chain_architecture.png"):
        story.append(Image("d:/seminar iot/assets/cold_chain_architecture.png", width=460, height=135))
        story.append(Paragraph("Figure 9.1: End-to-End Cold Chain Integrity Architecture from Milking Point to Urban Consumer.", caption_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("9.2 Telematics, IoT Fleet Monitoring & Route Optimization", h2_style))
    p11_iot = (
        "To guarantee thermal compliance during transit, Hatsun's transport fleet is integrated with GPS tracking and IoT wireless temperature "
        "sensors inside vehicle refrigerated cargo compartments. Central control rooms receive continuous data streams; if container temperature "
        "exceeds 6°C, automated SMS/app alerts flag the driver and depot supervisor to verify refrigeration unit operation before delivery."
    )
    story.append(Paragraph(p11_iot, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: INDUSTRIAL MICROBIOLOGY & QUALITY CONTROL
    # =========================================================================
    story.append(Paragraph("10.0 INDUSTRIAL MICROBIOLOGY & LABORATORY ASSURANCE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p12_micro = (
        "In modern dairy processing, the microbiology and chemical analytical laboratory acts as the supreme operational gatekeeper. "
        "Milk provides an ideal growth medium for bacteria, yeasts, and molds. A comprehensive microbiological control regime must distinguish "
        "between benign lactic acid cultures, spoilage organisms, and virulent foodborne pathogens."
    )
    story.append(Paragraph(p12_micro, body_style))

    story.append(Paragraph("10.1 Key Dairy Microorganisms & Target Pathogens", h2_style))
    micro_specs = [
        "<b>Lactic Acid Bacteria (LAB):</b> <i>Lactococcus lactis</i>, <i>Lactobacillus acidophilus</i>. Ferment lactose to lactic acid. Desirable in cultured curd/cheese manufacturing, but indicative of raw milk aging if present in excessive concentrations at reception.",
        "<b>Psychrotrophic Spoilage Organisms:</b> <i>Pseudomonas fluorescens</i>, <i>Pseudomonas fragi</i>. Can reproduce at refrigerated temperatures (4°C – 7°C) and synthesize heat-stable lipases and proteases that survive HTST pasteurization, inducing bitter off-flavors and age-gelation during extended storage.",
        "<b>Foodborne Pathogens Destroyed by Pasteurization:</b> <i>Salmonella enterica</i>, <i>Listeria monocytogenes</i>, enteropathogenic <i>Escherichia coli</i> (EPEC), <i>Campylobacter jejuni</i>, and <i>Staphylococcus aureus</i>.",
        "<b>Spore-Forming Microorganisms:</b> <i>Bacillus cereus</i> and <i>Clostridium</i> species. Bacterial endospores possess thick multi-layered keratin coats that survive pasteurization; controlled chilling (≤ 4°C) is essential to prevent their germination into vegetative cells."
    ]
    for ms in micro_specs:
        story.append(Paragraph(f"• {ms}", bullet_style))

    story.append(Paragraph("10.2 Routine Dairy Analytical Assays & Methodologies", h2_style))
    
    test_table_data = [
        [Paragraph("<b>Diagnostic Test</b>", table_header), Paragraph("<b>Target Biological / Chemical Parameter</b>", table_header), Paragraph("<b>Standard Operating Procedure & Significance</b>", table_header)],
        [
            Paragraph("<b>Standard Plate Count (SPC)</b>", table_cell),
            Paragraph("Total viable aerobic mesophilic bacteria", table_cell),
            Paragraph("Serial dilution in buffered peptone water, pour plated on Milk Agar / PCA. Incubated at 37°C for 48 hours. FSSAI limit for pasteurized milk: < 30,000 CFU/mL. Reflects overall plant sanitary efficiency.", table_cell)
        ],
        [
            Paragraph("<b>Coliform Fermentation Count</b>", table_cell),
            Paragraph("Fecal indicator bacteria (<i>E. coli</i>, <i>Enterobacter</i>)", table_cell),
            Paragraph("Plated on Violet Red Bile Agar (VRBA) at 37°C for 24 hours. Limit: < 10 CFU/mL in pasteurized milk. Absolute zero indicates post-pasteurization recontamination absence.", table_cell)
        ],
        [
            Paragraph("<b>Alkaline Phosphatase (ALP) Test</b>", table_cell),
            Paragraph("Pasteurization verification biomarker", table_cell),
            Paragraph("Enzyme native to raw milk with thermal destruction kinetics slightly higher than <i>Coxiella burnetii</i>. If ALP is destroyed (negative color reaction), complete pathogen eradication is scientifically confirmed.", table_cell)
        ],
        [
            Paragraph("<b>Methylene Blue Reduction (MBRT)</b>", table_cell),
            Paragraph("Raw milk microbial load estimation", table_cell),
            Paragraph("Methylene blue dye added to 10 mL milk in water bath at 37°C. Time taken for decolorization indicates bacterial respiration rate (> 5 hrs = Excellent, < 30 mins = Very Poor).", table_cell)
        ],
        [
            Paragraph("<b>Gerber Fat Assay & Lactometer</b>", table_cell),
            Paragraph("Fat% and Specific Gravity / SNF%", table_cell),
            Paragraph("Sulfuric acid digests proteins, amyl alcohol aids phase separation in Gerber butyrometer centrifuged at 1,100 RPM. Lactometer density reading determines SNF via Richmond formula.", table_cell)
        ],
    ]
    t_test = Table(test_table_data, colWidths=[95, 105, 285])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F294A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_test)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: SANITATION, CIP & FSSAI / HACCP COMPLIANCE
    # =========================================================================
    story.append(Paragraph("11.0 SANITATION ENGINEERING, CIP & FOOD SAFETY COMPLIANCE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p13_cip = (
        "Because milk residues form adhesive organic films (milkstone comprising calcium phosphate, denatured whey proteins, "
        "and butterfats) on metal equipment surfaces, inadequate sanitation rapidly fosters bacterial bio-films. To guarantee hygienic "
        "integrity without dismantling kilometers of stainless steel pipework, modern dairies rely on automated Clean-in-Place (CIP) systems."
    )
    story.append(Paragraph(p13_cip, body_style))

    story.append(Paragraph("11.1 The 5-Stage Automated Clean-in-Place (CIP) Cycle", h2_style))
    cip_steps = [
        "<b>1. Cold / Warm Water Pre-Rinse:</b> Soft water circulated at 50°C for 10–15 minutes, flushing out 90% of loose milk residues directly to the drain.",
        "<b>2. Alkaline Detergent Circulation (Caustic Wash):</b> 1.5% to 2.0% Sodium Hydroxide (NaOH) circulated at 75°C – 80°C for 20 minutes. Saponifies butterfats, peptizes organic proteins, and hydrolyzes adhering biofilms.",
        "<b>3. Intermediate Soft Water Rinse:</b> Flushes out residual caustic wash and detached organic debris.",
        "<b>4. Acid Detergent Circulation (Acid Wash):</b> 0.8% to 1.2% Nitric Acid (HNO3) or Phosphoric Acid circulated at 65°C for 15 minutes. Dissolves inorganic mineral scales, milkstone encrustations, and neutralizes residual alkalinity.",
        "<b>5. Final Sanitizing & Microbial Sterilization Rinse:</b> Cold flush with Peracetic Acid (PAA, 150 ppm) or hot water sanitization at 85°C for 15 minutes immediately prior to processing, rendering surfaces commercially sterile."
    ]
    for cs in cip_steps:
        story.append(Paragraph(f"• {cs}", bullet_style))

    story.append(Spacer(1, 4))
    if os.path.exists("d:/seminar iot/assets/haccp_flow.png"):
        story.append(Image("d:/seminar iot/assets/haccp_flow.png", width=460, height=130))
        story.append(Paragraph("Figure 11.1: Hazard Analysis and Critical Control Points (HACCP) Dairy Processing Safety Architecture.", caption_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("11.2 Statutory Regulatory Frameworks & FSSAI Standards", h2_style))
    p13_fssai = (
        "The Nanguneri plant operates in full compliance with the Food Safety and Standards Act, 2006 (FSSAI). Key mandates include:<br/>"
        "• Mandatory display of the 14-digit central FSSAI license number across all packaging graphics.<br/>"
        "• Strict compositional parameters: Toned Milk must contain minimum 3.0% Milk Fat and 8.5% SNF; Standardized Milk must contain "
        "4.5% Milk Fat and 8.5% SNF.<br/>"
        "• Zero tolerance for pathogenic <i>Listeria</i>, <i>Salmonella</i>, and pesticide/aflatoxin M1 chemical residues."
    )
    story.append(Paragraph(p13_fssai, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: SOCIO-ECONOMIC IMPACT & SUSTAINABILITY
    # =========================================================================
    story.append(Paragraph("12.0 SOCIO-ECONOMIC IMPACT, AUTOMATION & SUSTAINABILITY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    p14_socio = (
        "An industrial dairy facility serves as a vital economic engine bridging rural livestock farming with urban consumer economies. "
        "The operations of Hatsun Agro Product's Nanguneri facility ripple across agricultural households, gender empowerment initiatives, "
        "and regional technological advancement throughout southern Tamil Nadu."
    )
    story.append(Paragraph(p14_socio, body_style))

    story.append(Paragraph("12.1 Rural Economic Transformation & Women Empowerment", h2_style))
    p14_econ = (
        "<b>Predictable Bi-Weekly Income:</b> Before organized dairy collection, marginal farmers were vulnerable to unorganized local traders "
        "who dictated arbitrary rates and delayed settlements. Hatsun's direct AMCU payment guarantees consistent cash flow, empowering "
        "families to invest in children's education, agricultural upgrades, and healthcare.<br/>"
        "<b>Empowerment of Women Dairy Farmers:</b> In rural South India, women perform over 70% of livestock feeding, cleaning, and milking chores. "
        "By issuing AMCU bank accounts directly in women's names, the Hatsun ecosystem ensures direct financial independence and leadership within rural families.<br/>"
        "<b>Comprehensive Animal Welfare:</b> Hatsun deploys qualified veterinarians offering doorstep emergency care, cattle vaccinations, "
        "mineral supplement distribution, and artificial insemination, raising average milk yields from indigenous and crossbred cattle."
    )
    story.append(Paragraph(p14_econ, body_style))

    story.append(Paragraph("12.2 Industrial Automation (PLC / SCADA Architecture)", h2_style))
    p14_auto = (
        "The Nanguneri plant features advanced Supervisory Control and Data Acquisition (SCADA) and Programmable Logic Controllers (PLCs). "
        "Digital sensors continuously transmit line pressure, pasteurization temperatures, flow diversion states, and tank levels to central "
        "monitoring consoles. Automated pneumatic valves prevent manual operator errors, while audit-ready digital batch records guarantee "
        "unmatched compliance with international food safety certifications."
    )
    story.append(Paragraph(p14_auto, body_style))

    story.append(Paragraph("12.3 Environmental Engineering & Effluent Treatment (ETP)", h2_style))
    p14_etp = (
        "Dairy processing generates substantial organic wastewater containing milk fats, whey proteins, and cleaning detergents. "
        "The Nanguneri plant operates a zero-liquid-discharge (ZLD) Effluent Treatment Plant (ETP):<br/>"
        "• <b>Primary Treatment:</b> Fat-grease traps skim floating cream residues, followed by chemical coagulation and flocculation.<br/>"
        "• <b>Secondary Biological Treatment:</b> High-rate anaerobic digesters reduce organic BOD, generating biogas used to fuel plant steam boilers. "
        "Aerobic activated sludge aeration basins further digest residual organic pollutants.<br/>"
        "• <b>Tertiary Treatment & Recycling:</b> Dual-media sand filtration, activated carbon absorption, and UV disinfection yield crystal-clear "
        "treated water recycled for factory boiler feeds, cooling tower make-up, and extensive green-belt landscaping."
    )
    story.append(Paragraph(p14_etp, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: LEARNING OUTCOMES, RECOMMENDATIONS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("13.0 LEARNING OUTCOMES, RECOMMENDATIONS & CONCLUSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F294A"), spaceAfter=8))

    story.append(Paragraph("13.1 Key Student Learning Outcomes (Academic & Practical)", h2_style))
    learnings = [
        "<b>Integration of Food Microbiology:</b> Observed firsthand how thermal death principles (D-values and z-values) are applied in industrial HTST pasteurizers to destroy pathogens while preserving heat-sensitive whey proteins and vitamins.",
        "<b>Cold Chain Engineering:</b> Developed a thorough understanding of the thermodynamic cold chain, recognizing how chilling milk to ≤ 4°C at rural BMCs halts bacterial multiplication and safeguards the dairy supply chain.",
        "<b>Industrial Process Control:</b> Witnessed continuous centrifugal clarification, disc-stack cream separation, two-stage mechanical homogenization, and automated vertical Form-Fill-Seal (FFS) pouch packaging.",
        "<b>Quality Assurance Discipline:</b> Gained practical insight into dairy analytical testing—including the Alkaline Phosphatase assay, Gerber fat testing, MBRT, alcohol stability, and strict FSSAI compliance auditing."
    ]
    for lr in learnings:
        story.append(Paragraph(f"• {lr}", bullet_style))

    story.append(Paragraph("13.2 Strategic Recommendations for Operational Optimization", h2_style))
    recs = [
        "<b>Deployment of Renewable Energy:</b> Southern Tamil Nadu possesses exceptional solar and wind resources. Expanding rooftop solar PV installations can offset heavy refrigeration and pumping electrical loads.",
        "<b>Sustainable Packaging Materials:</b> Transitioning from conventional multilayer LDPE toward certified bio-based compostable polymers or high-recyclability mono-material films will reduce plastic waste in line with Extended Producer Responsibility (EPR) mandates.",
        "<b>Blockchain Traceability:</b> Introducing consumer-scannable on-pack QR codes will enable consumers to trace milk provenance back to rural chilling hubs, displaying live chilling timestamps and farm test scores.",
        "<b>Academic Collaboration & Internships:</b> Establishing structured research partnerships with Scott Christian College and regional universities will support microbial research, shelf-life testing, and technical talent recruitment."
    ]
    for rc in recs:
        story.append(Paragraph(f"• {rc}", bullet_style))

    story.append(Paragraph("13.3 Formal Conclusion", h2_style))
    p15_conc = (
        "The educational industrial visit to <b>Hatsun Agro Product Limited, Nanguneri</b>, provided an exceptional, multifaceted learning "
        "experience bridging theoretical academic microbiology with state-of-the-art dairy processing technology. The plant exemplifies how "
        "large-scale direct farmer procurement, precise automated thermodynamic treatment, stringent laboratory quality gates, and an unbroken "
        "refrigerated cold chain work harmoniously to transform raw agricultural milk into wholesome, pathogen-free dairy products for millions. "
        "The practical knowledge acquired regarding industrial microbiology, clean-in-place sanitation, and quality assurance forms an invaluable "
        "foundation for our academic curriculum and future scientific careers."
    )
    story.append(Paragraph(p15_conc, body_style))
    story.append(Spacer(1, 10))

    # Formal Completion Box
    complete_box = [
        [Paragraph("<para align='center'><b>INDUSTRIAL VISIT RECORD COMPLETED & VERIFIED</b><br/><font size='8' color='#334155'>Submitted by: <b>STEPHY BELCITTA P</b> (Class No: <b>878</b>) | Department of Microbiology<br/>Scott Christian College (Autonomous), Nagercoil – 629 003, Tamil Nadu</font></para>", table_cell)]
    ]
    t_comp = Table(complete_box, colWidths=[460])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F294A')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_comp)

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build completed without certificate.")

if __name__ == "__main__":
    build_pdf()
