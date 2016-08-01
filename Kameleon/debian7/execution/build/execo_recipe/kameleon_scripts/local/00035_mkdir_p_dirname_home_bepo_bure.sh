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
echo mkdir\ -p\ \$\(dirname\ /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config\)\;'
'cat\ \>\>/home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config\ \<\<EOF'
'Host\ execo_recipe'
'\ \ User\ root'
'\ \ ProxyCommand\ ssh\ -vvv\ -F\ /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config\ grenoble\ \"nc\ -q\ 1\ \`cat\ /home/bepo/Bureau/debian7/execution/build/execo_recipe/g5k_machine\ \|\ awk\ \'\{print\ \$NF\}\'\`\ \%p\"'
'EOF >> "${__ROOT_DIRECTORY__}/bash_history"



mkdir -p $(dirname /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config);
cat >>/home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config <<EOF
Host execo_recipe
  User root
  ProxyCommand ssh -vvv -F /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config grenoble "nc -q 1 `cat /home/bepo/Bureau/debian7/execution/build/execo_recipe/g5k_machine | awk '{print $NF}'` %p"
EOF

