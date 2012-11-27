
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

import subprocess
from . import file_operations as FileOperations

# ==========================================================================
# CLASS:
#   GitHandler
#
# CONSTRUCTOR:
#
# CLASS VARIABLES:
#
# DESCRIPTION:
# ==========================================================================
class GitHandler(object):
    """
    DESCRIPTION:

    PARAMETERS:
    """

    git = 'git'
    branch_name = "edited_book"
    


    # ==========================================================================
    # CONSTRUCTOR:
    #   __init__()
    # ==========================================================================
    def __init__(self):
        
        self.file_operations = FileOperations.FileOperations()

    
    # ==========================================================================
    # METHOD:
    #   init()
    # ==========================================================================
    def init(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = (self.git, 'init')
        subprocess.call(cmd)


    # ==========================================================================
    # METHOD:
    #   add_all()
    # ==========================================================================
    def add_all(self):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        list_of_files = self.file_operations.list_files_recursive("./","*")

        # filter out .git entries
        filtered = filter(self.file_operations.exclude_git_from_list, list_of_files)
        
        for filename in filtered:
            cmd = [self.git, 'add', filename]
            subprocess.call(cmd)


    # ==========================================================================
    # METHOD:
    #   commit(comment)
    # ==========================================================================
    def commit(self, comment):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = ['git', 'commit', '-a', '-m', comment]
        subprocess.call(cmd)

    # ==========================================================================
    # METHOD:
    #   tag(tag, comment)
    # ==========================================================================
    def tag(self, tag, comment):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = ['git', 'tag', '-a', tag, '-m', comment]
        subprocess.call(cmd)


    # ==========================================================================
    # METHOD:
    #   branch(id)
    # ==========================================================================
    def branch(self, branch):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = ['git', 'branch', branch]
        subprocess.call(cmd)
        
    # ==========================================================================
    # METHOD:
    #   checkout(id)
    # ==========================================================================
    def checkout(self, branch):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = ['git', 'checkout', branch]
        subprocess.call(cmd)

    
    # ==========================================================================
    # METHOD:
    #   format_patch(patch_file)
    # ==========================================================================
    def format_patch(self, patch_file):
        """
        DESCRIPTION:
            Create a patch based in diff between init tag and current
            working directory. Write file to "output/patches".
            
        PARAMETERS:
            None
            patch_file      name of patch file
        
        RETURN: 
        """
        
        # create a patch using git format-patch
        cmd = ['git', 'format-patch', 'init', '--stdout']
        try:
            # check_output not supported in Python 2.6
            #patch = subprocess.check_output(cmd, shell=False)
            patch = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except subprocess.CalledProcessError as cpe:
            print "Error creating patch: ", cpe

        # write string to file
        self.file_operations.write_file_final(patch_file, patch)
        

    # ==========================================================================
    # METHOD:
    #   check_patch(patch_file)
    # ==========================================================================
    def check_patch(self, patch_file):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """
        cmd = ['git', 'apply', '--stat', patch_file]
        subprocess.call(cmd)

        cmd = ['git', 'apply', '--check', patch_file]
        subprocess.call(cmd)


    # ==========================================================================
    # METHOD:
    #   apply_patch(patch_file)
    # ==========================================================================
    def apply_patch(self, patch_file):
        """
        DESCRIPTION:
            
        PARAMETERS:
        
        RETURN: 
        """

        cmd = ['git', 'am', '--signoff', patch_file]
        subprocess.call(cmd)
