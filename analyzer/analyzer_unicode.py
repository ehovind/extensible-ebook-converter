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

import sys
import chardet
import subprocess
import os

from analyzer.analyzer_factory import AnalyzerFactory

# ==========================================================================
# CLASS:
#   AnalyzerUnicode
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class AnalyzerUnicode(AnalyzerFactory):
    """
    DESCRIPTION:
        
    PARAMETERS:
    """
    
    # description of analyzer
    description = "A unicode analyzer"
    
    # supported methods for validation
    available_methods = {   "chardet":"Python Unicode detector",
                            "file": "BSD utility", }

    dependencies =  {   "chardet"   :   "library", 
                        "file"      :   "external"  }
   

    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__(self, path_info, method)
    # ==========================================================================
    def __init__(self, path_info, method):
        AnalyzerFactory.__init__( self,
                                  AnalyzerUnicode.description, 
                                  AnalyzerUnicode.available_methods, 
                                  AnalyzerUnicode.dependencies,
                                  path_info )
        self.method = method


    # ==========================================================================
    # METHOD:
    #   analyze(filename)
    # ==========================================================================
    def analyze(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        enc = None
        first = True

        # try to find the file encoding
        if os.path.isfile(filename):
            try:
                # detect encoding using chardet
                if self.method == "chardet":
                    if first:
                        first = False
                    raw_bytes = open(filename).read()
                    enc = self.analyze_chardet(raw_bytes)
                
                # detect encoding using file
                if self.method == "file":
                    if first:
                        first = False
                    enc = self.analyze_file(filename)

            except (OSError,IOError) as err:
                sys.stderr.write("EXCEPTION]: Analyzing file encoding\n ")
           
            # add to dictionary
            if "utf-8" not in enc and "ascii" not in enc and "binary" not in enc:
                status = "error"
            else:
                status = "ok"

            encoding_status = { "encoding"  :   enc,
                                "status"    :   status  }


            return encoding_status
    
    
    
    # ==========================================================================
    # METHOD:
    #   analyze_chardet(raw_bytes)
    # ==========================================================================
    def analyze_chardet(self, raw_bytes):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
            encoding    string      Type of encoding
        """
        encoding = None

        try: 
            # detect encoding and read result from dict
            result = chardet.detect(raw_bytes)
            encoding = result['encoding']
        except OSError:
            pass
        

        return encoding.lower()
        

    # ==========================================================================
    # METHOD:
    #   analyze_file(filename)
    # ==========================================================================
    def analyze_file(self, filename):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        encoding = None

        try:
            # check_output not supportet in Python 2.6
            stdout = subprocess.Popen(["file", "--mime-encoding", filename], 
                    stdout=subprocess.PIPE).communicate()[0]
            string = stdout.split(':')
            encoding = string[1]

        except subprocess.CalledProcessError as err:
            print "[ERROR] Could not determine encoding:", err
            print "[ERROR] Do manual research."
            sys.exit(1)

        return encoding.strip().lower()



    # ==========================================================================
    # METHOD:
    #   validate_encoding()
    # ==========================================================================
    def validate_encoding(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """


        all_files = self.file_operations.list_files(self.working_path, "*")

        print "[STATUS] analyzing file encoding... ",
        for filename in all_files:
            if os.path.isfile(filename):
                file_encoding = self.analyze(filename)
                enc =  file_encoding["encoding"]

                # detect non-valid encoding, iso-8859-1
                if "utf-8" not in enc and "ascii" not in enc \
                    and "binary" not in enc and "euc-kr" not in enc:
                    return False

        print "done."
        return True

