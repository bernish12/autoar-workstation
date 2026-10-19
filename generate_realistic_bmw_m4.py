"""
Generates an ultra-realistic, authentic BMW M-Series (M4 Coupe) 3D CAD Assembly OBJ model
specifically partitioned into 12 Industry 4.0 Standard Automotive Final Assembly Stations:

Station 01: chassis_spaceframe - BMW Carbon Core Monocoque, Floorpan & Bulkheads
Station 02: wiring_harness_electrical - 48V/12V Main Wiring Loom, High-Voltage Conduits & ECU Module
Station 03: cockpit_instrument_module - Magnesium Cross-Car Beam, BMW Curved Display & M-Steering
Station 04: engine_powertrain_marriage - S58 TwinPower Turbo Engine, 8-Speed M-Steptronic, CFRP Driveshaft & Differential
Station 05: suspension_adaptive_chassis - Double-Wishbone Front Axle, 5-Link Rear, EDC Electronic Dampers & Sway Bars
Station 06: exhaust_system_shielding - Stainless Steel Downpipes, Mid-Pipes, Resonators & Rear Muffler Canister
Station 07: brake_system_carbon_ceramic - 400mm Cross-Drilled Carbon-Ceramic Rotors, 6-Piston Calipers & Hub Studs
Station 08: m_carbon_bucket_seats - Lightweight CFRP Bucket Seats with Contoured Bolsters & Headrests
Station 09: greenhouse_glazing - Robotic Curved Windshield, Rear Window & Hofmeister Kink Glass
Station 10: aerodynamic_doors_mirrors - Frameless Aluminum Doors & M Twin-Stalk Aero Winglet Mirrors
Station 11: bmw_body_aero_fascia - Aerodynamic Body Shell, M Power Dome Hood, Kidney Grilles, Laserlights, Splitter & Diffuser
Station 12: wheels_tires_rolling - 19"/20" M-Forged Style 826M Wheels & Michelin Pilot Sport 4S Radial Tires
"""

import math
import os
import shutil

