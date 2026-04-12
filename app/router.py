from argparse import Namespace

from app.services.open_service import handle_open
from app.services.probe_service import handle_probe
from app.services.search_service import handle_search
from app.services.status_service import handle_status


def dispatch(args: Namespace) -> int:
    if args.command == "open":
        return handle_open(args.input, dump=args.dump)

    if args.command == "search":
        return handle_search(args.input, dump=args.dump)

    if args.command == "probe":
        return handle_probe(args.input)

    if args.command == "status":
        return handle_status()

    raise ValueError(f"Unknown command: {args.command}")