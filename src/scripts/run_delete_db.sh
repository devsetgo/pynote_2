#!/bin/bash
set -e
set -x
#delete db
rm ~/pynote_ii/app/sqlite_db/api.db
#delete logs
rm ~/pynote_ii/app/log/app_log.log
# run dev
uvicorn main:app --port 5000 --reload --log-level debug

