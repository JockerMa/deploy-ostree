# Changelog for deploy-ostree

All notable changes to deploy-ostree will be documented in this file. The format
is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this
project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

This changelog also includes the in-development version that will become the
next release. See also the [list of all released versions](https://pypi.org/project/deploy-ostree/#history).

## 1.1.0
### Added
* `--sysroot` parameter to allow specifying a different sysroot.
* `--root-karg` parameter to allow specifying the root partition to pass to the
  kernel.

## 1.0.0
* Initial release. Feature highlights are:
  - deploy libostree commits from local and HTTP remotes
  - create a new stateroot if needed, with an optional custom name
  - perform several predefined provisioning operations, like setting up fstab,
    creating a user, or adding authorized SSH keys
