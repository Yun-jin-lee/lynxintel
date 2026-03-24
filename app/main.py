from app.cli.commands import run_browse_command, run_probe_command, run_search_command
from app.cli.parser import build_parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "probe":
        return run_probe_command(args)

    if args.command == "search":
        return run_search_command(args)

    if args.command == "browse":
        return run_browse_command(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())