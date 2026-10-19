import math
import os
import shutil

def export_obj_cylinder(radius_top, radius_bottom, height, segments, offset=(0,0,0), rot_axis=None):
    verts = []
    faces = []
    half_h = height / 2.0
    ox, oy, oz = offset

    # Bottom cap center
    verts.append((ox, oy - half_h, oz))
    # Bottom circle
    for i in range(segments):
        a = (i * 2 * math.pi) / segments
        verts.append((ox + radius_bottom * math.cos(a), oy - half_h, oz + radius_bottom * math.sin(a)))
    
    # Top cap center
    top_center_idx = len(verts) + 1
    verts.append((ox, oy + half_h, oz))
    # Top circle
    for i in range(segments):
        a = (i * 2 * math.pi) / segments
        verts.append((ox + radius_top * math.cos(a), oy + half_h, oz + radius_top * math.sin(a)))

    return verts

def generate_knuckle_joint_obj():
    lines = [
        "# SOLIDWORKS CAD EXPORT: KNUCKLE JOINT ASSEMBLY",
        "# Machine Design Standard Proportions (d = 30mm)",
        "# Generated for AutoAR Smart Assembly Platform",
        "o Knuckle_Joint_Assembly"
    ]
    
    verts = []
    faces = []

    def add_box(center, size):
        cx, cy, cz = center
        sx, sy, sz = size[0]/2, size[1]/2, size[2]/2
        base = len(verts) + 1
        box_v = [
            (cx - sx, cy - sy, cz - sz),
            (cx + sx, cy - sy, cz - sz),
            (cx + sx, cy + sy, cz - sz),
            (cx - sx, cy + sy, cz - sz),
            (cx - sx, cy - sy, cz + sz),
            (cx + sx, cy - sy, cz + sz),
            (cx + sx, cy + sy, cz + sz),
            (cx - sx, cy + sy, cz + sz),
        ]
        verts.extend(box_v)
        box_f = [
            (base, base+1, base+2, base+3),
            (base+5, base+4, base+7, base+6),
            (base+4, base, base+3, base+7),
            (base+1, base+5, base+6, base+2),
            (base+3, base+2, base+6, base+7),
            (base+4, base+5, base+1, base),
        ]
        faces.extend(box_f)

    def add_cylinder(cx, cy, cz, r, h, segs=24, axis='Y'):
        base = len(verts) + 1
        half = h / 2.0
        # Bottom circle
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Y':
                verts.append((cx + r*math.cos(a), cy - half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx - half, cy + r*math.cos(a), cz + r*math.sin(a)))
            else:
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz - half))
        # Top circle
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Y':
                verts.append((cx + r*math.cos(a), cy + half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx + half, cy + r*math.cos(a), cz + r*math.sin(a)))
            else:
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz + half))

        # Side faces
        for i in range(segs):
            p1 = base + i
            p2 = base + ((i + 1) % segs)
            p3 = base + segs + ((i + 1) % segs)
            p4 = base + segs + i
            faces.append((p1, p2, p3, p4))

