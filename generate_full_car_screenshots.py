import os
from PIL import Image, ImageDraw, ImageFont

def draw_solidworks_chrome(draw, w, h, title, active_tab="Assembly"):
    # SolidWorks top ribbon title bar
    draw.rectangle([0, 0, w, 32], fill=(36, 41, 46))
    draw.text((16, 8), f"SOLIDWORKS 2026 Premium - [{title}]", fill=(230, 235, 240))
    draw.text((w - 180, 8), "G. BERNISH | MECH-AUTO-TECH", fill=(56, 189, 248))
    
    # Menu Bar
    draw.rectangle([0, 32, w, 56], fill=(45, 52, 58))
    menus = ["File", "Edit", "View", "Insert", "Tools", "Assembly", "Simulation", "Motion Study", "Window", "Help"]
    cx = 16
    for m in menus:
        draw.text((cx, 38), m, fill=(210, 220, 230))
        cx += len(m) * 9 + 18
        
    # CommandManager Ribbon Tabs
    draw.rectangle([0, 56, w, 84], fill=(54, 62, 70))
    tabs = ["Features", "Sketch", "Evaluate", "Assembly", "Motion", "SOLIDWORKS MBD"]
    tx = 16
    for t in tabs:
        is_active = (t == active_tab)
        bg = (68, 78, 88) if is_active else (54, 62, 70)
        draw.rectangle([tx, 58, tx + len(t) * 9 + 14, 84], fill=bg)
        draw.text((tx + 8, 64), t, fill=(255, 255, 255) if is_active else (160, 175, 190))
        tx += len(t) * 9 + 20
        
    # Ribbon Tools Bar
    draw.rectangle([0, 84, w, 140], fill=(68, 78, 88))
    draw.line([0, 140, w, 140], fill=(30, 35, 40), width=2)
    
    # FeatureManager Design Tree (Left side)
    draw.rectangle([0, 140, 280, h - 28], fill=(38, 44, 50))
    draw.line([280, 140, 280, h - 28], fill=(50, 58, 66), width=2)
    draw.rectangle([0, 140, 280, 168], fill=(48, 56, 64))
    draw.text((12, 146), "FeatureManager: Assembly Components", fill=(255, 255, 255))
    
    # Status bar at bottom
    draw.rectangle([0, h - 28, w, h], fill=(32, 36, 42))
    draw.text((16, h - 20), "Editing Assembly • Fully Defined • MMGS (millimeter, gram, second) • ISO 9001 Standard", fill=(140, 160, 180))
    draw.text((w - 220, h - 20), "Status: 100% Passed (Zero Errors)", fill=(52, 211, 153))

