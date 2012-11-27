
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

from shared import file_operations as FileOperations
from shared import xml_operations as XMLOperations
# ==========================================================================
# CLASS:
#   ParserFactory
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class ParserFactory(object):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """


    format_files = {"runeberg" :"Articles.lst"}


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(title, path_info, ebook_format)
    # ==========================================================================
    def __init__(self, title, path_info, source_format):

        # workspace path info
        self.title = title
        self.info_path =  path_info["info_path"]
        self.original_path =  path_info["original_path"]
        self.working_path =  path_info["working_path"]
        self.source_format = source_format
        self.a_lst_path = self.info_path + "a.lst"
        self.t_lst_path = self.info_path + "t.lst"
        
        # external classes
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()






    # ==========================================================================
    # METHOD:
    #   check_publication()
    # ==========================================================================
    def check_publication(self):
        """
        DESCRIPTION:
            Check publication state. Parsable meta information. 
            Abstract method, implemented in subclasses.
        
        PARAMETERS:
            None
        RETURN: 
            void
        """
        raise NotImplementedError("No parser implemented:", self.source_format)
        


    


    # ==========================================================================
    # METHOD:
    #   parse_source()
    # ==========================================================================
    def parse_source(self):
        """
        DESCRIPTION:
            Parse the publication source.
            Abstract method, implemented in subclasses.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        raise NotImplementedError("No parser implemented:", self.source_format)
