#!/usr/bin/env python3

"""
Synchronise versioned Agentic Engineering Platform assets into a consumer repo.

Canonical managed installation:

    .engineering/platform/

Runtime skill exposure:

    .agents/skills/

Consumer manifest:

    .engineering/platform.yaml

The Agentic Engineering Platform release remains authoritative.

Files managed by this script must not be edited directly in consumer
repositories.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is required.\n"
        "Install development dependencies first.",
        file=sys.stderr,
    )
    raise SystemExit(2)


DEFAULT_MANIFEST = Path(".engineering/platform.yaml")
DEFAULT_DESTINATION = Path(".engineering/platform")
DEFAULT_RUNTIME_SKILLS = Path(".agents/skills")
DEFAULT_RUNTIME_LOCK = Path(".agents/platform-skills-lock.json")

GITHUB_RELEASE_URL = (
    "https://github.com/{repository}/releases/download/{version}/{asset}"
)


@dataclass(frozen=True)
class PlatformConfig:
    name: str
    repository: str
    version: str
    skills: tuple[str, ...]
    standards: tuple[str, ...]
    policies: tuple[str, ...]
    templates: tuple[str, ...]
    scripts: tuple[str, ...]


def fail(
    message: str,
    exit_code: int = 1,
) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    raise SystemExit(exit_code)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Synchronise versioned Agentic Engineering Platform "
            "assets into the current repository."
        )
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=(
            "Platform manifest path "
            "(default: .engineering/platform.yaml)"
        ),
    )

    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
        help=(
            "Canonical managed platform destination "
            "(default: .engineering/platform)"
        ),
    )

    parser.add_argument(
        "--runtime-skills-destination",
        type=Path,
        default=DEFAULT_RUNTIME_SKILLS,
        help=(
            "Agent runtime skill discovery destination "
            "(default: .agents/skills)"
        ),
    )

    parser.add_argument(
        "--runtime-lock",
        type=Path,
        default=DEFAULT_RUNTIME_LOCK,
        help=(
            "Runtime skill lock file "
            "(default: .agents/platform-skills-lock.json)"
        ),
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Verify canonical platform assets and runtime skill "
            "exposure without modifying files."
        ),
    )

    return parser.parse_args()


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(
            f"Manifest does not exist: {path}"
        )

    try:
        raw = path.read_text(
            encoding="utf-8"
        )
        data = yaml.safe_load(raw)

    except OSError as exc:
        fail(
            f"Unable to read manifest {path}: {exc}"
        )

    except yaml.YAMLError as exc:
        fail(
            f"Invalid YAML in {path}: {exc}"
        )

    if not isinstance(
        data,
        dict,
    ):
        fail(
            f"Manifest must contain a YAML object: {path}"
        )

    return data


def require_string(
    value: Any,
    field_name: str,
) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
    ):
        fail(
            f"Manifest field '{field_name}' "
            "must be a non-empty string."
        )

    return value.strip()


def read_string_list(
    value: Any,
    field_name: str,
) -> tuple[str, ...]:
    if value is None:
        return tuple()

    if not isinstance(
        value,
        list,
    ):
        fail(
            f"Manifest field '{field_name}' "
            "must be a list."
        )

    result: list[str] = []

    for index, item in enumerate(value):
        if (
            not isinstance(item, str)
            or not item.strip()
        ):
            fail(
                f"Manifest field "
                f"'{field_name}[{index}]' "
                "must be a non-empty string."
            )

        normalised = item.strip()

        if (
            "/" in normalised
            or "\\" in normalised
            or normalised in {".", ".."}
        ):
            fail(
                f"Manifest field "
                f"'{field_name}[{index}]' "
                "must be a simple asset name."
            )

        result.append(
            normalised
        )

    if len(result) != len(set(result)):
        fail(
            f"Manifest field '{field_name}' "
            "contains duplicates."
        )

    return tuple(result)

def read_relative_path_list(
    value: Any,
    field_name: str,
) -> tuple[str, ...]:
    if value is None:
        return tuple()

    if not isinstance(value, list):
        fail(
            f"Manifest field '{field_name}' "
            "must be a list."
        )

    result: list[str] = []

    for index, item in enumerate(value):
        if (
            not isinstance(item, str)
            or not item.strip()
        ):
            fail(
                f"Manifest field "
                f"'{field_name}[{index}]' "
                "must be a non-empty string."
            )

        normalised = item.strip().replace("\\", "/")
        path = PurePosixPath(normalised)

        if (
            path.is_absolute()
            or ".." in path.parts
            or "." in path.parts
        ):
            fail(
                f"Manifest field "
                f"'{field_name}[{index}]' "
                "must be a safe relative path."
            )

        result.append(normalised)

    if len(result) != len(set(result)):
        fail(
            f"Manifest field '{field_name}' "
            "contains duplicates."
        )

    return tuple(result)

def load_config(
    manifest: Path,
) -> PlatformConfig:
    data = read_yaml(
        manifest
    )

    platform = data.get(
        "platform"
    )

    assets = data.get(
        "assets",
        {},
    )

    if not isinstance(
        platform,
        dict,
    ):
        fail(
            "Manifest must define "
            "a 'platform' object."
        )

    if not isinstance(
        assets,
        dict,
    ):
        fail(
            "Manifest 'assets' "
            "must be an object."
        )

    return PlatformConfig(
        name=require_string(
            platform.get("name"),
            "platform.name",
        ),
        repository=require_string(
            platform.get("repository"),
            "platform.repository",
        ),
        version=require_string(
            platform.get("version"),
            "platform.version",
        ),
        skills=read_string_list(
            assets.get("skills"),
            "assets.skills",
        ),
        standards=read_string_list(
            assets.get("standards"),
            "assets.standards",
        ),
        policies=read_string_list(
            assets.get("policies"),
            "assets.policies",
        ),
        templates=read_relative_path_list(
            assets.get("templates"),
            "assets.templates",
        ),
        scripts=read_relative_path_list(
            assets.get("scripts"),
            "assets.scripts",
        ),
    )


def archive_filename(
    config: PlatformConfig,
) -> str:
    return (
        f"{config.name}-"
        f"{config.version}.tar.gz"
    )


def checksum_filename(
    config: PlatformConfig,
) -> str:
    return (
        f"{archive_filename(config)}"
        ".sha256"
    )


def release_url(
    config: PlatformConfig,
    asset_name: str,
) -> str:
    return GITHUB_RELEASE_URL.format(
        repository=config.repository,
        version=config.version,
        asset=asset_name,
    )


def download(
    url: str,
    destination: Path,
) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "agentic-engineering-platform-sync"
            ),
            "Accept": (
                "application/octet-stream"
            ),
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=60,
        ) as response:
            with destination.open(
                "wb"
            ) as output:
                shutil.copyfileobj(
                    response,
                    output,
                )

    except urllib.error.HTTPError as exc:
        fail(
            f"Unable to download {url}: "
            f"HTTP {exc.code} {exc.reason}"
        )

    except urllib.error.URLError as exc:
        fail(
            f"Unable to download {url}: "
            f"{exc.reason}"
        )


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as source:
        while True:
            chunk = source.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(
                chunk
            )

    return digest.hexdigest()


def parse_checksum_file(
    checksum_path: Path,
    expected_filename: str,
) -> str:
    text = checksum_path.read_text(
        encoding="utf-8"
    ).strip()

    if not text:
        fail(
            "Downloaded checksum file is empty."
        )

    parts = text.split()

    if len(parts) < 2:
        fail(
            "Downloaded checksum file "
            "has an invalid format."
        )

    expected_hash = (
        parts[0]
        .strip()
        .lower()
    )

    referenced_file = (
        parts[-1]
        .lstrip("*")
        .strip()
    )

    if referenced_file != expected_filename:
        fail(
            "Checksum file references "
            "an unexpected artifact: "
            f"{referenced_file}"
        )

    if (
        len(expected_hash) != 64
        or any(
            char
            not in "0123456789abcdef"
            for char in expected_hash
        )
    ):
        fail(
            "Checksum file does not contain "
            "a valid SHA-256 value."
        )

    return expected_hash


def verify_archive(
    archive_path: Path,
    checksum_path: Path,
) -> str:
    expected_hash = parse_checksum_file(
        checksum_path,
        archive_path.name,
    )

    actual_hash = sha256_file(
        archive_path
    )

    if actual_hash != expected_hash:
        fail(
            "Platform release checksum "
            "verification failed.\n"
            f"Expected: {expected_hash}\n"
            f"Actual:   {actual_hash}"
        )

    print(
        f"Checksum verified: {actual_hash}"
    )

    return actual_hash


def validate_tar_member(
    member: tarfile.TarInfo,
) -> None:
    path = PurePosixPath(
        member.name
    )

    if path.is_absolute():
        fail(
            "Unsafe absolute path in "
            f"release archive: {member.name}"
        )

    if ".." in path.parts:
        fail(
            "Unsafe parent traversal in "
            f"release archive: {member.name}"
        )

    if (
        member.issym()
        or member.islnk()
    ):
        fail(
            "Links are not allowed in "
            "the platform archive: "
            f"{member.name}"
        )


def extract_archive(
    archive_path: Path,
    destination: Path,
) -> None:
    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with tarfile.open(
            archive_path,
            mode="r:gz",
        ) as archive:
            members = (
                archive.getmembers()
            )

            for member in members:
                validate_tar_member(
                    member
                )

            archive.extractall(
                path=destination,
                members=members,
                filter="data",
            )

    except tarfile.TarError as exc:
        fail(
            "Unable to extract "
            f"platform archive: {exc}"
        )


def require_source(
    release_root: Path,
    relative_path: Path,
) -> Path:
    source = (
        release_root
        / relative_path
    )

    if not source.exists():
        fail(
            "Requested platform asset "
            "does not exist in release: "
            f"{relative_path}"
        )

    return source


def copy_directory(
    release_root: Path,
    relative_path: Path,
    staging_root: Path,
) -> None:
    source = require_source(
        release_root,
        relative_path,
    )

    if not source.is_dir():
        fail(
            "Expected directory in "
            "platform release: "
            f"{relative_path}"
        )

    destination = (
        staging_root
        / relative_path
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copytree(
        source,
        destination,
    )


def copy_file(
    release_root: Path,
    relative_path: Path,
    staging_root: Path,
) -> None:
    source = require_source(
        release_root,
        relative_path,
    )

    if not source.is_file():
        fail(
            "Expected file in "
            "platform release: "
            f"{relative_path}"
        )

    destination = (
        staging_root
        / relative_path
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        source,
        destination,
    )


def populate_snapshot(
    config: PlatformConfig,
    release_root: Path,
    staging_root: Path,
) -> None:
    for skill in config.skills:
        copy_directory(
            release_root,
            Path("skills") / skill,
            staging_root,
        )

    for standard in config.standards:
        copy_directory(
            release_root,
            Path("standards") / standard,
            staging_root,
        )

    for policy in config.policies:
        copy_file(
            release_root,
            Path("policies")
            / f"{policy}.md",
            staging_root,
        )
    for template in config.templates:
        copy_file(
            release_root,
            Path("templates") / Path(template),
            staging_root,
        )
    for script in config.scripts:
        copy_file(
            release_root,
            Path("scripts").joinpath(
                *PurePosixPath(script).parts
            ),
            staging_root,
        )


def calculate_tree_hashes(
    root: Path,
    *,
    excluded_names: set[str] | None = None,
) -> dict[str, str]:
    excluded = (
        excluded_names
        if excluded_names
        else set()
    )

    hashes: dict[str, str] = {}

    if not root.exists():
        return hashes

    for path in sorted(
        root.rglob("*")
    ):
        if not path.is_file():
            continue

        relative = path.relative_to(
            root
        )

        if relative.name in excluded:
            continue

        hashes[
            relative.as_posix()
        ] = sha256_file(
            path
        )

    return hashes


def write_snapshot_metadata(
    config: PlatformConfig,
    staging_root: Path,
    archive_hash: str,
) -> None:
    version_file = (
        staging_root
        / "VERSION"
    )

    version_file.write_text(
        f"{config.version}\n",
        encoding="utf-8",
    )

    file_hashes = (
        calculate_tree_hashes(
            staging_root
        )
    )

    metadata = {
        "name": config.name,
        "repository": (
            config.repository
        ),
        "version": config.version,
        "archiveSha256": (
            archive_hash
        ),
        "managed": True,
        "message": (
            "Generated by "
            "platform_sync.py. "
            "Do not edit managed "
            "platform files manually."
        ),
        "assets": {
            "skills": list(
                config.skills
            ),
            "standards": list(
                config.standards
            ),
            "policies": list(
                config.policies
            ),
             "templates": list(
                config.templates
            ),
            "scripts": list(
                config.scripts
            ),
        },
        "files": file_hashes,
    }

    metadata_file = (
        staging_root
        / "platform-lock.json"
    )

    metadata_file.write_text(
        json.dumps(
            metadata,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def replace_snapshot(
    staging_root: Path,
    destination: Path,
) -> None:
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup: Path | None = None

    if destination.exists():
        backup = (
            destination.parent
            / f".{destination.name}.backup"
        )

        if backup.exists():
            shutil.rmtree(
                backup
            )

        destination.rename(
            backup
        )

    try:
        shutil.copytree(
            staging_root,
            destination,
        )

    except Exception:
        if destination.exists():
            shutil.rmtree(
                destination
            )

        if (
            backup
            and backup.exists()
        ):
            backup.rename(
                destination
            )

        raise

    if (
        backup
        and backup.exists()
    ):
        shutil.rmtree(
            backup
        )


def read_json_file(
    path: Path,
) -> dict[str, Any]:
    if not path.is_file():
        fail(
            f"Required JSON file "
            f"does not exist: {path}"
        )

    try:
        value = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as exc:
        fail(
            f"Invalid JSON in "
            f"{path}: {exc}"
        )

    if not isinstance(
        value,
        dict,
    ):
        fail(
            f"Expected JSON object "
            f"in {path}"
        )

    return value


def runtime_lock_data(
    config: PlatformConfig,
) -> dict[str, Any]:
    return {
        "managedBy": (
            "agentic-engineering-platform"
        ),
        "platform": config.name,
        "repository": (
            config.repository
        ),
        "version": config.version,
        "skills": list(
            config.skills
        ),
    }


def load_previous_managed_skills(
    runtime_lock: Path,
) -> set[str]:
    if not runtime_lock.is_file():
        return set()

    try:
        data = json.loads(
            runtime_lock.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        json.JSONDecodeError,
    ):
        fail(
            "Existing runtime skill lock "
            f"is invalid: {runtime_lock}"
        )

    skills = data.get(
        "skills",
        [],
    )

    if not isinstance(
        skills,
        list,
    ):
        fail(
            "Existing runtime skill lock "
            "contains an invalid skills list."
        )

    return {
        skill
        for skill in skills
        if isinstance(
            skill,
            str,
        )
    }


def expose_runtime_skills(
    config: PlatformConfig,
    canonical_destination: Path,
    runtime_skills_destination: Path,
    runtime_lock: Path,
) -> None:
    runtime_skills_destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    previous_managed = (
        load_previous_managed_skills(
            runtime_lock
        )
    )

    current_managed = set(
        config.skills
    )

    obsolete = (
        previous_managed
        - current_managed
    )

    for skill in sorted(
        obsolete
    ):
        obsolete_path = (
            runtime_skills_destination
            / skill
        )

        if obsolete_path.exists():
            print(
                "Removing obsolete "
                "managed runtime skill: "
                f"{skill}"
            )

            shutil.rmtree(
                obsolete_path
            )

    canonical_skills_root = (
        canonical_destination
        / "skills"
    )

    for skill in config.skills:
        source = (
            canonical_skills_root
            / skill
        )

        destination = (
            runtime_skills_destination
            / skill
        )

        if not source.is_dir():
            fail(
                "Canonical platform skill "
                f"is missing: {source}"
            )

        if destination.exists():
            if (
                skill
                not in previous_managed
            ):
                fail(
                    "Runtime skill destination "
                    "already exists but is not "
                    "recorded as platform-managed: "
                    f"{destination}"
                )

            shutil.rmtree(
                destination
            )

        shutil.copytree(
            source,
            destination,
        )

        print(
            "Exposed runtime skill: "
            f"{skill}"
        )

    runtime_lock.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    runtime_lock.write_text(
        json.dumps(
            runtime_lock_data(
                config
            ),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check_snapshot(
    config: PlatformConfig,
    destination: Path,
) -> list[str]:
    problems: list[str] = []

    lock_file = (
        destination
        / "platform-lock.json"
    )

    if not lock_file.is_file():
        return [
            "Canonical platform snapshot "
            "is not installed or "
            "platform-lock.json is missing."
        ]

    try:
        installed = json.loads(
            lock_file.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        return [
            "Canonical platform-lock.json "
            "contains invalid JSON."
        ]

    expected_fields = {
        "name": config.name,
        "repository": (
            config.repository
        ),
        "version": config.version,
        "assets": {
            "skills": list(
                config.skills
            ),
            "standards": list(
                config.standards
            ),
            "policies": list(
                config.policies
            ),
             "templates": list(
                config.templates
            ),
            "scripts": list(
                config.scripts
            )
        },
    }

    for key, expected in (
        expected_fields.items()
    ):
        actual = installed.get(
            key
        )

        if actual != expected:
            problems.append(
                "Canonical snapshot differs "
                f"for '{key}'."
            )

    recorded_files = installed.get(
        "files"
    )

    if not isinstance(
        recorded_files,
        dict,
    ):
        problems.append(
            "Canonical platform lock does "
            "not contain per-file hashes."
        )

        return problems

    current_files = (
        calculate_tree_hashes(
            destination,
            excluded_names={
                "platform-lock.json",
            },
        )
    )

    if current_files != recorded_files:
        expected_paths = set(
            recorded_files
        )

        actual_paths = set(
            current_files
        )

        for path in sorted(
            expected_paths
            - actual_paths
        ):
            problems.append(
                "Managed platform file "
                f"is missing: {path}"
            )

        for path in sorted(
            actual_paths
            - expected_paths
        ):
            problems.append(
                "Unexpected managed platform "
                f"file exists: {path}"
            )

        for path in sorted(
            expected_paths
            & actual_paths
        ):
            if (
                recorded_files[path]
                != current_files[path]
            ):
                problems.append(
                    "Managed platform file "
                    f"was modified: {path}"
                )

    return problems


def check_runtime_skills(
    config: PlatformConfig,
    canonical_destination: Path,
    runtime_skills_destination: Path,
    runtime_lock: Path,
) -> list[str]:
    problems: list[str] = []

    if not runtime_lock.is_file():
        return [
            "Runtime skill lock is missing: "
            f"{runtime_lock}"
        ]

    try:
        installed_lock = json.loads(
            runtime_lock.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        return [
            "Runtime skill lock "
            "contains invalid JSON."
        ]

    expected_lock = (
        runtime_lock_data(
            config
        )
    )

    if installed_lock != expected_lock:
        problems.append(
            "Runtime skill lock does not "
            "match the platform manifest."
        )

    for skill in config.skills:
        canonical = (
            canonical_destination
            / "skills"
            / skill
        )

        runtime = (
            runtime_skills_destination
            / skill
        )

        if not canonical.is_dir():
            problems.append(
                "Canonical skill is missing: "
                f"{skill}"
            )
            continue

        if not runtime.is_dir():
            problems.append(
                "Runtime skill is missing: "
                f"{skill}"
            )
            continue

        canonical_hashes = (
            calculate_tree_hashes(
                canonical
            )
        )

        runtime_hashes = (
            calculate_tree_hashes(
                runtime
            )
        )

        if (
            canonical_hashes
            != runtime_hashes
        ):
            problems.append(
                "Runtime skill differs from "
                "canonical platform skill: "
                f"{skill}"
            )

    return problems


def check_installation(
    config: PlatformConfig,
    destination: Path,
    runtime_skills_destination: Path,
    runtime_lock: Path,
) -> int:
    problems = []

    problems.extend(
        check_snapshot(
            config,
            destination,
        )
    )

    problems.extend(
        check_runtime_skills(
            config,
            destination,
            runtime_skills_destination,
            runtime_lock,
        )
    )

    if problems:
        print(
            "Platform installation check "
            "FAILED:"
        )

        for problem in problems:
            print(
                f" - {problem}"
            )

        return 1

    print(
        "Platform installation check "
        "PASSED."
    )

    print(
        f"Platform: "
        f"{config.name}"
    )

    print(
        f"Version: "
        f"{config.version}"
    )

    print(
        f"Canonical snapshot: "
        f"{destination}"
    )

    print(
        f"Runtime skills: "
        f"{runtime_skills_destination}"
    )

    return 0


def sync(
    config: PlatformConfig,
    destination: Path,
    runtime_skills_destination: Path,
    runtime_lock: Path,
) -> None:
    archive_name = (
        archive_filename(
            config
        )
    )

    checksum_name = (
        checksum_filename(
            config
        )
    )

    print(
        f"Synchronising "
        f"{config.name} "
        f"{config.version}"
    )

    print(
        f"Source: "
        f"{config.repository}"
    )

    with tempfile.TemporaryDirectory(
        prefix="aep-sync-"
    ) as temp_directory:
        temp = Path(
            temp_directory
        )

        archive_path = (
            temp
            / archive_name
        )

        checksum_path = (
            temp
            / checksum_name
        )

        release_root = (
            temp
            / "release"
        )

        staging_root = (
            temp
            / "snapshot"
        )

        archive_url = release_url(
            config,
            archive_name,
        )

        checksum_url = release_url(
            config,
            checksum_name,
        )

        print(
            "Downloading release artifact: "
            f"{archive_name}"
        )

        download(
            archive_url,
            archive_path,
        )

        print(
            "Downloading checksum: "
            f"{checksum_name}"
        )

        download(
            checksum_url,
            checksum_path,
        )

        archive_hash = (
            verify_archive(
                archive_path,
                checksum_path,
            )
        )

        extract_archive(
            archive_path,
            release_root,
        )

        staging_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        populate_snapshot(
            config,
            release_root,
            staging_root,
        )

        write_snapshot_metadata(
            config,
            staging_root,
            archive_hash,
        )

        replace_snapshot(
            staging_root,
            destination,
        )

    expose_runtime_skills(
        config,
        destination,
        runtime_skills_destination,
        runtime_lock,
    )

    print()
    print(
        "Platform synchronisation "
        "complete."
    )

    print(
        f"Installed version: "
        f"{config.version}"
    )

    print(
        f"Canonical snapshot: "
        f"{destination}"
    )

    print(
        f"Runtime skills: "
        f"{runtime_skills_destination}"
    )

    print()
    print(
        "Managed platform files and "
        "runtime-exposed skills must "
        "not be edited directly."
    )


def main() -> int:
    args = parse_arguments()

    manifest = (
        args.manifest.resolve()
    )

    destination = (
        args.destination.resolve()
    )

    runtime_skills_destination = (
        args.runtime_skills_destination.resolve()
    )

    runtime_lock = (
        args.runtime_lock.resolve()
    )

    config = load_config(
        manifest
    )

    if args.check:
        return check_installation(
            config,
            destination,
            runtime_skills_destination,
            runtime_lock,
        )

    sync(
        config,
        destination,
        runtime_skills_destination,
        runtime_lock,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