def generate_knuckle_joint_obj():
    lines = [
        "# SOLIDWORKS CAD EXPORT: MECHANICAL KNUCKLE JOINT ASSEMBLY",
        "# Machine Design Standard Proportions (d = 30mm)",
        "# Generated for AutoAR Smart Assembly Platform - G. BERNISH"
    ]
    verts = []
    faces = []

    def add_box(center, size):
        base = len(verts) + 1
        cx, cy, cz = center
        sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0
        box_v = [
            (cx - sx, cy - sy, cz - sz),
            (cx + sx, cy - sy, cz - sz),
            (cx + sx, cy + sy, cz - sz),
            (cx - sx, cy + sy, cz - sz),
            (cx - sx, cy - sy, cz + sz),
            (cx + sx, cy - sy, cz + sz),
            (cx + sx, cy + sy, cz + sz),
            (cx - sx, cy + sy, cz + sz),
        ]
        verts.extend(box_v)
        box_f = [
            (base, base+1, base+2, base+3),
            (base+5, base+4, base+7, base+6),
            (base+4, base, base+3, base+7),
            (base+1, base+5, base+6, base+2),
            (base+3, base+2, base+6, base+7),
            (base+4, base+5, base+1, base),
        ]
        faces.extend(box_f)

    def add_cylinder(cx, cy, cz, r, h, segs=24, axis='Y'):
        base = len(verts) + 1
        half = h / 2.0
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Y':
                verts.append((cx + r*math.cos(a), cy - half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx - half, cy + r*math.cos(a), cz + r*math.sin(a)))
            else:
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz - half))
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            if axis == 'Y':
                verts.append((cx + r*math.cos(a), cy + half, cz + r*math.sin(a)))
            elif axis == 'X':
                verts.append((cx + half, cy + r*math.cos(a), cz + r*math.sin(a)))
            else:
                verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz + half))

        for i in range(segs):
            p1 = base + i
            p2 = base + ((i + 1) % segs)
            p3 = base + segs + ((i + 1) % segs)
            p4 = base + segs + i
            faces.append((p1, p2, p3, p4))

    # Helper to flush an object
    def flush_object(obj_name, start_f_idx):
        lines.append(f"o {obj_name}")
        for f in faces[start_f_idx:]:
            lines.append(f"f {f[0]} {f[1]} {f[2]} {f[3]}")
        return len(faces)

    f_idx = 0

    # 1. Fork End
    add_cylinder(-1.6, 0, 0, 0.35, 1.8, segs=24, axis='X') # Left Rod
    add_cylinder(-0.65, 0, 0, 0.48, 0.35, segs=8, axis='X') # Octagonal collar
    add_box((-0.35, 0, 0), (0.7, 1.3, 0.75)) # Fork bridge
    add_cylinder(0, 0.52, 0, 0.6, 0.3, segs=32, axis='Y') # Upper fork ear
    add_cylinder(0, -0.52, 0, 0.6, 0.3, segs=32, axis='Y') # Lower fork ear
    f_idx_fork = len(faces)

    # 2. Eye End
    add_cylinder(1.6, 0, 0, 0.35, 1.8, segs=24, axis='X') # Right Rod
    add_cylinder(0.65, 0, 0, 0.48, 0.35, segs=8, axis='X') # Octagonal collar
    add_cylinder(0, 0, 0, 0.58, 0.65, segs=32, axis='Y') # Single Eye fitting in fork gap
    f_idx_eye = len(faces)

    # 3. Knuckle Pin
    add_cylinder(0, 0, 0, 0.32, 1.9, segs=24, axis='Y') # Main pin shank
    add_cylinder(0, 1.0, 0, 0.52, 0.25, segs=24, axis='Y') # Top pin head
    f_idx_pin = len(faces)

    # 4. Collar
    add_cylinder(0, -0.85, 0, 0.48, 0.2, segs=24, axis='Y') # Bottom collar
    f_idx_collar = len(faces)

    # 5. Taper Split Pin
    add_cylinder(0, -0.85, 0, 0.05, 0.8, segs=12, axis='X') # Taper Split Pin
    f_idx_taper = len(faces)

    # Emit all vertices first
    for v in verts:
        lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")

    # Emit named objects
    flush_object("fork_end", 0)
    flush_object("eye_end", f_idx_fork)
    flush_object("knuckle_pin", f_idx_eye)
    flush_object("collar", f_idx_pin)
    flush_object("taper_pin", f_idx_collar)

    return "\n".join(lines)

def generate_disc_brake_obj():
    lines = [
        "# SOLIDWORKS CAD EXPORT: AUTOMOTIVE VENTILATED ROTOR DISC (320mm)",
        "# Generated for AutoAR Smart Assembly Platform",
        "o Ventilated_Rotor_Disc"
    ]
    verts = []
    faces = []

    def add_cylinder(cx, cy, cz, r, h, segs=36, axis='Z'):
        base = len(verts) + 1
        half = h / 2.0
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz - half))
        for i in range(segs):
            a = (i * 2 * math.pi) / segs
            verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz + half))

        for i in range(segs):
            p1 = base + i
            p2 = base + ((i + 1) % segs)
            p3 = base + segs + ((i + 1) % segs)
            p4 = base + segs + i
            faces.append((p1, p2, p3, p4))

    # Rotor hat (bell)
    add_cylinder(0, 0, 0.25, 0.9, 0.35, segs=36)
    # Rotor outer braking disc face 1
    add_cylinder(0, 0, 0.45, 1.85, 0.08, segs=48)
    # Rotor inner braking disc face 2
    add_cylinder(0, 0, 0.32, 1.85, 0.08, segs=48)

    # 5 Wheel Stud Hub Snout
    add_cylinder(0, 0, 0.5, 0.4, 0.2, segs=24)

    for v in verts:
        lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")
    for f in faces:
        lines.append(f"f {f[0]} {f[1]} {f[2]} {f[3]}")

    return "\n".join(lines)

if __name__ == '__main__':
    # 1. Output folders
    target_dir = r"D:\solidworks"
    backup_dir = r"d:\new web record file\sample_cad_models"

    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # 2. Generate Knuckle Joint .OBJ
    knuckle_content = generate_knuckle_joint_obj()
    knuckle_path = os.path.join(target_dir, "Knuckle_Joint_Assembly.obj")
    with open(knuckle_path, "w") as f:
        f.write(knuckle_content)
    with open(os.path.join(backup_dir, "Knuckle_Joint_Assembly.obj"), "w") as f:
        f.write(knuckle_content)
    print(f"Created: {knuckle_path}")

    # 3. Generate Disc Brake Rotor .OBJ
    rotor_content = generate_disc_brake_obj()
    rotor_path = os.path.join(target_dir, "Automotive_Ventilated_Rotor_320mm.obj")
    with open(rotor_path, "w") as f:
        f.write(rotor_content)
    with open(os.path.join(backup_dir, "Automotive_Ventilated_Rotor_320mm.obj"), "w") as f:
        f.write(rotor_content)
    print(f"Created: {rotor_path}")

    print("ALL SOLIDWORKS CAD FILES SUCCESSFULLY GENERATED IN D:\\solidworks\\")