class OBJWriter:
    def __init__(self):
        self.vertices = []
        self.groups = {}
        self.current_group = "default"

    def set_group(self, name):
        self.current_group = name
        if name not in self.groups:
            self.groups[name] = []

    def add_vertex(self, x, y, z):
        self.vertices.append((round(x, 4), round(y, 4), round(z, 4)))
        return len(self.vertices)

    def add_face(self, v_indices):
        self.groups[self.current_group].append(v_indices)

    def add_quad(self, v1, v2, v3, v4):
        self.add_face([v1, v2, v3])
        self.add_face([v1, v3, v4])

    def add_cylinder(self, cx, cy, cz, r1, r2, length, axis='x', segments=18, cap_start=True, cap_end=True):
        hl = length / 2.0
        start_ring = []
        end_ring = []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            ca = math.cos(angle)
            sa = math.sin(angle)
            if axis == 'x':
                start_ring.append(self.add_vertex(cx - hl, cy + r1 * ca, cz + r1 * sa))
                end_ring.append(self.add_vertex(cx + hl, cy + r2 * ca, cz + r2 * sa))
            elif axis == 'y':
                start_ring.append(self.add_vertex(cx + r1 * ca, cy - hl, cz + r1 * sa))
                end_ring.append(self.add_vertex(cx + r2 * ca, cy + hl, cz + r2 * sa))
            else: # z
                start_ring.append(self.add_vertex(cx + r1 * ca, cy + r1 * sa, cz - hl))
                end_ring.append(self.add_vertex(cx + r2 * ca, cy + r2 * sa, cz + hl))

        for i in range(segments):
            nxt = (i + 1) % segments
            self.add_quad(start_ring[i], end_ring[i], end_ring[nxt], start_ring[nxt])

        if cap_start:
            c_start = self.add_vertex(cx - (hl if axis=='x' else 0), cy - (hl if axis=='y' else 0), cz - (hl if axis=='z' else 0))
            for i in range(segments):
                nxt = (i + 1) % segments
                self.add_face([c_start, start_ring[nxt], start_ring[i]])

        if cap_end:
            c_end = self.add_vertex(cx + (hl if axis=='x' else 0), cy + (hl if axis=='y' else 0), cz + (hl if axis=='z' else 0))
            for i in range(segments):
                nxt = (i + 1) % segments
                self.add_face([c_end, end_ring[i], end_ring[nxt]])

    def add_torus(self, cx, cy, cz, R, r, axis='z', ring_segs=22, pipe_segs=14):
        grid = []
        for i in range(ring_segs):
            phi = 2.0 * math.pi * i / ring_segs
            cp, sp = math.cos(phi), math.sin(phi)
            ring = []
            for j in range(pipe_segs):
                theta = 2.0 * math.pi * j / pipe_segs
                ct, st = math.cos(theta), math.sin(theta)
                rad = R + r * ct
                if axis == 'z':
                    px = cx + rad * cp
                    py = cy + rad * sp
                    pz = cz + r * st
                elif axis == 'x':
                    px = cx + r * st
                    py = cy + rad * cp
                    pz = cz + rad * sp
                else: # y
                    px = cx + rad * cp
                    py = cy + r * st
                    pz = cz + rad * sp
                ring.append(self.add_vertex(px, py, pz))
            grid.append(ring)

        for i in range(ring_segs):
            next_i = (i + 1) % ring_segs
            for j in range(pipe_segs):
                next_j = (j + 1) % pipe_segs
                self.add_quad(grid[i][j], grid[next_i][j], grid[next_i][next_j], grid[i][next_j])

    def add_box(self, cx, cy, cz, dx, dy, dz):
        hx, hy, hz = dx / 2.0, dy / 2.0, dz / 2.0
        v = [
            self.add_vertex(cx - hx, cy - hy, cz - hz), # 0
            self.add_vertex(cx + hx, cy - hy, cz - hz), # 1
            self.add_vertex(cx + hx, cy + hy, cz - hz), # 2
            self.add_vertex(cx - hx, cy + hy, cz - hz), # 3
            self.add_vertex(cx - hx, cy - hy, cz + hz), # 4
            self.add_vertex(cx + hx, cy - hy, cz + hz), # 5
            self.add_vertex(cx + hx, cy + hy, cz + hz), # 6
            self.add_vertex(cx - hx, cy + hy, cz + hz), # 7
        ]
        self.add_quad(v[0], v[3], v[2], v[1]) # Back
        self.add_quad(v[4], v[5], v[6], v[7]) # Front
        self.add_quad(v[3], v[7], v[6], v[2]) # Top
        self.add_quad(v[0], v[1], v[5], v[4]) # Bottom
        self.add_quad(v[0], v[4], v[7], v[3]) # Left
        self.add_quad(v[1], v[2], v[6], v[5]) # Right

    def add_loft(self, cross_sections):
        n_sections = len(cross_sections)
        if n_sections < 2:
            return
        n_points = len(cross_sections[0])
        for s in range(n_sections - 1):
            s1 = cross_sections[s]
            s2 = cross_sections[s + 1]
            for p in range(n_points - 1):
                self.add_quad(s1[p], s2[p], s2[p + 1], s1[p + 1])

    def save_obj(self, filepath):
        with open(filepath, 'w') as f:
            f.write("# BMW M-Series 12-Station Industrial Final Assembly 3D CAD Model\n")
            f.write("# AutoAR Platform - ISO 9001 / IATF 16949 Digital Twin Standard\n")
            f.write(f"# Vertices: {len(self.vertices)}\n\n")

            for x, y, z in self.vertices:
                f.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
            f.write("\n")

            for grp_name, faces in self.groups.items():
                if not faces:
                    continue
                f.write(f"\ng {grp_name}\n")
                f.write(f"o {grp_name}\n")
                f.write(f"usemtl {grp_name}Mat\n")
                for face in faces:
                    f.write("f " + " ".join(str(idx) for idx in face) + "\n")


