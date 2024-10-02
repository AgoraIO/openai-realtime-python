import argparse
import logging
from typing import TypedDict

from .logger import setup_logger

# Set up the logger with color and timestamp support
logger = setup_logger(name=__name__, log_level=logging.INFO)


class RealtimeKitOptions(TypedDict):
    channel_name: str
    uid: int

def parse_args():
    parser = argparse.ArgumentParser(description="Manage server and agent actions.")
    
    # Create a subparser for actions (server and agent)
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Subparser for the 'server' action (no additional arguments)
    subparsers.add_parser("server", help="Start the server")

    # Subparser for the 'agent' action (with required arguments)
    agent_parser = subparsers.add_parser("agent", help="Run an agent")
    agent_parser.add_argument("--channel_name", required=True, help="Channel Id / must")
    agent_parser.add_argument("--uid", type=int, default=0, help="User Id / default is 0")

    return parser.parse_args()


def parse_args_realtimekit() -> RealtimeKitOptions:
    args = parse_args()
    logger.info(f"Parsed arguments: {args}")

    if args.action == "agent":
        options: RealtimeKitOptions = {"channel_name": args.channel_name, "uid": args.uid}
        return options

    return None