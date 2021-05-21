""" the new sub-class of Region and his associated View
"""
import re
import sublime
# import sublime_plugin

class RegionMore(sublime.View, sublime.Region):
    """ View before Region (with these attributes)
        when instantiate, provides one id of the target view where region is !!!

    Attributes:
        a (TYPE): Description
        b (TYPE): Description
    """

    def set(self, a, b):
        """Summary

        Args:
            a (TYPE): Description
            b (TYPE): Description
        """
        self.a = a
        self.b = b

    def display(self):
        """Summary
        """
        print('view', self.id(), 'region lines a & b ', self.line(self.a), self.line(self.b))
    def string(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return self.substr(sublime.Region(self.a, self.b))

    def search(self, pattern, flags=0):
        """Summary

        Args:
            pattern (TYPE): Description
            flags (int, optional): Description

        Returns:
            TYPE: Description
        """
        match = re.search(pattern,self.substr(sublime.Region(self.a, self.b)), flags )
        if match:
            return match.group(0)
        else:
            return False

    def findall(self, pattern, flags=0): # not find_all in view class
        """ don't confuse with find_all of view class

        Args:
            pattern (TYPE): Description
            flags (int, optional): Description

        Returns:
            TYPE: Description
        """
        match = re.findall(pattern,self.substr(sublime.Region(self.a, self.b)), flags )
        if match:
            return match
        else:
            return False

    def more_finditer(self, pattern, flags=0):
        """ better than find_all
        because give span of each result

        Args:
            pattern (regex): Description
            flags (int, optional): Description

        Returns:
            list: matches
        """
        matches = []
        for i in re.finditer(pattern, self.substr(sublime.Region(self.a, self.b)), flags ):
            matches.append(i)
        return matches
