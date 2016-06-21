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
echo mkdir\ -p\ \$\(dirname\ /home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config\)\;'
'cat\ \>/home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config\ \<\<EOF'
'Host\ \*'
'\ \ UserKnownHostsFile\ /dev/null'
'\ \ StrictHostKeyChecking\ no'
'\ \ ConnectTimeout\ 2'
'\ \ LogLevel\ FATAL'
'\ \ ForwardAgent\ yes'
'\ \ Protocol\ 2'
'\ \ ControlPath\ /tmp/f74c0fc5a332\%r@\%h:\%p'
'\ \ ControlMaster\ auto'
'\ \ ControlPersist\ yes'
'\ \ Compression\ yes'
'Host\ g5kaccess'
'\ \ User\ fpopek'
'\ \ Hostname\ access.grid5000.fr'
'Host\ grenoble'
'\ \ User\ fpopek'
'\ \ ProxyCommand\ ssh\ -F\ /home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config\ g5kaccess\ \"nc\ -q\ 1\ grenoble\ \%p\"'
'EOF >> "${__ROOT_DIRECTORY__}/bash_history"



mkdir -p $(dirname /home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config);
cat >/home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config <<EOF
Host *
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  ConnectTimeout 2
  LogLevel FATAL
  ForwardAgent yes
  Protocol 2
  ControlPath /tmp/f74c0fc5a332%r@%h:%p
  ControlMaster auto
  ControlPersist yes
  Compression yes
Host g5kaccess
  User fpopek
  Hostname access.grid5000.fr
Host grenoble
  User fpopek
  ProxyCommand ssh -F /home/florian/Bureau/Kameleon/build/debian8_g5k/ssh_config g5kaccess "nc -q 1 grenoble %p"
EOF

