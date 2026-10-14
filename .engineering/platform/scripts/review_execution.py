#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "1"

SEQUENCE_PATTERN = re.compile(r"^(\d{4})-")


@dataclass(frozen=True)
class ReviewInput:
    review_type: str
    skill: str
    target: str
    target_sha256: str
    context: tuple[tuple[str, str], ...]
    platform_version: str
    protocol_version: str = PROTOCOL_VERSION


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as source:
        while True:
            chunk = source.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def repository_relative(
    root: Path,
    path: Path,
) -> str:
    try:
        relative = path.resolve().relative_to(
            root.resolve()
        )
    except ValueError:
        fail(
            "Review inputs must be inside "
            f"the repository: {path}"
        )

    return relative.as_posix()


def extract_metadata_value(
    text: str,
    key: str,
) -> str | None:
    pattern = re.compile(
        rf"^{re.escape(key)}:\s*(.+?)\s*$",
        re.MULTILINE,
    )

    match = pattern.search(text)

    if not match:
        return None

    value = (
        match.group(1)
        .strip()
        .strip("\"'")
    )

    if not value:
        return None

    return value


def review_metadata_value(
    review: Path,
    key: str,
) -> str | None:
    return extract_metadata_value(
        review.read_text(encoding="utf-8"),
        key,
    )


def resolve_input_file(
    root: Path,
    value: str,
) -> tuple[str, str]:
    path = root / value

    if not path.is_file():
        fail(
            f"Review input does not exist: {value}"
        )

    relative = repository_relative(
        root,
        path,
    )

    return (
        relative,
        sha256_file(path),
    )


def is_review_of_target(
    root: Path,
    context_value: str,
    target_path: str,
) -> bool:
    context_path = root / context_value

    if not context_path.is_file():
        return False

    try:
        relative = repository_relative(
            root,
            context_path,
        )
    except SystemExit:
        return False

    if "/reviews/" not in f"/{relative}":
        return False

    reviewed_artifact = review_metadata_value(
        context_path,
        "reviewed-artifact",
    )

    return reviewed_artifact == target_path


def normalized_context_entries(
    root: Path,
    target_path: str,
    contexts: list[str],
) -> tuple[tuple[str, str], ...]:
    entries: set[tuple[str, str]] = set()

    for context in contexts:
        if context == target_path:
            continue

        if is_review_of_target(
            root,
            context,
            target_path,
        ):
            continue

        entries.add(
            resolve_input_file(
                root,
                context,
            )
        )

    return tuple(
        sorted(
            entries,
            key=lambda item: item[0],
        )
    )


def build_review_input(
    root: Path,
    review_type: str,
    skill: str,
    target: str,
    contexts: list[str],
    platform_version: str,
) -> ReviewInput:
    target_path, target_hash = resolve_input_file(
        root,
        target,
    )

    ordered_context = normalized_context_entries(
        root=root,
        target_path=target_path,
        contexts=contexts,
    )

    return ReviewInput(
        review_type=review_type,
        skill=skill,
        target=target_path,
        target_sha256=target_hash,
        context=ordered_context,
        platform_version=platform_version,
    )


def manifest_dict(
    review_input: ReviewInput,
) -> dict[str, Any]:
    return {
        "reviewType": review_input.review_type,
        "skill": review_input.skill,
        "target": {
            "path": review_input.target,
            "sha256": review_input.target_sha256,
        },
        "context": [
            {
                "path": path,
                "sha256": sha256,
            }
            for path, sha256
            in review_input.context
        ],
        "platformVersion": (
            review_input.platform_version
        ),
        "protocolVersion": (
            review_input.protocol_version
        ),
    }

def rendered_manifest(
    review_input: ReviewInput,
) -> str:
    return json.dumps(
        manifest_dict(review_input),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )


def extract_execution_manifest(
    review_text: str,
) -> dict[str, Any]:
    pattern = re.compile(
        r"^## Execution Manifest\s*$"
        r".*?"
        r"^```json\s*$"
        r"\n(.*?)"
        r"^```\s*$",
        re.MULTILINE | re.DOTALL,
    )

    match = pattern.search(review_text)

    if not match:
        fail(
            "Canonical review does not contain "
            "a JSON Execution Manifest."
        )

    try:
        value = json.loads(
            match.group(1)
        )
    except json.JSONDecodeError as exc:
        fail(
            "Canonical review contains an "
            "invalid JSON Execution Manifest: "
            f"{exc}"
        )

    if not isinstance(value, dict):
        fail(
            "Canonical review Execution Manifest "
            "must be a JSON object."
        )

    return value


