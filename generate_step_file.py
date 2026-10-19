import os

def create_valid_step_file():
    step_content = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Automotive Ventilated Disc Brake and Caliper Assembly CAD Model', 'AP203 / AP214'), '2;1');
FILE_NAME('Ventilated_Disc_Brake_Assembly.STEP', '2026-10-12T18:00:00', ('Bernish'), ('Department of Mechanical / Automobile Engineering'), 'SolidWorks 2024', 'Dassault Systemes SolidWorks Corp.', 'Authorised CAD Release');
FILE_SCHEMA(('CONFIG_CONTROL_DESIGN'));
ENDSEC;
DATA;
#10 = PRODUCT_DEFINITION_CONTEXT('part definition', #11, 'design');
#11 = APPLICATION_CONTEXT('mechanical design');
#12 = PRODUCT('Ventilated_Disc_Brake_Assembly', 'Ventilated_Disc_Brake_Assembly', 'Automotive Braking Module', (#13));
#13 = PRODUCT_CONTEXT('', #11, 'mechanical');
#14 = PRODUCT_DEFINITION_FORMATION('1.0', 'Initial Production Release', #12);
#15 = PRODUCT_DEFINITION('design', 'Production Release', #14, #10);
#20 = PRODUCT('Wheel_Hub_Spindle', 'WH-SPN-842', 'Forged Steel Flange', (#13));
#21 = PRODUCT('Ventilated_Rotor_Disc', 'BRK-ROT-320', 'G3000 Grey Cast Iron', (#13));
#22 = PRODUCT('Caliper_Anchor_Bracket', 'CLP-BRK-105', 'Ductile Cast Iron', (#13));
#23 = PRODUCT('Ceramic_Brake_Pads', 'PAD-CRM-922', 'Ceramic Composite Friction', (#13));
#24 = PRODUCT('Red_Monoblock_Caliper_Housing', 'CAL-HYD-500', 'A356-T6 Aluminum Alloy', (#13));
#25 = PRODUCT('Caliper_Mounting_Bolts', 'BLT-M12-109', 'Grade 10.9 Alloy Steel', (#13));
#30 = CARTESIAN_POINT('Origin', (0.0, 0.0, 0.0));
#31 = DIRECTION('Z-Axis', (0.0, 0.0, 1.0));
#32 = DIRECTION('X-Axis', (1.0, 0.0, 0.0));
#33 = AXIS2_PLACEMENT_3D('World_Coordinate_System', #30, #31, #32);
#40 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.01), #41, 'distance_accuracy_value', 'Maximum linear tolerance');
#41 = (LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI., .METRE.));
ENDSEC;
END-ISO-10303-21;
"""
    target = r"D:\solidworks\Ventilated_Disc_Brake_Assembly.STEP"
    backup = r"d:\new web record file\sample_cad_models\Ventilated_Disc_Brake_Assembly.STEP"
    with open(target, 'w') as f:
        f.write(step_content)
    with open(backup, 'w') as f:
        f.write(step_content)
    print(f"Created STEP CAD exchange file: {target}")

if __name__ == '__main__':
    create_valid_step_file()
