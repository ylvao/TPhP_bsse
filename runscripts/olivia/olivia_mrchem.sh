#!/bin/sh
#SBATCH --account=nn14654k
#SBATCH --partition=large
#SBATCH --output=%j.out
#SBATCH --error=%j.err


#SBATCH --job-name=mrchem_bsse
#SBATCH --time=0-20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
export OMP_NUM_THREADS=16

#Modules
module --force purge --silent
module load NRIS/CPU
module load GCC/14.2.0
module load Python/3.13.1-GCCcore-14.2.0
module load OpenMPI/5.0.7-GCC-14.2.0
module load CMake/3.31.3-GCCcore-14.2.0
export CMAKE_TLS_VERIFY=0

dir="opt1_bp86_1e6"
name="15h_olivia"
cd "mrchem/$dir" || exit 1

/cluster/projects/nn14654k/ylvaos/mrchem/install/bin/mrchem --launcher='srun --distribution=cyclic:cyclic' "$name.inp"

rm -rf checkpoint
rm -rf orbitals
rm -rf plots

exit 0

