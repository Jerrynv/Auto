## Get the automatic script
   '<git clone https://github.com/Jerrynv/Auto.git'>

## Prerequisites
   Add the cuda the system path:
   export PATH=/usr/local/cuda/bin:$PATH

-------------------------------------------------------------------------------------------------
## if using the local cuda ran sdk, the --curan speacify the local cuda ran sdk workplace

'<--curan speacify the local cuda ran sdk work place, should be comiled, and can run the case locally. e.g. --curan /dgx/cuda-ran-sdk.0.5>'
--case  speacify the case name to run, all the cases were difined in './testcase/caselist.txt' 
    e.g. #####cuPHY_LDPC_Error_Correction: SNR10_104codewords_SinglePrecision, the suite name is cuPHY_LDPC_Error_Correction, case name is SNR10_104codewords_SinglePrecision
         --case SNR10_104codewords_SinglePrecision
--iter, -i, speacify the case to run how much times. e.g --iter 5, default is 1, if the --duration was used, this would be take no effect
--duration, -t, speacify the case to run how much time,unit is minute. e.g --duration 1, default is 0

run the single case
   python run.py --curan ran-sdk-abspath --case casename
run all case
   python run.py --curan ran-sdk-abspath --case all
run the case N(e.g 2,3,4,5) times
   python run.py --curan ran-sdk-abspath --case casename --iter N
run the case in limted time, unit: minutes
   python run.py --curan ran-sdk-abspath --case casename --duration N

-------------------------------------------------------------------------------------------------
## if don't speacify the cuda ran sdk workplace, the script will download/decompress/compile the latest version automaticly, the package was put in pkg folder.
--curan speacify the local cuda ran sdk work place, should be comiled, and can run the case locally. e.g. --curan /dgx/cuda-ran-sdk.0.5
--case  speacify the case name to run, all the cases were difined in './testcase/caselist.txt' 
    e.g. #####cuPHY_LDPC_Error_Correction: SNR10_104codewords_SinglePrecision, the suite name is cuPHY_LDPC_Error_Correction, case name is SNR10_104codewords_SinglePrecision
         --case SNR10_104codewords_SinglePrecision
--iter, -i, speacify the case to run how much times. e.g --iter 5, default is 1, if the --duration was used, this would be take no effect
--duration, -t, speacify the case to run how much time,unit is minute. e.g --duration 1, default is 0, 
--pkg speacify which package would be downloaded/decopress/compiled, the valus should be src or binary. e.g --pkg binary, default is binary

run the single case
   python run.py --case casename --pkg src/binaly --speacify the binary or src package, default is binary
run all case
   python run.py --curan --case all --pkg src
run the case N(e.g 2,3,4,5) times
   python run.py --case casename --iter N
run the case in limted time, unit: minutes
   python run.py --case casename --duration N
   
