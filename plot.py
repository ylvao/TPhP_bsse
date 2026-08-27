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
        "mrchem_azora" : [
            -7.697456416390e+03,
            -6.658932028029e+03,
            -1.038436985767e+03,
        ],
        "mrchem_azora_finite_gauss" : [
            -7.697377748158e+03,
            -6.658853708885e+03,
            -1.038436645699e+03,
        ],
        "x2csvpall_x2c" : [
            -6606.709432700070,
            -1036.810608885547,
            -7643.547362233830,
            -6606.676959773239,
            -1036.809223243764,
            -6606.681863259903,
            -1036.815486463181,
        ],
        "x2ctzvpall_x2c" : [
            -6608.888189858681,
            -1037.685210945295,
            -7646.594788778848,
            -6608.854694546976,
            -1037.684025128324,
        ],
        "x2cqzvpall_x2c" : [
            -6609.082012692437,
            -1037.747062141723,
        ],
        "x2csvpall_decontract" : [
            -6564.268490221530,
            -1036.126533371375,
            -7600.388635124013,
            -6564.257108845301,
            -1036.125351927646,
            -6564.203259838457,
            -1036.131964635204,
        ],
        "x2ctzvpall_decontract" : [
            -6565.407938797609,
            -1036.617941448911,
            -7602.010114221894,
            -6565.393458457239,
            -1036.616756058476,
        ],
        "x2cqzvpall_decontract" : [
            -6565.504236199567,
            -1036.652867725105,
        ],
        "x2csvpall_decontractaux" : [
            -6507.748975629833,
            -1035.653642877380,
            -7543.397298105525,
            -6507.736917103440,
            -1035.652256431394,
            -6507.687572030150,
            -1035.658886263958,
        ],
        "x2ctzvpall_decontractaux" : [
            -6512.270949682012,
            -1036.460416821472,
            -7548.724543719230,
            -6512.214963767406,
            -1036.459229548124,
            -6512.208387546120,
            -1036.460337534714,
        ],
        "x2cqzvpall_decontractaux" : [
            -6547.461151850408,
            -1036.532158812781,
            -7583.978557338136,
            -6547.446333595491,
            -1036.530971902773,
            -6547.390397252952,
            -1036.531222245958,
        ],
        "x2csvpallautoaux" : [
            -6457.464140064507,
            -1035.653441054311,
            -7493.148897261008,
            -6457.433660688902,
            -1035.652056221096,
            -6457.449421724786,
            -1035.658702649125,
        ],
        "x2ctzvpallautoaux" : [
            -6464.230726595519,
            -1036.460204399289,
            -7500.716492114463,
            -6464.152049519033,
            -1036.459019033720,
            -6464.210334578886,
            -1036.460145995863,
        ],
        "x2cqzvpallautoaux" : [
            -6503.082006515240,
            -1036.531940850964,
            -7539.630529591277,
            -6503.048980976405,
            -1036.530755588942,
            -6503.051727846171,
        ],
        "x2csvpall" : [
            -6610.767070578890,
            -1035.654244439687,
            -7646.460558640125,
            -6610.737427791694,
            -1035.652858710550,
            -6610.746176165217,
            -1035.659482913096,
        ],
        "x2ctzvpall" : [
            -6613.736417823699,
            -1036.461093799232,
            -7650.242242195896,
            -6613.664315172910,
            -1036.459906352057,
            -6613.721545662605,
            -1036.460991972370,
        ],
        "x2cqzvpall" : [
            -6652.060610836634,
            -1036.532779597259,
            -7688.629997783797,
            -6652.020688032772,
            -1036.531592617281,
            -6652.037113341959,
            -1036.531819226166,
        ],
        "sto3g" : [
            -6584.836047544839,
            -1024.026289911667,
            -7608.918870346964,
            -6584.800379368661,
            -1024.025376817237,
            -6584.837412896922,
            -1024.077261520772,
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
            -1035.768178349703,
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
            -1036.586581742763,
        ],
        "def2qzvp" : [
            -2170.782588960151,
            -1036.644046685794,
            -3207.447776543782,
            -2170.748208017691,
            -1036.642859121321,
            -2170.748474197015,
            -1036.643049199972,
        ],
        "def2qzvpd" : [
            -2170.783261596269,
            -1036.644358885852,
            -3207.448809628129,
            -2170.748920402685,
            -1036.643170357016,
            -2170.749176244482,
            -1036.643339296565,
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

ligand = "pph3" # refers to main ligand of the system
basis_sets = ["def2svp", "def2tzvp", "def2qzvp"]
basis_sets2 = ["def2svpd", "def2tzvpd", "def2qzvpd"]
basis_x2c = ["x2csvpall", "x2ctzvpall", "x2cqzvpall"]
basis_x2c_autoaux = ["x2csvpallautoaux", "x2ctzvpallautoaux", "x2cqzvpallautoaux"]
basis_x2c_deconaux = ["x2csvpall_decontractaux", "x2ctzvpall_decontractaux", "x2cqzvpall_decontractaux"]


mrchem = (dE(data[ligand]["mrchem"][1], data[ligand]["mrchem"][2], data[ligand]["mrchem"][0]) * to_kcal)
mrchem_azora = (dE(data[ligand]["mrchem_azora"][1], data[ligand]["mrchem_azora"][2], data[ligand]["mrchem_azora"][0]) * to_kcal)
mrchem_azora_finitegauss = (dE(data[ligand]["mrchem_azora_finite_gauss"][1], data[ligand]["mrchem_azora_finite_gauss"][2], data[ligand]["mrchem_azora_finite_gauss"][0]) * to_kcal)

orca_sto3g = (dE(data[ligand]["sto3g"][0], data[ligand]["sto3g"][1], data[ligand]["sto3g"][2]) * to_kcal)
A, B, AB, AA, BB, AAB, BAB = data[ligand]["sto3g"]
orca_sto3g_cp = calc_bsse(AB, A, B, AAB, AA, BAB, BB)


orca     = []
orca_D    = []
orca_x2c = []
orca_x2c_autoaux = []
orca_x2c_deconaux = []
orca_cp     = []
orca_cp_D    = []
orca_cp_x2c = []
orca_cp_x2c_autoaux = []
orca_cp_x2c_deconaux = []

orca_pph3       = []
orca_pph3_azora = []
orca_pph3_aug   = []
orca_pph3_x2c   = []
orca_15h_x2c    = []
orca_1b_x2c     = []
orca_pph3_x2c_autoaux = []
orca_15h_x2c_autoaux  = []
orca_1b_x2c_autoaux   = []
orca_pph3_x2c_deconaux = []
orca_15h_x2c_deconaux  = []
orca_1b_x2c_deconaux   = []

mrchem_pph3   = (data[ligand]["mrchem"][2])
mrchem_pph3_azora   = (data[ligand]["mrchem_azora"][2])
mrchem_1b   = (data[ligand]["mrchem"][0])
mrchem_15h   = (data[ligand]["mrchem"][1])
mrchem_15h_azora   = (data[ligand]["mrchem_azora"][1])

def populate_orca_lists(basis_list, no_bsse_list, cp_list, B_list = None, A_list = None, AB_list = None):
    for basis in basis_list:
    # Same order as the orca bsse input file
        A, B, AB, AA, BB, AAB, BAB = data[ligand][basis]
        no_bsse_list.append(dE(A, B, AB) * to_kcal)
        cp_list.append(calc_bsse(AB, A, B, AAB, AA, BAB, BB) * to_kcal)
        if A_list is not None:
            A_list.append(A) # 15h
        if B_list is not None:
            B_list.append(B) # PPh3
        if AB_list is not None:
            AB_list.append(AB) # 1b

populate_orca_lists(basis_sets, orca, orca_cp, orca_pph3)
populate_orca_lists(basis_sets2, orca_D, orca_cp_D, orca_pph3_aug)
populate_orca_lists(basis_x2c, orca_x2c, orca_cp_x2c, orca_pph3_x2c, orca_15h_x2c, orca_1b_x2c)
populate_orca_lists(basis_x2c, orca_x2c_autoaux, orca_cp_x2c_autoaux, orca_pph3_x2c_autoaux, orca_15h_x2c_autoaux, orca_1b_x2c_autoaux)
populate_orca_lists(basis_x2c, orca_x2c_deconaux, orca_cp_x2c_deconaux, orca_pph3_x2c_deconaux, orca_15h_x2c_deconaux, orca_1b_x2c_deconaux)

xs = list(range(len(basis_sets)))
xs2 = list(range(len(basis_sets2)))
xs_x2c = list(range(len(basis_x2c)))

colors = [
    "#DF6CD1",
    "#16A97A",
    "#32D277",
    "#6054AB",
    "#6AADEB",
    "#EA4A7F",
    "#F07EC0",
]


def apply_plot_style(ax):
    ax.set_ylabel(r"$\mathbf{\Delta}$E [kcal/mol]")
    ax.set_xlabel("Basis-sets")
    ax.set_title(r"Dissosciation Energy of PPh$_{\mathbf{3}}$ from Ru-complex")
    ax.set_xticks(xs)
    ax.set_xticklabels(["def2-SVP/D", "def2-TZVP/D", "def2-QZVP/D"])
    # ax.set_facecolor("#CDEBEF")


def reset_plot(ax):
    ax.clear()
    apply_plot_style(ax)


def plot_and_scatter(ax, x, y, c_index, label, style = "solid"):
    ax.plot(x, y, color=colors[c_index], linewidth = 2, label=label, linestyle = style)
    ax.scatter(x, y, color=colors[c_index], s=50)

def savefig(filename):
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename)