def create_full_car_step1(output_path):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (26, 32, 44))
    draw = ImageDraw.Draw(img)
    draw_solidworks_chrome(draw, w, h, "FullCar_Chassis_Spaceframe_Drafting.SLDASM", "Sketch")
    
    # Feature Tree Items
    tree_items = [
        "[-] Full_Car_Assembly (Bernish)",
        "  |-- Front Plane", "  |-- Top Plane", "  |-- Right Plane", "  |-- Origin",
        "  [+] 3D_Sketch_Spaceframe_Rails",
        "  [+] SmartDimension_Wheelbase_2600mm",
        "  [+] SmartDimension_Track_1600mm",
        "  [+] Structural_Member_RollCage_45x2.5",
        "  [+] Honeycomb_Floorpan_Extrude",
        "  [+] Crash_Bumper_Box_Front_Rear"
    ]
    for i, item in enumerate(tree_items):
        draw.text((16, 180 + i * 22), item, fill=(200, 220, 240) if "Smart" not in item else (56, 189, 248))
        
    # Center Canvas: 2D/3D Spaceframe Chassis Wireframe Drafting
    cx, cy = 760, 420
    # Grid lines
    for gx in range(300, 1260, 40):
        draw.line([gx, 150, gx, 680], fill=(35, 43, 56), width=1)
    for gy in range(150, 680, 40):
        draw.line([300, gy, 1260, gy], fill=(35, 43, 56), width=1)
        
    # Main Spaceframe Rails
    draw.rectangle([cx - 320, cy - 80, cx + 320, cy + 80], outline=(0, 240, 255), width=3)
    draw.line([cx - 320, cy, cx + 320, cy], fill=(0, 200, 240), width=2)
    # Cross members
    for cm in [-240, -120, 0, 120, 240]:
        draw.line([cx + cm, cy - 80, cx + cm, cy + 80], fill=(0, 240, 255), width=2)
    # Diagonal braces
    draw.line([cx - 240, cy - 80, cx - 120, cy + 80], fill=(0, 180, 220), width=2)
    draw.line([cx - 120, cy - 80, cx, cy + 80], fill=(0, 180, 220), width=2)
    draw.line([cx, cy - 80, cx + 120, cy + 80], fill=(0, 180, 220), width=2)
    draw.line([cx + 120, cy - 80, cx + 240, cy + 80], fill=(0, 180, 220), width=2)
    
    # Roll cage profile
    draw.polygon([(cx - 140, cy - 80), (cx - 90, cy - 180), (cx + 90, cy - 180), (cx + 140, cy - 80)], outline=(245, 158, 11), width=3)
    draw.line([cx - 90, cy - 180, cx + 90, cy - 180], fill=(245, 158, 11), width=3)
    
    # Dimension Callouts
    draw.line([cx - 320, cy + 120, cx + 320, cy + 120], fill=(251, 191, 36), width=2)
    draw.text((cx - 70, cy + 128), "WHEELBASE = 2600.00 mm", fill=(251, 191, 36))
    draw.line([cx - 340, cy - 80, cx - 340, cy + 80], fill=(251, 191, 36), width=2)
    draw.text((cx - 430, cy - 6), "WIDTH = 1600.00 mm", fill=(251, 191, 36))
    
    # Title Tag
    draw.rectangle([w - 380, 160, w - 20, 240], fill=(15, 23, 42), outline=(0, 240, 255), width=2)
    draw.text((w - 365, 172), "SOLIDWORKS 2026: STEP 1 DRAFTING", fill=(0, 240, 255))
    draw.text((w - 365, 194), "Tubular Spaceframe 3D Parametric Sketch", fill=(255, 255, 255))
    draw.text((w - 365, 214), "Designer: G. BERNISH (MECH-AUTO-TECH)", fill=(16, 185, 129))
    
    img.save(output_path, quality=95)