def fingerprint(
    review_input: ReviewInput,
) -> str:
    normalized = json.dumps(
        manifest_dict(review_input),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(
        normalized
    ).hexdigest()


def review_sequence(path: Path) -> int:
    match = SEQUENCE_PATTERN.match(
        path.name
    )

    if not match:
        return 0

    return int(match.group(1))


def completed_reviews(
    reviews_dir: Path,
) -> list[Path]:
    if not reviews_dir.exists():
        return []

    result: list[Path] = []

    for review in reviews_dir.glob("*.md"):
        if (
            review_metadata_value(
                review,
                "status",
            )
            == "completed"
        ):
            result.append(review)

    return sorted(
        result,
        key=review_sequence,
    )


def find_equivalent_review(
    reviews_dir: Path,
    input_fingerprint: str,
    protocol_version: str = PROTOCOL_VERSION,
) -> Path | None:
    for review in completed_reviews(
        reviews_dir
    ):
        recorded_protocol = review_metadata_value(
            review,
            "protocol-version",
        )

        recorded_fingerprint = (
            review_metadata_value(
                review,
                "input-fingerprint",
            )
        )

        if (
            recorded_protocol == protocol_version
            and recorded_fingerprint
            == input_fingerprint
        ):
            return review

    return None


def find_latest_review_for_target(
    reviews_dir: Path,
    target_path: str,
) -> Path | None:
    matches = [
        review
        for review in completed_reviews(
            reviews_dir
        )
        if review_metadata_value(
            review,
            "reviewed-artifact",
        )
        == target_path
    ]

    if not matches:
        return None

    return max(
        matches,
        key=review_sequence,
    )


def next_sequence(
    reviews_dir: Path,
) -> int:
    highest = 0

    if not reviews_dir.exists():
        return 1

    for path in reviews_dir.glob("*.md"):
        highest = max(
            highest,
            review_sequence(path),
        )

    return highest + 1


def format_sequence(value: int) -> str:
    return f"{value:04d}"


def review_id(
    review: Path | None,
) -> str | None:
    if review is None:
        return None

    return review_metadata_value(
        review,
        "id",
    )


def add_lineage(
    result: dict[str, Any],
    existing: Path | None,
    predecessor: Path | None,
    force: bool,
) -> None:
    if existing is not None:
        if force:
            result["rerunOf"] = review_id(
                existing
            )

        return

    if predecessor is None:
        return

    predecessor_protocol = review_metadata_value(
        predecessor,
        "protocol-version",
    )

    predecessor_fingerprint = review_metadata_value(
        predecessor,
        "input-fingerprint",
    )

    if (
        predecessor_protocol != PROTOCOL_VERSION
        or not predecessor_fingerprint
        or predecessor_fingerprint == "none"
    ):
        result["legacyPredecessor"] = (
            review_id(predecessor)
        )
        return

    result["supersedes"] = review_id(
        predecessor
    )


def command_prepare(
    args: argparse.Namespace,
) -> int:
    root = args.root.resolve()

    reviews_dir = (
        root
        / args.reviews_dir
    ).resolve()

    review_input = build_review_input(
        root=root,
        review_type=args.type,
        skill=args.skill,
        target=args.target,
        contexts=args.context or [],
        platform_version=args.platform_version,
    )

    input_fingerprint = fingerprint(
        review_input
    )

    existing = find_equivalent_review(
        reviews_dir,
        input_fingerprint,
    )

    predecessor = find_latest_review_for_target(
        reviews_dir,
        review_input.target,
    )

    sequence = next_sequence(
        reviews_dir
    )

    result: dict[str, Any] = {
        "protocolVersion": PROTOCOL_VERSION,
        "executionMode": "canonical",
        "reviewType": args.type,
        "skill": args.skill,
        "inputFingerprint": (
            input_fingerprint
        ),
        "manifest": manifest_dict(
            review_input
        ),
        "renderedManifest": rendered_manifest(
            review_input
        ),
        "equivalentReview": (
            repository_relative(
                root,
                existing,
            )
            if existing
            else None
        ),
        "nextSequence": (
            format_sequence(sequence)
        ),
        "shouldExecute": (
            existing is None
            or args.force
        ),
        "forcedRerun": (
            bool(existing)
            and args.force
        ),
    }

    add_lineage(
        result=result,
        existing=existing,
        predecessor=predecessor,
        force=args.force,
    )

    if existing and not args.force:
        result["reason"] = (
            "Equivalent completed review "
            "already exists."
        )

    elif existing and args.force:
        result["reason"] = (
            "Equivalent completed review "
            "exists, but an explicit rerun "
            "was requested."
        )

    else:
        result["reason"] = (
            "No equivalent completed "
            "review found."
        )

    output = json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )

    if args.output:
        output_path = (
            root
            / args.output
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            output + "\n",
            encoding="utf-8",
        )

    print(output)

    return 0


