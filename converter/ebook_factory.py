
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
#   EbookFactory
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class EbookFactory(object):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """

       
    colophon_html = "colophon.html"
    preface_html = "preface.html"
    cover_gif = "cover.gif"


    foreword_text = "text/foreword.html"
    preface_text = "text/preface.html"
    epilogue_text = "text/epilogue.html"
    epilogue_text = "text/epilogue.html"

    # ==========================================================================
    # CONSTRUCTOR:
    #   ___init__(path_info, ebook_source)
    # ==========================================================================

    def __init__(self, path_info, ebook_source):
        self.ebook_source = ebook_source
        
        # workspace path info
        self.working_path =  path_info["working_path"]
        
        # external classes
        self.file_operations = FileOperations.FileOperations()
        self.xml_operations = XMLOperations.XMLOperations()


    # ==========================================================================
    # ABSTRACT METHOD:
    #   validate_source(self)
    # ==========================================================================
    def validate_source(self):
        """
        DESCRIPTION:
            Validate ePub.
            Abstract method, implemented in subclasses.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        raise NotImplementedError(" Abstract method, need to implement this")
    
    
    # ==========================================================================
    # ABSTRACT METHOD:
    #   build():
    # ==========================================================================
    def build(self):
        """
        DESCRIPTION:
            Build ePub.
            Abstract method, implemented in subclasses.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        raise NotImplementedError(" Abstract method, need to implement this")


    # ==========================================================================
    # ABSRACT METHOD:
    #   compress()
    # ==========================================================================
    def compress(self):
        """
        DESCRIPTION:
            Compress ePub.
            Abstract method, implemented in subclasses.
        PARAMETERS:
            None
        RETURN: 
            void
        """
        raise NotImplementedError(" Abstract method, need to implement this")
    





