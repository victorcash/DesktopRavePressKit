"""Build the public gallery, plain-text copy and deterministic essential pack."""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = 'https://github.com/victorcash/DesktopRavePressKit'
RAW = PUBLIC + '/raw/refs/heads/main/'
CREDIT = 'Desktop Rave: Idle Audio Club / 28 Ducks'
LINK = re.compile(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)')
ARCHIVE = 'Downloads/Desktop-Rave-Demo-Press-Pack.zip'


def public_link(document: str, target: str) -> str:
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith('#'):
        return target
    resolved = (ROOT / document).parent.joinpath(unquote(parsed.path)).resolve()
    path = resolved.relative_to(ROOT).as_posix()
    kind = 'tree' if resolved.is_dir() else 'blob'
    suffix = ('#' + parsed.fragment) if parsed.fragment else ''
    return f'{PUBLIC}/{kind}/main/{quote(path)}{suffix}'


def plain_text(document: str, text: str) -> str:
    # The opening row is navigation, not release copy.
    text = text.split('\n\n', 1)[1]

    def expand(match: re.Match) -> str:
        label, target = match.groups()
        return label if target.startswith('mailto:') else f'{label} ({public_link(document, target)})'

    text = LINK.sub(expand, text)
    text = re.sub(r'^#{1,6} ', '', text, flags=re.MULTILINE).replace('**', '')
    return re.sub(r'^\*([^\n]+)\*$', r'\1', text, flags=re.MULTILINE)


