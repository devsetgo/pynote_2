#!/bin/bash
set -e
set -x

# mkdocs
mkdocs build

# Copy Contribute to Github Contributing
cp ~/pynote_ii_task_service/docs/index.md ~/pynote_ii_task_service/README.md


mkdocs gh-deploy