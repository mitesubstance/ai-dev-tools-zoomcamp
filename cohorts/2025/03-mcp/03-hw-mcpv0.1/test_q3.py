"""Q3 test: fetch minsearch GitHub page via Jina Reader and print char count."""

from scrape import fetch_markdown


def main() -> None:
    url = "https://github.com/alexeygrigorev/minsearch"
    text = fetch_markdown(url)
    print(len(text))


if __name__ == "__main__":
    main()
