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
echo echo\ \$PWD'
''
'git\ clone\ https://github.com/fpruvost/spack'
'export\ SPACK_ROOT\=\$PWD/spack/'
'export\ PATH\=\$SPACK_ROOT/bin:\$PATH\ \ \ \ \ \ \ \ \ \ '
'cd\ spack/'
'git\ checkout\ morse'
'cd\ ../\ \ \ \ \ \ \ \ \ \ '
''
'pip\ install\ --user\ execo'
''
'python\ ../../execo_script.py\ grenoble\ 0\ 1\ \"1:00:00\" >> "${__ROOT_DIRECTORY__}/bash_history"



echo $PWD

git clone https://github.com/fpruvost/spack
export SPACK_ROOT=$PWD/spack/
export PATH=$SPACK_ROOT/bin:$PATH          
cd spack/
git checkout morse
cd ../          

pip install --user execo

python ../../execo_script.py grenoble 0 1 "1:00:00"