txt_col = "#003349"
plt.rcParams.update({
    'figure.facecolor'   : "#CDEBEF",
    'text.color'         : txt_col,
    'axes.labelcolor'    : txt_col,
    'axes.edgecolor'     : txt_col,
    'xtick.color'        : txt_col,
    'ytick.color'        : txt_col,
    'axes.titleweight'   : "bold",
    'axes.labelweight'   : "bold",
    'axes.spines.top'    : False,
    'axes.spines.right'  : False,

    })
# print(plt.rcParams.keys())

dash = (0, (3, 1, 1, 1, 1, 1))
fig, ax = plt.subplots()
fig.tight_layout
reset_plot(ax)

plot_and_scatter(ax, xs, orca, 1, "No corrections")
plot_and_scatter(ax, xs, orca_cp, 2, "CP", style = dash)
plot_and_scatter(ax, xs2, orca_D, 3, "Diffuse basis")
plot_and_scatter(ax, xs2, orca_cp_D, 4, "Diffuse basis, CP", style = dash)
ax.plot(xs, [mrchem for _ in range(len(xs))], color=colors[0], linewidth=2.5, label="MRChem")
ax.plot(xs, [mrchem_azora for _ in range(len(xs))], color=colors[5], linewidth=2.5, label="MRChem with AZORA")
# ax.plot(xs, [mrchem_azora_finitegauss for _ in range(len(xs))], color=colors[6], linewidth=2.5, label="MRChem with AZORA and Finite Gauss", linestyle="dashdot")
# ax.scatter([0], orca_sto3g, color="black", linewidth=2.5, label="STO-3G")
# ax.scatter([0], orca_sto3g_cp, color="gray", linewidth=2.5, label="STO-3G, CP")
savefig("plot_delta_e.png")

