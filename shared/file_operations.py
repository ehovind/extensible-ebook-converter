
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
import codecs
import glob
import urllib2
import fnmatch

# ==========================================================================
# CLASS:
#   FileOperations
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class FileOperations():
    """
    DESCRIPTION:

    PARAMETERS:
    """

    def __init__(self):
        self.temp = None

    # ==========================================================================
    # METHOD:
    #   write_file_final(path, data, mode="w"):
    # ==========================================================================
    @staticmethod
    def write_file_final(path, data, mode="w"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        try:
            # check directory exists
            f = open(path, mode)
            f.write(data)
            f.close()
        except IOError as err:
            print "Writing file error: " +err
        
        finally:
            f.close()
    # ==========================================================================
    # METHOD:
    #   read_unicode_final(filename, mode="r", encoding="utf-8")
    # ==========================================================================
    @staticmethod
    def read_unicode_final(filename, mode="r", encoding="utf-8"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        # research: utFile, xml_declaration=True, encoding='utf-16') 
        try:
            # check directory exists
            f = codecs.open(filename, mode, encoding)
            data = f.read()
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()

        return data

    # ==========================================================================
    # METHOD:
    #   read_lines_final(filename, mode="r", encoding="utf-8")    
    # ==========================================================================
    @staticmethod
    def read_lines_final(filename, mode="r", encoding="utf-8"):
        """
        DESCRIPTION:
             
        PARAMETERS:
        
        RETURN: 
        """
        data = list()

        try:
            f = codecs.open(filename, mode, encoding)
            data = f.readlines()
        except IOError as err:
            print "Reading lines error: " +err
        
        finally:
            f.close()

        return data
    
    # ==========================================================================
    # METHOD:
    #   write_unicode_final(filename, data, mode="w", encoding="utf-8")
    # ==========================================================================
    @staticmethod
    def write_unicode_final(filename, data, mode="w", encoding="utf-8"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        try:
            # check directory exists
            f = codecs.open(filename, mode, encoding)
            f.write(data)
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()


    # ==========================================================================
    # METHOD:
    #   read_xml_final(filename, mode="r")
    # ==========================================================================
    @staticmethod
    def read_xml_final(filename, mode="r"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        try:
            # check directory exists
            f = open(filename, mode)
            data = f.read()
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()

        return data

    # ==========================================================================
    # METHOD:
    #   write_xml_final(filename, data, mode="w")
    # ==========================================================================
    @staticmethod
    def write_xml_final(filename, data, mode="w"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        try:
            # check directory exists
            f = open(filename, mode)
            f.write(data)
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()

    # ==========================================================================
    # METHOD:
    #   download_file(path, url):
    # ==========================================================================
    def download_file(self, path, url):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
    
        # download file
        try:
            response  = urllib2.urlopen(url)
            archive = response.read()
        except urllib2.URLError as err:
            print "Download file failed: ", err

        # convert to utf-8
        try:
            archive_unicode = unicode(archive, 'ISO-8859-1')
        except UnicodeDecodeError:
            print "Text already unicode"

        self.write_unicode_final(path, archive_unicode)



    # ==========================================================================
    # METHOD:
    #   write_xml(filename, data, mode="w", encoding="utf-8")
    # ==========================================================================
    @staticmethod
    def write_xml(filename, data, mode="w", encoding="utf-8"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        try:
            # check directory exists
            f = codecs.open(filename, mode, encoding)
            f.write(data)
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()

    # ==========================================================================
    # METHOD:
    #   write_xml_new(filename, data, mode="w")
    # ==========================================================================
    @staticmethod
    def write_xml_new(filename, data, mode="w"):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        try:
            # check directory exists
            f = open(filename, mode)
            f.write(data)
        except IOError as err:
            print "Writing xml error: " +err
        
        finally:
            f.close()


    
    # ==========================================================================
    # METHOD:
    #   list_files(path, expression)
    # ==========================================================================
    @staticmethod
    def list_files(path, expression):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        files = list()
        
        try:
            files = glob.glob(path + expression)
        except OSError as err:
            print err
        
        return sorted(files)
    
    # ==========================================================================
    # METHOD:
    #   list_files_recursive(path, expression)
    # ==========================================================================
    @staticmethod
    def list_files_recursive(path, expression):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        files = list()
        
        try:
            for root, dirnames, filenames in os.walk(path):
                for filename in fnmatch.filter(filenames, expression): 
                    files.append(os.path.join(root, filename))
        except OSError as err:
            print err
        
        return sorted(files)
    
    # ==========================================================================
    # METHOD:
    #   list_publication_files(path)
    # ==========================================================================
    def list_publication_files(self, path):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        files = self.list_files(path, "*.html")
        
        files.append(path + "Metadata")
        files.append(path + "Articles.lst")
        
        return sorted(files)


    # ==========================================================================
    # METHOD:
    #   filename_only_final(path)
    # ==========================================================================
    @staticmethod
    def filename_only_final(path):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        head, filename = os.path.split(path)
        
        return filename
    

    # ==========================================================================
    # METHOD:
    #   exclude_git_from_list(files)
    # ==========================================================================
    @staticmethod
    def exclude_git_from_list(files):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        # exclude was not found
        if files.find(".git") is -1:
            return True
        else:
            return False

