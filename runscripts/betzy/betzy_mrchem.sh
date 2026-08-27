#!/bin/bash -l
#SBATCH -A nn14654k
## SBATCH --nodes=16
## SBATCH --tasks-per-node=6
## SBATCH --exclusive
## SBATCH --time=20:00:0

#SBATCH --nodes=16
#SBATCH --tasks-per-node=4       # 2 MPI ranks per socket
#SBATCH --cpus-per-task=32       # 32 OpenMP threads per rank
#SBATCH --exclusive
#SBATCH --time=20:00:00

source /cluster/projects/nn14654k/ylvaos/mrchem/tools/betzy.env

export UCX_LOG_LEVEL=ERROR

dir="opt1_bp86_1e6"
inp="1b_azora_finite_gauss"

cd mrchem/$dir

/cluster/projects/nn14654k/ylvaos/mrchem/install/bin/mrchem -D $inp.inp
mpirun --rank-by node -map-by socket -bind-to socket /usr/bin/time -f %M /cluster/projects/nn14654k/ylvaos/mrchem/install/bin/mrchem.x $inp.json > $inp.out

rm -rf checkpoint
rm -rf orbitals
rm -rf plots