def build_12_station_bmw_m4():
    builder = OBJWriter()

    # =========================================================================
    # STATION 01: CHASSIS FLOORPAN & CARBON CORE MONOCOQUE
    # =========================================================================
    builder.set_group("chassis_spaceframe")
    # Carbon Core Lower Floorpan & Aerodynamic Undertray
    builder.add_box(0.0, -0.28, 0.0, 4.4, 0.06, 1.82)
    # Transmission Tunnel Backbone
    builder.add_box(0.0, -0.15, 0.0, 3.8, 0.22, 0.36)
    # Front Engine Cradle / Subframe Rails
    builder.add_box(1.4, -0.20, -0.65, 1.5, 0.12, 0.14)
    builder.add_box(1.4, -0.20, 0.65, 1.5, 0.12, 0.14)
    # Front Crossmember & Steering Rack Mount
    builder.add_box(1.4, -0.22, 0.0, 0.14, 0.10, 1.30)
    # Rear Axle Subframe Cradle & Differential Carrier
    builder.add_box(-1.4, -0.20, -0.62, 1.3, 0.12, 0.14)
    builder.add_box(-1.4, -0.20, 0.62, 1.3, 0.12, 0.14)
    builder.add_box(-1.4, -0.20, 0.0, 0.18, 0.12, 1.25)
    # Safety Firewall (Cockpit / Engine separation)
    builder.add_box(0.78, 0.05, 0.0, 0.06, 0.60, 1.65)
    # Rear Luggage / Bulkhead Wall
    builder.add_box(-1.15, 0.10, 0.0, 0.06, 0.55, 1.60)
    # Side Impact Sill Rails
    builder.add_box(0.0, -0.20, -0.84, 2.7, 0.16, 0.12)
    builder.add_box(0.0, -0.20, 0.84, 2.7, 0.16, 0.12)

    # =========================================================================
    # STATION 02: ELECTRICAL ARCHITECTURE & MAIN CABIN WIRING HARNESS
    # =========================================================================
    builder.set_group("wiring_harness_electrical")
    # High-Voltage 48V Orange Busway Cable Trunk (running along right tunnel channel)
    builder.add_cylinder(0.0, -0.12, 0.24, 0.022, 0.022, 3.6, axis='x', segments=10)
    # Main 12V Cabin Wiring Harness (running along left floor sill channel)
    builder.add_cylinder(0.0, -0.22, -0.74, 0.028, 0.028, 3.2, axis='x', segments=10)
    # Engine Bay Wiring Branch & Sensor Junction Box
    builder.add_cylinder(1.25, 0.12, -0.42, 0.018, 0.018, 0.85, axis='z', segments=8)
    builder.add_cylinder(1.25, 0.12, 0.42, 0.018, 0.018, 0.85, axis='z', segments=8)
    # Master Electronic Control Unit (ECU / DME Gateway Module)
    builder.add_box(0.75, 0.32, 0.58, 0.16, 0.12, 0.22)
    # 48V Lithium-Ion Mild-Hybrid Battery Pack & Tray (under rear trunk floor)
    builder.add_box(-1.60, -0.18, 0.0, 0.38, 0.14, 0.55)

    # =========================================================================
    # STATION 03: COCKPIT MODULE & MAGNESIUM CROSS-CAR BEAM
    # =========================================================================
    builder.set_group("cockpit_instrument_module")
    # Structural Magnesium Cross-Car Beam (bolted between A-pillars)
    builder.add_cylinder(0.54, 0.28, 0.0, 0.045, 0.045, 1.48, axis='z', segments=12)
    # Main Dashboard Architecture
    builder.add_box(0.52, 0.32, 0.0, 0.36, 0.22, 1.25)
    # BMW Curved Display (12.3" Driver Cluster + 14.9" Control Display)
    builder.add_box(0.50, 0.44, -0.10, 0.06, 0.14, 0.78)
    # Steering Column & 3-Spoke M-Sport Steering Wheel
    builder.add_cylinder(0.44, 0.32, -0.32, 0.035, 0.035, 0.24, axis='x', segments=10)
    builder.add_torus(0.38, 0.36, -0.32, R=0.16, r=0.016, axis='x', ring_segs=18, pipe_segs=10)
    builder.add_box(0.38, 0.36, -0.32, 0.02, 0.08, 0.08) # M Roundel Center Hub
    builder.add_box(0.40, 0.38, -0.38, 0.015, 0.08, 0.02) # Left Carbon Shift Paddle
    builder.add_box(0.40, 0.38, -0.26, 0.015, 0.08, 0.02) # Right Carbon Shift Paddle
    # M Sports Pedal Box (Brake, Accelerator, Footrest)
    builder.add_box(0.68, -0.12, -0.32, 0.08, 0.14, 0.24)
    # Center Console with M Carbon Gear Selector & iDrive Controller
    builder.add_box(-0.15, 0.08, 0.0, 0.85, 0.16, 0.32)

    # =========================================================================
    # STATION 04: "DIE HOCHZEIT" - POWERTRAIN MARRIAGE
    # =========================================================================
    builder.set_group("engine_powertrain_marriage")
    # BMW S58 / S63 TwinPower Turbo Engine Block (Cast Closed-Deck)
    builder.add_box(1.35, 0.04, 0.0, 0.85, 0.42, 0.52)
    # Cylinder Head & M Carbon Engine Shroud
    builder.add_box(1.35, 0.28, 0.0, 0.82, 0.10, 0.48)
    # Intake Plenum & Twin Indirect Intercoolers
    builder.add_box(1.38, 0.32, -0.16, 0.55, 0.14, 0.20)
    builder.add_box(1.38, 0.32, 0.16, 0.55, 0.14, 0.20)
    # Twin Mono-Scroll Turbochargers
    builder.add_cylinder(1.22, 0.02, -0.32, 0.11, 0.11, 0.16, axis='y', segments=14)
    builder.add_cylinder(1.22, 0.02, 0.32, 0.11, 0.11, 0.16, axis='y', segments=14)
    # High-Performance Aluminum Cooling Radiator & Oil Cooler
    builder.add_box(2.15, 0.02, 0.0, 0.08, 0.45, 0.98)
    # Carbon Fiber Engine Strut Tower V-Brace
    builder.add_box(1.28, 0.38, -0.36, 0.58, 0.04, 0.06)
    builder.add_box(1.28, 0.38, 0.36, 0.58, 0.04, 0.06)
    builder.add_box(1.58, 0.38, 0.0, 0.06, 0.04, 0.72)
    # 8-Speed M-Steptronic Transmission Bellhousing
    builder.add_box(0.72, -0.06, 0.0, 0.65, 0.34, 0.38)
    # Lightweight CFRP Driveshaft
    builder.add_cylinder(-0.45, -0.12, 0.0, 0.045, 0.045, 1.70, axis='x', segments=12)
    # M Active Electronically Controlled Rear Differential
    builder.add_box(-1.40, -0.12, 0.0, 0.35, 0.26, 0.32)

    # =========================================================================
    # STATION 05: ADAPTIVE M-SUSPENSION, RUNNING GEAR & AXLES
    # =========================================================================
    builder.set_group("suspension_adaptive_chassis")
    # Front Double-Wishbone Axle (Left & Right)
    for sign in [-1.0, 1.0]:
        z_pos = sign * 0.75
        # Lower Forged Control Arm
        builder.add_box(1.40, -0.22, z_pos * 0.7, 0.12, 0.04, 0.42)
        # Upper Wishbone Arm
        builder.add_box(1.40, 0.12, z_pos * 0.7, 0.10, 0.035, 0.38)
        # Adaptive M Coilover Damper with Electronic Valving
        builder.add_cylinder(1.40, 0.08, z_pos, 0.045, 0.045, 0.46, axis='y', segments=12)
        # Front Wheel Hub Carrier / Knuckle
        builder.add_box(1.40, -0.05, sign * 0.85, 0.14, 0.20, 0.08)
        # Steering Tie Rod
        builder.add_cylinder(1.50, -0.18, z_pos * 0.6, 0.02, 0.02, 0.42, axis='z', segments=8)
    # Front Anti-Roll Stabilizer Bar
    builder.add_cylinder(1.55, -0.22, 0.0, 0.025, 0.025, 1.45, axis='z', segments=12)

    # Rear Five-Link Independent Lightweight Axle (Left & Right)
    for sign in [-1.0, 1.0]:
        z_pos = sign * 0.78
        # High-Torque Rear Drive Half-Shafts with CV Joints
        builder.add_cylinder(-1.40, -0.10, z_pos * 0.55, 0.032, 0.032, 0.58, axis='z', segments=10)
        # 5-Link Kinematic Control Links
        builder.add_box(-1.40, -0.22, z_pos * 0.7, 0.14, 0.04, 0.45)
        builder.add_box(-1.40, 0.02, z_pos * 0.7, 0.12, 0.035, 0.40)
        # Rear Damper Strut & Coil Spring
        builder.add_cylinder(-1.40, 0.10, z_pos, 0.048, 0.048, 0.48, axis='y', segments=12)
        # Rear Wheel Carrier / Hub
        builder.add_box(-1.40, -0.05, sign * 0.87, 0.16, 0.22, 0.09)
    # Rear Anti-Roll Sway Bar
    builder.add_cylinder(-1.45, -0.22, 0.0, 0.022, 0.022, 1.48, axis='z', segments=12)

    # =========================================================================
    # STATION 06: EXHAUST SYSTEM & THERMAL SHIELDING
    # =========================================================================
    builder.set_group("exhaust_system_shielding")
    # Twin Stainless Steel Turbo Downpipes & Particulate Filters
    builder.add_cylinder(0.85, -0.08, -0.14, 0.045, 0.045, 0.55, axis='x', segments=10)
    builder.add_cylinder(0.85, -0.08, 0.14, 0.045, 0.045, 0.55, axis='x', segments=10)
    # Underbody Embossed Aluminum Thermal Heat Shielding
    builder.add_box(-0.35, -0.18, 0.0, 2.2, 0.015, 0.42)
    # Dual Stainless Steel Mid-Pipes with X-Pipe Crossover
    builder.add_cylinder(-0.35, -0.22, -0.12, 0.038, 0.038, 1.9, axis='x', segments=10)
    builder.add_cylinder(-0.35, -0.22, 0.12, 0.038, 0.038, 1.9, axis='x', segments=10)
    # Rear Transverse Muffler Silencer Canister with Electronic Exhaust Flaps
    builder.add_box(-2.02, -0.16, 0.0, 0.32, 0.22, 0.95)

    # =========================================================================
    # STATION 07: M CARBON-CERAMIC BRAKE SYSTEM
    # =========================================================================
    builder.set_group("brake_system_carbon_ceramic")
    wheel_locs = [
        (1.40, -0.05, -0.88, 'front_left'),
        (1.40, -0.05, 0.88, 'front_right'),
        (-1.40, -0.05, -0.90, 'rear_left'),
        (-1.40, -0.05, 0.90, 'rear_right')
    ]
    for wx, wy, wz, loc in wheel_locs:
        is_front = 'front' in loc
        sign = 1.0 if wz > 0 else -1.0
        rotor_r = 0.24 if is_front else 0.22
        # 400mm / 380mm Cross-Drilled Carbon Ceramic Double Disc Rotor
        builder.add_cylinder(wx, wy, wz - sign * 0.02, rotor_r, rotor_r, 0.028, axis='z', segments=24)
        # Center Lightweight Aluminum Hat / Bell
        builder.add_cylinder(wx, wy, wz - sign * 0.015, rotor_r * 0.48, rotor_r * 0.48, 0.035, axis='z', segments=20)
        # 5 Wheel Hub Lug Studs
        for s in range(5):
            sang = 2.0 * math.pi * s / 5.0
            sx = wx + 0.065 * math.cos(sang)
            sy = wy + 0.065 * math.sin(sang)
            builder.add_cylinder(sx, sy, wz + sign * 0.01, 0.009, 0.009, 0.03, axis='z', segments=8)
        # 6-Piston (Front) / 4-Piston (Rear) Monobloc M Gold Caliper
        caliper_h = 0.28 if is_front else 0.22
        caliper_w = 0.10
        caliper_d = 0.09
        cx = wx - 0.14 if is_front else wx + 0.12
        cy = wy + 0.12
        cz = wz + sign * 0.015
        builder.add_box(cx, cy, cz, caliper_w, caliper_h, caliper_d)
        # Sintered Ceramic Brake Pad Backplates
        builder.add_box(cx, cy, cz - sign * 0.035, caliper_w * 0.85, caliper_h * 0.75, 0.015)

    # =========================================================================
    # STATION 08: M CARBON BUCKET SEATS & INTERIOR REFINEMENT
    # =========================================================================
    builder.set_group("m_carbon_bucket_seats")
    # Dual Lightweight CFRP Racing Bucket Seats (Driver & Passenger)
    for sign in [-1.0, 1.0]:
        sz = sign * 0.32
        # Floor Mounting Adjustment Rails
        builder.add_box(-0.25, -0.06, sz - 0.16, 0.54, 0.025, 0.035)
        builder.add_box(-0.25, -0.06, sz + 0.16, 0.54, 0.025, 0.035)
        # Ergonomic Seat Cushion with Lateral Thigh Supports
        builder.add_box(-0.25, 0.02, sz, 0.50, 0.14, 0.44)
        # Carbon Shell Backrest with Deep Thorax Bolsters
        builder.add_box(-0.52, 0.38, sz, 0.12, 0.62, 0.42)
        # Integrated Headrest with Harness Pass-Through Openings
        builder.add_box(-0.54, 0.72, sz, 0.10, 0.16, 0.22)
    # Rear Sport Bench Seat Cushion
    builder.add_box(-0.85, 0.08, 0.0, 0.45, 0.18, 1.25)
    builder.add_box(-1.08, 0.35, 0.0, 0.12, 0.45, 1.20)

    # =========================================================================
    # STATION 09: GLAZING - ROBOTIC WINDSHIELD & GREENHOUSE GLASS
    # =========================================================================
    builder.set_group("greenhouse_glazing")
    # Raked Front Acoustic & Thermally Insulated Curved Windshield
    builder.add_box(0.58, 0.62, 0.0, 0.65, 0.03, 1.25)
    # Fastback Rear Window (Heated Backlight Glass)
    builder.add_box(-0.95, 0.60, 0.0, 0.70, 0.03, 1.20)
    # Left & Right Side Glazing with Signature BMW Hofmeister Kink
    for sign in [-1.0, 1.0]:
        wz = sign * 0.68
        builder.add_box(-0.15, 0.58, wz, 1.15, 0.26, 0.03)

    # =========================================================================
    # STATION 10: DOORS & AERODYNAMIC M TWIN-STALK MIRRORS
    # =========================================================================
    builder.set_group("aerodynamic_doors_mirrors")
    # Left & Right Lightweight Aluminum Door Skins & Weatherstripping
    for sign in [-1.0, 1.0]:
        dz = sign * 0.88
        builder.add_box(0.15, 0.15, dz, 1.35, 0.55, 0.06)
        # Flush Integrated Aerodynamic Door Handles
        builder.add_box(0.05, 0.34, dz + sign * 0.032, 0.16, 0.04, 0.02)
        # M-Aerodynamic Twin-Stalk Mirror Assembly with Upper Aero Winglet
        mz = sign * 0.96
        builder.add_cylinder(0.68, 0.40, mz * 0.88, 0.022, 0.022, 0.10, axis='z', segments=10)
        builder.add_box(0.66, 0.44, mz, 0.18, 0.10, 0.16)
        builder.add_box(0.64, 0.49, mz - sign * 0.03, 0.08, 0.02, 0.06)

    # =========================================================================
    # STATION 11: EXTERIOR BODY SHELL, POWER DOME HOOD, KIDNEY GRILLE & AERO
    # =========================================================================
    builder.set_group("bmw_body_aero_fascia")
    # Multi-Profile Parametric Aerodynamic Body Shell Lofting
    loft_specs = [
        (2.42, -0.32, -0.26, -0.05, 0.28, 0.28, 0.84, 0.85, 0.82, 0.40),
        (2.32, -0.30, -0.20,  0.08, 0.42, 0.42, 0.86, 0.87, 0.85, 0.48),
        (2.22, -0.28, -0.15,  0.18, 0.52, 0.52, 0.87, 0.88, 0.87, 0.54),
        (2.00, -0.25, -0.10,  0.26, 0.60, 0.60, 0.88, 0.89, 0.88, 0.58),
        (1.40, -0.20, -0.02,  0.34, 0.66, 0.66, 0.94, 0.95, 0.94, 0.64), # Flared Front Arch
        (0.82, -0.24, -0.16,  0.32, 0.70, 0.70, 0.88, 0.90, 0.89, 0.66),
        (0.32, -0.24, -0.16,  0.32, 0.68, 0.98, 0.87, 0.89, 0.88, 0.60),
        (-0.22, -0.24, -0.16, 0.32, 0.68, 1.02, 0.87, 0.89, 0.88, 0.58), # Carbon Roof Peak
        (-0.85, -0.24, -0.16, 0.34, 0.70, 0.92, 0.90, 0.92, 0.91, 0.56),
        (-1.40, -0.20, -0.02, 0.36, 0.72, 0.76, 0.95, 0.97, 0.95, 0.58), # Flared Rear Arch
        (-1.95, -0.24, -0.14, 0.30, 0.68, 0.72, 0.91, 0.93, 0.90, 0.54),
        (-2.25, -0.28, -0.18, 0.16, 0.58, 0.60, 0.88, 0.89, 0.86, 0.48),
        (-2.38, -0.32, -0.25, -0.02, 0.42, 0.42, 0.84, 0.85, 0.80, 0.38),
    ]
    rings = []
    for (x, y_bot, y_sil, y_blt, y_cwl, y_ruf, w_bot, w_sil, w_blt, w_ruf) in loft_specs:
        c_y = y_ruf - 0.025 if (x < 0.6 and x > -1.2) else (y_ruf + 0.02 if (x >= 0.8 and x <= 2.1) else y_ruf)
        pts = [
            (-w_bot, y_bot),
            (-w_sil, y_sil),
            (-w_blt, y_blt * 0.65),
            (-w_blt, y_blt),
            (-w_ruf * 0.95, y_ruf * 0.82 + y_blt * 0.18),
            (-w_ruf * 0.65, y_ruf),
            (0.0, c_y),
            (w_ruf * 0.65, y_ruf),
            (w_ruf * 0.95, y_ruf * 0.82 + y_blt * 0.18),
            (w_blt, y_blt),
            (w_blt, y_blt * 0.65),
            (w_sil, y_sil),
            (w_bot, y_bot),
        ]
        ring_v = [builder.add_vertex(x, py, pz) for (pz, py) in pts]
        rings.append(ring_v)
    builder.add_loft(rings)

    # Front Nose Cap & Rear Fascia Cap
    c_front = builder.add_vertex(2.44, -0.15, 0.0)
    for p in range(len(rings[0]) - 1):
        builder.add_face([c_front, rings[0][p], rings[0][p + 1]])
    c_rear = builder.add_vertex(-2.40, -0.10, 0.0)
    for p in range(len(rings[-1]) - 1):
        builder.add_face([c_rear, rings[-1][p + 1], rings[-1][p]])

    # Twin Kidney Grilles with High-Gloss Shadowline M-Slats
    for sign in [-1.0, 1.0]:
        kz = sign * 0.16
        builder.add_torus(2.26, 0.14, kz, R=0.14, r=0.016, axis='x', ring_segs=20, pipe_segs=10)
        builder.add_cylinder(2.24, 0.14, kz, 0.13, 0.13, 0.02, axis='x', segments=16)
        for s in range(7):
            soff = (s - 3) * 0.032
            builder.add_box(2.26, 0.14, kz + soff, 0.03, 0.22, 0.008)

    # Sculpted M-Power Dome on Hood & BMW Roundel Emblem
    builder.add_box(1.55, 0.66, 0.0, 0.90, 0.035, 0.38)
    builder.add_box(1.50, 0.67, 0.0, 0.70, 0.025, 0.26)
    builder.add_box(1.55, 0.65, -0.24, 0.95, 0.018, 0.012)
    builder.add_box(1.55, 0.65, 0.24, 0.95, 0.018, 0.012)
    builder.add_cylinder(2.22, 0.53, 0.0, 0.035, 0.035, 0.012, axis='y', segments=16)

    # BMW Icon Adaptive Quad Projector Headlights
    for sign in [-1.0, 1.0]:
        hz = sign * 0.58
        builder.add_box(2.10, 0.28, hz, 0.25, 0.12, 0.28)
        builder.add_cylinder(2.14, 0.28, hz - sign * 0.07, 0.038, 0.038, 0.03, axis='x', segments=14)
        builder.add_cylinder(2.11, 0.29, hz + sign * 0.06, 0.034, 0.034, 0.03, axis='x', segments=14)

    # Front M-Bumper Splitter & Triple Air Dams
    builder.add_box(2.40, -0.32, 0.0, 0.16, 0.03, 1.76)
    builder.add_box(2.34, -0.16, 0.0, 0.06, 0.18, 0.88)
    builder.add_box(2.32, -0.16, -0.68, 0.08, 0.20, 0.32)
    builder.add_box(2.32, -0.16, 0.68, 0.08, 0.20, 0.32)

    # Rear Decklid Lip Spoiler, L-Shaped 3D Taillights & Carbon Diffuser
    builder.add_box(-2.02, 0.74, 0.0, 0.14, 0.04, 1.15)
    for sign in [-1.0, 1.0]:
        tz = sign * 0.64
        builder.add_box(-2.28, 0.44, tz, 0.10, 0.10, 0.36)
        builder.add_box(-2.26, 0.38, tz + sign * 0.12, 0.08, 0.08, 0.08)
    builder.add_box(-2.36, -0.26, 0.0, 0.14, 0.12, 1.45)
    for fz in [-0.45, -0.15, 0.15, 0.45]:
        builder.add_box(-2.38, -0.28, fz, 0.16, 0.08, 0.022)

    # Quad Polished Chrome M-Sport Exhaust Tips
    for ez in [-0.62, -0.52, 0.52, 0.62]:
        builder.add_cylinder(-2.44, -0.22, ez, 0.048, 0.048, 0.12, axis='x', segments=16)
        builder.add_cylinder(-2.44, -0.22, ez, 0.038, 0.038, 0.13, axis='x', segments=14)

    # =========================================================================
    # STATION 12: M-FORGED STYLE 826M WHEELS & MICHELIN TIRES
    # =========================================================================
    builder.set_group("wheels_tires_rolling")
    wheel_data = [
        (1.40, -0.05, -0.91, 'front_left'),
        (1.40, -0.05, 0.91, 'front_right'),
        (-1.40, -0.05, -0.93, 'rear_left'),
        (-1.40, -0.05, 0.93, 'rear_right')
    ]
    for wx, wy, wz, loc in wheel_data:
        is_front = 'front' in loc
        sign = 1.0 if wz > 0 else -1.0
        tire_r = 0.34
        tire_width = 0.25 if is_front else 0.28
        rim_r = 0.25

        # Michelin Pilot Sport 4S Radial Tires
        builder.add_torus(wx, wy, wz, R=tire_r - 0.05, r=0.055, axis='z', ring_segs=24, pipe_segs=16)
        builder.add_cylinder(wx, wy, wz, tire_r, tire_r, tire_width * 0.75, axis='z', segments=24, cap_start=False, cap_end=False)
        builder.add_cylinder(wx, wy, wz + sign * (tire_width / 2.0), tire_r * 0.96, rim_r * 1.05, 0.015, axis='z', segments=24)
        builder.add_cylinder(wx, wy, wz - sign * (tire_width / 2.0), tire_r * 0.96, rim_r * 1.05, 0.015, axis='z', segments=24)

        # BMW M-Forged Style 826M Wheels (Rim Lip & Barrel)
        builder.add_cylinder(wx, wy, wz + sign * 0.02, rim_r, rim_r, tire_width * 0.65, axis='z', segments=24, cap_start=False, cap_end=False)
        builder.add_cylinder(wx, wy, wz + sign * (tire_width * 0.35), rim_r, rim_r * 0.94, 0.02, axis='z', segments=24)
        # Center Hub & Floating BMW Cap
        builder.add_cylinder(wx, wy, wz + sign * 0.03, rim_r * 0.28, rim_r * 0.28, 0.04, axis='z', segments=20)
        builder.add_cylinder(wx, wy, wz + sign * 0.055, rim_r * 0.14, rim_r * 0.14, 0.015, axis='z', segments=16)

        # 5 Pairs of Double Spokes (10 Split Y-Spokes)
        for p in range(5):
            main_ang = 2.0 * math.pi * p / 5.0
            for spk_offset in [-0.11, 0.11]:
                ang = main_ang + spk_offset
                ca, sa = math.cos(ang), math.sin(ang)
                spoke_len = rim_r * 0.72
                spk_mid_r = rim_r * 0.58
                sx = wx + spk_mid_r * ca
                sy = wy + spk_mid_r * sa
                sz = wz + sign * 0.035
                builder.add_box(sx, sy, sz, 0.032, spoke_len, 0.022)

    return builder


