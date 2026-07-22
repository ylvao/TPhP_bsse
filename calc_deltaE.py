# Trimethylphosphine ligand

m_1b    = -5830.418959220
m_15h   = -5369.101389557 
m_TPhP  = -461.2137003838

o_1b_sv   = -1480.308115908194 
o_15h_sv  = -1019.259281874870 
o_TPhP_sv = -460.931128029112  

o_1b_tz   = -1481.111434358668
o_15h_tz  = -1019.804655560083
o_TPhP_tz = -461.188051158824 

o_1b_qz   = -1481.192530204503 
o_15h_qz  = -1019.861408689002 
o_TPhP_qz = -461.212430812868  

# Phosphine ligand

# m_1b    = -5.476343590773e+03
# m_15h   = -5.133127519611e+03
# m_TPhP  = -3.432051284664e+02

# o_1b_sv   = -1126.668431724374 
# o_15h_sv  = -783.582575852568  
# o_TPhP_sv =  -343.069823141603 

# o_1b_tz   = -1127.068647191947
# o_15h_tz  = -783.861089849263 
# o_TPhP_tz = -343.191660968047 

# o_1b_qz   = -1127.117806365314
# o_15h_qz  = -783.896515368660 
# o_TPhP_qz =  -343.205210726147


############################################################################

to_kcal = 627.51

def dE(a, b, c):
    d = a - b - c
    return [d, d * to_kcal]

def dMRChem(m, o):
    d = o - m
    return [d, d * to_kcal]

m_dE = dE(m_1b, m_15h, m_TPhP)
o_dE_sv = dE(o_1b_sv, o_15h_sv, o_TPhP_sv)
o_dE_tz = dE(o_1b_tz, o_15h_tz, o_TPhP_tz)
o_dE_qz = dE(o_1b_qz, o_15h_qz, o_TPhP_qz)

dm_sv = dMRChem(m_dE[0], o_dE_sv[0])
dm_tz = dMRChem(m_dE[0], o_dE_tz[0])
dm_qz = dMRChem(m_dE[0], o_dE_qz[0])


print_str = f"""
% $\Delta E$ & {m_dE[0]} ({m_dE[1]}) & {o_dE_sv[0]} ({o_dE_sv[1]}) & {o_dE_tz[0]} ({o_dE_tz[1]}) & {o_dE_qz[0]} ({o_dE_qz[1]})
$\Delta E$ & {m_dE[0]:.5f} ({m_dE[1]:.5f}) & {o_dE_sv[0]:.5f} ({o_dE_sv[1]:.5f}) & {o_dE_tz[0]:.5f} ({o_dE_tz[1]:.5f}) & {o_dE_qz[0]:.5f} ({o_dE_qz[1]:.5f})

% $\Delta$MRChem & - & {dm_sv[0]} ({dm_sv[1]}) & {dm_tz[0]} ({dm_tz[1]}) & {dm_qz[0]} ({dm_qz[1]})
$\Delta$MRChem & - & {dm_sv[0]:5.5f} ({dm_sv[1]:5.5f}) & {dm_tz[0]:.5f} ({dm_tz[1]:.5f}) & {dm_qz[0]:.5f} ({dm_qz[1]:.5f})
"""

print(print_str)