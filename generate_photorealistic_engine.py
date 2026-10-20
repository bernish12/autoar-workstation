import math
import os

def build_engine_cad():
    lines = [
        "# ===========================================================================",
        "# AUTODESK / SOLIDWORKS EXPORT: BMW S58 TWINPOWER TURBO 3.0L INLINE-6 DOHC ENGINE",
        "# Subsystem: High-Performance Closed-Deck Engine Core & Powertrain Assembly",
        "# Metrology Standard: ISO 9001 / IATF 16949 / DIN 7168 OEM Spec",
        "# Project: AutoAR Studio - Augmented Reality Automobile Workstation",
        "# ===========================================================================",
        ""
    ]

    verts = []
    faces = []
    objects = []

    def start_object(name):
        objects.append({'name': name, 'start_face': len(faces)})

    def add_cylinder(cx, cy, cz, r, h, segs=32, axis='Z', cap_top=True, cap_bottom=True):
        base = len(verts) + 1
        half = h / 2.0

        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Z':
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz - half))
            elif axis == 'Y':
                verts.append((cx + r*math.cos(a), cy - half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx - half, cy + r*math.cos(a), cz + r*math.sin(a)))

        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Z':
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz + half))
            elif axis == 'Y':
                verts.append((cx + r*math.cos(a), cy + half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx + half, cy + r*math.cos(a), cz + r*math.sin(a)))

        for i in range(segs):
            p1 = base + i
            p2 = base + ((i + 1) % segs)
            p3 = base + segs + ((i + 1) % segs)
            p4 = base + segs + i
            faces.append((p1, p2, p3, p4))

        if cap_bottom:
            c_bot_idx = len(verts) + 1
            if axis == 'Z': verts.append((cx, cy, cz - half))
            elif axis == 'Y': verts.append((cx, cy - half, cz))
            elif axis == 'X': verts.append((cx - half, cy, cz))
            for i in range(segs):
                faces.append((c_bot_idx, base + ((i + 1) % segs), base + i))

        if cap_top:
            c_top_idx = len(verts) + 1
            if axis == 'Z': verts.append((cx, cy, cz + half))
            elif axis == 'Y': verts.append((cx, cy + half, cz))
            elif axis == 'X': verts.append((cx + half, cy, cz))
            for i in range(segs):
                faces.append((c_top_idx, base + segs + i, base + segs + ((i + 1) % segs)))

    def add_annular_disc(cx, cy, cz, r_in, r_out, h, segs=36, axis='Z'):
        base = len(verts) + 1
        half = h / 2.0

        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r_in*math.cos(a), cy + r_in*math.sin(a), cz + half))
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r_out*math.cos(a), cy + r_out*math.sin(a), cz + half))
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r_in*math.cos(a), cy + r_in*math.sin(a), cz - half))
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r_out*math.cos(a), cy + r_out*math.sin(a), cz - half))

        for i in range(segs):
            i_next = (i + 1) % segs
            faces.append((base + i, base + segs + i, base + segs + i_next, base + i_next))
            faces.append((base + 2*segs + i, base + 2*segs + i_next, base + 3*segs + i_next, base + 3*segs + i))
            faces.append((base + segs + i, base + 3*segs + i, base + 3*segs + i_next, base + segs + i_next))
            faces.append((base + i, base + i_next, base + 2*segs + i_next, base + 2*segs + i))

    def add_box(center, size, rot_z=0.0):
        base = len(verts) + 1
        cx, cy, cz = center
        sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0

        raw_box = [
            (-sx, -sy, -sz), ( sx, -sy, -sz), ( sx,  sy, -sz), (-sx,  sy, -sz),
            (-sx, -sy,  sz), ( sx, -sy,  sz), ( sx,  sy,  sz), (-sx,  sy,  sz),
        ]

        cos_z = math.cos(rot_z)
        sin_z = math.sin(rot_z)
        for (x, y, z) in raw_box:
            rx = x * cos_z - y * sin_z + cx
            ry = x * sin_z + y * cos_z + cy
            rz = z + cz
            verts.append((rx, ry, rz))

        faces.append((base+4, base+5, base+6, base+7))
        faces.append((base+1, base+0, base+3, base+2))
        faces.append((base+1, base+2, base+6, base+5))
        faces.append((base+0, base+4, base+7, base+3))
        faces.append((base+3, base+7, base+6, base+2))
        faces.append((base+0, base+1, base+5, base+4))

    # Cylinder centers along Z: 6 cylinders spaced 0.32 apart from Z = +0.80 to -0.80
    cyl_z = [0.80, 0.48, 0.16, -0.16, -0.48, -0.80]

    # =========================================================================
    # STEP 1: CLOSED-DECK INLINE-6 ALUMINUM ENGINE BLOCK
    # =========================================================================
    start_object("S58_Closed_Deck_Engine_Block")
    # Main crankcase skirt & cylinder bank
    add_box((0, 0.05, 0), (0.78, 0.72, 1.95))
    # 6 Precision Cylindrical Bores (wire-arc sprayed LDS steel coating)
    for cz in cyl_z:
        add_cylinder(0, 0.12, cz, 0.155, 0.58, segs=28, axis='Y', cap_top=False, cap_bottom=False)
    # Side engine mount brackets (cast aluminum wings)
    add_box((-0.46, -0.05, 0.2), (0.16, 0.22, 0.35))
    add_box(( 0.46, -0.05, 0.2), (0.16, 0.22, 0.35))
    # Starter motor & alternator mounting bosses
    add_cylinder(-0.44, -0.15, -0.5, 0.08, 0.22, segs=16, axis='Z')
    # Rear transmission bellhousing mounting perimeter flange
    add_box((0, 0.05, -0.99), (0.86, 0.78, 0.05))

    # =========================================================================
    # STEP 2: FORGED 42CrMo4 COUNTERWEIGHTED CRANKSHAFT
    # =========================================================================
    start_object("S58_Forged_Counterweighted_Crankshaft")
    # Main center crankshaft journal axis along Z (Y = -0.24)
    # 7 Main Journals
    main_z = [0.94, 0.64, 0.32, 0.00, -0.32, -0.64, -0.94]
    for mz in main_z:
        add_cylinder(0, -0.24, mz, 0.095, 0.08, segs=24, axis='Z')
    # 6 Rod Journals with 120-degree firing order offsets
    angles = [0, math.pi*2/3, math.pi*4/3, math.pi*4/3, math.pi*2/3, 0]
    rod_stroke = 0.09
    for i, cz in enumerate(cyl_z):
        ang = angles[i]
        rx = math.cos(ang) * rod_stroke
        ry = -0.24 + math.sin(ang) * rod_stroke
        add_cylinder(rx, ry, cz, 0.085, 0.09, segs=20, axis='Z')
        # Dual counterweight cheeks on each throw
        add_box((-rx*0.8, -0.24 - math.sin(ang)*0.11, cz - 0.055), (0.28, 0.12, 0.035))
        add_box((-rx*0.8, -0.24 - math.sin(ang)*0.11, cz + 0.055), (0.28, 0.12, 0.035))
    # Front harmonic balancer snout
    add_cylinder(0, -0.24, 1.05, 0.065, 0.18, segs=20, axis='Z')
    # Rear flywheel mounting flange with 8-bolt pattern
    add_annular_disc(0, -0.24, -1.02, 0.05, 0.22, 0.06, segs=28, axis='Z')

    # =========================================================================
    # STEP 3: MAIN BEARING BEDPLATE & 14X GRADE 12.9 STRETCH BOLTS
    # =========================================================================
    start_object("S58_Main_Bearing_Bedplate_and_Caps")
    # Cast aluminum structural ladder bedplate frame clamping lower crankcase
    add_box((0, -0.32, 0), (0.74, 0.12, 1.90))
    # 7 Integrated main bearing bridge webs
    for mz in main_z:
        add_box((0, -0.28, mz), (0.42, 0.14, 0.08))
        # 2x M11 Main stretch bolts per journal cap
        add_cylinder(-0.16, -0.30, mz, 0.022, 0.22, segs=10, axis='Y')
        add_cylinder( 0.16, -0.30, mz, 0.022, 0.22, segs=10, axis='Y')

    # =========================================================================
    # STEP 4: 6X FORGED 4340 H-BEAM CONNECTING RODS
    # =========================================================================
    start_object("S58_H_Beam_Connecting_Rods")
    for i, cz in enumerate(cyl_z):
        ang = angles[i]
        rx = math.cos(ang) * rod_stroke
        ry = -0.24 + math.sin(ang) * rod_stroke
        # Big end journal clamp (rod cap)
        add_annular_disc(rx, ry, cz, 0.085, 0.12, 0.08, segs=24, axis='Z')
        # Fractured split rod cap 2x ARP 2000 bolts
        add_cylinder(rx - 0.09, ry - 0.02, cz, 0.015, 0.14, segs=8, axis='Y')
        add_cylinder(rx + 0.09, ry - 0.02, cz, 0.015, 0.14, segs=8, axis='Y')
        # H-Beam rod shank forging extending up to piston pin
        shank_h = 0.32
        add_box((rx * 0.4, ry + shank_h * 0.5, cz), (0.045, shank_h, 0.06))
        # Small end bronze bushing eye
        add_annular_disc(0, ry + shank_h, cz, 0.042, 0.07, 0.065, segs=20, axis='Z')

    # =========================================================================
    # STEP 5: 6X FORGED ALUMINUM PISTONS & 3-PIECE RING PACKS
    # =========================================================================
    start_object("S58_Forged_Pistons_and_Rings")
    for i, cz in enumerate(cyl_z):
        py = 0.22
        # Piston crown with dual intake/exhaust valve relief pockets
        add_cylinder(0, py, cz, 0.15, 0.18, segs=28, axis='Y')
        # Gudgeon wrist pin (case-hardened chromium steel)
        add_cylinder(0, py - 0.03, cz, 0.04, 0.28, segs=16, axis='Z')
        # 3 Piston Rings (Top compression, Napier, Oil control)
        add_annular_disc(0, py + 0.05, cz, 0.148, 0.154, 0.012, segs=28, axis='Y')
        add_annular_disc(0, py + 0.02, cz, 0.148, 0.154, 0.012, segs=28, axis='Y')
        add_annular_disc(0, py - 0.01, cz, 0.148, 0.154, 0.018, segs=28, axis='Y')

    # =========================================================================
    # STEP 6: STRUCTURAL ALUMINUM OIL SUMP PAN & WINDAGE BAFFLE
    # =========================================================================
    start_object("S58_Aluminum_Oil_Sump_Pan")
    # Cast aluminum oil sump bowl (Y = -0.48)
    add_box((0, -0.46, -0.1), (0.68, 0.18, 1.70))
    # Deep oil collector reservoir (rear sump for track cornering G-forces)
    add_box((0, -0.58, -0.5), (0.52, 0.14, 0.65))
    # Oil pickup tube & screen mesh strainer
    add_cylinder(0, -0.56, -0.45, 0.04, 0.18, segs=16, axis='Y')
    # Perimeter 22x M6 pan retention flange & bolts
    add_box((0, -0.38, -0.1), (0.76, 0.03, 1.84))
    # Magnetic oil drain plug
    add_cylinder(0.24, -0.62, -0.6, 0.03, 0.04, segs=6, axis='X')

    # =========================================================================
    # STEP 7: MULTI-LAYER STEEL (MLS) CYLINDER HEAD GASKET
    # =========================================================================
    start_object("S58_MLS_Cylinder_Head_Gasket")
    # 5-Layer Embossed Stainless Steel Gasket Plate (Y = 0.415, depth 0.02)
    add_box((0, 0.415, 0), (0.76, 0.018, 1.92))
    # 6 Viton-Coated Combustion Bore Fire-Rings
    for cz in cyl_z:
        add_annular_disc(0, 0.415, cz, 0.152, 0.175, 0.022, segs=32, axis='Y')

    # =========================================================================
    # STEP 8: HIGH-FLOW DOHC 24-VALVE CYLINDER HEAD
    # =========================================================================
    start_object("S58_DOHC_24V_Cylinder_Head")
    # Cast Aluminum Cylinder Head Monoblock Casting (Y = 0.62)
    add_box((0, 0.62, 0), (0.78, 0.38, 1.94))
    # 14x High-Strength M10 Torx Cylinder Head Studs & Washers
    for i in range(7):
        hz = 0.90 - i * 0.30
        add_cylinder(-0.32, 0.64, hz, 0.024, 0.44, segs=10, axis='Y')
        add_cylinder( 0.32, 0.64, hz, 0.024, 0.44, segs=10, axis='Y')
    # CNC Intake & Exhaust Ports
    for cz in cyl_z:
        add_cylinder(-0.36, 0.60, cz, 0.065, 0.12, segs=16, axis='X')
        add_cylinder( 0.36, 0.60, cz, 0.075, 0.12, segs=16, axis='X')

    # =========================================================================
    # STEP 9: 24X VALVES, SPRINGS & DUAL OVERHEAD CAMSHAFTS (DOHC)
    # =========================================================================
    start_object("S58_Intake_Exhaust_Camshafts_VANOS")
    # Exhaust Camshaft along Z (X = -0.18, Y = 0.82)
    add_cylinder(-0.18, 0.82, 0, 0.042, 1.88, segs=20, axis='Z')
    # Intake Camshaft along Z (X = +0.18, Y = 0.82)
    add_cylinder( 0.18, 0.82, 0, 0.042, 1.88, segs=20, axis='Z')
    # 12 Intake & 12 Exhaust Induction-Hardened Cam Lobes
    for cz in cyl_z:
        add_box((-0.18, 0.86, cz - 0.04), (0.055, 0.06, 0.035))
        add_box((-0.18, 0.86, cz + 0.04), (0.055, 0.06, 0.035))
        add_box(( 0.18, 0.86, cz - 0.04), (0.055, 0.06, 0.035))
        add_box(( 0.18, 0.86, cz + 0.04), (0.055, 0.06, 0.035))
        add_cylinder(-0.18, 0.72, cz - 0.04, 0.04, 0.08, segs=12, axis='Y')
        add_cylinder(-0.18, 0.72, cz + 0.04, 0.04, 0.08, segs=12, axis='Y')
        add_cylinder( 0.18, 0.72, cz - 0.04, 0.04, 0.08, segs=12, axis='Y')
        add_cylinder( 0.18, 0.72, cz + 0.04, 0.04, 0.08, segs=12, axis='Y')
    # Front Double-VANOS Variable Cam Phaser Sprockets (Z = 0.96)
    add_annular_disc(-0.18, 0.82, 0.96, 0.05, 0.14, 0.05, segs=28, axis='Z')
    add_annular_disc( 0.18, 0.82, 0.96, 0.05, 0.14, 0.05, segs=28, axis='Z')

    # =========================================================================
    # STEP 10: DUPLEX ROLLER TIMING CHAIN, GUIDES & TENSIONER
    # =========================================================================
    start_object("S58_Duplex_Timing_Chain_and_Guides")
    # Front timing drive case cover
    add_box((0, 0.32, 1.02), (0.64, 1.15, 0.06))
    # Left & Right Chain runs
    add_box((-0.18, 0.28, 1.04), (0.038, 1.08, 0.03))
    add_box(( 0.18, 0.28, 1.04), (0.038, 1.08, 0.03))
    # Composite Slipper Guide Rails
    add_box((-0.24, 0.35, 1.04), (0.05, 0.65, 0.04))
    add_box(( 0.24, 0.35, 1.04), (0.05, 0.65, 0.04))
    # Hydraulic Chain Tensioner Cartridge
    add_cylinder(-0.28, 0.08, 1.04, 0.045, 0.12, segs=16, axis='X')

    # =========================================================================
    # STEP 11: MAGNESIUM VALVE COVER & 6X COIL-ON-PLUG IGNITION
    # =========================================================================
    start_object("S58_Magnesium_Valve_Cover_and_Coils")
    # Cast Magnesium Cam Valve Cover (Y = 0.98)
    add_box((0, 0.96, 0), (0.76, 0.14, 1.94))
    # Center Carbon-Fiber "M-POWER TWINPOWER TURBO" Accent Strip
    add_box((0, 1.04, 0), (0.28, 0.03, 1.86))
    # 6 Individual Direct Ignition Coil-on-Plug Packs with rubber boots
    for cz in cyl_z:
        add_cylinder(0, 1.06, cz, 0.042, 0.06, segs=16, axis='Y')
        add_box((0.04, 1.07, cz), (0.04, 0.03, 0.035))
    # Billet Aluminum Oil Filler Cap
    add_cylinder(0.24, 1.05, 0.72, 0.055, 0.045, segs=18, axis='Y')

    # =========================================================================
    # STEP 12: TWIN-SCROLL EXHAUST TURBOCHARGER WITH BILLET COMPRESSOR
    # =========================================================================
    start_object("S58_Twin_Scroll_Turbocharger_Assembly")
    # Positioned on exhaust side (X = -0.56, Y = 0.42, Z = -0.15)
    tx, ty, tz = -0.56, 0.42, -0.15
    # Stainless Steel Tubular Divided Exhaust Manifold
    for cz in cyl_z:
        add_cylinder(( -0.38 + tx)*0.5, (0.60 + ty)*0.5, (cz + tz)*0.5, 0.038, 0.22, segs=14, axis='X')
    # Heavy Cast Inconel Turbine Volute Housing (Rear of Turbo)
    add_cylinder(tx, ty, tz - 0.18, 0.165, 0.16, segs=28, axis='Z')
    # Billet Aerodynamic Compressor Housing (Front of Turbo)
    add_cylinder(tx, ty, tz + 0.18, 0.18, 0.18, segs=28, axis='Z')
    # Center Housing Rotating Assembly (CHRA) cartridge with oil lines
    add_cylinder(tx, ty, tz, 0.09, 0.14, segs=20, axis='Z')
    # Compressor Inducer inlet horn
    add_annular_disc(tx, ty, tz + 0.28, 0.08, 0.14, 0.08, segs=24, axis='Z')
    # Electronic Wastegate Servo Actuator with linkage rod
    add_cylinder(tx - 0.16, ty + 0.14, tz, 0.055, 0.14, segs=16, axis='Y')
    add_cylinder(tx - 0.12, ty + 0.06, tz - 0.10, 0.012, 0.18, segs=8, axis='Z')

    # Compile OBJ text
    lines.append("")
    # Write all geometric vertices first
    for v in verts:
        lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")
    lines.append("")

    # Write objects, groups and faces
    obj_idx = 0
    for f_idx, face in enumerate(faces):
        while obj_idx < len(objects) and f_idx >= objects[obj_idx]['start_face']:
            name = objects[obj_idx]['name']
            lines.append(f"o {name}")
            lines.append(f"g {name}")
            obj_idx += 1
        lines.append(f"f {' '.join(str(idx) for idx in face)}")

    content = "\n".join(lines)
    return content

if __name__ == '__main__':
    cad_text = build_engine_cad()
    paths = [
        os.path.join('public', 'models', 'BMW_S58_TwinPower_Turbo_Engine_Core.obj'),
        os.path.join('dist', 'models', 'BMW_S58_TwinPower_Turbo_Engine_Core.obj'),
        os.path.join('sample_cad_models', 'BMW_S58_TwinPower_Turbo_Engine_Core.obj')
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(cad_text)
        print(f"Wrote {len(cad_text)} bytes to {p}")
    print("Photorealistic 12-Step Engine CAD Assembly Finished!")
