import argparse
from agent.ingestion import ingest_urls, ingest_folder
from agent.claim_extraction import extract_claims
from agent.validation import validate_claims
from agent.grouping import group_claims
from agent.digest import generate_digest
from agent.exporter import export_sources
import os
from agent.vizualization import visualize_groups

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--urls_file", required=False, help="Path to a text file containing URLs (one per line)"
    )
    parser.add_argument(
        "--folder_path", required=False, help="Path to a folder containing text/HTML files"
    )
    parser.add_argument("--topic", required=True)

    args = parser.parse_args()

    sources = []

    # Ingest URLs if provided
    if args.urls_file:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        if urls:
            sources.extend(ingest_urls(urls))

    # Ingest local folder files if provided
    if args.folder_path:
        if os.path.exists(args.folder_path):
            sources.extend(ingest_folder(args.folder_path))
        else:
            print(f"Folder not found: {args.folder_path}")

    if not sources:
        print("No sources were loaded. Exiting.")
        return

    print("Loaded sources:")
    for s in sources:
        print(s.source_id, len(s.content))

    all_claims = []

    for source in sources:
        claims = extract_claims(source)
        validated = validate_claims(claims, source.content)
        all_claims.extend(validated)

    groups = group_claims(all_claims)
    visualize_groups(groups)

    os.makedirs("data/outputs", exist_ok=True)
    digest_file_path = "data/outputs/digest.md"

    if not groups:
        with open(digest_file_path, "w", encoding="utf-8") as f:
            f.write(f"# Research Digest: {args.topic}\n\n")
            f.write("No valid claims were extracted from the provided sources.\n")
        print("Digest created (no claims).")
        return

    sources_lookup = {s.source_id: s for s in sources}
    digest = generate_digest(groups, args.topic, sources_lookup)

    with open(digest_file_path, "w", encoding="utf-8") as f:
        f.write(digest)

    export_sources(groups, "data/outputs/sources.json", sources)
    print(f"Digest and sources exported. Total claims grouped: {len(groups)}")


if __name__ == "__main__":
    main()
