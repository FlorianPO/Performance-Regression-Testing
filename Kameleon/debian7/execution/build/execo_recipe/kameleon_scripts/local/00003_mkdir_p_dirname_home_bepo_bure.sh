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
'cat\ \>/home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config\ \<\<EOF'
'Host\ \*'
'\ \ UserKnownHostsFile\ /dev/null'
'\ \ StrictHostKeyChecking\ no'
'\ \ ConnectTimeout\ 2'
'\ \ LogLevel\ FATAL'
'\ \ ForwardAgent\ yes'
'\ \ Protocol\ 2'
'\ \ ControlPath\ /tmp/a9dc3a1db868\%r@\%h:\%p'
'\ \ ControlMaster\ auto'
'\ \ ControlPersist\ yes'
'\ \ Compression\ yes'
'Host\ g5kaccess'
'\ \ User\ fpopek'
'\ \ Hostname\ access.grid5000.fr'
'Host\ grenoble'
'\ \ User\ fpopek'
'\ \ ProxyCommand\ ssh\ -F\ /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config\ g5kaccess\ -W\ \%h:\%p'
'EOF >> "${__ROOT_DIRECTORY__}/bash_history"



mkdir -p $(dirname /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config);
cat >/home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config <<EOF
Host *
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  ConnectTimeout 2
  LogLevel FATAL
  ForwardAgent yes
  Protocol 2
  ControlPath /tmp/a9dc3a1db868%r@%h:%p
  ControlMaster auto
  ControlPersist yes
  Compression yes
Host g5kaccess
  User fpopek
  Hostname access.grid5000.fr
Host grenoble
  User fpopek
  ProxyCommand ssh -F /home/bepo/Bureau/debian7/execution/build/execo_recipe/ssh_config g5kaccess -W %h:%p
EOF

