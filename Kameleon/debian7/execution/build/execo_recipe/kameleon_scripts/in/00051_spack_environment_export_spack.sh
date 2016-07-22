#!/usr/bin/env bash

set -o pipefail
set -o allexport

__ROOT_DIRECTORY__=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function save_env {
    # Save environment
    
    (comm -3 <(declare | sort) <(declare -f | sort)) > "${__ROOT_DIRECTORY__}/bash_env"
}

trap 'save_env' INT TERM EXIT

# Load environment
source "${__ROOT_DIRECTORY__}/bash_env" 2> /dev/null || true

# Log cmd
echo \#\ SPACK\ ENVIRONMENT'
'export\ SPACK_ROOT\=\$PWD/../debian_g5k/spack/'
'export\ PATH\=\$SPACK_ROOT/bin:\$PATH'
''
'\#\ NODE\ INFO'
'bash\ get_info.sh\ node_info.org'
''
'\#\ SPACK\ PACKAGES'
'python\ chameleon_package_builder.py\ revisions.csv\ \$SPACK_ROOT'
'python\ starpu_package_builder.py\ revisions.csv\ \$SPACK_ROOT'
''
'\#\ EXECO'
'python\ execo_script.py\ revisions.csv >> "${__ROOT_DIRECTORY__}/bash_history"



# SPACK ENVIRONMENT
export SPACK_ROOT=$PWD/../debian_g5k/spack/
export PATH=$SPACK_ROOT/bin:$PATH

# NODE INFO
bash get_info.sh node_info.org

# SPACK PACKAGES
python chameleon_package_builder.py revisions.csv $SPACK_ROOT
python starpu_package_builder.py revisions.csv $SPACK_ROOT

# EXECO
python execo_script.py revisions.csv

