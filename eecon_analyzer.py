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
from analyzer import source_analyzer as SourceAnalyzer


# ==============================================================================
# CONFIGURATION:
# ==============================================================================
WORKSPACE = "workspace/project_runeberg/" 


# ==============================================================================
# FUNCTION:
#   main()
# ==============================================================================
def main():
    """
    DESCRIPTION:
        Main
        
    PARAMETERS:
        None
    
    RETURN: 
        void
    """


    # parse arguments
    args = parse_command()

    # process staging area and build a report
    source_analyzer = SourceAnalyzer.SourceAnalyzer(WORKSPACE, args)
    source_analyzer.process()





# ==============================================================================
# FUNCTION:
#   parse_command()
# ==============================================================================
def parse_command():
    """
    DESCRIPTION:
        Parse the arguments from command line.
        
    PARAMETERS:
        None
    
    RETURN: 
        void
    """
    print "[STATUS] parsing arguments... ",


    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument("--language", choices=["sv", "nb", "da", "la"], 
            help="select a publicatio language")
    parser.add_argument("--markup", choices=["lxml", "tidy"], 
            help="select a markup parser")
    parser.add_argument("--encoding", choices=["file", "chardet"], 
            help="select a encoding detector")
    parser.add_argument("--metadata", choices=["dc"], 
            help="select a metadata analyzer")
    parser.add_argument("--spellcheck", choices=["aspell"], 
            help="select a spellchecker")
    parser.add_argument("--title", help="title of publication")
    parser.add_argument("-f", "--format", action="store_true", 
            help="supported output formats")

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


