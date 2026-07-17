#!/bin/bash
# Add this to your shellrc like this:
# source <path-to-this-file>/knbn-rc.sh

here="$( cd "$( dirname "$0" )"; pwd )"
alias k="cd ${here} && uv run knbn"
alias t="k add"
