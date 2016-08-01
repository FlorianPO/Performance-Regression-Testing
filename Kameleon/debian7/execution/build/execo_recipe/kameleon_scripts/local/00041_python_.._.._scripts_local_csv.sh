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
echo python\ ../../scripts_local/csv_filler.py\ ../../input_data/revisions.csv\ ../../input_data/commands.csv\ ../../input_data/branches.csv'
'cp\ ../../input_data/revisions.csv\ ../../scripts/revisions_abstract.csv'
'cp\ ../../scripts_local/csv_reader.py\ ../../scripts/csv_reader.py >> "${__ROOT_DIRECTORY__}/bash_history"



python ../../scripts_local/csv_filler.py ../../input_data/revisions.csv ../../input_data/commands.csv ../../input_data/branches.csv
cp ../../input_data/revisions.csv ../../scripts/revisions_abstract.csv
cp ../../scripts_local/csv_reader.py ../../scripts/csv_reader.py

