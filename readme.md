# Script to encode dvd backups to something playable.

This repo contains a very basic script to encode dvd backups (in .iso or
directory format) to m4vs using handbrake, and a systemctl timer to run it at
4am every morning when I can spare the cpu cycles.

The logic is extremely simple and I guess most people would have written a bash
one-liner.  But I seem to be better at Python than bash...

## Installation

Clone this repo.  Then:
```bash
cd dvd2m4v
$EDITOR dvd2m4v.conf # correct the paths
make
sudo make install
```

## uninstallation

```bash
sudo make uninstall
```

## Config
Currently only two settings may be set in the config file: the indir and
(optionally) the outdir (if not set outdir = indir).

The script may be called directly without using the systemd units, and any
options passed on the command line override those set in the config file.
