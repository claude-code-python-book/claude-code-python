$ uv lock
exit 0
$ uv lock --check
exit 0
# (someone adds a dependency to pyproject.toml and forgets to re-lock)
$ uv lock --check
error: The lockfile at `uv.lock` needs to be updated, but `--check` was
       provided.

hint: To update the lockfile, run `uv lock`.
exit 1
