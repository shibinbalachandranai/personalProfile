import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import config
from generator import generate_post
from approver import run_approval_flow
from poster import post_to_linkedin, LinkedInPostError


def save_draft(topic: str, text: str, status: str, post_id: str = None) -> Path:
    config.DRAFTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = config.DRAFTS_DIR / f"{timestamp}.json"
    data = {
        "topic": topic,
        "text": text,
        "status": status,
        "word_count": len(text.split()),
        "created_at": datetime.now().isoformat(),
        "posted_id": post_id,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_draft(path: str) -> tuple[str, str]:
    """Returns (topic, text) from a saved draft JSON."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("topic", ""), data["text"]


def main():
    parser = argparse.ArgumentParser(
        description="Generate and post LinkedIn content using Claude AI."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--topic", type=str, help="Topic for the post")
    group.add_argument("--draft", type=str, help="Path to a saved draft JSON to load")
    args = parser.parse_args()

    if not config.ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY is not set. Add it to your .env file.")
        sys.exit(1)

    # Determine starting topic and post text
    if args.draft:
        print(f"Loading draft: {args.draft}")
        topic, post = load_draft(args.draft)
    else:
        topic = args.topic
        print("Generating post with Claude..." + (f" (topic: {topic})" if topic else ""))
        post = generate_post(topic)
        if not topic:
            # Capture whichever topic was randomly chosen
            # generator picks internally; we use a placeholder for the draft
            topic = "(auto-selected)"

    # Approval loop
    while True:
        text, action = run_approval_flow(post)

        if action in ("approved", "edited"):
            draft_path = save_draft(topic, text, "pending")
            print(f"\nDraft saved: {draft_path}")
            print("Posting to LinkedIn...")
            try:
                result = post_to_linkedin(text)
                post_id = result.get("id", "unknown")
                save_draft(topic, text, "posted", post_id)
                print(f"Posted successfully! Post ID: {post_id}")
            except LinkedInPostError as e:
                print(f"\nFailed to post: {e}")
                print(f"Your draft has been saved at: {draft_path}")
                sys.exit(1)
            break

        elif action == "regenerate":
            print("\nRegenerating post with Claude...")
            post = generate_post(topic if topic != "(auto-selected)" else None)

        elif action == "save_draft":
            draft_path = save_draft(topic, text, "draft")
            print(f"\nDraft saved: {draft_path}")
            break

        elif action == "quit":
            print("Exiting without saving.")
            break


if __name__ == "__main__":
    main()
