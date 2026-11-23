# app/ in this case

The implementation is the existing Unreal Engine 5.9 project two folders up (`sphirus.uproject`), not a game in this folder.
`r2g freeze` fingerprints the contract files plus whatever is in `app/`, so this folder holds one file:

- `UNREAL_SOURCE_MANIFEST.json` - sha256, size and mtime of the Unreal assets, maps, settings and pass tools this case refers to,
  written by `Tools/R2G_20261123/unreal_source_manifest.py`. Rerun it, then `r2g freeze`, whenever one of those files changes.

It is a hash record. It does not check art quality, does not build and does not prove a playtest. The project has no git; rollback is
the `manifest233` backup named in `../STATUS.txt`.
