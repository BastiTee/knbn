#!/bin/bash
: '
Developer shortcuts
'

here="$( cd "$( dirname "$0" )"; pwd )"

alias knbn-demo="cd ${here} && KNBN_DATA_DIR=demo uv run knbn"

function knbn_create_clear() {
    data_dir="$( mktemp -d )"
    echo $data_dir
    KNBN_DATA_DIR=$data_dir uv run knbn
}
alias knbn-clear="cd ${here} && knbn_create_clear"
