#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_97_4215_176704_END__ 1>&2
    echo -n __CMD_OUT_97_4215_176704_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_97_4215_176704_BEGIN__ 1>&2
    echo -n __CMD_OUT_97_4215_176704_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/00097_tar_xvf_kameleon_scripts_out.t.sh

