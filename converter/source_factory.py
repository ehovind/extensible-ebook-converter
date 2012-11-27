
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
#   SourceFactory
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class SourceFactory(object):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """
    
    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(title, metadata, articles, pages)
    # ==========================================================================
    def __init__(self, title, metadata, articles, pages):
        self.title = title
        self.pages = pages
        self.metadata = metadata                
        self.articles = articles              



    # ==========================================================================
    # METHOD:
    #   get_title()
    # ==========================================================================
    def get_title(self):
        """
        DESCRIPTION:
            Get the publication title.
        PARAMETERS:
            None
        RETURN: 
            title   string      Title of publication.
        """
        return self.title

    # ==========================================================================
    # METHOD:
    #   get_metadata()
    # ==========================================================================
    def get_metadata(self):
        """
        DESCRIPTION:
            Get the metadata for publication extracted from Metadata.
        PARAMETERS:
            None
        RETURN: 
            metadata    dict        Metadata elements.
        """
        return self.metadata
    
    
    # ==========================================================================
    # METHOD:
    #   get_articles(self)
    # ==========================================================================
    def get_articles(self):
        """
        DESCRIPTION:
            Get the articles in publication extracted from Articles.lst
        PARAMETERS:
            None
        RETURN: 
            articles    list        Articles entries.
        """
        return self.articles

    # ==========================================================================
    # METHOD:
    #   get_page_info()
    # ==========================================================================
    def get_pages(self):
        """
        DESCRIPTION:
            Get page information extrated from Pages.lst
        PARAMETERS:
            None
        RETURN: 
            page_info   dict    Page information.
        """
        return self.pages

