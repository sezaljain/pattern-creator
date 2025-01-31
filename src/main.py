"""Main module for pattern creation."""


def create_pattern(size: int) -> str:
    """Create a simple star pattern.

    Args:
        size: The size of the pattern

    Returns:
        The pattern as a string
    """
    pattern = []
    for i in range(size):
        pattern.append("*" * (i + 1))
    return "\n".join(pattern)


def main() -> None:
    """Main function."""
    pattern = create_pattern(5)
    print(pattern)


if __name__ == "__main__":
    main()
