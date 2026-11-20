bash -c 'export INVOICER_MODE=test'
bash -c 'echo "mode=${INVOICER_MODE:-unset}"'   # prints mode=unset
