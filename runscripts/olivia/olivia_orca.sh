#!/bin/sh
#SBATCH --account=nn14654k
#SBATCH --partition=small
#SBATCH --output=%j.out
#SBATCH --error=%j.err


#SBATCH --job-name=orca_func_tester
#SBATCH --time=0-20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3G
export OMP_NUM_THREADS=1

#Modules
module --force purge --silent
module load NRIS/CPU
module load OpenMPI/5.0.9-GCC-14.3.0
export CMAKE_TLS_VERIFY=0

dir="orca/opt1_bp86/bbcp"
name="bbcp_def2tzvp"

# cd .. # include if called from runscripts/olivia
# cd ..
cd $dir || exit 1

/cluster/projects/nn14654k/ylvaos/orca_6_1_1_linux_x86-64_shared_openmpi418/orca "$name.inp" > "$name.out"

exit 0
