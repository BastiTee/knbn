# Changelog

## 0.0.1

- Initial release

## How to release a new version

- Finish development on branch and merge to main
- Update this changelog, bump version number in `pyproject.toml` and commit
- Run

```shell
VERSION=$( grep '^version' pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/' ) &&\
echo "Release: ${VERSION}" &&\
git tag -a ${VERSION} -m "Version ${VERSION}" &&\
git push --tags
```

- Create a new release under <https://github.com/BastiTee/kindle-to-markdown/releases>
- Push to PyPi

```shell
uv publish
```
