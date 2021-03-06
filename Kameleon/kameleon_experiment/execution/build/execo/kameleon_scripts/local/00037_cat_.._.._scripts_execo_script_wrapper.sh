#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_37_6809_375000_END__ 1>&2
    echo -n __CMD_OUT_37_6809_375000_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_37_6809_375000_BEGIN__ 1>&2
    echo -n __CMD_OUT_37_6809_375000_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian8/execution/build/execo/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian8/execution/build/execo/kameleon_scripts/local/00037_cat_.._.._scripts_execo_script.sh

