#!/bin/sh
# pip refuses an artifact whose hash differs from the one in requirements.txt.
set -u
unset UV_NATIVE_TLS
D=/tmp/hashdemo17
rm -rf "$D" && mkdir -p "$D/shared/src/shared" && cd "$D"
echo '"""shared."""' > shared/src/shared/__init__.py
cat > shared/pyproject.toml <<'TOML'
[project]
name = "shared"
version = "1.0.0"
requires-python = ">=3.12"

[build-system]
requires = ["uv_build>=0.11,<0.12"]
build-backend = "uv_build"
TOML
uv build --offline -q --wheel shared -o dist
H=$(sha256sum dist/shared-1.0.0-py3-none-any.whl | cut -d' ' -f1)
printf 'shared==1.0.0 --hash=sha256:%s\n' "$H" > requirements.txt
PIP="python3 -m pip install -q --root-user-action=ignore --no-index --find-links dist --require-hashes -r requirements.txt"
echo '$ pip install --require-hashes -r requirements.txt'
$PIP --target t1 2>&1; echo "exit $?"
echo '# (the same version is rebuilt with different contents)'
echo '"""shared, with something extra."""' > shared/src/shared/__init__.py
rm dist/*.whl && uv build --offline -q --wheel shared -o dist
echo '$ pip install --require-hashes -r requirements.txt'
$PIP --target t2 > out.txt 2>&1; rc=$?
sed 's#file:///tmp/hashdemo17/#file:///.../#' out.txt; echo "exit $rc"
