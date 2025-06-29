export OMP_NUM_THREADS=1

for mec in $(ls mec* -d);
do 
	cd "$mec"
	echo "$(pwd)"
	mpirun --bind-to none -np 30 --use-hwthread-cpus siesta < G.fdf > G.out
	cd ..
done
cd ..
