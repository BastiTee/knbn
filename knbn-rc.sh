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

# Function to invoke knbn by calling 'k'
k()  { (cd "${here}" && uv run knbn "$@"); }
# Function to create a new task by prompting properties
t()  { k add "$@"; }
# Function to create a new task by title only (using all defaults)
tt() { k add --fast "$@"; }
