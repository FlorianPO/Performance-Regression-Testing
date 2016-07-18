#!/usr/bin/env bash

set -o pipefail
set -o allexport

__ROOT_DIRECTORY__=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function save_env {
    # Save environment
    set +x
    (comm -3 <(declare | sort) <(declare -f | sort)) > "${__ROOT_DIRECTORY__}/bash_env"
}

trap 'save_env' INT TERM EXIT

# Load environment
source "${__ROOT_DIRECTORY__}/bash_env" 2> /dev/null || true

# Log cmd
echo mkdir\ -p\ \$\(dirname\ /home/fpopek/kameleon_workdir/debian_g5k/ssh_config\)\;'
'cat\ \>/home/fpopek/kameleon_workdir/debian_g5k/ssh_config\ \<\<EOF'
'Host\ debian_g5k'
'\ \ User\ root'
'\ \ Hostname\ \$machine'
'\ \ UserKnownHostsFile\ /dev/null'
'\ \ StrictHostKeyChecking\ no'
'\ \ ConnectTimeout\ 2'
'\ \ LogLevel\ FATAL'
'\ \ ForwardAgent\ yes'
'\ \ Protocol\ 2'
'EOF >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

mkdir -p $(dirname /home/fpopek/kameleon_workdir/debian_g5k/ssh_config);
cat >/home/fpopek/kameleon_workdir/debian_g5k/ssh_config <<EOF
Host debian_g5k
  User root
  Hostname $machine
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  ConnectTimeout 2
  LogLevel FATAL
  ForwardAgent yes
  Protocol 2
EOF

