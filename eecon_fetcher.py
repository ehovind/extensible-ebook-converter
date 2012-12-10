#!/usr/bin/env python
"""
This file is part of Extensible eBook Converter (EeCon),
an advanced ebook analysis and conversion tool.
Copyright (C) 2012 Espen Hovind <espehov@ifi.uio.no>

EeCon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Eeon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EeCon.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
from fetcher import fetcher as Fetcher


# ==============================================================================
# CONFIGURATION:
# ==============================================================================
WORKSPACE = "workspace/project_runeberg/"
VALID_DOMAINS = ("runeberg.org",)


# ==============================================================================
# FUNCTION:
#   main()
# ==============================================================================
def main():
    """
    DESCRIPTION:
        
    PARAMETERS:
    
    RETURN: 
    """

    # parse arguments
    args = parse_command()

    # fetch and initalize the workspace
    fetcher = Fetcher.Fetcher(WORKSPACE, VALID_DOMAINS, args)

    # process the arguments
    fetcher.process()


# ==============================================================================
# FUNCTION:
#   parse_command()
# ==============================================================================
def parse_command():
    """
    DESCRIPTION:
    Parse the user-provided command using argparse.
        
    PARAMETERS:
        None
    
    RETURN: 
        Dictionary of command line options
    """
    print "[STATUS] parsing arguments... ",

    # create an ArgumentParser
    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument("--auto-markup", action="store_true", 
            help="Automatic conversion from HTML to XHTML (best effort)")
    parser.add_argument("--auto-populate", action="store_true",
            help="Automatic population from Project Runeberg Pages files")
    parser.add_argument("--auto-utf8", action="store_true", 
            help="auto convert publication files to UTF-8")
    parser.add_argument("--patch", help="apply pre-made git patch")
    parser.add_argument("--source", 
            help="fetch a ebook archive URL or filename")
    parser.add_argument("--title", 
            help="title of publication")

    # parse the command into a ArgumentParser object
    args = parser.parse_args()

    print "ok."

    # return a dict with command line options
    return vars(args)



# ==============================================================================
# MODULE:
#   __name__
# ==============================================================================
if __name__ == "__main__":
    main()