def create_full_car_step2(output_path):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (24, 29, 38))
    draw = ImageDraw.Draw(img)
    draw_solidworks_chrome(draw, w, h, "FullCar_Powertrain_Marriage_Station.SLDASM", "Assembly")
    
    # Feature Tree Items
    tree_items = [
        "[-] Full_Car_Assembly (Bernish)",
        "  [+] Spaceframe_Chassis <Fixed>",
        "  [-] Powertrain_Marriage_Station",
        "    |-- Concentric_Mate_EngineCrankshaft",
        "    |-- Coincident_Mate_HydraulicMounts_4x",
        "    |-- Distance_Mate_FirewallClearance_45mm",
        "    |-- Parallel_Mate_TransaxleOutputFlange",
        "  [+] V8_Engine_Block_TwinTurbo",
        "  [+] 7Speed_DualClutch_Transaxle",
        "  [+] Quad_Inconel_Exhaust_Headers"
    ]
    for i, item in enumerate(tree_items):
        draw.text((16, 180 + i * 22), item, fill=(200, 220, 240) if "Mate" not in item else (251, 191, 36))
        
    cx, cy = 760, 420
    # Spaceframe ghost outline
    draw.rectangle([cx - 320, cy - 100, cx + 320, cy + 100], outline=(70, 85, 105), width=2)
    
    # Engine Block 3D CAD representation (Cast Aluminum Shaded)
    draw.rectangle([cx - 80, cy - 70, cx + 120, cy + 70], fill=(100, 116, 139), outline=(148, 163, 184), width=3)
    # Cylinder heads V-shape
    draw.polygon([(cx - 70, cy - 60), (cx - 40, cy - 110), (cx + 20, cy - 110), (cx - 10, cy - 60)], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw.polygon([(cx + 30, cy - 60), (cx + 60, cy - 110), (cx + 120, cy - 110), (cx + 90, cy - 60)], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    # Transmission casing
    draw.rectangle([cx - 180, cy - 50, cx - 80, cy + 50], fill=(71, 85, 105), outline=(148, 163, 184), width=2)
    # Exhaust headers curving out
    draw.line([cx - 20, cy + 40, cx - 180, cy + 90], fill=(245, 158, 11), width=4)
    draw.line([cx + 60, cy + 40, cx - 180, cy + 110], fill=(245, 158, 11), width=4)
    
    # Hydraulic Marriage Lift Arrows
    draw.polygon([(cx + 20, cy + 190), (cx + 20, cy + 130), (cx - 10, cy + 130), (cx + 20, cy + 90), (cx + 50, cy + 130), (cx + 20, cy + 130)], fill=(16, 185, 129), outline=(255, 255, 255))
    draw.text((cx + 60, cy + 120), "VEHICLE MARRIAGE HYDRAULIC DOCKING", fill=(16, 185, 129))
    
    # Title Tag
    draw.rectangle([w - 400, 160, w - 20, 240], fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((w - 385, 172), "SOLIDWORKS 2026: STEP 2 MARRIAGE", fill=(16, 185, 129))
    draw.text((w - 385, 194), "Mid-Engine V8 Powertrain & Transaxle Docking", fill=(255, 255, 255))
    draw.text((w - 385, 214), "Designer: G. BERNISH (MECH-AUTO-TECH)", fill=(56, 189, 248))
    
    img.save(output_path, quality=95)

def create_full_car_step3(output_path):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (20, 25, 34))
    draw = ImageDraw.Draw(img)
    draw_solidworks_chrome(draw, w, h, "FullCar_Suspension_and_Body_Assembly.SLDASM", "Assembly")
    
    # Feature Tree Items
    tree_items = [
        "[-] Full_Car_Assembly (Bernish)",
        "  [+] Spaceframe_Chassis <Fixed>",
        "  [+] Powertrain_Marriage_Unit",
        "  [-] Front_Rear_Suspension_Subframes",
        "    |-- Double_Wishbone_A-Arms (4-Corner)",
        "    |-- Racing_Coilovers_YellowSprings",
        "    |-- SteeringRack_Electronic_PAS",
        "  [+] Ventilated_DiscBrake_Corners (4x)",
        "  [-] Aerodynamic_Carbon_Body_Shell",
        "    |-- Surface_Loft_Hood_Splitter",
        "    |-- Glass_Cockpit_Canopy",
        "    |-- GT_Wing_Spoiler_Carbon_Downforce"
    ]
    for i, item in enumerate(tree_items):
        draw.text((16, 180 + i * 22), item, fill=(200, 220, 240) if "Carbon" not in item else (56, 189, 248))
        
    cx, cy = 760, 420
    # 4 Wheels CAD representation
    wheels = [(cx - 240, cy - 130), (cx + 240, cy - 130), (cx - 240, cy + 130), (cx + 240, cy + 130)]
    for wx, wy in wheels:
        draw.ellipse([wx - 35, wy - 35, wx + 35, wy + 35], fill=(30, 41, 59), outline=(148, 163, 184), width=3)
        draw.ellipse([wx - 22, wy - 22, wx + 22, wy + 22], fill=(71, 85, 105), outline=(0, 240, 255), width=2)
        # Red Caliper
        draw.rectangle([wx - 26, wy - 10, wx - 16, wy + 10], fill=(239, 68, 68))
        
    # Sculpted Sports Car Body Shell Outline
    draw.polygon([
        (cx - 300, cy - 60), (cx - 260, cy - 110), (cx - 140, cy - 115), 
        (cx - 60, cy - 80), (cx + 100, cy - 80), (cx + 200, cy - 115),
        (cx + 290, cy - 100), (cx + 310, cy - 50), (cx + 310, cy + 50),
        (cx + 290, cy + 100), (cx + 200, cy + 115), (cx + 100, cy + 80),
        (cx - 60, cy + 80), (cx - 140, cy + 115), (cx - 260, cy + 110),
        (cx - 300, cy + 60)
    ], fill=(14, 116, 144, 180), outline=(56, 189, 248), width=3)
    
    # Windshield / Cockpit
    draw.polygon([(cx - 70, cy - 50), (cx + 70, cy - 50), (cx + 50, cy + 50), (cx - 50, cy + 50)], fill=(15, 23, 42), outline=(0, 240, 255), width=2)
    # Rear GT Spoiler
    draw.rectangle([cx - 320, cy - 80, cx - 305, cy + 80], fill=(245, 158, 11), outline=(255, 255, 255), width=2)
    draw.text((cx - 390, cy - 8), "GT WING", fill=(245, 158, 11))
    
    # Title Tag
    draw.rectangle([w - 400, 160, w - 20, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.text((w - 385, 172), "SOLIDWORKS 2026: STEP 3 BODY & WHEELS", fill=(56, 189, 248))
    draw.text((w - 385, 194), "Carbon Monocoque Shell & 4-Corner Integration", fill=(255, 255, 255))
    draw.text((w - 385, 214), "Designer: G. BERNISH (MECH-AUTO-TECH)", fill=(16, 185, 129))
    
    img.save(output_path, quality=95)

def create_full_car_step4(output_path):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (245, 248, 252)) # Standard ISO A1 Blueprint paper background
    draw = ImageDraw.Draw(img)
    
    # Outer Border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(15, 23, 42), width=3)
    draw.rectangle([28, 28, w - 28, h - 28], outline=(15, 23, 42), width=1)
    
    # Title Block (Bottom Right)
    tb_x, tb_y = w - 460, h - 140
    draw.rectangle([tb_x, tb_y, w - 28, h - 28], fill=(255, 255, 255), outline=(15, 23, 42), width=2)
    draw.line([tb_x, tb_y + 35, w - 28, tb_y + 35], fill=(15, 23, 42), width=1)
    draw.line([tb_x, tb_y + 70, w - 28, tb_y + 70], fill=(15, 23, 42), width=1)
    draw.line([tb_x + 220, tb_y, tb_x + 220, tb_y + 70], fill=(15, 23, 42), width=1)
    
    draw.text((tb_x + 10, tb_y + 8), "DRAWING NO: AR-AUTO-FULLCAR-2026", fill=(15, 23, 42))
    draw.text((tb_x + 230, tb_y + 8), "REV: A03 (PRODUCTION)", fill=(15, 23, 42))
    draw.text((tb_x + 10, tb_y + 44), "TITLE: FULL VEHICLE MASTER ASSEMBLY", fill=(15, 23, 42))
    draw.text((tb_x + 230, tb_y + 44), "SCALE: 1:10 (METRIC)", fill=(15, 23, 42))
    draw.text((tb_x + 10, tb_y + 82), "CHIEF DESIGN ENGINEER: G. BERNISH", fill=(2, 132, 199))
    draw.text((tb_x + 230, tb_y + 82), "IATF 16949 / ISO 9001 COMPLIANT", fill=(5, 150, 105))
    
    # BOM Table (Top Right)
    bom_x, bom_y = w - 460, 40
    draw.rectangle([bom_x, bom_y, w - 28, 300], fill=(255, 255, 255), outline=(15, 23, 42), width=2)
    draw.rectangle([bom_x, bom_y, w - 28, bom_y + 26], fill=(226, 232, 240))
    draw.text((bom_x + 10, bom_y + 6), "ITEM | PART NAME | QTY | MATERIAL", fill=(15, 23, 42))
    
    bom_rows = [
        " 01   Tubular Spaceframe Chassis   01   4130 Chromoly Steel",
        " 02   Mid-Engine V8 Powertrain     01   Cast A356 Al Alloy",
        " 03   7-Speed Dual-Clutch Trans    01   Forged Alloy Magnesium",
        " 04   Double Wishbone Subframe     04   Forged 6061-T6 Al",
        " 05   Racing Coilovers & Dampers   04   High-Tensile Spring Steel",
        " 06   Ventilated Brake Rotors 380  04   G3000 Gray Cast Iron",
        " 07   Brembo 6-Piston Calipers     04   Forged Aluminum Monoblock",
        " 08   Carbon-Composite Body Shell  01   Pre-preg Carbon Fiber",
        " 09   Forged 5-Spoke Alloy Wheels  04   Forged 6061-T6 Rim",
        " 10   Performance Radial Tires     04   Silica-Infused Rubber"
    ]
    for r_i, r_text in enumerate(bom_rows):
        draw.line([bom_x, bom_y + 26 + (r_i + 1) * 23, w - 28, bom_y + 26 + (r_i + 1) * 23], fill=(226, 232, 240), width=1)
        draw.text((bom_x + 8, bom_y + 30 + r_i * 23), r_text, fill=(30, 41, 59))
        
    # Center-Left: Exploded Orthographic Blueprint Views
    # Top View
    draw.text((50, 50), "SECTION A-A: PLAN VIEW & EXPLODED CHASSIS ALIGNMENT", fill=(15, 23, 42))
    draw.rectangle([80, 80, 540, 240], outline=(15, 23, 42), width=2)
    draw.line([80, 160, 540, 160], fill=(2, 132, 199), width=1) # Centerline
    # Side View
    draw.text((50, 280), "ELEVATION VIEW: POWERTRAIN TO CHASSIS DATUM", fill=(15, 23, 42))
    draw.rectangle([80, 310, 540, 460], outline=(15, 23, 42), width=2)
    # Front View
    draw.text((50, 500), "FRONT TRACK VIEW: CAMBER & CASTER GEOMETRY (-1.5 DEG)", fill=(15, 23, 42))
    draw.rectangle([80, 530, 320, 670], outline=(15, 23, 42), width=2)
    
    # Official QA Stamp
    draw.rectangle([w - 420, h - 210, w - 240, h - 155], outline=(5, 150, 105), width=2)
    draw.text((w - 410, h - 200), "SOLIDWORKS CAD", fill=(5, 150, 105))
    draw.text((w - 410, h - 180), "APPROVED & RELEASED", fill=(5, 150, 105))
    draw.text((w - 410, h - 165), "OCT 12, 2026 • G. BERNISH", fill=(5, 150, 105))
    
    img.save(output_path, quality=95)

if __name__ == '__main__':
    target_dir = "D:/solidworks"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    p1 = os.path.join(target_dir, "FullCar_Step1_SolidWorks_Chassis_Spaceframe_Drafting.jpg")
    p2 = os.path.join(target_dir, "FullCar_Step2_SolidWorks_Powertrain_Marriage_Station.jpg")
    p3 = os.path.join(target_dir, "FullCar_Step3_SolidWorks_Suspension_and_Body_Assembly.jpg")
    p4 = os.path.join(target_dir, "FullCar_Step4_SolidWorks_Exploded_Vehicle_BOM_Blueprint.jpg")
    
    create_full_car_step1(p1)
    create_full_car_step2(p2)
    create_full_car_step3(p3)
    create_full_car_step4(p4)
    print("All 4 Full Car SolidWorks CAD Screenshots created in D:\\solidworks\\ successfully!")
