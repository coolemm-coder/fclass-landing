#!/usr/bin/env python3
"""Disabled cold-outreach sender.

This file used to contain executable email outreach payloads. It is intentionally
neutralized: outbound email must not be sent from a committed script without
owner approval, reviewed recipients, reviewed copy, and an explicit dry-run log.
"""

import sys


def main() -> int:
    print(
        "send_outreach_4.py is disabled. "
        "Prepare outreach as a reviewed draft, then send manually or through an approved workflow."
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
