#!/bin/bash
: '

A convenience rc-file to configure your knbn instance.
Add this to your shellrc like this:

source <path-to-this-file>/knbn-rc.sh

Prior to invoking this, you can set environment variables to
configure your experience, if needed:

export EDITOR=vim  # Change your default terminal editor
export KNBN_DATA_DIR=/path/to/my/data  # Change your data location

'

here="$( cd "$( dirname "$0" )"; pwd )"

# Alias to invoke knbn by calling 'k'
alias k="cd ${here} && uv run knbn"
# Alias to create a new task by prompting properties
alias t="k add"
# Alias to create a new task by title only (using all defaults)
alias tt="k add --fast"

# Developer shortcuts
alias knbn-demo="cd ${here} && KNBN_DATA_DIR=demo uv run knbn"
function knbn_create_clear() {
    data_dir="$( mktemp -d )"
    echo ${data_dir}
    KNBN_DATA_DIR=${data_dir} uv run knbn
    open ${data_dir}
}
alias knbn-clear="cd ${here} && knbn_create_clear"
