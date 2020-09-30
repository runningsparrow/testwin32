# -*- coding: utf-8 -*-
import os 
import threading
import time
import win32api
import win32gui
import win32con


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
        
    
    def run(self):

        #delay 
        time.sleep(3)
        
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
        win32api.SendMessage(editHandle, win32con.WM_SETTEXT, 0, "测试1")
        
        command_dict = {  # [目录的编号, 打开的窗口名]  
                    "open": [3, u"打开"],
                    "save": [4, u"保存"],
                    
                }  
        
        """操作菜单"""

        menu = win32gui.GetMenu(notepadHhandle)
        menu = win32gui.GetSubMenu(menu, 0)  
        cmd_ID = win32gui.GetMenuItemID(menu, command_dict["open"][0])
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
     


    


    