#!/usr/bin/env python

import sys
from malcheck_client.gui import main_gui
from malcheck_client.gui import message_box
from malcheck_client.utils import is_admin, internet_check_by_requests


def main():
    if not is_admin():
        message_box("Oops!", "This program requires run as Administrator", 0)
        sys.exit(1)

    if not internet_check_by_requests():
        message_box("Oops!", "Please check your internet connection", 0)
        sys.exit(2)

    main_gui()


if __name__ == "__main__":
    main()
