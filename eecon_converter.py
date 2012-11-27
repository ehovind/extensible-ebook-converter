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
from converter import ebook_converter as EbookConverter



# ==========================================================================
# CONFIGURATION:
# ==========================================================================
WORKSPACE = "workspace/project_runeberg/"


# ==========================================================================
# FUNCTION:
#   main()
# ==========================================================================
def main():
    """ 
    DESCRIPTION:
        
    PARAMETERS:
    
    RETURN: 
    """
    
    # parse arguments
    args = parse_command()
    

    # start the ebook conversion process
    ebook_converter = EbookConverter.EbookConverter(WORKSPACE, args)
    ebook_converter.process()



# ==========================================================================
# FUNCTION:
#   parse_command()
# ==========================================================================
def parse_command():
    """ 
    DESCRIPTION:
        Parse the arguments from command line.
        
    PARAMETERS:
        None
    
    RETURN: 
        void
    """


    print "[STATUS] parsing arguments..."


    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument("--title", help="title of publication")
    parser.add_argument("--output-format", choices=["epub"], 
            help="select a output format")
    parser.add_argument("--compress-only", action="store_true", 
            help="compress ePub container after manual modifications")

    # parse the command into a ArgumentParser object
    args = parser.parse_args()

    # return a dict with command line options
    return vars(args)



# ==========================================================================
# MODULE:
#   __name__
# ==========================================================================
if __name__ == "__main__":
    main()


