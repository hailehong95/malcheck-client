#!/usr/bin/env python

import click

from malcheck_utils.clean import malcheck_clean
from malcheck_utils.build import malcheck_build
from malcheck_utils.update import malcheck_update
from malcheck_utils.extract import malcheck_extract
from malcheck_utils.version import malcheck_version
from malcheck_utils.keygen import malcheck_keygen, malcheck_copy_key


@click.group()
def cli():
    """A CLI Utility for MalCheck Client"""
    pass


@cli.command(name="version", help="Show MalCheck utility version")
def version():
    malcheck_version()


@cli.command(name="clean", help="Clean all temporary working files")
def clean():
    malcheck_clean()


@cli.command(name="keygen", help="RSA keypair generator")
def keygen():
    malcheck_keygen()


@cli.command(name="make", help="Create MalCheck client bundle")
def make():
    malcheck_update()
    malcheck_extract()
    malcheck_copy_key()


@cli.command(name="build", help="Build MalCheck client")
def build():
    malcheck_update()
    malcheck_extract()
    malcheck_copy_key()
    malcheck_build()


if __name__ == "__main__":
    cli()
