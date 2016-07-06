#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_1_29432_53774_END__ 1>&2
    echo -n __CMD_OUT_1_29432_53774_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_1_29432_53774_BEGIN__ 1>&2
    echo -n __CMD_OUT_1_29432_53774_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/custom_local/build/custom_local/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/custom_local/build/custom_local/kameleon_scripts/local/00001_echo_the_local_context_has_bee.sh

