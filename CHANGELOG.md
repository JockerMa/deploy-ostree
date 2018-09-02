# Changelog for deploy-ostree
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
* Initial release.
  - Deploy libostree commits from local and HTTP remotes.
  - Create a new stateroot if needed, with an optional custom name.
  - Perform several predefined provisioning operations, like setting up fstab,
    creating a user, or adding authorized SSH keys.
