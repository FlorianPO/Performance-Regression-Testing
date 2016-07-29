#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_89_7402_568001_END__ 1>&2
    echo -n __CMD_OUT_89_7402_568001_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_89_7402_568001_BEGIN__ 1>&2
    echo -n __CMD_OUT_89_7402_568001_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/florian/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/bash_rc" /home/florian/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/00089_cat_kameleon_workdir_pipe_cat_.sh

