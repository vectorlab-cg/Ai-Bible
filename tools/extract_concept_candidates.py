"""Map working segments to candidate concepts using transparent keyword rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CONCEPTS: dict[str, tuple[str, ...]] = {
    "ai-foundations": ("artificial intelligence", "machine learning", "llm", "large language model"),
    "generative-ai": ("generative ai", "generative artificial intelligence"),
    "rag": ("rag", "retrieval augmented generation", "retrieval-augmented generation"),
    "embeddings-vector-search": ("embedding", "vector database", "vector search"),
    "context-engineering": ("context engineering", "context window", "context management"),
    "fine-tuning": ("fine-tuning", "fine tuning", "lora", "fine-tuned"),
    "agents": ("ai agent", "ai agents", "agentic", "agentic engineering", "super agents"),
    "skills-and-mcp": ("agent skill", "skills", "model context protocol", "mcp"),
    "memory-and-tools": ("agentic harness", "tool use", "memory", "progressive disclosure"),
    "rules-and-model-choice": ("business rules", "rules engine", "when not to use ai", "machine learning"),
    "evaluation": ("benchmark", "evaluation", "eval", "llm as a judge"),
    "observability": ("mlflow", "tracing", "observability", "telemetry"),
    "software-engineering": ("software engineering", "code review", "code quality", "developer productivity"),
    "architecture": ("architecture", "architectural", "system design", "orchestration"),
    "security": ("cybersecurity", "security", "prompt injection", "red team", "vulnerability"),
    "governance-risk": ("governance", "risk", "explainability", "iso 42001", "nist"),
    "privacy-sovereignty": ("digital sovereignty", "data sovereignty", "privacy"),
    "hallucinations": ("hallucination", "hallucinations", "grounded", "grounding"),
    "infrastructure": ("gpu", "cpu", "vllm", "llama.cpp", "compute"),
    "cost-outcomes": ("tokenmaxxing", "valuemaxxing", "cost", "outcomes"),
    "data-systems": ("large database models", "sql data", "database model", "digital librarian"),
    "temporal-news": ("anthropic", "openai", "hugging face", "ibm's", "nvidia", "stripe", "reddit", "thinking machines", "pacing", "glm-5.2", "muse", "astra", "deepseek"),
}

WORD_PATTERN = re.compile(r"\s+")


def load_segments(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def find_matches(segment: dict[str, Any]) -> list[dict[str, Any]]:
    haystack = WORD_PATTERN.sub(" ", f"{segment['title']} {segment['text']}".lower())
    matches: list[dict[str, Any]] = []
    for concept_id, terms in CONCEPTS.items():
        matched_terms = sorted({term for term in terms if term in haystack})
        if matched_terms:
            matches.append(
                {
                    "concept_id": concept_id,
                    "matched_terms": matched_terms,
                    "score": len(matched_terms),
                }
            )
    return sorted(matches, key=lambda item: (-item["score"], item["concept_id"]))


def write_candidates(input_file: Path, output_file: Path) -> tuple[int, int]:
    segments = load_segments(input_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    matched_segments = 0
    candidate_links = 0
    with output_file.open("w", encoding="utf-8") as handle:
        for segment in segments:
            matches = find_matches(segment)
            if matches:
                matched_segments += 1
                candidate_links += len(matches)
            result = {
                "segment_id": segment["segment_id"],
                "source_id": segment["source_id"],
                "title": segment["title"],
                "category": segment["category"],
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "concept_candidates": matches,
            }
            handle.write(json.dumps(result, ensure_ascii=True) + "\n")
    return matched_segments, candidate_links


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("segments_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    matched_segments, candidate_links = write_candidates(args.segments_file, args.output_file)
    print(f"Mapped {matched_segments} segments to {candidate_links} candidate concept links")


if __name__ == "__main__":
    main()
