import argparse
import shutil
import os
import sys


parser = argparse.ArgumentParser(
    description="Script to restore configuration files to default settings."
)
parser.add_argument(
    "-c",
    "--config",
    help="Restore config.yaml to default settings",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-t",
    "--theme",
    help="Restore theme.yaml to default settings",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-a",
    "--all",
    help="Restore all configuration files to default settings",
    action="store_true",
    default=False,
)
args = parser.parse_args()


def restore_theme():
    print("Restoring theme to default settings...")
    abs_path_to_restore = os.path.abspath("../src/bot/theme.yaml")
    abs_path_to_move = os.path.abspath("./defaults/theme.yaml")
    shutil.copy(abs_path_to_move, abs_path_to_restore)
    print("Successfully restored theme.yaml to default settings")


def restore_config():
    print("Restoring configuration to default settings...")
    abs_path_to_restore = os.path.abspath("../src/bot/config.yaml")
    abs_path_to_move = os.path.abspath("./defaults/config.yaml")
    shutil.copy(abs_path_to_move, abs_path_to_restore)
    print("Successfully restored theme.yaml to default settings")


def main():
    if len(sys.argv) <= 1:
        print("No arguments specified, run with -h flag for help")
        sys.exit(1)
    if args.config:
        restore_config()
    if args.theme:
        restore_theme()
    if args.all:
        restore_theme()
        restore_config()


if __name__ == "__main__":
    main()
