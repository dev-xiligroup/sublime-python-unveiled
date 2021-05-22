"""xili_regionmore.py
this example contains a new class (in modules) to provide more methods to sublime.Region with only few methods

# v 210521 - first public dev release

"""
# import re

import imp
import sublime
import sublime_plugin
# import os.path

import RegionMore.modules.xili_mod_buffermore_class
imp.reload( RegionMore.modules.xili_mod_buffermore_class ) # for dev
from RegionMore.modules.xili_mod_buffermore_class import BufferMore # the new sub class

# after buffer !! see when Region Buffer is instantiated
import RegionMore.modules.xili_mod_regionmore_class as rm
imp.reload( rm ) # for dev
from RegionMore.modules.xili_mod_regionmore_class import RegionMore # the new sub class

class TestRegionMoreCommand(sublime_plugin.TextCommand):

    """to test classes
    """

    def run(self, edit, **args):

        """
        moreregion = RegionMore( self.view.id())
        moreregion.set(1000,199)
        print(moreregion, moreregion.id(), moreregion.size(), moreregion.begin(),'<<toto', moreregion.sel()[0])
        moreregion.display()
        print(moreregion.string())
        print(moreregion.search(r'scripts'))
        print(moreregion.findall(r'scripts'))
        """
        thew = self.view.window()
        thew_vars = thew.extract_variables()
        print(' active view ', thew.active_view().id())
        fext = thew_vars['file_extension']
        print(' self win ',thew_vars)

        # viewb = thew.open_file('bufffer.php') # create an empty view if not exist !!!

        #if os.path.isfile(thew_vars['packages']+'/User/buffer.php'):
            #viewb = thew.open_file(thew_vars['packages']+'/User/buffer.php') # car asynchorone so path needed 'buffer.php')
            #print('file exists', viewb.id())
            #viewb.close()
        #else:
            #print('not find')
        # new
        #viewn = thew.new_file()

        #print(' new win ', thd)
        #print(' new win ', viewn.id())
        print('--before inst. class--> ',BufferMore.name )
        #MyBuffer1 = BufferMore.new_buffer(self.view) # not yet class like object but return an object
        MyBuffer1 = BufferMore( -1, self.view ) # new instantiation
        thd = MyBuffer1.window().extract_variables()
        print(' new win not saved ', thd)
        buf_args = {
            "path":thd['packages'],
            "subpath":['User','testbuff'], # or not list
            "filename":'filebuff',
            'file_extension': fext # same as target file/view
        }
        MyBuffer1.set(buf_args) # where the buffer will be saved !
        # header of buffer
        if fext == 'php':
            len_vn = MyBuffer1.insert(edit,0,'<?php\nfunction too () {\n\t $ = 0;\n}\n')
        # print (viewn.substr(sublime.Region(1, 10)))
            len_vn += MyBuffer1.insert(edit,len_vn,'# below - part inserted for RegionMore\n')
        # print (viewn.substr(sublime.Region(1, 30)))
            selector_test = "meta.function"
            indice = 2
        elif fext == 'py':
            len_vn = MyBuffer1.insert(edit,0,'"""below - part inserted for RegionMore"""\n')
            selector_test = "comment"
            indice = 0
        region = self.view.find_by_selector(selector_test) # only list of function...
        if not isinstance(region, list):
            region = [region]
            # test on 2
        region_test = region[indice]
        if isinstance(region_test, sublime.Region):
            pos_a = len_vn
            len_vn += MyBuffer1.insert(edit,len_vn, self.view.substr(region_test))
            pos_b = len_vn
            # search inside buffer
            Region_Buffer = RegionMore(MyBuffer1.id()) # only in inserted part !
            Region_Buffer.set(pos_a, pos_b)
            print('match in more ',Region_Buffer.findall(r'get_.+?_mod', 0 ))

            result = Region_Buffer.more_finditer(r'\$content_width', 0)
            if result:
                print(len(result),'iter in more ',result[0].span(), result[0].group())

        # see results
        MyBuffer1.save()
        thd = MyBuffer1.window().extract_variables()
        print(' new win saved ', thd)
        print(' new buffer id ', MyBuffer1.id())
        if not MyBuffer1.is_loading():
            print('try close')
            if 'close' in args and args['close'] is True:
                MyBuffer1.close() # undocumented why this not work -> run_command('close_file')
        print(' active view ', thew.active_view().id())

        # select in original
        if isinstance(region_test, sublime.Region) and result:
            region_selected = []
            for one_result in result:
                region_selected.append(sublime.Region(region_test.a + one_result.span()[0], region_test.a + one_result.span()[1]))
            # print(region_selected)
            if not isinstance(region_selected, list):
                region_selected = [region_selected]

            # shows in color !
            self.view.add_regions("test", region_selected, "region.greenish", "circle",
            flags=sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL)
        #MyBuffer = BufferMore(viewn.id())

        sublime.active_window().focus_view(self.view) # not documented ! back to target file
        print('--inst--> ',MyBuffer1.view_id ) # as id()
        print(BufferMore.buffers)
        collection = BufferMore.buffermores()
        ids = []
        for viewobj in collection:
            ids.append(viewobj.id())
        print(ids)
        #del MyBuffer1
        #print(BufferMore.buffers)
        #print(BufferMore.buffermores())
        print(self.view.window().views())
        #print('region ', Region_Buffer.string())
        """
        print (self.view.style_for_scope('meta.function'))
        print('----> ',BufferMore.nameis( ' is good' ))
        print('--inst--> ',MyBuffer1.name )
        print('--class--> ',BufferMore.name )

        # print(MyBuffer2)
        #MyBuffer2 = BufferMore.new_buffer(self.view)
        """
        #MyBuffer2 = MyBuffer1.new_buffer(self.view) # => error because impossible instantiated class

class DevRefreshListener(sublime_plugin.EventListener):

    """ specific event for this plugin in dev
    """

    def on_post_save(self, view):
        """tests if one of the files of plugin was saved !
        """
        in_dev_step = 'RegionMore' in view.settings().get('development') # in current user's preferences
        # print("Before test...")
        # the catalog of the plugin's modules
        plugin_files = [

            "modules/xili_mod_regionmore_class.py",
            "modules/xili_mod_buffermore_class.py",

        ]
        if in_dev_step and view.file_name().endswith(".py"):
            for plugin_file in plugin_files:
                if view.file_name().endswith(plugin_file):
                    print("After saving this file (view): ", view.file_name())
                    sublime_plugin.reload_plugin('RegionMore.xili_regionmore') # the root of this plugin

    # end
