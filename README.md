# deploy-ostree: deploy and provision an OSTree commit

[![pipeline status](https://gitlab.com/fkrull/deploy-ostree/badges/master/pipeline.svg)](https://gitlab.com/fkrull/deploy-ostree/pipelines)
[![PyPI](https://img.shields.io/pypi/v/deploy-ostree.svg)](https://pypi.org/project/deploy-ostree/)
[![python versions](https://img.shields.io/pypi/pyversions/deploy-ostree.svg)](https://pypi.org/project/deploy-ostree/)

`deploy-ostree` is a tool to deploy and configure an [OSTree][ostree] commit
without user input from a simple configuration file. It will:

* set up the remote
* pull the commit
* create the stateroot
* check out and deploy the tree
* run additional provisioners to make the deployed system useful

Its original intended use case was automatic tests; accordingly, it should not
be seen as a replacement for an end-user installer. `deploy-ostree` can serve
as a tool to install a regular system, but it may also take shortcuts and do
things in a way that are fine for a disposable test environment, but might not
be fine in long-lived system.

## Requirements

* [Python][python] 3.5 or newer
* [OSTree][ostree] 2018.4 or newer (older versions may work, but weren't tested)

[python]: https://python.org
[ostree]: https://ostree.readthedocs.io

Running `deploy-ostree` from inside a libostree deployment requires no
additional configuration (provided the bootloader is set up correctly). To run
`deploy-ostree` on a system that's not using libostree, you need to first run
`ostree admin init-fs /` to set up the libostree system repository and directory
structure. In addition, you may need to set up the bootloader. How to do this
depends on the OS, the architecture, and the bootloader in use.

## Installation

You can install deploy-ostree using pip:

```console
$ pip3 install deploy-ostree
```

## Usage

```console
# deploy-ostree <config path or HTTP URL>
```

This requires root permissions. If `deploy-ostree` exits successfully, your new
OSTree deployment should be ready to boot.

#### Command-Line Arguments

* **--sysroot=SYSROOT**: install into the specified target root directory,
  rather than `/`. Just like for `/`, the directory needs to exist and be
  initialized for libostree use with `ostree admin init-fs <sysroot path>`.
* **--karg-root=ROOT**: set the kernel `root` boot parameter to the given value.
  By default, the `root` parameter of the current boot is used.
* **--fstab=FSTAB**: copy the given file into the deployment as `/etc/fstab`. If
  this parameter is omitted, the system fstab (`/etc/fstab`) is used.

#### A Note on SELinux

While not recommended, certain combinations of SELinux-using host systems and
SELinux-using deployed systems might require disabling SELinux before deploying
to avoid clashes between the host's SELinux policies and the SELinux labels in
the deployed tree. To temporarily disable SELinux:

```console
# setenforce 0
```

## Configuration Format

Configuration files must be valid [JSON][json] files (this means no comments can
be used). The top-level element must be a JSON object. Available configuration
keys are documented below. Any unknown keys are ignored.

[json]: https://www.json.org/

* **url** or **path** *(required)*: path or URL to the OSTree repository to
  pull from. Exactly one of these must be specified. If a relative path is
  specified, it is interpreted relative to:
  * if the configuration is a local file: the directory of the configuration
    file.
  * the current working directory otherwise.
* **ref** *(required)*: OSTree commit to deploy.
* **remote**: name for the OSTree remote. If this remote already exists, it it
  replaced. By default, a random name is used.
* **stateroot**: name of the OSTree stateroot to use. By default, a random name
  is generated.
* **kernel-args**: list of additional kernel arguments. The root partition is
  always determined and included in the kernel command line automatically.
* **default-provisioners**: list of provisioners to run after the OSTree commit
  is checked out. This must be an array of JSON objects. Each provisioner object
  must have a key `provisioner` specifying one of the default provisioners
  listed below. Additionally, provisioner-specific options can be set as further
  keys.

## Default Provisioners

These are the default provisioners bundled with `deploy-ostree`. Any options
documented below must be specified in the provisioner configuration object.

#### etc-network-interfaces

Set up the loopback interface and one other interface for DHCP with
[/etc/network/interfaces][etc-network-interfaces]. This probably only applies
to Debian-based systems and only for DHCP configuration. If you need different
configuration, you will have to supply your own provisioner or use something
like NetworkManager.

* **interface**: name of the interface to configure. By default, the default
  network interface is retrieved from `/proc/net/route`. However, this might
  differ between systems (especially if only one is using
  [predictable interface names][predictable]) so it's not guaranteed to work.

[etc-network-interfaces]: https://wiki.debian.org/NetworkConfiguration
[predictable]: https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/

#### root-password

Set the root password.

* **password** *(required)*: root password to set.

#### create-user

Create a user. This does try to create the home directory, but if your system
requires anything more than the stateroot's `/var` being mounted, it may not
work.

* **username** *(required)*: username of the user to create.
* **password** *(required)*: password of the user to create.
* **shell**: shell for the user. If not specified, the default shell is used.

#### passwordless-sudo

Set up a user for passwordless `sudo` access. For this to have any effect,
`sudo` must be installed on your system.

* **user** *(required)*: name of the user.

#### authorized-keys

Copy an SSH `authorized_keys` file from the host system into the deployed
system. This is useful in [Vagrant][vagrant] scenarios, as it allows you to copy
the SSH key used by Vagrant into the deployed system.

* **path** *(required)*: path of the keys file to copy into the deployed system.
  This is a path on the system that is running `deploy-ostree`, not in the
  deployed system.
* **user** *(required)*: name of the user to receive the keys. This must be a
  user in the deployed system. The file is copied to `.ssh/authorized_keys`
  inside the user's home directory.

[vagrant]: https://vagrantup.com

## Example Config

This configuration will download and deploy [CentOS Atomic Host][centos-atomic],
set up `/etc/fstab`, and create a user and set it up for passwordless `sudo`.

```json
{
    "url": "http://mirror.centos.org/centos/7/atomic/x86_64/repo/",
    "ref": "centos-atomic-host/7/x86_64/standard",
    "remote": "centos-atomic",
    "stateroot": "centos-atomic-host",
    "kernel-args": ["quiet", "splash"],

    "default-provisioners": [
        {
            "provisioner": "create-user",
            "username": "atomic",
            "password": "atomic",
            "shell": "/usr/bin/bash"
        },
        {
            "provisioner": "passwordless-sudo",
            "user": "atomic"
        }
    ]
}
```

Note that CentOS Atomic Host includes [cloud-init][cloud-init] which means it
will spend some time unsuccessfully doing its cloud setup. This is awkward, but
there's not a lot of OSTree systems to demonstrate with so here we are.

[centos-atomic]: https://wiki.centos.org/SpecialInterestGroup/Atomic/Download
[cloud-init]: http://www.projectatomic.io/blog/2014/10/getting-started-with-cloud-init/

## Version History

See [the changelog][changelog] for a list of versions and their changes.

[changelog]: https://gitlab.com/fkrull/deploy-ostree/blob/master/CHANGELOG.md
