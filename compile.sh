
cd ./parser

COMPILER="gfortran-8"
COMPILER_OPTIONS="-nocpp -O3 -o"
INSTALL_FOLDER=$(pwd)

${COMPILER} ${COMPILER_OPTIONS} ./ifg_parser glob_prepro4.F90 glob_OPUSparms.F90 ifg_parser.F90
