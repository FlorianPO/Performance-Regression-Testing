#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_87_2694_32673_END__ 1>&2
    echo -n __CMD_OUT_87_2694_32673_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_87_2694_32673_BEGIN__ 1>&2
    echo -n __CMD_OUT_87_2694_32673_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/florian/Bureau/Polaris/Kameleon/build/debian_g5k/kameleon_scripts/local/bash_rc" /home/florian/Bureau/Polaris/Kameleon/build/debian_g5k/kameleon_scripts/local/00087_cat_home_florian_bureau_polari.sh

