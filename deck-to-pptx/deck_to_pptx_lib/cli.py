from __future__ import annotations

import argparse
from pathlib import Path

from .config import DEFAULT_MAX_SLIDES, STYLE_ALIASES
from .intake.normalizer import normalize_bundle
from .intake.source_router import route_source
from .planner.deck_builder import build_deck
from .planner.qa_checker import run_qa
from .planner.scene_planner import plan_scenes
from .renderer.pptx_renderer import render_deck_to_pptx
from .utils.text import slugify


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a PPTX deck from a topic, brief, or materials folder.")
    parser.add_argument("source", help="Topic text or local path")
    parser.add_argument("--outline", default="", help="Optional outline or supporting notes")
    parser.add_argument("--audience", default="", help="Target audience")
    parser.add_argument("--tone", default="", help="Tone hint")
    parser.add_argument("--style", default="auto", choices=list(STYLE_ALIASES.keys()), help="Visual style")
    parser.add_argument("--max-slides", type=int, default=DEFAULT_MAX_SLIDES, help="Maximum slide count")
    parser.add_argument("--lang", default="auto", help="Language hint")
    parser.add_argument("--output", default="", help="Output PPTX path")
    return parser


def _default_output_path(source: str, provided_output: str) -> Path:
    if provided_output:
        return Path(provided_output).expanduser().resolve()
    return (Path.cwd() / f"{slugify(source)}.pptx").resolve()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    bundle = route_source(
        args.source,
        outline=args.outline,
        audience=args.audience,
        tone=args.tone,
        language=args.lang,
    )
    source = normalize_bundle(bundle)
    scenes = plan_scenes(source, max_slides=args.max_slides)
    deck = build_deck(
        source,
        scenes,
        style=args.style,
        audience=args.audience,
        tone=args.tone,
    )
    deck = run_qa(deck)
    output_path = _default_output_path(source.title, args.output)
    render_deck_to_pptx(deck, output_path)

    print(f"source: {bundle.mode}")
    print(f"title: {source.title}")
    print(f"style: {deck.style_direction}")
    print(f"slides: {len(deck.slides)}")
    print(f"output: {output_path}")
    if deck.qa_notes:
        print(f"qa: {'; '.join(deck.qa_notes)}")
    return 0
