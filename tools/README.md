# Maintaining the press kit

The public entry point is [README](../README.md). Keep unfinished quotes, launch copy and internal campaign notes outside this public repository.

## Rebuild the deliverables

Use Python 3.10+ with Pillow available:

```text
python tools/prepare_press_kit.py
python tools/prepare_press_kit.py --check
git diff --check
```

The first command refreshes the plain-text press release and press copy, proportional screenshot previews, captioned gallery, essential ZIP, and download size/checksum. The second validates generated content without writing it, checks local links and checks the archive. It returns a nonzero exit code if anything is stale or invalid.

Full-resolution source images remain unchanged. The ZIP uses descriptive filenames; existing repository filenames and links stay valid. Original screenshots are the supplied images from the campaign, not new captures. The JSON catalog records captions and which images belong in the essential pack. Caption or selection changes belong in `tools/press-assets.json`; the gallery is generated.

The ZIP includes the written press material, four selected original screenshots, a transparent English logo and landscape key art. Videos and wallpapers remain separate. Links in the ZIP's Markdown documents point to the public kit so they remain usable when only the compact selection is extracted.

## Before publishing an update

1. Verify the demo/full-game dates and availability on Steam. Confirm any changed gameplay statements against the intended demo build.
2. Add a dated entry to [Updates](../Press%20Kit/Updates.md). Distinguish kit edits from game build changes.
3. Update the source Markdown and asset catalog; run the commands above.
4. Inspect generated previews and the ZIP contents. Confirm that no private keys, contacts, internal notes or unapproved quotes entered the pack.
5. Commit and push the intended files, then check the README, copy, gallery and ZIP while signed out. Match the ZIP download's SHA-256 against [download details](../Downloads/README.md).

At launch, confirm the demo is actually downloadable before changing copy to “available now.” Keep the dated pre-launch release as an archive or replace it deliberately; never publish a launch claim merely because the scheduled time has passed.
