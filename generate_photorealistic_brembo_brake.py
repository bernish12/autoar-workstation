import math
import os

def build_brembo_disc_brake_cad():
    lines = [
        "# ===========================================================================",
        "# AUTODESK / SOLIDWORKS EXPORT: 320MM VENTILATED FLOATING RACING DISC BRAKE",
        "# Subsystem: Brembo 4-Piston Monobloc Caliper & High-Carbon Steel Vented Rotor",
        "# Metrology Standard: ISO 9001 / IATF 16949 / Brembo Racing Spec",
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
            # Front (+Z)
            faces.append((base + i, base + segs + i, base + segs + i_next, base + i_next))
            # Back (-Z)
            faces.append((base + 2*segs + i, base + 2*segs + i_next, base + 3*segs + i_next, base + 3*segs + i))
            # Outer Rim
            faces.append((base + segs + i, base + 3*segs + i, base + 3*segs + i_next, base + segs + i_next))
            # Inner Bore
            faces.append((base + i, base + i_next, base + 2*segs + i_next, base + 2*segs + i))

    def add_box(center, size, rot_z=0.0):
        cx, cy, cz = center
        sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0
        base = len(verts) + 1
        
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

        faces.append((base+4, base+5, base+6, base+7)) # front (+Z)
        faces.append((base+1, base+0, base+3, base+2)) # back (-Z)
        faces.append((base+1, base+2, base+6, base+5)) # right (+X)
        faces.append((base+0, base+4, base+7, base+3)) # left (-X)
        faces.append((base+3, base+7, base+6, base+2)) # top (+Y)
        faces.append((base+0, base+1, base+5, base+4)) # bottom (-Y)

    # =========================================================================
    # STEP 1: WHEEL HUB & AXLE SPINDLE BEARING
    # =========================================================================
    start_object("Wheel_Hub_and_Spindle")
    add_cylinder(0, 0, -0.45, 0.35, 1.10, segs=32, axis='Z') # Axle spindle shaft
    add_cylinder(0, 0, -0.05, 0.54, 0.32, segs=32, axis='Z') # Inner bearing journal
    add_cylinder(0, 0, 0.16, 1.08, 0.22, segs=36, axis='Z')  # Main hub flange
    add_cylinder(0, 0, 0.38, 0.39, 0.36, segs=32, axis='Z')  # Center snout
    add_cylinder(0, 0, 0.58, 0.29, 0.08, segs=24, axis='Z')  # Grease dust cap

    # =========================================================================
    # STEP 2: BEARING CIRCLIP & 5X M12 WHEEL STUDS
    # =========================================================================
    start_object("Wheel_Studs_and_Lock_Circlip")
    # Retaining Circlip snap-ring seated in groove
    add_annular_disc(0, 0, -0.15, 0.48, 0.58, 0.04, segs=32)
    # 5 M12 Boron Steel Wheel Studs with chrome hex lug nuts
    for i in range(5):
        a = (i * 2 * math.pi) / 5
        sx = math.cos(a) * 0.72
        sy = math.sin(a) * 0.72
        add_cylinder(sx, sy, 0.28, 0.09, 0.06, segs=6, axis='Z')  # Stud hex base collar
        add_cylinder(sx, sy, 0.60, 0.065, 0.56, segs=16, axis='Z') # Threaded stud shank
        add_cylinder(sx, sy, 0.62, 0.095, 0.20, segs=6, axis='Z')  # Chrome Lug Nut

    # =========================================================================
    # STEP 3: ABS/ESC MULTIPOLE MAGNETIC TONE RING & ACTIVE HALL SENSOR
    # =========================================================================
    start_object("ABS_Tone_Ring_and_Hall_Sensor")
    # Multipole magnetic encoder ring on rear hub shoulder
    add_annular_disc(0, 0, -0.02, 0.56, 0.72, 0.05, segs=48)
    # 48 magnetic alternating poles (micro-ridges)
    for i in range(24):
        a = (i * 2 * math.pi) / 24
        add_cylinder(math.cos(a)*0.64, math.sin(a)*0.64, -0.02, 0.025, 0.055, segs=8, axis='Z')
    # Hall effect wheel speed sensor body
    add_box((-0.52, 0.48, -0.02), (0.16, 0.28, 0.14), rot_z=0.45)
    # Sensor probe tip positioned within 0.65mm of the tone ring
    add_cylinder(-0.44, 0.40, -0.02, 0.04, 0.12, segs=12, axis='X')
    # Sensor wiring harness cable
    add_cylinder(-0.62, 0.58, -0.02, 0.025, 0.35, segs=12, axis='Y')

    # =========================================================================
    # STEP 4: 320MM VENTILATED ROTOR DISC, FLOATING BELL & RACING SLOTS
    # =========================================================================
    start_object("Rotor_Hat_Anodized_Bell")
    # Central bell drum body in anodized gunmetal aluminum
    add_annular_disc(0, 0, 0.30, 0.76, 0.96, 0.32, segs=36)
    add_annular_disc(0, 0, 0.46, 0.39, 0.96, 0.08, segs=36) # Front mounting flange
    add_annular_disc(0, 0, 0.17, 0.94, 1.10, 0.08, segs=36) # Flange transition
    # 10 Floating Stainless Steel Bobbin Drive Bushings
    for i in range(10):
        a = (i * 2 * math.pi) / 10
        bx = math.cos(a) * 1.08
        by = math.sin(a) * 1.08
        add_cylinder(bx, by, 0.38, 0.045, 0.28, segs=12, axis='Z')
        add_cylinder(bx, by, 0.53, 0.065, 0.03, segs=12, axis='Z')

    start_object("Ventilated_Brake_Rotor_Vanes")
    # Front precision-ground friction disc track (r=1.04 to r=1.95, thickness 0.08, centered at z=0.50)
    add_annular_disc(0, 0, 0.50, 1.04, 1.95, 0.08, segs=64)
    # Outer precision chamfer rim (front)
    add_annular_disc(0, 0, 0.50, 1.93, 1.97, 0.076, segs=64)
    # Rear friction disc track (r=1.04 to r=1.95, thickness 0.08, centered at z=0.26)
    add_annular_disc(0, 0, 0.26, 1.04, 1.95, 0.08, segs=64)
    # Outer precision chamfer rim (rear)
    add_annular_disc(0, 0, 0.26, 1.93, 1.97, 0.076, segs=64)
    # 24 Internal Curved Directional Cooling Air Vanes (visible inside vent channels)
    for i in range(24):
        a = (i * 2 * math.pi) / 24
        vr = 1.50
        add_box((math.cos(a)*vr, math.sin(a)*vr, 0.38), (0.78, 0.05, 0.16), rot_z=a + 0.35)

    # =========================================================================
    # STEP 5: CALIPER ANCHOR MOUNTING BRACKET
    # =========================================================================
    start_object("Caliper_Mounting_Bracket")
    add_box((0.68, 1.62, 0.38), (1.70, 0.38, 0.58), rot_z=-0.35) # Main bridge
    add_box((0.10, 1.88, 0.16), (0.42, 0.62, 0.32), rot_z=-0.35) # Upper mounting ear
    add_box((1.24, 1.32, 0.16), (0.42, 0.62, 0.32), rot_z=-0.35) # Lower mounting ear
    add_box((0.68, 1.50, 0.55), (1.35, 0.12, 0.14), rot_z=-0.35) # Front abutment guide rail
    add_box((0.68, 1.50, 0.21), (1.35, 0.12, 0.14), rot_z=-0.35) # Rear abutment guide rail

    # =========================================================================
    # STEP 6: STAINLESS STEEL ANTI-RATTLE SHIMS & SPRING CLIPS
    # =========================================================================
    start_object("Stainless_AntiRattle_Shims_and_Spring_Clips")
    # Upper and lower pad slide stainless abutment clips
    add_box((0.14, 1.76, 0.38), (0.18, 0.22, 0.48), rot_z=-0.35)
    add_box((1.22, 1.26, 0.38), (0.18, 0.22, 0.48), rot_z=-0.35)
    # Pad retaining spring cross-clip on top bridge
    add_box((0.68, 1.82, 0.38), (1.20, 0.06, 0.44), rot_z=-0.35)
    add_cylinder(0.68, 1.82, 0.38, 0.028, 0.48, segs=12, axis='Z')

    # =========================================================================
    # STEP 7: DUAL CERAMIC BRAKE PADS (Outer & Inner)
    # =========================================================================
    start_object("Ceramic_Brake_Pads")
    # Outer Pad (Ceramic friction lining + Steel backing plate)
    add_box((0.68, 1.56, 0.56), (1.26, 0.42, 0.10), rot_z=-0.35)
    add_box((0.68, 1.56, 0.62), (1.40, 0.50, 0.04), rot_z=-0.35)
    add_cylinder(0.12, 1.76, 0.62, 0.04, 0.05, segs=12, axis='Z')
    add_cylinder(1.22, 1.28, 0.62, 0.04, 0.05, segs=12, axis='Z')

    # Inner Pad (Ceramic friction lining + Steel backing plate)
    add_box((0.68, 1.56, 0.20), (1.26, 0.42, 0.10), rot_z=-0.35)
    add_box((0.68, 1.56, 0.14), (1.40, 0.50, 0.04), rot_z=-0.35)
    add_cylinder(0.12, 1.76, 0.14, 0.04, 0.05, segs=12, axis='Z')
    add_cylinder(1.22, 1.28, 0.14, 0.04, 0.05, segs=12, axis='Z')

    # =========================================================================
    # STEP 8: BREMBO MONOBLOC 4-PISTON RACING RED CALIPER & CHROME PISTONS
    # =========================================================================
    start_object("Caliper_Cylinder_and_Housing_Red")
    # Outer Caliper Half with sculpted curves
    add_box((0.70, 1.62, 0.72), (1.80, 0.66, 0.22), rot_z=-0.35)
    add_box((0.70, 1.88, 0.68), (1.65, 0.18, 0.18), rot_z=-0.35)
    add_box((0.70, 1.36, 0.68), (1.65, 0.18, 0.18), rot_z=-0.35)
    # Inner Caliper Half
    add_box((0.70, 1.62, 0.05), (1.80, 0.66, 0.22), rot_z=-0.35)
    # Connecting arch bridges (leaves inspection window open)
    add_box((0.16, 1.90, 0.38), (0.42, 0.48, 0.50), rot_z=-0.35)
    add_box((1.20, 1.32, 0.38), (0.42, 0.48, 0.50), rot_z=-0.35)
    add_box((0.68, 1.86, 0.38), (0.46, 0.24, 0.50), rot_z=-0.35)

    start_object("Brembo_Dual_Hydraulic_Pistons")
    # 4 Chrome Machined Hydraulic Pistons (Twin 40mm Front & Rear)
    add_cylinder(0.42, 1.76, 0.84, 0.23, 0.08, segs=24, axis='Z')
    add_cylinder(0.96, 1.46, 0.84, 0.23, 0.08, segs=24, axis='Z')
    add_cylinder(0.42, 1.76, -0.07, 0.23, 0.08, segs=24, axis='Z')
    add_cylinder(0.96, 1.46, -0.07, 0.23, 0.08, segs=24, axis='Z')

    start_object("Brembo_Branding_Emblem")
    # Crisp White Brembo Lettering Badge on Caliper Face
    add_box((0.68, 1.62, 0.835), (0.95, 0.22, 0.015), rot_z=-0.35)

    # =========================================================================
    # STEP 9: GUIDE PIN SLIDER FASTENER BOLTS
    # =========================================================================
    start_object("Guide_Pin_Fastener_Bolts")
    # Upper Guide Pin Slider Bolt
    add_cylinder(0.08, 1.88, 0.84, 0.11, 0.14, segs=6, axis='Z')
    add_cylinder(0.08, 1.88, 0.76, 0.14, 0.04, segs=24, axis='Z')
    add_cylinder(0.08, 1.88, 0.46, 0.075, 0.58, segs=16, axis='Z')
    # Lower Guide Pin Slider Bolt
    add_cylinder(1.24, 1.32, 0.84, 0.11, 0.14, segs=6, axis='Z')
    add_cylinder(1.24, 1.32, 0.76, 0.14, 0.04, segs=24, axis='Z')
    add_cylinder(1.24, 1.32, 0.46, 0.075, 0.58, segs=16, axis='Z')

    # =========================================================================
    # STEP 10: BLEEDER SCREW, BANJO BOLT & HELIUM TEST PORT
    # =========================================================================
    start_object("Bleeder_Valve_and_Banjo_Line")
    # Bleeder screw nipple & hex valve nut
    add_cylinder(0.44, 2.08, 0.52, 0.045, 0.24, segs=16, axis='Y')
    add_cylinder(0.44, 2.20, 0.52, 0.07, 0.08, segs=6, axis='Y')
    add_cylinder(0.44, 2.26, 0.52, 0.05, 0.05, segs=12, axis='Y') # Rubber cap
    # Banjo Hydraulic Fluid Connector & crossover line
    add_cylinder(0.68, 1.95, 0.52, 0.035, 0.55, segs=12, axis='X')
    add_cylinder(0.96, 1.95, 0.52, 0.065, 0.12, segs=6, axis='Z') # Banjo bolt

    # =========================================================================
    # WRITE OUT OBJ FILE
    # =========================================================================
    for v in verts:
        lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")

    for idx, obj in enumerate(objects):
        obj_name = obj['name']
        start_f = obj['start_face']
        end_f = objects[idx + 1]['start_face'] if idx + 1 < len(objects) else len(faces)
        
        lines.append("")
        lines.append(f"o {obj_name}")
        lines.append(f"g {obj_name}")
        lines.append(f"usemtl mtl_{obj_name}")

        for f_i in range(start_f, end_f):
            f = faces[f_i]
            if len(f) == 3:
                lines.append(f"f {f[0]} {f[1]} {f[2]}")
            elif len(f) == 4:
                lines.append(f"f {f[0]} {f[1]} {f[2]} {f[3]}")

    return "\n".join(lines)

if __name__ == '__main__':
    content = build_brembo_disc_brake_cad()
    filename = "Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj"
    
    targets = [
        os.path.join(r"public\models", filename),
        os.path.join(r"dist\models", filename),
        os.path.join(r"sample_cad_models", filename),
    ]

    for p in targets:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding='utf-8') as f:
                f.write(content)
            print(f"Wrote {len(content)} bytes to {p}")
        except Exception as e:
            print(f"Error {p}: {e}")

    print("Photorealistic 10-Step Disc Brake CAD Assembly Finished!")
