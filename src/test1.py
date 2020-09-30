# -*- coding: utf-8 -*-
import os 
import threading
import time
import win32api
import win32gui
import win32con
import ctypes


# #查找窗口句柄
# win32gui.FindWindow()
# #查找指定窗口的菜单
# win32gui.GetMenu()
# #查找某个菜单的子菜单
# win32gui.GetSubMenu()
# #获得子菜单的ID
# win32gui.GetMenuItemID()
# #获得某个子菜单的内容
# win32gui.GetMenuItemInfo()
# #给句柄发送通知（点击事件）
# win32gui.PostMessage()　　


class Test1(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.filename = ''

    def getfilename(self,textfile):
        self.filename = textfile
    
    def run(self):
        file = os.path.abspath(os.path.dirname(os.path.abspath("__file__"))) + "/resource/" + self.filename

        print(file)
        os.system(r'notepad ' + file)
            

class Test2(threading.Thread):
    
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.widgets = []

    # 遍历子窗口
    def get_child_windows(self,child_window, param):
        widget = {
            'handle': child_window,
            'class': win32gui.GetClassName(child_window),  # 得到的HWND获取对应Window的Class属性
            'title': win32gui.GetWindowText(child_window),  # 得到的HWND获取对应Window的标题名
            'pos': win32gui.GetWindowRect(child_window)
        }
        self.widgets.append(widget) 
    
    def run(self):

        #delay 
        time.sleep(2)
        
        # """
        # 记事本实例
        # """
        #获取实例
        notepadHhandle = win32gui.FindWindow("Notepad", None)
        # notepadHhandle = win32gui.FindWindow(None,"text1.txt")
        print ("记事本实例 %x" % (notepadHhandle))

        #获取句柄
        editHandle = find_subHandle(notepadHhandle, [("Edit",0)])
        print ("句柄 %x" % (editHandle))

        """修改edit中的值"""
        # win32api.SendMessage(editHandle, win32con.WM_SETTEXT, 0, "测试1")
        
        command_dict = {  # [目录的编号, 打开的窗口名]  
                    "new": [0, u"新建"],
                    "newwin": [1, u"新窗口"],
                    "open": [2, u"打开"],
                    "save": [3, u"保存"],
                    "saveas": [4, u"另存为"],
                    "quit": [9, u"退出"],
                }  
        
        """操作菜单 另存为"""

        menu = win32gui.GetMenu(notepadHhandle)
        menu = win32gui.GetSubMenu(menu, 0)  
        cmd_ID = win32gui.GetMenuItemID(menu, command_dict["saveas"][0])
        if cmd_ID == -1:
            print("没有找到相应的菜单")
        else:
            print ("菜单id:%x" % (cmd_ID))
        win32gui.PostMessage(notepadHhandle, win32con.WM_COMMAND, cmd_ID, 0)  



        #window "另存为" 
        time.sleep(2)
        #获取实例
        notepadHhandle_save = win32gui.FindWindow(None,"另存为")
        print ("另存为 %x" % (notepadHhandle))


        #获取编码选择句柄
        notepadcombobox = win32gui.FindWindowEx(notepadHhandle_save,None,"ComboBox",None)
        print("编码 %x" % (notepadcombobox))

        #设置为ANSI
        ANSI=0
        UTF8=3
        win32gui.PostMessage(notepadcombobox,win32con.CB_SETCURSEL,ANSI,0)

        #获取保存按钮句柄
        notepadbutton = win32gui.FindWindowEx(notepadHhandle_save,None,"Button","保存(&S)")
        print("另存为按钮 %x" % (notepadbutton))


        #回车
        win32gui.PostMessage(notepadbutton, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

        win32gui.PostMessage(notepadbutton, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


        
        #window "确认另存为"
        time.sleep(2)
        #获取实例
        notepadHhandle_confirmsave = win32gui.FindWindow(None,"确认另存为")
        print ("确认另存为 %x" % (notepadHhandle_confirmsave))

        
        win32gui.EnumChildWindows(notepadHhandle_confirmsave,self.get_child_windows, None)


        for widget in self.widgets:
            # print(widget['handle'])
            # print(widget['class'])
            # print(widget['title'])
            # print(widget['pos'])

            if widget['title'] == "是(&Y)" and widget['class'] == "Button":

                print(widget['title'])
                print(widget['class'])
                print(widget['pos'])

                # print(widget['pos'][1])

                point = (widget['pos'][0], widget['pos'][1])
                win32api.SetCursorPos(point)
                #点击鼠标
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


        #关闭记事本
        time.sleep(2)
        cmd_ID = win32gui.GetMenuItemID(menu, command_dict["quit"][0])
        if cmd_ID == -1:
            print("没有找到相应的菜单")
        else:
            print ("菜单id:%x" % (cmd_ID))
        win32gui.PostMessage(notepadHhandle, win32con.WM_COMMAND, cmd_ID, 0)  




        

        
        
        



#############
def find_idxSubHandle(pHandle, winClass, index=0):
    """ 
                已知子窗口的窗体类名 
                寻找第index号个同类型的兄弟窗口 
    """  
    assert type(index) == int and index >= 0  
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)  
    while index > 0:  
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)  
        index -= 1  
    return handle  
 
def find_subHandle(pHandle, winClassList):  
    """ 
             递归寻找子窗口的句柄 
    pHandle是祖父窗口的句柄 
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈 
    """  
    assert type(winClassList) == list  
    if len(winClassList) == 1:  
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
    else:  
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
        return find_subHandle(pHandle, winClassList[1:])  

if __name__ == "__main__":

    file = "text1.txt"
    t1 = Test1(1, "Thread-1", 1)
    t1.getfilename(file)
    t2 = Test2(2, "Thread-2", 2)
    
    try:
        t1.start()
        t2.start()
    except Exception as e:
        print(e)
     


    


    