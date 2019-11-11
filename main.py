import argparse

from src import to_csv
from src import get_searcher, AVAILABLE_SEARCHERS
from src.scraper import requester


def get_parser():
    parser = argparse.ArgumentParser(description="Scrap azlyrics page")

    parser.add_argument(
        "--output", "-o",
        type=str,
        dest="output_file",
        default="output.csv",
        required=True,
        help="Output file name."
    )

    parser.add_argument(
        "--search_by",
        choices=AVAILABLE_SEARCHERS,
        type=str,
        dest="search_by",
        required=True,
        help="Set how to search by parameter."
    )

    parser.add_argument(
        "--search", "-s",
        type=str,
        dest="search",
        required=True,
        help="Search the following string."
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        dest="batch_size",
        help="Set the request batch size."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser()
    if args.batch_size:
        requester.batch_requests = args.batch_size

    searcher = get_searcher(name=args.search_by)
    for result in searcher(args.search):
        to_csv(output_file=args.output_file, songs=result.run())
