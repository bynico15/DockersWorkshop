#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
backend_dir="$project_dir/backend"
python="$backend_dir/.venv/bin/python"

if [ ! -x "$python" ]; then
    printf '%s\n' 'No se encontró el entorno virtual de la API.' \
        'Instálalo siguiendo las instrucciones de backend/README.md.' >&2
    exit 1
fi

cd "$backend_dir"
exec "$python" -m uvicorn app.main:app --reload "$@"
