Get the automatic script
   git clone https://github.com/Jerrynv/Auto.git

-------------------------------------------------------------------------------------------------
if using the local cuda ran sdk, the --curan speacify the local cuda ran sdk workplace

run the single case
   python run.py --curan ran-sdk-abspath --case casename
run all case
   python run.py --curan ran-sdk-abspath --case all
run the case N(e.g 2,3,4,5) times
   python run.py --curan ran-sdk-abspath --case casename --iter N
run the case in limted time, unit: minutes
   python run.py --curan ran-sdk-abspath --case casename --duration N

-------------------------------------------------------------------------------------------------
if don't speacify the cuda ran sdk workplace, the script will download/decompress/compile the latest version automaticly, the package was put in pkg folder.

run the single case
   python run.py --case casename --pkg src/binaly --speacify the binary or src package, default is binary
run all case
   python run.py --curan --case all --pkg src
run the case N(e.g 2,3,4,5) times
   python run.py --case casename --iter N
run the case in limted time, unit: minutes
   python run.py --case casename --duration N
   
