from pathlib import Path


def main() -> None:
    env = Path(".env.sample")
    if not env.exists():
        env.write_text("PROJECT_NAME=sample\nDESCRIPTION=sample description\n")
    out = Path("output")
    out.mkdir(exist_ok=True)


if __name__ == "__main__":
    main()
