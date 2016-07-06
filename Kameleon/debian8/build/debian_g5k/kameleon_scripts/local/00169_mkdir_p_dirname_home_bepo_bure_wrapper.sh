#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_169_6906_39685_END__ 1>&2
    echo -n __CMD_OUT_169_6906_39685_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_169_6906_39685_BEGIN__ 1>&2
    echo -n __CMD_OUT_169_6906_39685_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian8/build/debian_g5k/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian8/build/debian_g5k/kameleon_scripts/local/00169_mkdir_p_dirname_home_bepo_bure.sh
