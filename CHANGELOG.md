# Changelog for deploy-ostree

All notable changes to deploy-ostree will be documented in this file. The format
is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this
project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

This changelog also includes the in-development version that will become the
next release. See also the [list of all released versions](https://pypi.org/project/deploy-ostree/#history).

## 1.1.0
### Added
* `--sysroot` parameter to allow specifying a different sysroot.
* `--karg-root` parameter to allow specifying the root partition to pass to the
  kernel.

### Changed
* The system `/etc/fstab` is now always copied into the deployment. The
  `etc-fstab` builtin provisioner is now a no-op.

### Deprecated
* The `etc-fstab` provisioner is now a no-op and will be removed in a future
  release.

## 1.0.0
* Initial release. Feature highlights are:
  - deploy libostree commits from local and HTTP remotes
  - create a new stateroot if needed, with an optional custom name
  - perform several predefined provisioning operations, like setting up fstab,
    creating a user, or adding authorized SSH keys
