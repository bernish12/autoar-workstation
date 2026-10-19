import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCX_PATH = r"D:\seminar iot\Industrial_Visit_Report_Hatsun_STEPHY_BELCITTA.docx"

def create_docx():
    doc = docx.Document()

    # Set Margins (0.75 in)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # PAGE 1: TITLE COVER
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(40)
    p.paragraph_format.space_after = Pt(20)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("INDUSTRIAL VISIT TO HATSUN\nAGRO PRODUCT NANGUNERI")
    run.font.name = "Arial"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 41, 74)

    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_after = Pt(40)
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("22 September 2026")
    r_date.font.name = "Arial"
    r_date.font.size = Pt(13)
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(51, 65, 85)

    p_rep = doc.add_paragraph()
    p_rep.paragraph_format.space_after = Pt(30)
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = p_rep.add_run("A REPORT")
    r_rep.font.name = "Arial"
    r_rep.font.size = Pt(18)
    r_rep.font.bold = True
    r_rep.font.color.rgb = RGBColor(15, 41, 74)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(8)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Submitted by")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True

    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_after = Pt(4)
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_name.add_run("STEPHY BELCITTA P")
    r_name.font.name = "Arial"
    r_name.font.size = Pt(15)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(15, 41, 74)

    p_cls = doc.add_paragraph()
    p_cls.paragraph_format.space_after = Pt(4)
    p_cls.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cls = p_cls.add_run("I B.Sc. Microbiology")
    r_cls.font.name = "Arial"
    r_cls.font.size = Pt(12)

    p_roll = doc.add_paragraph()
    p_roll.paragraph_format.space_after = Pt(14)
    p_roll.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_roll = p_roll.add_run("Class No: 878")
    r_roll.font.name = "Arial"
    r_roll.font.size = Pt(13)
    r_roll.font.bold = True
    r_roll.font.color.rgb = RGBColor(30, 58, 138)

    p_col = doc.add_paragraph()
    p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_col = p_col.add_run("Department of Microbiology\nScott Christian College (Autonomous)\nNagercoil – 629 003, Tamil Nadu")
    r_col.font.name = "Arial"
    r_col.font.size = Pt(11)
    r_col.font.bold = True

    doc.add_page_break()

    # Detailed chapters (Without Certificate)
    chapters = [
        ("EXECUTIVE SUMMARY & REPORT PREAMBLE", [
            ("Preamble",
             "This industrial visit report documents the academic study and technical observations conducted during an on-site visit to the Hatsun Agro Product Limited dairy processing plant situated at Nanguneri, Tirunelveli District, Tamil Nadu, on 22 September 2026. As part of the undergraduate curriculum in Microbiology at Scott Christian College (Autonomous), this investigation bridges theoretical classroom concepts—such as microbial thermal kinetics, pasteurization verification assays, and pathogen control—with modern automated dairy engineering practices.\n\nThe report follows the complete dairy value chain from decentralized village milk collection and rapid bulk chilling, through raw intake platform diagnostics, high-temperature short-time (HTST) pasteurization, pressure homogenization, and automated Form-Fill-Seal (FFS) packaging, to refrigerated cold chain logistics and Clean-in-Place (CIP) sanitation engineering.")
        ]),
        ("1.0 INTRODUCTION & OBJECTIVES OF THE INDUSTRIAL VISIT", [
            ("Background & Industry Context",
             "Milk is an exceptionally complex biological liquid rich in emulsified fats, caseins, lactose, vitamins, and minerals. However, its high moisture content (aw ~ 0.99) and near-neutral pH render it highly prone to rapid bacterial proliferation under tropical temperatures. India is the world's foremost milk producer, yet over 75% of milk is gathered from smallholder farmers. The organized dairy industry overcomes this by operating an unbroken refrigerated cold chain that collects milk immediately after harvesting and processes it under rigorous hygienic conditions. The Nanguneri plant of Hatsun Agro Product Ltd. is an outstanding benchmark of this model."),
            ("Objectives of the Study",
             "• Understand modern dairy processing technology: reception, clarification, pasteurization, homogenization, and packaging.\n• Study cold chain logistics and temperature preservation at 4°C from village collection to consumer.\n• Connect classroom microbiology with industrial practice: microbial kinetics, pathogens (Salmonella, Listeria, E. coli), and quality control.\n• Examine analytical laboratory protocols, adulteration screening, and regulatory FSSAI / HACCP standards.")
        ]),
        ("2.0 COMPANY PROFILE: HATSUN AGRO PRODUCT LIMITED (HAP)", [
            ("Corporate History & Growth",
             "Founded in 1970 by Mr. R. G. Chandramogan, Hatsun Agro Product Ltd. (HAP) has expanded into India's largest private-sector dairy company. Headquartered in Chennai, HAP operates modern milk processing plants, chilling centers, and cold logistics chains across Tamil Nadu, Karnataka, Andhra Pradesh, Telangana, and Maharashtra."),
            ("Brand Portfolio",
             "• Arokya Milk & Curd: Highly trusted household dairy brand offering standardized nutritional liquid milk variants.\n• Hatsun Range: Quality butter, ghee, curd, paneer, and milk powders.\n• Arun Icecreams: Pioneer ice cream brand with vast deep-freeze retail networks across South India.\n• ibaco: Premium artisanal ice cream and frozen dessert experience parlours.\n• Oyalo: Convenient ready-to-eat culinary preparations.")
        ]),
        ("3.0 THE NANGUNERI PROCESSING PLANT: INFRASTRUCTURE & LAYOUT", [
            ("Plant Role & Strategic Location",
             "Located in Tirunelveli district, Nanguneri is surrounded by rich dairy farming communities. The plant receives milk daily from thousands of farmers, processes it under automated conditions, and distributes it to Madurai, Tirunelveli, Thoothukudi, Nagercoil, and Kerala."),
            ("Zonal Plant Architecture",
             "• Raw Milk Reception Dock (RMRD): Tanker intake bays, automatic sampling, and chilling.\n• Silo Farm: Stainless steel insulated storage tanks maintaining raw milk at 4°C.\n• Processing Hall: Centrifugal clarifiers, cream separators, HTST pasteurizers, and homogenizers.\n• Packaging Bay: Form-Fill-Seal (FFS) automated machines under HEPA-filtered clean air.\n• Cold Storage: Blast-chilled warehouse maintaining finished products at 2°C – 4°C.\n• Central Quality Assurance Lab: Advanced chemical and microbiological testing facilities.")
        ]),
        ("4.0 GRASSROOTS PROCUREMENT & COLD CHAIN INITIATION", [
            ("Village Collection Centers (VCC)",
             "Farmers bring fresh milk morning and evening. Automatic Milk Collection Units (AMCU) measure weight, fat percentage, and SNF in seconds. Testing results are displayed transparently to farmers, and payments are transferred directly to bank accounts."),
            ("Bulk Milk Coolers (BMC) & Insulated Tankers",
             "Milk is quickly chilled to 4°C in Bulk Milk Coolers to halt bacterial growth. Insulated stainless steel road tankers transport chilled milk to Nanguneri, maintaining temperatures strictly under 4°C throughout the transit.")
        ]),
        ("5.0 RAW MILK RECEPTION & PRE-PROCESSING PURIFICATION", [
            ("Platform Testing at RMRD",
             "Every tanker is tested before unloading: Temperature check (≤ 4°C), Clot-on-Boiling (COB), Alcohol stability, titratable acidity, and rapid adulterant strips (screening for urea, starch, neutralizers, detergents, and antibiotics)."),
            ("Centrifugal Clarification & Standardization",
             "Milk passes through inline strainers and centrifugal clarifiers operating at 6,000 RPM, removing somatic cells and dirt. Centrifugal cream separators adjust fat content to produce standardized milk variants (Full Cream, Standardized, Toned, and Double Toned).")
        ]),
        ("6.0 CORE THERMAL PROCESSING: HTST PASTEURIZATION & HOMOGENIZATION", [
            ("High-Temperature Short-Time (HTST) Pasteurization",
             "Milk is heated to 72°C – 75°C for 15 seconds in plate heat exchangers, followed by rapid cooling to 4°C. An automated Flow Diversion Valve diverts milk back if the temperature drops below 72°C, ensuring 100% destruction of pathogenic bacteria (Mycobacterium, Salmonella, Listeria)."),
            ("High-Pressure Homogenization",
             "Milk is forced through minute valves at 150–200 bar. This shatters fat globules from 10 microns to under 1.5 microns, preventing cream separation, improving whiteness, and imparting a rich uniform taste.")
        ]),
        ("7.0 VALUE-ADDED DAIRY PRODUCT PROCESSING", [
            ("Manufacture of Curd, Ghee, Butter & Paneer",
             "• Curd (Dahi): Pasteurized milk inoculated with lactic cultures (Lactobacillus, Streptococcus) and fermented at 42°C.\n• Butter & Ghee: Cream churned into butter; slow simmering at 115°C evaporates moisture leaving clarified aromatic ghee.\n• Paneer: Coagulated with food-grade citric acid at 85°C, pressed into blocks, and chilled.\n• Milk Powder: Surplus skim milk concentrated and spray-dried in high-temperature drying towers.")
        ]),
        ("8.0 AUTOMATED PACKAGING & ASEPTIC FILLING SYSTEMS", [
            ("Form-Fill-Seal (FFS) Operations",
             "Pouch packaging operates automatically using food-grade multi-layer LDPE/LLDPE films. The film inner layer is UV-sterilized before filling. Automated vertical FFS machines fill, seal, and cut pouches touch-free at speeds over 5,000 pouches/hour."),
            ("Batch Coding & Traceability",
             "Laser printers mark batch numbers, packaging date, expiry date, MRP, and FSSAI license numbers on each pouch, enabling complete supply chain traceability.")
        ]),
        ("9.0 REFRIGERATED COLD CHAIN & DISTRIBUTION ARCHITECTURE", [
            ("Cold Chain Network",
             "Pouches are crated and moved to cold rooms (2°C–4°C). Insulated reefer trucks deliver crates to regional depots. Retail booths with deep chillers and early-morning home delivery ensure consumers receive fresh milk daily without temperature abuse.")
        ]),
        ("10.0 INDUSTRIAL MICROBIOLOGY & LABORATORY QUALITY GATES", [
            ("Dairy Bacteriology & Microbial Assays",
             "• Standard Plate Count (SPC): Aerobic colony count (< 30,000 CFU/mL).\n• Coliform Test: Plated on VRBA (< 10 CFU/mL; indicates sanitation level).\n• Alkaline Phosphatase (ALP) Test: Confirms pasteurization adequacy (destruction of ALP enzyme).\n• MBRT: Measures raw milk bacterial reduction rate.")
        ]),
        ("11.0 SANITATION ENGINEERING, CLEAN-IN-PLACE (CIP) & FOOD SAFETY", [
            ("Automated Clean-in-Place (CIP)",
             "5-stage cleaning: 1) Warm water pre-rinse, 2) Hot caustic soda (NaOH, 1.5–2%) at 80°C, 3) Intermediate water rinse, 4) Nitric acid wash (HNO3, 1%) at 65°C to remove milkstone, 5) Final sanitizing rinse with peracetic acid/hot water.\nCompliance with FSSAI regulations, ISO 22000, and HACCP critical control points.")
        ]),
        ("12.0 SOCIO-ECONOMIC IMPACT, AUTOMATION & SUSTAINABILITY", [
            ("Community Impact & Green Initiatives",
             "• Direct farmer payments and women empowerment in rural dairy husbandry.\n• PLC/SCADA automation ensuring high efficiency and low error rates.\n• Zero Liquid Discharge Effluent Treatment Plant (ETP) recycling treated water for cooling towers and gardening, and converting biogas to boiler energy.")
        ]),
        ("13.0 LEARNING OUTCOMES, RECOMMENDATIONS & CONCLUSION", [
            ("Learning Outcomes",
             "Observed industrial application of food microbiology, thermodynamics of pasteurization, cold chain logistics, and quality assurance."),
            ("Recommendations & Conclusion",
             "Encourage solar energy expansion, biodegradable packaging development, and consumer QR-code traceability. The visit to Hatsun Agro Product Nanguneri provided invaluable practical insights into large-scale dairy science.")
        ])
    ]

    for chap_title, chap_sections in chapters:
        h = doc.add_heading(chap_title, level=1)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(6)
        
        for sec_title, sec_text in chap_sections:
            h2 = doc.add_heading(sec_title, level=2)
            h2.paragraph_format.space_before = Pt(6)
            h2.paragraph_format.space_after = Pt(3)
            
            p_body = doc.add_paragraph(sec_text)
            p_body.paragraph_format.line_spacing = 1.15
            p_body.paragraph_format.space_after = Pt(6)

    doc.save(DOCX_PATH)
    print("DOCX updated without certificate at", DOCX_PATH)

if __name__ == "__main__":
    create_docx()
