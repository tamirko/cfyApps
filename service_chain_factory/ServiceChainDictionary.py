
# Vyata : Router
# FortiGate :FW
# Nominum : DNS server
# PaloAlto : FW
# CSR : Router (Cisco)
# vTM : LB (Virtual Traffic Manager  - Brocade)

blueprints_real_names = ["Vyata", "FortiGate" , "Nominum", "PaloAlto" , "CSR", "vTM"]

# The following blueprints combinations will NOT be generated
excluded_real_blueprints_sets = [['Vxyata', 'CSR'], ['FxortiGate', 'PaloAlto'], ['vTM', 'CSR']]


# The following relationships NOT will be generated
# Dummy - Find real ones
excluded_relationships = [['Vyata', 'CSR'], ['CxSR', 'Vyata'], ['vxTM', 'CSR'], ["PxaloAlto", "CSR"], ["Vxyata", "Nxominum"]]




