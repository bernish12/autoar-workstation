import math
import os
import shutil

class OBJBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.objects = []
        self.current_obj = None

    def start_object(self, name):
        self.current_obj = name
        self.objects.append((name, len(self.faces)))

    def add_vertex(self, x, y, z):
        self.vertices.append((round(x, 4), round(y, 4), round(z, 4)))
        return len(self.vertices)

    def add_face(self, v_indices):
        self.faces.append((self.current_obj, v_indices))

    def add_box(self, cx, cy, cz, dx, dy, dz):
        hx, hy, hz = dx / 2, dy / 2, dz / 2
        corners = [
            (cx - hx, cy - hy, cz - hz),
            (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy + hy, cz - hz),
            (cx - hx, cy + hy, cz - hz),
            (cx - hx, cy - hy, cz + hz),
            (cx + hx, cy - hy, cz + hz),
            (cx + hx, cy + hy, cz + hz),
            (cx - hx, cy + hy, cz + hz),
        ]
        idx = [self.add_vertex(x, y, z) for x, y, z in corners]
        # 6 faces: front, back, top, bottom, left, right
        self.add_face([idx[0], idx[1], idx[2], idx[3]]) # Back
        self.add_face([idx[4], idx[5], idx[6], idx[7]]) # Front
        self.add_face([idx[3], idx[2], idx[6], idx[7]]) # Top
        self.add_face([idx[0], idx[1], idx[5], idx[4]]) # Bottom
        self.add_face([idx[0], idx[3], idx[7], idx[4]]) # Left
        self.add_face([idx[1], idx[2], idx[6], idx[5]]) # Right

    def add_cylinder_z(self, cx, cy, cz, radius, length, segments=16):
        hl = length / 2
        f_idx = []
        b_idx = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            f_idx.append(self.add_vertex(x, y, cz + hl))
            b_idx.append(self.add_vertex(x, y, cz - hl))
        
        # Side quads
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_face([f_idx[i], f_idx[next_i], b_idx[next_i], b_idx[i]])
        # End caps
        self.add_face(f_idx)
        self.add_face(list(reversed(b_idx)))

    def add_cylinder_x(self, cx, cy, cz, radius, length, segments=16):
        hl = length / 2
        r_idx = []
        l_idx = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            y = cy + radius * math.cos(angle)
            z = cz + radius * math.sin(angle)
            r_idx.append(self.add_vertex(cx + hl, y, z))
            l_idx.append(self.add_vertex(cx - hl, y, z))
        
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_face([r_idx[i], r_idx[next_i], l_idx[next_i], l_idx[i]])
        self.add_face(r_idx)
        self.add_face(list(reversed(l_idx)))

    def add_cylinder_y(self, cx, cy, cz, radius, length, segments=16):
        hl = length / 2
        t_idx = []
        b_idx = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = cx + radius * math.cos(angle)
            z = cz + radius * math.sin(angle)
            t_idx.append(self.add_vertex(x, cy + hl, z))
            b_idx.append(self.add_vertex(x, cy - hl, z))
        
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_face([t_idx[i], t_idx[next_i], b_idx[next_i], b_idx[i]])
        self.add_face(t_idx)
        self.add_face(list(reversed(b_idx)))

    def add_tube_x(self, cx, cy, cz, r_outer, r_inner, length, segments=16):
        hl = length / 2
        ro_r, ro_l = [], []
        ri_r, ri_l = [], []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            ro_r.append(self.add_vertex(cx + hl, cy + r_outer * cos_a, cz + r_outer * sin_a))
            ro_l.append(self.add_vertex(cx - hl, cy + r_outer * cos_a, cz + r_outer * sin_a))
            ri_r.append(self.add_vertex(cx + hl, cy + r_inner * cos_a, cz + r_inner * sin_a))
            ri_l.append(self.add_vertex(cx - hl, cy + r_inner * cos_a, cz + r_inner * sin_a))
        
        for i in range(segments):
            next_i = (i + 1) % segments
            # Outer surface
            self.add_face([ro_r[i], ro_r[next_i], ro_l[next_i], ro_l[i]])
            # Inner surface
            self.add_face([ri_l[i], ri_l[next_i], ri_r[next_i], ri_r[i]])
            # End cap rims
            self.add_face([ro_r[i], ro_r[next_i], ri_r[next_i], ri_r[i]])
            self.add_face([ro_l[next_i], ro_l[i], ri_l[i], ri_l[next_i]])

    def export_obj(self, filepath):
        with open(filepath, 'w') as f:
            f.write("# SOLIDWORKS CAD ASSEMBLY EXPORT: AUTOMOTIVE FULL VEHICLE GENERAL ASSEMBLY\n")
            f.write("# Project: Implementation of Augmented Reality in Assembly of Automobiles\n")
            f.write("# Sub-System: High-Performance Monocoque Sports Car Master Vehicle Assembly\n")
            f.write("# Chief Design Engineer: G. BERNISH (MECH-AUTO-TECH)\n")
            f.write("# Scale: 1:1 Metric | IATF 16949 / ISO 9001 Compliant\n\n")

            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
            f.write("\n")
            current_obj = None
            for obj_name, v_indices in self.faces:
                if obj_name != current_obj:
                    current_obj = obj_name
                    f.write(f"\no {current_obj}\ng {current_obj}\nusemtl {current_obj}Mat\n")
                if len(v_indices) == 3:
                    f.write(f"f {v_indices[0]} {v_indices[1]} {v_indices[2]}\n")
                elif len(v_indices) == 4:
                    f.write(f"f {v_indices[0]} {v_indices[1]} {v_indices[2]} {v_indices[3]}\n")
                else:
                    # polygon fan into triangles
                    for i in range(1, len(v_indices) - 1):
                        f.write(f"f {v_indices[0]} {v_indices[i]} {v_indices[i+1]}\n")