def generate() -> dict[str, bytes]:
    outputs: dict[str, bytes] = {}
    for name in ['Press Release', 'Press Copy']:
        document = f'Press Kit/{name}.md'
        text = (ROOT / document).read_text(encoding='utf-8')
        outputs[f'Press Kit/{name}.txt'] = plain_text(document, text).encode('utf-8')

    assets = json.loads((ROOT / 'tools/press-assets.json').read_text(encoding='utf-8'))
    assert len({a['name'] for a in assets}) == len(assets), 'Duplicate asset name'
    gallery = [
        '# Desktop Rave — screenshot gallery', '',
        '[Press-kit home](../README.md) · [Essential ZIP](../Downloads/README.md) · '
        '[Logos and key art](../GraphicAssets/README.md)', '',
        f'Suggested credit: **{CREDIT}**. Captions below may be copied or adapted '
        'under the [press-kit license](../LICENSE). Click an image for the original PNG.', '',
        '**About these images:** these are supplied gameplay captures, with no recorded '
        'capture Build IDs. They illustrate the game; UI and content can differ from the '
        'current demo. The Level 11 showcase is identified below and is not in the '
        'essential demo pack. See the [demo FAQ](../Press%20Kit/Demo%20FAQ.md) for demo limits.', '',
        'Previews are reduced in size only. Downloaded originals retain the supplied pixels. '
        'The essential ZIP uses the descriptive filenames shown below.', '',
    ]
    captions = [f'Suggested credit: {CREDIT}', '',
                'Supplied gameplay captures; capture Build IDs are not recorded. '
                'UI and content may differ from the current demo.', '']
    members: dict[str, bytes] = {}
    for asset in assets:
        source = ROOT / asset['source']
        assert source.resolve().is_relative_to(ROOT), 'Asset must stay inside the kit'
        assert source.is_file(), source
        preview = f"Screenshots/Previews/{asset['name']}.png"
        with Image.open(source) as original:
            width, height = original.size
            thumb = original.copy()
            thumb.thumbnail((640, 360), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            thumb.save(buffer, format='PNG', optimize=True)
            outputs[preview] = buffer.getvalue()
        raw_url = RAW + quote(asset['source'])
        gallery.extend([
            f"## {asset['title']}", '',
            f'<a href="{raw_url}"><img src="Previews/{asset["name"]}.png" '
            f'width="480" alt="{html.escape(asset["caption"], quote=True)}"></a>', '',
            asset['caption'], '',
            f"**{asset['kind']}** · {width} × {height} PNG · "
            f"[Original PNG]({raw_url})" + (' · **Included in essential pack**' if asset['pack'] else ''), '',
            f"Suggested filename: `{asset['name']}.png`", '',
        ])
        if asset['pack']:
            filename = f"Images/{asset['name']}.png"
            members[filename] = source.read_bytes()
            captions.extend([filename, asset['caption'], f"Type: {asset['kind']}", ''])
    outputs['Screenshots/README.md'] = ('\n'.join(gallery)).encode('utf-8')

    for source, destination in [
        ('GraphicAssets/library_logo_transparent.png', 'Branding/desktop-rave-logo-transparent.png'),
        ('GraphicAssets/store_capsule_main.png', 'Branding/desktop-rave-key-art-landscape.png'),
    ]:
        members[destination] = (ROOT / source).read_bytes()
    captions.extend(['Branding/desktop-rave-key-art-landscape.png',
                     'Promotional artwork for Desktop Rave: Idle Audio Club.',
                     'Type: promotional key art, not a gameplay screenshot.', ''])
    members['CAPTIONS.txt'] = '\n'.join(captions).encode('utf-8')
    members['LICENSE'] = (ROOT / 'LICENSE').read_text(encoding='utf-8').encode('utf-8')
    documents = sorted((ROOT / 'Press Kit').glob('*.md'))
    for path in documents:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        portable = LINK.sub(lambda m: f'[{m[1]}]({public_link(relative, m[2])})', text)
        members[relative] = portable.encode('utf-8')
    for relative, content in outputs.items():
        if relative.endswith('.txt'):
            members[relative] = content
    members['START-HERE.txt'] = (
        'DESKTOP RAVE: IDLE AUDIO CLUB — ESSENTIAL PRESS PACK\n\n'
        'Prepared 26 September 2026. No embargo.\n'
        'Scheduled free demo: 30 September 2026, 18:00 CEST / 16:00 UTC.\n'
        'Check Steam availability and update pre-launch wording before later publication.\n\n'
        'Press Kit/: announcement, shorter copy, facts, FAQ, reviewer and recording help.\n'
        'Images/: four supplied, original 4K gameplay screenshots with descriptive filenames.\n'
        'Branding/: transparent English logo and landscape key art.\n'
        'CAPTIONS.txt: suggested captions, credit and capture context.\n'
        'LICENSE: permission for coverage, including monetized coverage.\n\n'
        f'Updated kit, all images and separate video downloads: {PUBLIC}\n'
        'Demo: https://store.steampowered.com/app/4987280/\n'
        'Full game: https://store.steampowered.com/app/3952790/\n'
        'Press contact: contact@28ducks.com\n'
    ).encode('utf-8')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, content in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 26, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content)
    archive_bytes = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        assert archive.testzip() is None, 'Invalid ZIP CRC'
        assert len(archive.namelist()) == len(set(archive.namelist())), 'Duplicate ZIP member'
        for name, content in members.items():
            assert archive.read(name) == content, name
    outputs[ARCHIVE] = archive_bytes
    digest = hashlib.sha256(archive_bytes).hexdigest()
    outputs['Downloads/README.md'] = (
        '# Essential press pack\n\n'
        f'**[Download the ZIP]({RAW}{ARCHIVE})** — **{len(archive_bytes)/1048576:.1f} MiB**, '
        f'{len(archive_bytes):,} bytes. No account or repository clone is needed.\n\n'
        'Includes the press release and shorter copy in Markdown/plain text, press facts, demo FAQ, '
        'reviewer and recording guides, contact details, dated build information, four original '
        '4K screenshots, a transparent English logo, landscape key art, captions and the license.\n\n'
        'The selected screenshots show the heart-shaped club, cyan club / Floor Skin collection, '
        'building placement and club beside notes. Filenames describe each image. The Level 11 '
        'showcase and annotated promotion image are not included.\n\n'
        '[Browse all screenshots](../Screenshots/README.md) · [Separate videos](../Trailer/README.md) · '
        '[Optional wallpapers](../Wallpaper/) · [Press-kit home](../README.md)\n\n'
        'Open `START-HERE.txt` after extracting the ZIP. Its written materials link back to the '
        'public kit for extras. This pack contains pre-launch copy dated 26 September 2026; '
        'check Steam availability before publishing later.\n\n'
        f'SHA-256: `{digest}`\n'
    ).encode('utf-8')
    return outputs


def validate_links() -> None:
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        targets = [m[1] for m in LINK.findall(text)]
        targets += re.findall(r'<img[^>]+src="([^"]+)"', text)
        for target in targets:
            parsed = urlsplit(target)
            if target.startswith(RAW):
                resolved = ROOT / unquote(parsed.path.split('/main/', 1)[1])
            elif parsed.scheme or target.startswith('#'):
                continue
            else:
                resolved = path.parent / unquote(parsed.path)
            assert resolved.exists(), f'{path.relative_to(ROOT)}: missing {target}'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without writing files')
    args = parser.parse_args()
    outputs = generate()
    stale = []
    for relative, content in outputs.items():
        target = ROOT / relative
        # Git may check out text with CRLF; compare normalized UTF-8 text.
        matches = target.exists() and (
            target.read_text(encoding='utf-8') == content.decode('utf-8')
            if target.suffix in {'.md', '.txt'} else target.read_bytes() == content
        )
        if not matches:
            stale.append(relative)
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
    if args.check and stale:
        print('Stale generated files:\n' + '\n'.join(stale), file=sys.stderr)
        return 1
    validate_links()
    print(f'PASS: {len(outputs)} generated files, local links, original asset bytes and ZIP integrity.')
    if not args.check:
        print(f'Updated {len(stale)} files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
