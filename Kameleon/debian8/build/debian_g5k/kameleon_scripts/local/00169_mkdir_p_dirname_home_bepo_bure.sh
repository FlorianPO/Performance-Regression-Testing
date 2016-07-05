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
echo mkdir\ -p\ \$\(dirname\ /home/bepo/Bureau/debian8/build/debian_g5k/debian_g5k.yaml\)\;'
'cat\ \>/home/bepo/Bureau/debian8/build/debian_g5k/debian_g5k.yaml\ \<\<EOF'
'\#'
'\#\ Kameleon\ generated\ based\ on\ kadeploy\ description\ file'
'\#'
''
'name:\ debian_g5k'
''
'version:\ 1'
''
'os:\ linux'
''
'image:'
'\ \ file:\ debian_g5k.tar.gz'
'\ \ kind:\ tar'
'\ \ compression:\ gzip'
''
'postinstalls:'
'\ \ -\ archive:\ server:///grid5000/postinstalls/debian-x64-base-2.6-post.tgz'
'\ \ \ \ compression:\ gzip'
'\ \ \ \ script:\ traitement.ash\ /rambin'
''
'boot:'
'\ \ kernel:\ /vmlinuz'
'\ \ initrd:\ /initrd.img'
''
'filesystem:\ ext4'
'EOF >> "${__ROOT_DIRECTORY__}/bash_history"



mkdir -p $(dirname /home/bepo/Bureau/debian8/build/debian_g5k/debian_g5k.yaml);
cat >/home/bepo/Bureau/debian8/build/debian_g5k/debian_g5k.yaml <<EOF
#
# Kameleon generated based on kadeploy description file
#

name: debian_g5k

version: 1

os: linux

image:
  file: debian_g5k.tar.gz
  kind: tar
  compression: gzip

postinstalls:
  - archive: server:///grid5000/postinstalls/debian-x64-base-2.6-post.tgz
    compression: gzip
    script: traitement.ash /rambin

boot:
  kernel: /vmlinuz
  initrd: /initrd.img

filesystem: ext4
EOF

