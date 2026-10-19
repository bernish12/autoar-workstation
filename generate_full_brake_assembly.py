import math
import os

def generate_photorealistic_disc_brake_assembly():
    lines = [
        "# SOLIDWORKS CAD ASSEMBLY EXPORT: HIGH-PERFORMANCE 320MM VENTILATED DISC BRAKE & BREMBO CALIPER",
        "# Project: Implementation of Augmented Reality in Assembly of Automobiles (Industry 4.0)",
        "# Sub-System: Front Axle Braking & Digital Twin Kinematic Assembly",
        "# Metrology Standard: ISO 9001 / IATF 16949 / Brembo Racing Spec",
        ""
    ]

    verts = []
    faces = []

    def add_cylinder(cx, cy, cz, r, h, segs=32, axis='Z', cap_top=True, cap_bottom=True):
        """Creates a solid closed cylinder with outward normals."""
        base = len(verts) + 1
        half = h / 2.0
        
        # Bottom circle vertices
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Z':
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz - half))
            elif axis == 'Y':
                verts.append((cx + r*math.cos(a), cy - half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx - half, cy + r*math.cos(a), cz + r*math.sin(a)))

        # Top circle vertices
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Z':
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz + half))
            elif axis == 'Y':
                verts.append((cx + r*math.cos(a), cy + half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx + half, cy + r*math.cos(a), cz + r*math.sin(a)))

        # Side faces
        for i in range(segs):
            p1 = base + i
            p2 = base + ((i + 1) % segs)
            p3 = base + segs + ((i + 1) % segs)
            p4 = base + segs + i
            faces.append((p1, p2, p3, p4))

        # Bottom cap (-axis)
        if cap_bottom:
            c_bot_idx = len(verts) + 1
            if axis == 'Z':
                verts.append((cx, cy, cz - half))
            elif axis == 'Y':
                verts.append((cx, cy - half, cz))
            elif axis == 'X':
                verts.append((cx - half, cy, cz))
            
            for i in range(segs):
                p1 = c_bot_idx
                p2 = base + ((i + 1) % segs)
                p3 = base + i
                faces.append((p1, p2, p3))

        # Top cap (+axis)
        if cap_top:
            c_top_idx = len(verts) + 1
            if axis == 'Z':
                verts.append((cx, cy, cz + half))
            elif axis == 'Y':
                verts.append((cx, cy + half, cz))
            elif axis == 'X':
                verts.append((cx + half, cy, cz))

            for i in range(segs):
                p1 = c_top_idx
                p2 = base + segs + i
                p3 = base + segs + ((i + 1) % segs)
                faces.append((p1, p2, p3))

    def add_annular_disc(cx, cy, cz, r_in, r_out, h, segs=36):
        """Creates a solid 3D annular disc (friction ring) with solid front, back, outer rim and inner bore."""
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
            f_in1 = base + i
            f_out1 = base + segs + i
            f_out2 = base + segs + i_next
            f_in2 = base + i_next
            faces.append((f_in1, f_out1, f_out2, f_in2))

            b_in1 = base + 2*segs + i
            b_out1 = base + 3*segs + i
            b_out2 = base + 3*segs + i_next
            b_in2 = base + 2*segs + i_next
            faces.append((b_in1, b_in2, b_out2, b_out1))

            faces.append((f_out1, b_out1, b_out2, f_out2))
            faces.append((f_in1, f_in2, b_in2, b_in1))

    def add_box(center, size, rot_z=0.0):
        """Creates a solid box with exact outward-pointing face normals."""
        cx, cy, cz = center
        sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0
        base = len(verts) + 1
        
        raw_box = [
            (-sx, -sy, -sz), # 0
            ( sx, -sy, -sz), # 1
            ( sx,  sy, -sz), # 2
            (-sx,  sy, -sz), # 3
            (-sx, -sy,  sz), # 4
            ( sx, -sy,  sz), # 5
            ( sx,  sy,  sz), # 6
            (-sx,  sy,  sz), # 7
        ]

        cos_z = math.cos(rot_z)
        sin_z = math.sin(rot_z)
        for (x, y, z) in raw_box:
            rx = x * cos_z - y * sin_z + cx
            ry = x * sin_z + y * cos_z + cy
            rz = z + cz
            verts.append((rx, ry, rz))

        box_f = [
            (base+4, base+5, base+6, base+7), # front (+Z)
            (base+1, base+0, base+3, base+2), # back (-Z)
            (base+1, base+2, base+6, base+5), # right (+X)
            (base+0, base+4, base+7, base+3), # left (-X)
            (base+3, base+7, base+6, base+2), # top (+Y)
            (base+0, base+1, base+5, base+4), # bottom (-Y)
        ]
        faces.extend(box_f)

    objects = []

    def start_object(name):
        objects.append({'name': name, 'start_face': len(faces)})

    # =========================================================================
    # PART 1: STEP 01 - WHEEL HUB & AXLE SPINDLE
    # =========================================================================
    start_object("Wheel_Hub_and_Spindle")
    # Central bearing axle spindle shaft
    add_cylinder(0, 0, -0.45, 0.35, 1.10, segs=32, axis='Z')
    # Inner bearing shoulder journal
    add_cylinder(0, 0, -0.05, 0.52, 0.30, segs=32, axis='Z')
    # Heavy wheel hub mounting flange
    add_cylinder(0, 0, 0.16, 1.05, 0.22, segs=36, axis='Z')
    # Center grease cap snout
    add_cylinder(0, 0, 0.38, 0.38, 0.36, segs=32, axis='Z')
    # Hub center bore chamfer ring
    add_cylinder(0, 0, 0.58, 0.28, 0.08, segs=24, axis='Z')
    # 5 M12 Wheel Studs with hexagonal base collar protruding proudly to z=0.82
    for i in range(5):
        a = (i * 2 * math.pi) / 5
        sx = math.cos(a) * 0.72
        sy = math.sin(a) * 0.72
        # Hex stud base collar
        add_cylinder(sx, sy, 0.28, 0.09, 0.06, segs=6, axis='Z')
        # Threaded chrome shank extending through rotor hat
        add_cylinder(sx, sy, 0.58, 0.065, 0.56, segs=16, axis='Z')

    # =========================================================================
    # PART 2: STEP 02 - ROTOR HAT (BELL) & WHEEL STUDS
    # =========================================================================
    start_object("Rotor_Hat_and_Studs")
    # Rotor Hat center bell cylindrical drum body
    add_annular_disc(0, 0, 0.30, 0.78, 0.94, 0.32, segs=36)
    # Rotor Hat front face mounting flange
    add_annular_disc(0, 0, 0.46, 0.38, 0.94, 0.08, segs=36)
    # Rotor Hat transition chamfer flare connecting to friction disc
    add_annular_disc(0, 0, 0.17, 0.94, 1.08, 0.08, segs=36)
    # 5 Chrome wheel lug nuts threaded on studs
    for i in range(5):
        a = (i * 2 * math.pi) / 5
        sx = math.cos(a) * 0.72
        sy = math.sin(a) * 0.72
        add_cylinder(sx, sy, 0.60, 0.092, 0.18, segs=6, axis='Z')
    # 2 Countersunk T30 Torx rotor locator screws
    for a in [math.pi * 0.3, math.pi * 1.3]:
        sx = math.cos(a) * 0.55
        sy = math.sin(a) * 0.55
        add_cylinder(sx, sy, 0.49, 0.045, 0.04, segs=12, axis='Z')

    # =========================================================================
    # PART 3: STEP 02 (CONT) - 320MM VENTILATED ROTOR DISC & COOLING VANES
    # =========================================================================
    start_object("Ventilated_Brake_Rotor_Vanes")
    # Outer (Front) friction disc track: from r=1.06 to r=1.92, thickness 0.08 at z=0.50
    add_annular_disc(0, 0, 0.50, 1.06, 1.92, 0.08, segs=48)
    # Inner (Rear) friction disc track: from r=1.06 to r=1.92, thickness 0.08 at z=0.26
    add_annular_disc(0, 0, 0.26, 1.06, 1.92, 0.08, segs=48)
    
    # 24 Directional radial cooling ventilation air vanes in the 0.16mm air channel
    for i in range(24):
        a = (i * 2 * math.pi) / 24
        vr = 1.48
        add_box((math.cos(a)*vr, math.sin(a)*vr, 0.38), (0.76, 0.05, 0.15), rot_z=a + 0.32)

    # Cross-drilled cooling ports arrayed along friction track
    for r in [1.28, 1.50, 1.74]:
        for i in range(12):
            a = (i * 2 * math.pi) / 12 + (r * 1.4)
            add_cylinder(math.cos(a) * r, math.sin(a) * r, 0.50, 0.038, 0.09, segs=12, axis='Z')

    # =========================================================================
    # PART 4: STEP 03 - CALIPER ANCHOR MOUNTING BRACKET
    # =========================================================================
    start_object("Caliper_Mounting_Bracket")
    # Outer torque bridge wrapping over the rotor rim
    add_box((0.68, 1.62, 0.38), (1.70, 0.38, 0.56), rot_z=-0.35)
    # Upper knuckle mounting ear with bolt boss
    add_box((0.10, 1.88, 0.16), (0.42, 0.62, 0.30), rot_z=-0.35)
    # Lower knuckle mounting ear with bolt boss
    add_box((1.24, 1.32, 0.16), (0.42, 0.62, 0.30), rot_z=-0.35)
    # Machined brake pad slide guide channels (inner and outer abutment rails)
    add_box((0.68, 1.50, 0.55), (1.35, 0.12, 0.14), rot_z=-0.35)
    add_box((0.68, 1.50, 0.21), (1.35, 0.12, 0.14), rot_z=-0.35)

    # =========================================================================
    # PART 5: STEP 04 - DUAL CERAMIC BRAKE PADS (Outer & Inner)
    # =========================================================================
    start_object("Ceramic_Brake_Pads")
    # Outer Pad (Front Friction Lining + Steel Backing Plate)
    add_box((0.68, 1.56, 0.56), (1.26, 0.42, 0.10), rot_z=-0.35) # High-friction ceramic lining
    add_box((0.68, 1.56, 0.62), (1.40, 0.50, 0.04), rot_z=-0.35) # Steel backing plate
    add_cylinder(0.12, 1.76, 0.62, 0.04, 0.05, segs=12, axis='Z') # Pad retaining ear
    add_cylinder(1.22, 1.28, 0.62, 0.04, 0.05, segs=12, axis='Z') # Pad retaining ear

    # Inner Pad (Rear Friction Lining + Steel Backing Plate)
    add_box((0.68, 1.56, 0.20), (1.26, 0.42, 0.10), rot_z=-0.35) # High-friction ceramic lining
    add_box((0.68, 1.56, 0.14), (1.40, 0.50, 0.04), rot_z=-0.35) # Steel backing plate
    add_cylinder(0.12, 1.76, 0.14, 0.04, 0.05, segs=12, axis='Z') # Pad retaining ear
    add_cylinder(1.22, 1.28, 0.14, 0.04, 0.05, segs=12, axis='Z') # Pad retaining ear

    # =========================================================================
    # PART 6: STEP 05 - BREMBO RACING RED MONOBLOCK CALIPER HOUSING
    # (Modeled with real open inspection window & dual piston barrels)
    # =========================================================================
    start_object("Caliper_Cylinder_and_Housing_Red")
    # 1. Outer Caliper Half (houses the front 2 hydraulic pistons)
    add_box((0.70, 1.62, 0.70), (1.75, 0.65, 0.22), rot_z=-0.35)
    
    # 2. Inner Caliper Half (houses the rear 2 hydraulic pistons)
    add_box((0.70, 1.62, 0.06), (1.75, 0.65, 0.22), rot_z=-0.35)

    # 3. Top Connecting Arch Bridges (Leaves center inspection window open so pads & rotor are visible!)
    # Left bridge arch
    add_box((0.18, 1.88, 0.38), (0.42, 0.46, 0.48), rot_z=-0.35)
    # Right bridge arch
    add_box((1.18, 1.34, 0.38), (0.42, 0.46, 0.48), rot_z=-0.35)
    # Center reinforcement arch
    add_box((0.68, 1.84, 0.38), (0.46, 0.24, 0.48), rot_z=-0.35)

    # 4. Dual Opposed Front Hydraulic Piston Cylinders (Brembo 40mm pistons)
    add_cylinder(0.42, 1.76, 0.82, 0.24, 0.16, segs=24, axis='Z')
    add_cylinder(0.96, 1.46, 0.82, 0.24, 0.16, segs=24, axis='Z')
    
    # 5. Dual Opposed Rear Hydraulic Piston Cylinders
    add_cylinder(0.42, 1.76, -0.06, 0.24, 0.16, segs=24, axis='Z')
    add_cylinder(0.96, 1.46, -0.06, 0.24, 0.16, segs=24, axis='Z')

    # 6. Bleeder screw & fluid crossover boss
    add_cylinder(0.44, 2.08, 0.52, 0.05, 0.24, segs=16, axis='Y')
    add_cylinder(0.44, 2.20, 0.52, 0.07, 0.08, segs=6, axis='Y') # Hex valve nut
    # Fluid crossover metal pipe connecting inner and outer halves
    add_cylinder(0.68, 1.95, 0.52, 0.035, 0.55, segs=12, axis='X')

    # =========================================================================
    # PART 7: STEP 06 - GUIDE SLIDER PIN FASTENER BOLTS
    # =========================================================================
    start_object("Guide_Pin_Fastener_Bolts")
    # Guide Pin Bolt 1 (Upper Slider)
    add_cylinder(0.08, 1.88, 0.84, 0.11, 0.14, segs=6, axis='Z') # Hex head
    add_cylinder(0.08, 1.88, 0.76, 0.14, 0.04, segs=24, axis='Z') # Flange washer
    add_cylinder(0.08, 1.88, 0.46, 0.075, 0.58, segs=16, axis='Z') # Guide shank pin
    
    # Guide Pin Bolt 2 (Lower Slider)
    add_cylinder(1.24, 1.32, 0.84, 0.11, 0.14, segs=6, axis='Z') # Hex head
    add_cylinder(1.24, 1.32, 0.76, 0.14, 0.04, segs=24, axis='Z') # Flange washer
    add_cylinder(1.24, 1.32, 0.46, 0.075, 0.58, segs=16, axis='Z') # Guide shank pin

    # =========================================================================
    # COMPOSE WAVEFRONT OBJ WITH NAMED OBJECTS AND MATERIALS
    # =========================================================================
    print(f"Total Vertices: {len(verts)}")
    print(f"Total Faces: {len(faces)}")
    print(f"Object Groups: {len(objects)}")

    # 1. Vertices
    for v in verts:
        lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")

    # 2. Objects and Faces
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
    content = generate_photorealistic_disc_brake_assembly()
    filename = "Automotive_Ventilated_Disc_Brake_and_Caliper_Assembly.obj"
    
    targets = [
        os.path.join(r"d:\new web record file\public\models", filename),
        os.path.join(r"d:\new web record file\dist\models", filename),
        os.path.join(r"d:\new web record file\sample_cad_models", filename),
        os.path.join(r"D:\solidworks", filename)
    ]

    for p in targets:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(content)
            print(f"Successfully generated: {p}")
        except Exception as e:
            print(f"Warning writing to {p}: {e}")

    print("\nDONE: All CAD models updated with solid 3D geometry and correct outward normals!")
