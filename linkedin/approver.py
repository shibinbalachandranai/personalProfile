def run_approval_flow(post: str) -> tuple:
    """
    Present the post to the user and collect their decision.

    Returns:
        (text, action) where action is one of:
            "approved", "edited", "regenerate", "save_draft", "quit"
        text is None only when action is "regenerate", "save_draft", or "quit"
        and no edits were made.
    """
    while True:
        word_count = len(post.split())
        print("\n" + "=" * 60)
        print("GENERATED POST")
        print("=" * 60)
        print(post)
        print("=" * 60)
        print(f"Word count: {word_count}")
        print()
        print("Options:")
        print("  [A] Approve and post to LinkedIn")
        print("  [E] Edit the post manually")
        print("  [R] Regenerate with Claude")
        print("  [S] Save as draft (don't post)")
        print("  [Q] Quit without saving")
        print()

        choice = input("Your choice: ").strip().upper()

        if choice == "A":
            return (post, "approved")

        elif choice == "E":
            edited = _edit_post(post)
            if edited is not None:
                return (edited, "edited")
            # User cancelled edit — loop back to show menu again

        elif choice == "R":
            return (None, "regenerate")

        elif choice == "S":
            return (post, "save_draft")

        elif choice == "Q":
            return (None, "quit")

        else:
            print("Invalid choice. Please enter A, E, R, S, or Q.")


def _edit_post(original: str) -> str | None:
    """
    Let the user type a replacement post line by line.
    Type END on its own line to finish. Type CANCEL to abort.
    Returns the edited text, or None if the user cancelled.
    """
    print()
    print("Enter your edited post below.")
    print("Type END on its own line when finished, or CANCEL to go back.")
    print("-" * 60)

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        if line.strip().upper() == "CANCEL":
            print("Edit cancelled.")
            return None
        lines.append(line)

    edited = "\n".join(lines).strip()
    if not edited:
        print("No content entered. Edit cancelled.")
        return None

    word_count = len(edited.split())
    print()
    print("-" * 60)
    print("Preview of edited post:")
    print(edited)
    print("-" * 60)
    print(f"Word count: {word_count}")
    confirm = input("Accept this edit? [Y/N]: ").strip().upper()
    if confirm == "Y":
        return edited
    else:
        print("Edit discarded.")
        return None
