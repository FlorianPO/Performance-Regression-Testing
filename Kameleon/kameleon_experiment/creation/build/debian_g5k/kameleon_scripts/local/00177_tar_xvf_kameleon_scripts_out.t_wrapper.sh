#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_177_6059_552322_END__ 1>&2
    echo -n __CMD_OUT_177_6059_552322_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_177_6059_552322_BEGIN__ 1>&2
    echo -n __CMD_OUT_177_6059_552322_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian8/creation/build/debian_g5k/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian8/creation/build/debian_g5k/kameleon_scripts/local/00177_tar_xvf_kameleon_scripts_out.t.sh

