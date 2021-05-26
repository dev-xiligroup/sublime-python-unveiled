""" the new sub-class of Region and his associated View
"""
import re
import sublime

class RegionMore(sublime.View, sublime.Region):
    """View before Region (with these attributes)
        when instantiate, provides one id of the target view where region is !!!

    Attributes:
        a (int): Description as in Region
        b (int): Description as in Region
        view_id (int): Description as in View
    """
    def __init__(self, view_id, *positions):
        """Summary

        Args:
            view_id (integer): id f associated view
            *positions: tuple a et b positions
        """
        self.view_id = view_id # mandatory if instatiante via __init__ in subclass
        self.a = 0
        self.b = 0
        if positions and len(positions) == 2: # need a tuple of two elements
            self.a = positions[0]
            self.b = positions[1]

    def set(self, a, b):
        """ to change a & b

        Args:
            a (int): Description
            b (int): Description
        """
        self.a = a
        self.b = b

    def __del__(self):
        print("RegionMore ",self.view_id," deleted")

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
