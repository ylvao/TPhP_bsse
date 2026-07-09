
file="geomopt_wb97x-d4_def2svp/15h_opt"

# Olivia
orcapath="/cluster/projects/nn14654k/ylvaos/orca_6_1_1_linux_x86-64_shared_openmpi418/orca_2json"
mrchempath="/cluster/projects/nn14654k/ylvaos/mrchem/tools/initial_guess/from_orca.py"

$orcapath orca/"$file".loc
python3 $mrchempath orca/"$file".json

cp mrchem.bas mrchem/initial_guess/$file
cp mrchem.mop mrchem/initial_guess/$file

rm mrchem.bas mrchem.mop