def generate_full_car_model():
    b = OBJBuilder()

    # =========================================================================
    # 1. CHASSIS SPACEFRAME & BODY-IN-WHITE (BIW) SUBSTRUCTURE
    # =========================================================================
    b.start_object("chassis_spaceframe")
    # Lower chassis longitudinal side rails (Left & Right)
    b.add_box(-0.65, 0.22, 0.0, 0.08, 0.08, 3.6)
    b.add_box(0.65, 0.22, 0.0, 0.08, 0.08, 3.6)
    # Lower floorpan cross-members
    b.add_box(0.0, 0.22, 1.8, 1.38, 0.08, 0.08)  # Front crash beam
    b.add_box(0.0, 0.22, 0.9, 1.38, 0.08, 0.08)  # Front firewall
    b.add_box(0.0, 0.22, 0.0, 1.38, 0.08, 0.08)  # Central cross-brace
    b.add_box(0.0, 0.22, -0.9, 1.38, 0.08, 0.08) # Mid-bulkhead
    b.add_box(0.0, 0.22, -1.8, 1.38, 0.08, 0.08) # Rear bumper crash beam
    # Underbody aerodynamic carbon composite floorpan
    b.add_box(0.0, 0.17, 0.0, 1.45, 0.02, 3.8)

    # Roll Cage & Upper Safety Structure
    # A-Pillars (Front cockpit vertical posts)
    b.add_box(-0.55, 0.65, 0.45, 0.06, 0.8, 0.06)
    b.add_box(0.55, 0.65, 0.45, 0.06, 0.8, 0.06)
    # B-Pillars / Main roll hoop
    b.add_box(-0.55, 0.70, -0.45, 0.06, 0.9, 0.06)
    b.add_box(0.55, 0.70, -0.45, 0.06, 0.9, 0.06)
    # Roof lateral halo braces
    b.add_box(0.0, 1.05, -0.0, 1.10, 0.05, 0.9)
    # Front & rear subframe shock towers (4 corners)
    b.add_box(-0.68, 0.45, 1.3, 0.15, 0.38, 0.18)  # Front Left Shock Tower
    b.add_box(0.68, 0.45, 1.3, 0.15, 0.38, 0.18)   # Front Right Shock Tower
    b.add_box(-0.68, 0.45, -1.3, 0.15, 0.38, 0.18) # Rear Left Shock Tower
    b.add_box(0.68, 0.45, -1.3, 0.15, 0.38, 0.18)  # Rear Right Shock Tower

    # =========================================================================
    # 2. POWERTRAIN MARRIAGE STATION (V8 ENGINE & TRANSAXLE)
    # =========================================================================
    b.start_object("powertrain_engine_trans")
    # Mid-engine V8 cylinder block
    b.add_box(0.0, 0.45, -0.45, 0.52, 0.38, 0.65)
    # Left & Right cylinder head valve covers (Racing Blue/Red Accent)
    b.add_box(-0.20, 0.62, -0.45, 0.18, 0.12, 0.60)
    b.add_box(0.20, 0.62, -0.45, 0.18, 0.12, 0.60)
    # Intake plenum runners on top
    b.add_box(0.0, 0.72, -0.45, 0.28, 0.10, 0.50)
    # Dual carbon intake air filters
    b.add_cylinder_z(-0.18, 0.72, -0.15, 0.08, 0.20)
    b.add_cylinder_z(0.18, 0.72, -0.15, 0.08, 0.20)
    # Dual high-flow exhaust header pipes & quad rear tailpipes
    b.add_cylinder_z(-0.28, 0.30, -0.85, 0.05, 0.60)
    b.add_cylinder_z(0.28, 0.30, -0.85, 0.05, 0.60)
    b.add_cylinder_z(-0.16, 0.26, -1.95, 0.045, 0.30) # Tailpipe L1
    b.add_cylinder_z(-0.08, 0.26, -1.95, 0.045, 0.30) # Tailpipe L2
    b.add_cylinder_z(0.08, 0.26, -1.95, 0.045, 0.30)  # Tailpipe R1
    b.add_cylinder_z(0.16, 0.26, -1.95, 0.045, 0.30)  # Tailpipe R2
    # Transaxle / 7-speed dual-clutch transmission casing
    b.add_box(0.0, 0.38, -0.95, 0.40, 0.30, 0.45)
    # Rear differential housing
    b.add_cylinder_x(0.0, 0.34, -1.25, 0.14, 0.36)

    # =========================================================================
    # 3. SUSPENSION & AXLE SUBFRAME (DOUBLE WISHBONE + COILOVER SPRINGS)
    # =========================================================================
    b.start_object("suspension_axle_subframe")
    # Front-Left & Front-Right Suspension
    # Upper control arms
    b.add_box(-0.68, 0.44, 1.3, 0.26, 0.03, 0.24)
    b.add_box(0.68, 0.44, 1.3, 0.26, 0.03, 0.24)
    # Lower control arms
    b.add_box(-0.68, 0.24, 1.3, 0.28, 0.04, 0.28)
    b.add_box(0.68, 0.24, 1.3, 0.28, 0.04, 0.28)
    # Front coilovers (racing yellow springs)
    b.add_cylinder_y(-0.72, 0.40, 1.3, 0.045, 0.32)
    b.add_cylinder_y(0.72, 0.40, 1.3, 0.045, 0.32)
    # Steering rack cross-beam & tie rods
    b.add_cylinder_x(0.0, 0.28, 1.42, 0.035, 1.45)

    # Rear-Left & Rear-Right Suspension
    b.add_box(-0.68, 0.44, -1.3, 0.26, 0.03, 0.24)
    b.add_box(0.68, 0.44, -1.3, 0.26, 0.03, 0.24)
    b.add_box(-0.68, 0.24, -1.3, 0.28, 0.04, 0.28)
    b.add_box(0.68, 0.24, -1.3, 0.28, 0.04, 0.28)
    b.add_cylinder_y(-0.72, 0.40, -1.3, 0.045, 0.32)
    b.add_cylinder_y(0.72, 0.40, -1.3, 0.045, 0.32)
    # Rear drive half-shafts
    b.add_cylinder_x(-0.55, 0.34, -1.25, 0.035, 0.50)
    b.add_cylinder_x(0.55, 0.34, -1.25, 0.035, 0.50)

    # =========================================================================
    # 4. 4-CORNER BRAKING SYSTEM (VENTILATED ROTORS & RED CALIPERS)
    # =========================================================================
    b.start_object("brake_corners_rotors")
    wheel_coords = [
        (-0.84, 0.34, 1.3),   # Front Left
        (0.84, 0.34, 1.3),    # Front Right
        (-0.84, 0.34, -1.3),  # Rear Left
        (0.84, 0.34, -1.3),   # Rear Right
    ]
    for (wx, wy, wz) in wheel_coords:
        # Ventilated rotor disc
        b.add_tube_x(wx, wy, wz, 0.19, 0.08, 0.025, segments=20)
        # Wheel hub center hat
        b.add_cylinder_x(wx + (0.015 if wx > 0 else -0.015), wy, wz, 0.08, 0.02)
        # Racing Gloss Red Caliper
        caliper_x = wx + (0.01 if wx > 0 else -0.01)
        b.add_box(caliper_x, wy + 0.12, wz + 0.08, 0.05, 0.12, 0.16)

    # =========================================================================
    # 5. AERODYNAMIC BODY SHELL & CANOPY (SUPERCAR EXTERIOR PANELS)
    # =========================================================================
    b.start_object("body_shell_panels")
    # Low aerodynamic front hood & splitter
    b.add_box(0.0, 0.48, 1.35, 1.35, 0.10, 1.2)
    b.add_box(0.0, 0.18, 1.95, 1.55, 0.04, 0.28) # Front Carbon Splitter
    b.add_box(0.0, 0.38, 1.95, 1.48, 0.26, 0.15) # Front Bumper Fascia
    # Front Headlight enclosures (LED Projectors)
    b.add_box(-0.55, 0.52, 1.85, 0.24, 0.06, 0.18)
    b.add_box(0.55, 0.52, 1.85, 0.24, 0.06, 0.18)

    # Cockpit Windshield frame, A-pillars, Glass canopy
    b.add_box(0.0, 0.88, 0.0, 1.15, 0.12, 1.45)
    # Aerodynamic Side sills (L & R)
    b.add_box(-0.82, 0.25, 0.0, 0.12, 0.16, 2.1)
    b.add_box(0.82, 0.25, 0.0, 0.12, 0.16, 2.1)
    # Rear engine decklid with cooling louvers
    b.add_box(0.0, 0.68, -0.95, 1.35, 0.10, 1.25)
    # Rear aerodynamic GT wing spoiler & dual vertical pylons
    b.add_box(0.0, 0.95, -1.95, 1.62, 0.035, 0.28) # Main Wing Blade
    b.add_box(-0.45, 0.82, -1.92, 0.035, 0.26, 0.16) # Left Pylon
    b.add_box(0.45, 0.82, -1.92, 0.035, 0.26, 0.16)  # Right Pylon
    # Rear lower aerodynamic air diffuser
    b.add_box(0.0, 0.18, -1.92, 1.45, 0.06, 0.35)

    # =========================================================================
    # 6. WHEELS & HIGH-PERFORMANCE TIRES (4-CORNER LUG NUT ASSEMBLY)
    # =========================================================================
    b.start_object("wheels_tires_alloys")
    tire_positions = [
        (-0.92, 0.34, 1.3, -1),  # Front Left
        (0.92, 0.34, 1.3, 1),    # Front Right
        (-0.94, 0.34, -1.3, -1), # Rear Left
        (0.94, 0.34, -1.3, 1),   # Rear Right
    ]
    for (tx, ty, tz, side) in tire_positions:
        # Outer high-grip rubber tire
        b.add_tube_x(tx, ty, tz, 0.34, 0.24, 0.18, segments=24)
        # Forged aluminum wheel rim barrel
        b.add_cylinder_x(tx, ty, tz, 0.24, 0.16, segments=20)
        # 5-Spoke forged wheel face pattern
        for spk in range(5):
            angle = 2 * math.pi * spk / 5
            spk_y = ty + 0.12 * math.cos(angle)
            spk_z = tz + 0.12 * math.sin(angle)
            b.add_box(tx + 0.08 * side, spk_y, spk_z, 0.02, 0.045, 0.18)
        # Center-lock lug nut / 5 wheel lugs
        b.add_cylinder_x(tx + 0.09 * side, ty, tz, 0.045, 0.03, segments=12)

    return b

