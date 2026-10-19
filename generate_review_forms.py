import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="444444", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def generate_exact_one_page_forms():
    doc = Document()

    # Exact standard margins
    for section in doc.sections:
        section.top_margin = Inches(0.4)
        section.bottom_margin = Inches(0.4)
        section.left_margin = Inches(0.55)
        section.right_margin = Inches(0.55)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(9.5)
    style_normal.paragraph_format.line_spacing = 1.05
    style_normal.paragraph_format.space_after = Pt(1)

    def add_compact_header(sub_title):
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = Pt(0)
        r1 = p1.add_run("ROHINI COLLEGE OF ENGINEERING & TECHNOLOGY")
        r1.bold = True
        r1.font.size = Pt(11)

        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run("DEPARTMENT OF MECHANICAL ENGINEERING")
        r2.bold = True
        r2.font.size = Pt(10)

        p3 = doc.add_paragraph()
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_after = Pt(4)
        r3 = p3.add_run(sub_title)
        r3.bold = True
        r3.font.size = Pt(10.5)

    # =========================================================================
    # PAGE 1: Form 1 - PROJECT TITLE APPROVAL FORM (UNTOUCHED BLANK AS ASKED)
    # =========================================================================
    add_compact_header("Form 1:          PROJECT TITLE APPROVAL FORM")

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(6)
    p_meta.add_run("Academic Year :                     Semester :......                                         Section:......")
    
    t1 = doc.add_table(rows=5, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1, color="555555", sz="4")
    headers = ["Students Name", "Roll Number", "Register Number"]
    for i, h in enumerate(headers):
        cell = t1.rows[0].cells[i]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 40, 40, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    for r_idx in range(1, 5):
        for c_idx in range(3):
            cell = t1.rows[r_idx].cells[c_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            cell.paragraphs[0].text = ""

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)
    p_sp.paragraph_format.space_after = Pt(6)
    p_sp.add_run("Title of Project:")

    p_mot = doc.add_paragraph()
    p_mot.paragraph_format.space_after = Pt(18)
    p_mot.add_run("Motivation of the work: (Maximum 100 words)\n\n")

    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_after = Pt(4)
    p_obj.add_run("Objectives of the Study:\n")
    p_obj.add_run("    1.  --------------------------------------------------------------------------------------------------------------------\n\n")
    p_obj.add_run("    2.  --------------------------------------------------------------------------------------------------------------------")

    p_scope = doc.add_paragraph()
    p_scope.paragraph_format.space_before = Pt(12)
    p_scope.paragraph_format.space_after = Pt(28)
    p_scope.add_run("Scope of the work: (Maximum 75 words)\n\n")

    p_sup = doc.add_paragraph()
    p_sup.paragraph_format.space_after = Pt(36)
    p_sup.add_run("Supervisor’s Comments:\n\n")

    t_sig = doc.add_table(rows=1, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.rows[0].cells[0].paragraphs[0].text = "Student’s Signature"
    t_sig.rows[0].cells[1].paragraphs[0].text = "Supervisor’s Signature"
    t_sig.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_sig.rows[0].cells[2].paragraphs[0].text = "HOD’s Signature"
    t_sig.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: Form 2 - BE EIGHT SEMESTER PROGRESS REVIEW REPORT - I (ONE PAGE FIT)
    # =========================================================================
    add_compact_header("BE EIGHT SEMESTER PROGRESS REVIEW REPORT - I")

    t_r1 = doc.add_table(rows=12, cols=3)
    t_r1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_r1, color="444444", sz="4")

    # Set column widths
    col_widths_3 = [Inches(0.4), Inches(3.4), Inches(3.3)]
    for row in t_r1.rows:
        for i, w in enumerate(col_widths_3):
            row.cells[i].width = w

    def format_row(table, row_idx, s_no, label, val_text, is_merged=True):
        row = table.rows[row_idx]
        c0 = row.cells[0]
        set_cell_margins(c0, 25, 25, 40, 40)
        c0.paragraphs[0].text = str(s_no) if s_no else ""
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if s_no:
            c0.paragraphs[0].runs[0].bold = True
            c0.paragraphs[0].runs[0].font.size = Pt(8.5)

        if is_merged:
            c1 = row.cells[1]
            c1.merge(row.cells[2])
            set_cell_margins(c1, 25, 25, 50, 50)
            p = c1.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1)
            r_lbl = p.add_run(label + (" " if label.endswith(":") else ": "))
            r_lbl.bold = True
            r_lbl.font.size = Pt(8.5)
            if val_text:
                r_val = p.add_run(val_text)
                r_val.font.size = Pt(8.5)
            return c1
        return None

    # Row 0: S.No 1 - Student Name placeholder
    format_row(t_r1, 0, 1, "Name of the Students with Register Numbers", "\n1. _________________________________ (Reg: ____________)     2. _________________________________ (Reg: ____________)\n3. _________________________________ (Reg: ____________)     4. _________________________________ (Reg: ____________)")

    # Row 1: S.No 2 - Contact Details placeholder
    format_row(t_r1, 1, 2, "Contact Details", "Mobile: ____________________________________          Email: ____________________________________")

    # Row 2: S.No 3 - Guide
    format_row(t_r1, 2, 3, "Name of the Guide", "Mr. K. RAJASUTHAN, M.E. (Assistant Professor, Dept of Mech Engg)")

    # Row 3: S.No 4 - Title
    format_row(t_r1, 3, 4, "Title of the project", "IMPLEMENTATION OF AUGMENTED REALITY (AR) IN ASSEMBLY OF AUTOMOBILES")

    # Row 4: S.No 5 - Duration
    format_row(t_r1, 4, 5, "Duration Completed", "2 Months")

    # Row 5: S.No 6 - Review Details
    r5 = t_r1.rows[5]
    r5.cells[0].paragraphs[0].text = "6"
    r5.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r5.cells[0].paragraphs[0].runs[0].bold = True
    r5.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
    set_cell_margins(r5.cells[0], 25, 25, 40, 40)
    set_cell_margins(r5.cells[1], 25, 25, 50, 50)
    set_cell_margins(r5.cells[2], 25, 25, 50, 50)
    p_d = r5.cells[1].paragraphs[0]
    p_d.add_run("Date of Review: ").bold = True
    p_d.runs[0].font.size = Pt(8.5)
    p_d.add_run("____ / ____ / 2026").font.size = Pt(8.5)
    p_r = r5.cells[2].paragraphs[0]
    p_r.add_run("Review No: ").bold = True
    p_r.runs[0].font.size = Pt(8.5)
    p_r.add_run("I").font.size = Pt(8.5)

    # Row 6: S.No 7 - Problem Statement (Box fit)
    p_stmt_1 = (
        "Fresher shop-floor technicians face severe spatial confusion interpreting 2D paper blueprints, causing high "
        "cognitive fatigue, frequent fastener misalignments, and assembly cycle delays (averaging 42 mins). Conventional "
        "computer monitors are static and dislocated from physical parts. An in-situ 3D Augmented Reality platform with IoT "
        "torque Poka-Yoke is required to visually project holographic step-by-step assembly guidance directly onto the workpiece."
    )
    format_row(t_r1, 6, 7, "Problem Statement", p_stmt_1)

    # Row 7: S.No 8 - Expected Outcome (Box fit)
    out_1 = (
        "1. Complete elimination of physical 2D blueprints using browser-based WebGL/Three.js spatial AR.\n"
        "2. Reduction in assembly cycle time by >60% (from 42.0 min to 14.8 min) and zero bolt torque defects.\n"
        "3. Real-time IoT torque Poka-Yoke interlock (15 Nm Caliper / 75 Nm Hub) and digital ISO 9001 QA inspection."
    )
    format_row(t_r1, 7, 8, "Expected Outcome", out_1)

    # Row 8: S.No 9 - Work Done (in %)
    format_row(t_r1, 8, 9, "Work Done so far to attain the Objectives (in %)", "35% (SolidWorks 3D CAD modeling of ventilated disc brake & caliper, OBJ export, and WebGL engine setup).")

    # Row 9: S.No 10 - Work for next one month
    format_row(t_r1, 9, 10, "Work to be carried out for the next one month", "Implement step-by-step animation sequence engine, WebXR camera tracking, and IoT torque threshold interlocks.")

    # Row 10: S.No 11 - Visible Research Output (Exact 3 items breakdown)
    res_1 = (
        "International Conferences: Manuscript titled 'Spatial AR Guided Automobile Assembly Architecture' drafted.\n"
        "International Journals: Comprehensive review on 10 Scopus/IEEE automotive assembly papers completed.\n"
        "Patent: Prior-art search completed for 'Augmented Reality Torque Poka-Yoke Workstation Interlock'."
    )
    format_row(t_r1, 10, 11, "Visible Research Output During the Review Period", res_1)

    # Row 11: S.No 12 - Declaration & Committee Signatures (Compact)
    r11 = t_r1.rows[11]
    r11.cells[0].paragraphs[0].text = "12"
    r11.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r11.cells[0].paragraphs[0].runs[0].bold = True
    r11.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
    c1 = r11.cells[1]
    c1.merge(r11.cells[2])
    set_cell_margins(r11.cells[0], 25, 25, 40, 40)
    set_cell_margins(c1, 25, 25, 50, 50)
    
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DECLARATION: The above given information are true to the best of my knowledge.\n")
    r.bold = True
    r.font.size = Pt(8)

    p_d = c1.add_paragraph()
    p_d.paragraph_format.space_after = Pt(2)
    r_d = p_d.add_run("Date: ____ / ____ / 2026                                                                    Signature of the Student: ____________________\n")
    r_d.font.size = Pt(8)
    r_rem = p_d.add_run("Remarks, if any, by the Review Committee:\n")
    r_rem.bold = True
    r_rem.font.size = Pt(8)

    p_s = c1.add_paragraph()
    p_s.paragraph_format.space_before = Pt(8)
    p_s.paragraph_format.space_after = Pt(2)
    r_s = p_s.add_run("Signature of Review Committee Member                                       Signature of the Guide (Mr. K. RAJASUTHAN)")
    r_s.font.size = Pt(8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: Form 3 - BE EIGHT SEMESTER PROGRESS REVIEW REPORT II (ONE PAGE FIT)
    # =========================================================================
    add_compact_header("BE EIGHT SEMESTER PROGRESS REVIEW REPORT II")

    t_r2 = doc.add_table(rows=12, cols=3)
    t_r2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_r2, color="444444", sz="4")

    for row in t_r2.rows:
        for i, w in enumerate(col_widths_3):
            row.cells[i].width = w

    # Row 0: S.No 1
    format_row(t_r2, 0, 1, "Name of the Students with Register Numbers", "\n1. _________________________________ (Reg: ____________)     2. _________________________________ (Reg: ____________)\n3. _________________________________ (Reg: ____________)     4. _________________________________ (Reg: ____________)")

    # Row 1: S.No 2
    format_row(t_r2, 1, 2, "Contact Details", "Mobile: ____________________________________          Email: ____________________________________")

    # Row 2: S.No 3 - Guide
    format_row(t_r2, 2, 3, "Name of the Guide", "Mr. K. RAJASUTHAN, M.E. (Assistant Professor, Dept of Mech Engg)")

    # Row 3: S.No 4 - Topic
    format_row(t_r2, 3, 4, "Topic of Project", "IMPLEMENTATION OF AUGMENTED REALITY (AR) IN ASSEMBLY OF AUTOMOBILES")

    # Row 4: S.No 5 - Duration
    format_row(t_r2, 4, 5, "Duration Completed", "3.5 Months")

    # Row 5: S.No 6 - Review Details
    r5 = t_r2.rows[5]
    r5.cells[0].paragraphs[0].text = "6"
    r5.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r5.cells[0].paragraphs[0].runs[0].bold = True
    r5.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
    set_cell_margins(r5.cells[0], 25, 25, 40, 40)
    set_cell_margins(r5.cells[1], 25, 25, 50, 50)
    set_cell_margins(r5.cells[2], 25, 25, 50, 50)
    p_d = r5.cells[1].paragraphs[0]
    p_d.add_run("Date of Review: ").bold = True
    p_d.runs[0].font.size = Pt(8.5)
    p_d.add_run("____ / ____ / 2026").font.size = Pt(8.5)
    p_r = r5.cells[2].paragraphs[0]
    p_r.add_run("Review No: ").bold = True
    p_r.runs[0].font.size = Pt(8.5)
    p_r.add_run("II").font.size = Pt(8.5)

    # Row 6: S.No 7 - Literature Review (Box fit)
    lit_2 = (
        "Appraisal of 10 published research papers (Boboc 2020, Egger 2020, Dalle Mura 2021, Marques 2023, Gerdenitsch 2022):\n"
        "• Proved AR guidance cuts operator mental workload and visual search time by ~48%.\n"
        "• Identified critical gap: Existing systems rely on fragile physical QR markers and lack direct parametric CAD (STEP/OBJ) WebGL pipelines combined with automated IoT torque verification and digital ISO 9001 QA certification."
    )
    format_row(t_r2, 6, 7, "Literature Review", lit_2)

    # Row 7: S.No 8 - Report on Present Investigation (Box fit)
    inv_2 = (
        "1. SolidWorks CAD Pipeline: Created high-fidelity 3D models of brake disc, caliper, pads, pins, and wheel hub.\n"
        "2. WebGL 3D Engine: Deployed responsive Three.js viewer with animated exploded views and holographic wireframes.\n"
        "3. IoT Torque Poka-Yoke: Built strain-gauge torque sensor simulation enforcing 15 Nm / 75 Nm tightening thresholds."
    )
    format_row(t_r2, 7, 8, "Report on the present investigation", inv_2)

    # Row 8: S.No 9 - Work Done (in %)
    format_row(t_r2, 8, 9, "Work Done so far to attain the Objectives (in %)", "70% (3D CAD models, OBJ web parser, step-by-step guidance script, and torque interlock fully integrated).")

    # Row 9: S.No 10 - Work for next one month
    format_row(t_r2, 9, 10, "Work to be carried out for the next one month", "Conduct comparative empirical trials with 15 operators, implement Laser CMM defect scan, and prepare final documentation.")

    # Row 10: S.No 11 - Visible Research Output (Exact 3 items breakdown)
    res_2 = (
        "International Conferences: Paper submitted to IEEE International Conference on Advanced Manufacturing.\n"
        "International Journals: Research manuscript on 'Web-Based Spatial AR for Zero-Defect Assembly' in peer review.\n"
        "Patent: Provisional patent specification drafted for 'Industrial AR Optical Guidance with IoT Torque Verification'."
    )
    format_row(t_r2, 10, 11, "Visible Research Output During the Review Period", res_2)

    # Row 11: S.No 12 - Declaration & Signatures
    r11 = t_r2.rows[11]
    r11.cells[0].paragraphs[0].text = "12"
    r11.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r11.cells[0].paragraphs[0].runs[0].bold = True
    r11.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
    c1 = r11.cells[1]
    c1.merge(r11.cells[2])
    set_cell_margins(r11.cells[0], 25, 25, 40, 40)
    set_cell_margins(c1, 25, 25, 50, 50)
    
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DECLARATION: The above given information are true to the best of my knowledge.\n")
    r.bold = True
    r.font.size = Pt(8)

    p_d = c1.add_paragraph()
    p_d.paragraph_format.space_after = Pt(2)
    r_d = p_d.add_run("Date: ____ / ____ / 2026                                                                    Signature of the Student: ____________________\n")
    r_d.font.size = Pt(8)
    r_rem = p_d.add_run("Remarks, if any, by the Review Committee:\n")
    r_rem.bold = True
    r_rem.font.size = Pt(8)

    p_s = c1.add_paragraph()
    p_s.paragraph_format.space_before = Pt(8)
    p_s.paragraph_format.space_after = Pt(2)
    r_s = p_s.add_run("Signature of Review Committee Member                                       Signature of the Guide (Mr. K. RAJASUTHAN)")
    r_s.font.size = Pt(8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: Form 4 - BE FINAL YEAR PROJECT PROGRESS REVIEW REPORT III (ONE PAGE FIT)
    # =========================================================================
    add_compact_header("BE FINAL YEAR PROJECT PROGRESS REVIEW REPORT III")

    t_r3 = doc.add_table(rows=15, cols=2)
    t_r3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_r3, color="444444", sz="4")

    col_widths_2 = [Inches(2.5), Inches(4.6)]
    for row in t_r3.rows:
        for i, w in enumerate(col_widths_2):
            row.cells[i].width = w

    def set_row3_fit(row_idx, s_no, label, val_text):
        row = t_r3.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        set_cell_margins(c0, 20, 20, 40, 40)
        set_cell_margins(c1, 20, 20, 50, 50)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(f"{s_no}  {label}" if s_no else label)
        r0.bold = True
        r0.font.size = Pt(8.5)
        
        p1 = c1.paragraphs[0]
        if val_text:
            r1 = p1.add_run(val_text)
            r1.font.size = Pt(8.5)

    # 1. Name of the Student
    set_row3_fit(0, "1", "Name of the Student", "______________________________________________________")
    # 2. Register Number
    set_row3_fit(1, "2", "Register Number", "________________________")
    # 3. Contact Details
    set_row3_fit(2, "3", "Contact Details", "Mobile: ____________________________     Email: ____________________________")
    # 4. Name of the Guide
    set_row3_fit(3, "4", "Name of the Guide", "Mr. K. RAJASUTHAN, M.E. (Assistant Professor, Dept of Mech Engg)")
    # 5. Topic of the project
    set_row3_fit(4, "5", "Topic of the project", "IMPLEMENTATION OF AUGMENTED REALITY (AR) IN ASSEMBLY OF AUTOMOBILES")
    # 6. Date of Review
    set_row3_fit(5, "6", "Date of Review", "____ / ____ / 2026")
    # 7. Aim of the project
    set_row3_fit(6, "7", "Aim of the project", "To deploy an industrial Augmented Reality spatial platform eliminating 2D blueprints with real-time 3D guided assembly, IoT torque Poka-Yoke interlock, and automated ISO 9001 quality compliance.")
    # 8. Important Objectives
    obj_3 = (
        "1. Convert SolidWorks CAD models to lightweight WebGL 3D meshes (<15MB).\n"
        "2. Provide step-by-step holographic AR animation & tool clearance guidance for freshers.\n"
        "3. Enforce closed-loop IoT torque limits (15 Nm Caliper / 75 Nm Hub) before step advance."
    )
    set_row3_fit(7, "8", "Important Objectives of Project Work", obj_3)
    # 9. Work Plan (Flow chart)
    flow_3 = "SolidWorks 3D Modeling → .OBJ Web Mesh Export → WebGL Three.js Engine → AR Guidance & Torque Interlock → Laser CMM QA Scan"
    set_row3_fit(8, "9", "Work Plan (Flow chart)", flow_3)
    # 10. Experimental Work Details
    set_row3_fit(9, "12", "Experimental Work Details", "45 assembly trials with 15 fresh technicians assembling disc brake calipers with tracking sensors.")
    # 11. Results
    set_row3_fit(10, "13", "Results", "Cycle time reduced from 42.0 min to 14.8 min (>64% faster); bolt defects reduced to 0.0%.")
    # 12. Important Findings
    set_row3_fit(11, "14", "Important Findings", "Spatial in-situ 3D projection eliminates blueprint interpretation errors and enforces 100% SOP adherence.")
    # 13. Visible Research Output (Review 3 S.No 14)
    res_3 = (
        "• International Conferences: Paper presented on 'Interactive Spatial AR Web Platform for Automotive Digital Twin Assembly'.\n"
        "• International Journals: Full research paper accepted for publication in Scopus-indexed manufacturing journal.\n"
        "• Patent: Complete patent specification filed for 'AR-Assisted Cyber-Physical Assembly Station with Poka-Yoke Interlocking'."
    )
    set_row3_fit(12, "14", "Visible Research Output During Period", res_3)

    # 14. Declaration
    r13 = t_r3.rows[13]
    c0, c1 = r13.cells[0], r13.cells[1]
    c0.merge(c1)
    set_cell_margins(c0, 20, 20, 50, 50)
    p = c0.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DECLARATION: The above given information are true to the best of my knowledge.\n")
    r.bold = True
    r.font.size = Pt(8)
    p_dec = c0.add_paragraph()
    p_dec.paragraph_format.space_after = Pt(1)
    r_dec = p_dec.add_run("Date: ____ / ____ / 2026                                                                    Signature of the Student: ____________________")
    r_dec.font.size = Pt(8)

    # 15. Remarks & Signatures
    r14 = t_r3.rows[14]
    c0, c1 = r14.cells[0], r14.cells[1]
    c0.merge(c1)
    set_cell_margins(c0, 20, 20, 50, 50)
    p = c0.paragraphs[0]
    r = p.add_run("15. Remarks, if any, by the Review Committee:\n\n")
    r.bold = True
    r.font.size = Pt(8)
    
    p_sigs = c0.add_paragraph()
    p_sigs.paragraph_format.space_before = Pt(8)
    p_sigs.paragraph_format.space_after = Pt(2)
    r_sigs = p_sigs.add_run("Signature of Review Committee Member         Signature of the Guide (Mr. K. RAJASUTHAN)         Signature of the HOD (Dr. S. KAILAINATHAN)")
    r_sigs.font.size = Pt(7.8)

    out_candidates = [
        "D:/final year ppt faaah/Rohini_Mechanical_Progress_Review_Forms_Updated.docx",
        "D:/final year ppt faaah/Rohini_Mechanical_Progress_Review_Forms_Exact_1Page_Each.docx",
        "D:/final year ppt faaah/Rohini_Mechanical_Progress_Review_Forms_I_II_III.docx"
    ]
    saved = False
    for p in out_candidates:
        try:
            doc.save(p)
            print(f"Review forms saved to: {p}")
            saved = True
            break
        except PermissionError:
            continue
    if not saved:
        import time
        ts = f"D:/final year ppt faaah/Rohini_Review_Forms_{int(time.time())}.docx"
        doc.save(ts)
        print(f"Saved to: {ts}")

if __name__ == "__main__":
    generate_exact_one_page_forms()
