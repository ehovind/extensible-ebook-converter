
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

from converter.source_factory import SourceFactory

# ==========================================================================
# CLASS:
#   SourceRuneberg(SourceFactory)
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class SourceRuneberg(SourceFactory):
    """
    DESCRIPTION:
    
    PARAMETERS:
    """


    # ==========================================================================
    # CONSTRUCTOR:
    #    __init__(title, metadata, articles, pages)
    # ==========================================================================
    def __init__(self, title, metadata, articles, pages):

        SourceFactory.__init__(     self, title, metadata, 
                                    articles, pages         )





