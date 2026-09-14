#!/bin/bash
: '
Developer shortcuts
'

here="$( cd "$( dirname "$0" )"; pwd )"

knbn-demo() { (cd "${here}" && KNBN_DATA_DIR=demo uv run knbn "$@"); }

knbn-clear() {
    data_dir="$( mktemp -d )"
    echo "$data_dir"
    (cd "${here}" && KNBN_DATA_DIR="$data_dir" uv run knbn "$@")
}