reset_plot(ax)

plot_and_scatter(ax, xs, orca_pph3, 2, "No diffuse basis")
plot_and_scatter(ax, xs2, orca_pph3_aug, 4, "Diffuse basis")
ax.plot(xs, [mrchem_pph3 for _ in range(len(xs))], color=colors[0], linewidth=2.5, label="MRChem")
ax.plot(xs, [mrchem_pph3_azora for _ in range(len(xs))], color=colors[5], linewidth=2.5, label="MRChem with AZORA")
ax.set_ylabel("E [hartree]")
ax.set_title("Total Energy of PPh3")
savefig("plot_tot_e_pph3.png")

reset_plot(ax)

plot_and_scatter(ax, xs_x2c, orca_15h_x2c, 1, "Orca")
# Does not make any difference
# plot_and_scatter(ax, xs_x2c, orca_15h_x2c_autoaux, 4, "Orca with AutoAux")
# plot_and_scatter(ax, xs_x2c, orca_15h_x2c_deconaux, 3, "Orca with DecontractAux")
ax.plot(xs, [mrchem_15h for _ in range(len(xs))], color=colors[0], linewidth=2.5, label="MRChem")
ax.plot(xs, [mrchem_15h_azora for _ in range(len(xs))], color=colors[5], linewidth=2.5, label="MRChem with azora")
ax.set_ylabel("E [hartree]")
ax.set_title("Total Energy of Ru-complex with Two Ligands")
ax.set_xticklabels(["X2C-SVPall", "X2C-TZVPall", "X2C-QZVPall"])
savefig("plot_tot_e_15h_x2c.png")

reset_plot(ax)

plot_and_scatter(ax, xs_x2c, orca_x2c, 1, "No correction")
plot_and_scatter(ax, xs_x2c, orca_cp_x2c, 4, "CP", style=dash)
# Does not make any difference
# plot_and_scatter(ax, xs_x2c, orca_no_bsse_x2c_autoaux, 2, "No correction, AutoAux")
# plot_and_scatter(ax, xs_x2c, orca_cp_corr_x2c_autoaux, 2, "CP correction, AutoAux")
# plot_and_scatter(ax, xs_x2c, orca_no_bsse_x2c_deconaux, 3, "No correction, DecontractAux")
# plot_and_scatter(ax, xs_x2c, orca_cp_corr_x2c_deconaux, 3, "CP correction, DecontractAux")
ax.plot(xs, [mrchem for _ in range(len(xs))], color=colors[0], linewidth=2.5, label="MRChem")
ax.plot(xs, [mrchem_azora for _ in range(len(xs))], color=colors[5], linewidth=2.5, label="MRChem with AZORA")
ax.set_xticklabels(["X2C-SVPall", "X2C-TZVPall", "X2C-QZVPall"])
savefig("plot_delta_e_x2c.png")
