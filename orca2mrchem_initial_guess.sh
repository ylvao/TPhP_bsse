
mol="1b"
# file="opt1_bp86_ph3/for_mrchem_init_guess/"$mol"_x2csvp_ph3"
file="opt1_bp86_pme3/for_mrchem_init_guess/x2csvp_pme3_Compound_3"
destpath="opt1_x2csvp_pme3/"$mol"_pme3"

mkdir -p mrchem/initial_guess/$destpath

# Olivia
orcapath="/cluster/projects/nn14654k/ylvaos/orca_6_1_1_linux_x86-64_shared_openmpi418/orca_2json"
mrchempath="/cluster/projects/nn14654k/ylvaos/mrchem/tools/initial_guess/from_orca.py"

# Laptop
# orcapath="/home/ylvao/work/software/orca_6_1_1_linux_x86-64_shared_openmpi418/orca_2json"
# mrchempath="/home/ylvao/work/software/mrchem/tools/initial_guess/from_orca.py"

$orcapath orca/"$file".loc
python3 $mrchempath orca/"$file".json

cp mrchem.bas mrchem/initial_guess/$destpath
cp mrchem.mop mrchem/initial_guess/$destpath

rm mrchem.bas mrchem.mop