from __future__ import annotations

from typing import Any

import os
import json
from datetime import date


def export_selected_assets(asset_folder: str, version: int = 1):
    """
    Exports the currently selected assets in Maya to FBX files.
    """
    metadata = os.path.join(asset_folder, 'metadata.json')
    export_folder = os.path.join(asset_folder, f'v_{version:03d}')

    generate_metadata(a)

    # mkdir and write metadata
    os.makedirs(export_folder, exist_ok=True)
    with open(metadata, 'w') as f:
        f.write(f'{{"version": {version}}}')


def generate_metadata(asset_name: str, version: int, files: dict[str, str], author: str, asset_path: str) -> dict[str, Any]:
    """
    Creates or updates asset metadata
    """
    metadata_path = os.path.join(asset_path, 'metadata.json').replace("\\", "/")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {'name': asset_name, 'versions': []}

    for v in metadata['versions']:
        if v['version'] == version:
            raise ValueError(f"Version {version} already exists for asset '{asset_name}'.")

    entry = {
        'version': version,
        'files': files,
        'author': author,
        'date': date.today().isoformat()
    }

    metadata['versions'].append(entry)
    metadata['versions'].sort(key=lambda v: int(v['version'][1:]))
    metadata['latest'] = version

    return metadata


def write_metadata(metadata: dict[str, Any], output_path: str) -> None:
    """
    Writes asset metadata to a JSON file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)


def make_thumbnail_playblast(output_path, width=512, height=512):
    """
    Generates thumbnail using playblast
    """
    import maya.cmds as cmds
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmds.playblast(
        frame=cmds.currentTime(q=True),
        format="image",
        completeFilename=output_path,
        forceOverwrite=True,
        widthHeight=(width, height),
        showOrnaments=False,
        percent=100,
        quality=100
    )