def command_check(
    args: argparse.Namespace,
) -> int:
    root = args.root.resolve()

    review_path = (
        root
        / args.review
    )

    if not review_path.is_file():
        fail(
            "Review does not exist: "
            f"{args.review}"
        )

    review_text = review_path.read_text(
        encoding="utf-8"
    )

    recorded_protocol = review_metadata_value(
        review_path,
        "protocol-version",
    )

    if recorded_protocol != PROTOCOL_VERSION:
        fail(
            "Review protocol version is not "
            "compatible with the current "
            f"protocol. Review={recorded_protocol!r}, "
            f"current={PROTOCOL_VERSION!r}"
        )

    recorded_execution_mode = (
        review_metadata_value(
            review_path,
            "execution-mode",
        )
    )

    if recorded_execution_mode != "canonical":
        fail(
            "Review is not canonical. "
            "Execution manifest verification "
            "applies only to canonical reviews."
        )

    recorded = review_metadata_value(
        review_path,
        "input-fingerprint",
    )

    if (
        not recorded
        or recorded == "none"
    ):
        fail(
            "Review does not contain a "
            "canonical input fingerprint."
        )

    review_input = build_review_input(
        root=root,
        review_type=args.type,
        skill=args.skill,
        target=args.target,
        contexts=args.context or [],
        platform_version=args.platform_version,
    )

    actual = fingerprint(
        review_input
    )

    if actual != recorded:
        print(
            "Review input fingerprint "
            "does not match current inputs."
        )

        print(
            f"Recorded: {recorded}"
        )

        print(
            f"Current:  {actual}"
        )

        return 1

    recorded_target_hash = (
        review_metadata_value(
            review_path,
            "target-sha256",
        )
    )

    if (
        recorded_target_hash
        != review_input.target_sha256
    ):
        print(
            "Review target SHA-256 does not "
            "match current target."
        )

        print(
            "Recorded: "
            f"{recorded_target_hash}"
        )

        print(
            "Current:  "
            f"{review_input.target_sha256}"
        )

        return 1

    persisted_manifest = (
        extract_execution_manifest(
            review_text
        )
    )

    expected_manifest = manifest_dict(
        review_input
    )

    if persisted_manifest != expected_manifest:
        print(
            "Persisted execution manifest "
            "does not match current "
            "canonical inputs."
        )

        print(
            "Persisted:"
        )

        print(
            json.dumps(
                persisted_manifest,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )

        print(
            "Expected:"
        )

        print(
            json.dumps(
                expected_manifest,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )

        return 1

    print(
        "Review input fingerprint "
        "matches current inputs."
    )

    print(
        "Review execution manifest "
        "matches current inputs."
    )

    return 0


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare and validate deterministic "
            "engineering review execution."
        )
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    prepare = subparsers.add_parser(
        "prepare"
    )

    prepare.add_argument(
        "--type",
        required=True,
    )

    prepare.add_argument(
        "--skill",
        required=True,
    )

    prepare.add_argument(
        "--target",
        required=True,
    )

    prepare.add_argument(
        "--context",
        action="append",
        default=[],
    )

    prepare.add_argument(
        "--reviews-dir",
        required=True,
    )

    prepare.add_argument(
        "--platform-version",
        required=True,
    )

    prepare.add_argument(
        "--force",
        action="store_true",
    )

    prepare.add_argument(
        "--output",
    )

    prepare.set_defaults(
        handler=command_prepare
    )

    check = subparsers.add_parser(
        "check"
    )

    check.add_argument(
        "--type",
        required=True,
    )

    check.add_argument(
        "--skill",
        required=True,
    )

    check.add_argument(
        "--target",
        required=True,
    )

    check.add_argument(
        "--context",
        action="append",
        default=[],
    )

    check.add_argument(
        "--platform-version",
        required=True,
    )

    check.add_argument(
        "--review",
        required=True,
    )

    check.set_defaults(
        handler=command_check
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
