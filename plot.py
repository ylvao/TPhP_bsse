import matplotlib.pyplot as plt
import numpy as np

to_kcal = 627.15


def calc_bsse(AB, A, B, AAB, AA, BAB, BB):
    return (AB - A - B - AAB + AA - BAB + BB)

def dE(A, B, AB):
    return AB - A - B

# hartree
data = {
    "pph3": {
        "mrchem" : [
            -7.556679444023e+03, # 1b (AB)
            -6.520018498931e+03, # 15h (A)
            -1.036647302394e+03, # PPh3 (B)
        ],
        "def2svp" : [
            -2168.905161567229, # A
            -1035.725629100780, # B
            -3204.657750388669, # AB
            -2168.872606823358, # AA
            -1035.724249855712, # BB
            -2168.876610161623, # AAB
            -1035.730108096595, # BAB
        ],
        "def2svpd" : [
            -2168.979286305878,
            -1035.760278527500,
            -3204.779893188574,
            -2168.951580440749,
            -1035.759104140504,
            -2168.959551014362,
            0,
        ],
        "def2tzvp" : [
            -2170.655315618085, # A
            -1036.584001955480, # B
            -3207.261477247182, # AB
            -2170.621422171998, # AA
            -1036.582817045620, # BB
            -2170.622650691153,
            -1036.583747205645,
        ],
        "def2tzvpd" : [
            -2170.661658972940,
            -1036.586641118505,
            -3207.271069620780,
            -2170.627903935866,
            -1036.585442863314,
            -2170.629218925415,
            0,
        ],
        "def2qzvp" : [
            -2170.782588960151,
            -1036.644046685794,
            -3207.447776543782,
            -2170.748208017691,
            -1036.642859121321,
            -2170.748474197015,
            -1036.643049199972,
        ]
    },
    "ph3": {
        "mrchem" : [
            -5.476343590773e+03,
            -5.133127519611e+03,
            -3.432051284664e+02,
        ],
        "def2tzvp": [
            -783.896515368581,
            -343.205210725975,
            -1127.117806365128,
            -783.834198107267,
            -343.204238930680,
            -783.834307927292,
            -343.204273401243,
        ]
        },
    "pme3": {
        "mrchem" : [
            -5830.418959220,
            -5369.162853394,
            -461.2137003838,
        ],
        "def2tzvp": [

        ]
        },
    "pet3": {
        "mrchem" : [
            -6.184324438986e+03,
            -5.605108965257e+03,
            -5.791918249236e+02,
        ],
        "def2tzvp": [

        ]
        },
    "ptbu3": {
        "mrchem" : [

        ],
        "def2tzvp": [

        ]
        },
}

ligand = "pph3"
basis_sets = ["def2svp", "def2tzvp", "def2qzvp"]
basis_sets2 = ["def2svpd", "def2tzvpd"]

mrchem = (dE(data[ligand]["mrchem"][1], data[ligand]["mrchem"][2], data[ligand]["mrchem"][0]) * to_kcal)
orca_no_bsse = []
orca_no_bsse2 = []
orca_cp_corr = []
orca_cp_corr2 = []
for basis in basis_sets:
    # Same order as the orca bsse input file
    A, B, AB, AA, BB, AAB, BAB = data[ligand][basis]
    orca_no_bsse.append(dE(A, B, AB) * to_kcal)
    orca_cp_corr.append(calc_bsse(AB, A, B, AAB, AA, BAB, BB) * to_kcal)
for basis in basis_sets2:
    # Same order as the orca bsse input file
    A, B, AB, AA, BB, AAB, BAB = data[ligand][basis]
    orca_no_bsse2.append(dE(A, B, AB) * to_kcal)
    orca_cp_corr2.append(calc_bsse(AB, A, B, AAB, AA, BAB, BB) * to_kcal)

print(mrchem)
print(orca_no_bsse)
print(orca_cp_corr)
xs = list(range(len(basis_sets)))
xs2 = list(range(len(basis_sets2)))

plt.plot(xs, orca_no_bsse, label = "orca no bsse")
plt.plot(xs2, orca_no_bsse2, label = "orca no bsse aug")
# plt.plot(xs, orca_cp_corr, label = "orca bb-cp corrected")
plt.plot(xs, [mrchem for _ in range(len(xs))], label = "mrchem")


plt.legend()
plt.savefig("plot.png")


