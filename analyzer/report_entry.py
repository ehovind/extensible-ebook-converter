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

# ==========================================================================
# CLASS:
#   ReportEntry
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class ReportEntry(object):
    


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(entry_type, filename))
    # ==========================================================================
    def __init__(self, entry_type, filename):
        self.entry_type = entry_type
        self.filename = filename
        
        # properties (data attributes)
        self.encoding = None
        self.metadata_status = None
        self.articles_status = None
        self.markup_status = None
        self.spellcheck_status = None
        self.detailed_report = None
        self.errors = None

        

    # ==========================================================================
    # METHOD:
    #   set_errors(errors)
    # ==========================================================================
    def set_errors(self, errors):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.errors = errors
    
    # ==========================================================================
    # METHOD:
    #   set_encoding(encoding)
    # ==========================================================================
    def set_encoding(self, encoding):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.encoding = encoding

    # ==========================================================================
    # METHOD:
    #   set_articles_status(articles_status)
    # ==========================================================================
    def set_articles_status(self, articles_status):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.articles_status = articles_status
    # ==========================================================================
    # METHOD:
    #   set_metadata_status(metadata_status)
    # ==========================================================================
    def set_metadata_status(self, metadata_status):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.metadata_status = metadata_status

    # ==========================================================================
    # METHOD:
    #   set_markup_status(markup_status)
    # ==========================================================================
    def set_markup_status(self, markup_status):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.markup_status = markup_status
    
    # ==========================================================================
    # METHOD:
    #   set_spellcheck_status(spellcheck_status)
    # ==========================================================================
    def set_spellcheck_status(self, spellcheck_status):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        self.spellcheck_status = spellcheck_status

    # ==========================================================================
    # METHOD:
    #   get_type()
    # ==========================================================================
    def get_type(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.entry_type
    # ==========================================================================
    # METHOD:
    #   get_filename()
    # ==========================================================================
    def get_filename(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.filename

    # ==========================================================================
    # METHOD:
    #   get_encoding()
    # ==========================================================================
    def get_encoding(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.encoding

    # ==========================================================================
    # METHOD:
    #   get_markup_status()
    # ==========================================================================
    def get_markup_status(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.markup_status
    
    # ==========================================================================
    # METHOD:
    #   get_spellcheck_status()
    # ==========================================================================
    def get_spellcheck_status(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.spellcheck_status
    
    # ==========================================================================
    # METHOD:
    #   get_metadata_status()
    # ==========================================================================
    def get_metadata_status(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.metadata_status
    
    # ==========================================================================
    # METHOD:
    #   get_articles_status()
    # ==========================================================================
    def get_articles_status(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        return self.articles_status

