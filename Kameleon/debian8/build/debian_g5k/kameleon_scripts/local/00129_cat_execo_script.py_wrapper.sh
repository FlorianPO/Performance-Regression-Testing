#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_129_9689_149836_END__ 1>&2
    echo -n __CMD_OUT_129_9689_149836_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_129_9689_149836_BEGIN__ 1>&2
    echo -n __CMD_OUT_129_9689_149836_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian8/build/debian_g5k/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian8/build/debian_g5k/kameleon_scripts/local/00129_cat_execo_script.py.sh