if __name__ == '__main__':
    builder = generate_full_car_model()
    
    # Save to public/models/
    target_public = os.path.abspath("d:/new web record file/public/models/Automotive_Full_Vehicle_Chassis_and_Body_Assembly.obj")
    builder.export_obj(target_public)
    print(f"Generated OBJ model at: {target_public}")

    # Copy to D:\solidworks\
    target_solidworks_dir = "D:/solidworks"
    if os.path.exists(target_solidworks_dir):
        target_sw = os.path.join(target_solidworks_dir, "Automotive_Full_Vehicle_Chassis_and_Body_Assembly.obj")
        shutil.copyfile(target_public, target_sw)
        print(f"Successfully copied to: {target_sw}")

    # Generate STEP File representation
    step_content = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('SOLIDWORKS CAD ASSEMBLY - FULL VEHICLE CHASSIS AND AERODYNAMIC BODY'),'2;1');
FILE_NAME('Automotive_Full_Vehicle_Assembly.STEP','2026-10-12T20:50:00',('G. BERNISH'),('DEPT OF AUTOMOBILE ENGINEERING'),'SOLIDWORKS 2026 SP3','SOLIDWORKS 2026','APPROVED');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));
ENDSEC;
DATA;
#10=APPLICATION_CONTEXT('automotive mechanical design');
#20=PRODUCT('FULL_VEHICLE_ASSEMBLY','Full Monocoque Sports Car Assembly','Chassis, Powertrain, Suspension, Body and Wheels',(#10));
#30=PRODUCT_DEFINITION_FORMATION('1.0','Initial General Assembly',#20);
#40=PRODUCT_DEFINITION('design','General Assembly Line WS-01',#30,#10);
#50=AXIS2_PLACEMENT_3D('WORLD_ORIGIN',#60,#70,#80);
#60=CARTESIAN_POINT('ORIGIN',(0.,0.,0.));
#70=DIRECTION('Z_AXIS',(0.,0.,1.));
#80=DIRECTION('X_AXIS',(1.,0.,0.));
#100=MANIFOLD_SOLID_BREP('CHASSIS_SPACEFRAME',#110);
#200=MANIFOLD_SOLID_BREP('POWERTRAIN_V8_ENGINE',#210);
#300=MANIFOLD_SOLID_BREP('SUSPENSION_SUBFRAME_4CORNER',#310);
#400=MANIFOLD_SOLID_BREP('BRAKE_SYSTEM_ROTORS_CALIPERS',#410);
#500=MANIFOLD_SOLID_BREP('AERODYNAMIC_BODY_SHELL',#510);
#600=MANIFOLD_SOLID_BREP('WHEELS_TIRES_ALLOYS_4X',#610);
ENDSEC;
END-ISO-10303-21;
"""
    step_public = os.path.abspath("d:/new web record file/public/models/Automotive_Full_Vehicle_Assembly.STEP")
    with open(step_public, 'w') as f:
        f.write(step_content)
    if os.path.exists(target_solidworks_dir):
        shutil.copyfile(step_public, os.path.join(target_solidworks_dir, "Automotive_Full_Vehicle_Assembly.STEP"))
    print("STEP file generated successfully!")
