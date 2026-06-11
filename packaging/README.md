# Packaging

How Claude Session Manager is packaged for each channel.

| Channel | Files | Notes |
| --- | --- | --- |
| **`.deb`** (GitHub releases) | `scripts/build_deb.sh` | Hand-rolled binary deb attached to each release. |
| **AUR** | `packaging/aur/` | `PKGBUILD` + `.SRCINFO`; see `packaging/aur/README.md`. |
| **PyPI** | `pyproject.toml` + `.github/workflows/publish-pypi.yml` | Auto-published on GitHub Release via trusted publishing. |
| **Ubuntu PPA** | `debian/` + `packaging/build-ppa-source.sh` | Source upload to Launchpad; see below. |

## Ubuntu PPA

PPA: [`ppa:matemiller992/claude-session-manager`](https://launchpad.net/~matemiller992/+archive/ubuntu/claude-session-manager)

The `debian/` directory uses the **native** source format and builds with
`dh` + `pybuild`, installing the desktop entry, icons, and metainfo on top of
the wheel.

### Releasing a new version

1. Bump the version in `pyproject.toml` / `__init__.py` as usual, and add a new
   top entry to `debian/changelog`:
   ```bash
   dch -v <VER> -D noble "New upstream release."   # or edit by hand
   ```
   Commit it.
2. Build the signed source package from the committed HEAD:
   ```bash
   packaging/build-ppa-source.sh
   ```
   (Requires `debhelper dh-python pybuild-plugin-pyproject devscripts` and the
   signing GPG key in the keyring.)
3. Upload:
   ```bash
   dput ppa:matemiller992/claude-session-manager \
     /tmp/csm-ppa/claude-session-manager_<VER>_source.changes
   ```

Launchpad emails an acceptance notice, then builds and publishes the `.deb`.

> One-time maintainer setup: a Launchpad account, a GPG key registered there
> and on `keyserver.ubuntu.com`, the Ubuntu Code of Conduct signed, and the PPA
> created.
