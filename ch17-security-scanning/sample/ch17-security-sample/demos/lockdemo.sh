#!/bin/sh
# Lock-file drift and hash checking, offline, with two local packages.
set -u
unset UV_NATIVE_TLS
D=/tmp/lockdemo17
rm -rf "$D" && mkdir -p "$D" && cd "$D"
for pkg in shared covers_cli; do
  mkdir -p "$pkg/src/$pkg"
  echo "\"\"\"$pkg.\"\"\"" > "$pkg/src/$pkg/__init__.py"
  cat > "$pkg/pyproject.toml" <<TOML
[project]
name = "$pkg"
version = "1.0.0"
requires-python = ">=3.12"

[build-system]
requires = ["uv_build>=0.11,<0.12"]
build-backend = "uv_build"
TOML
done
mkdir app && cat > app/pyproject.toml <<'TOML'
[project]
name = "app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["shared"]

[tool.uv.sources]
shared = { path = "../shared" }
TOML
cd app
echo '$ uv lock'; uv lock --offline -q 2>&1; echo "exit $?"
echo '$ uv lock --check'; uv lock --check --offline -q 2>&1; echo "exit $?"
sed -i 's/dependencies = \["shared"\]/dependencies = ["shared", "covers_cli"]/' pyproject.toml
printf 'covers_cli = { path = "../covers_cli" }\n' >> pyproject.toml
echo '# (someone adds a dependency to pyproject.toml and forgets to re-lock)'
echo '$ uv lock --check'; uv lock --check --offline -q 2>&1; echo "exit $?"
