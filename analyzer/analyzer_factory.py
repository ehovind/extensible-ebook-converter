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

import os
import subprocess
import sys

from converter import parser_runeberg as ParserRuneberg
from shared import file_operations as FileOperations
from shared import xml_operations as XMLOperations
# ==========================================================================
# CLASS:
#   AnalyzerFactory
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerFactory(object):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    description = "Analyzer"
    available_methods = {}
    dependencies = {}
    


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(description, available_methods, dependencies, path_info)
    # ==========================================================================
    def __init__(self, description, available_methods, dependencies, path_info):
        AnalyzerFactory.description = description
        AnalyzerFactory.available_methods = available_methods
        AnalyzerFactory.dependencies = dependencies
        self.path_info = path_info

        # workspace path info
        self.working_path =  path_info["working_path"]
        self.report_path = path_info["report_path"]

        # external classes
        self.parser_runeberg = ParserRuneberg.ParserRuneberg(None, path_info)
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()



    # ==========================================================================
    # METHOD:
    #   check_dependencies()
    # ==========================================================================
    def check_dependencies(self, message):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        print "\tsearching for dependencies... ", message,
        
        if len(AnalyzerFactory.dependencies.keys()) is 0:
            print "ok."
            return

        for tool in AnalyzerFactory.dependencies.keys():
            dependency = AnalyzerFactory.dependencies[tool]

            


            # check if python library is installed
            if dependency is "library":
                try:
                    __import__ (tool)
                except ImportError:
                    print "[FATAL] No libary: ", tool
                    sys.exit(1)
            
            # check if external binary exists
            if dependency is "external":
                try:     
                    subprocess.call(tool, stdout=open(os.devnull,'w'), 
                            stderr=subprocess.STDOUT)
                except OSError:
                    print "[FATAL] No binary: ", tool
                    sys.exit(1)

        print "ok. "

            
    # ==========================================================================
    # METHOD:
    #   analyze(filename)
    # ==========================================================================
    def analyze(self, filename):
        """
        DESCRIPTION:
            Process command line arguments.
            Abstract method, implemented in subclasses.
            
        PARAMETERS:
            file    string      name of file to analyze
        
        RETURN: 
            status  dict        status information
        """
        raise NotImplementedError( "No implementation available" )
