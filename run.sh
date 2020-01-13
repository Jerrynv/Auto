export CUDA_HOME=/usr/local/cuda/bin
export PATH=$CUDA_HOME:$PATH

PROJECT_PATH='/home/dgx/Jerry/test'
cd $PROJECT_PATH

para1='--case all'
para2='-i 5'

python run.py $para1 $para2