def main():
    print("Building 12-Station Industry 4.0 BMW M-Series CAD Model...")
    builder = build_12_station_bmw_m4()

    output_dir = os.path.join(os.path.dirname(__file__), 'public', 'models')
    os.makedirs(output_dir, exist_ok=True)
    target_obj = os.path.join(output_dir, 'BMW_M_Series_Complete_Body_Assembly.obj')

    builder.save_obj(target_obj)
    print(f"Generated 12-Station OBJ: {target_obj}")
    print(f"Total Vertices: {len(builder.vertices)}")
    total_faces = sum(len(f) for f in builder.groups.values())
    print(f"Total Faces: {total_faces}")
    print(f"Total Groups: {len(builder.groups)} -> {list(builder.groups.keys())}")

    dist_dir = os.path.join(os.path.dirname(__file__), 'dist', 'models')
    if os.path.exists(dist_dir):
        dist_target = os.path.join(dist_dir, 'BMW_M_Series_Complete_Body_Assembly.obj')
        shutil.copyfile(target_obj, dist_target)
        print(f"Copied to dist: {dist_target}")

    sw_dir = r"D:\solidworks"
    if os.path.exists(sw_dir):
        sw_target = os.path.join(sw_dir, 'BMW_M_Series_Complete_Body_Assembly.obj')
        shutil.copyfile(target_obj, sw_target)
        print(f"Copied to SolidWorks directory: {sw_target}")

if __name__ == '__main__':
    main()
