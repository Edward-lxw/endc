# *-* coding=utf-8
import logging
import os
import parse_uecap
import wx

global ue_txt_path
global contents_out
global contents_in

def my_test(self):
    test_text = contents_in.GetValue()
    parse_uecap.my_test2(test_text)

# text mode : input is UE cap full text
def my_run(self):
    result = []
    test_text = ""
    test_text = contents_in.GetValue()
    result = parse_uecap.get_uecap(test_text)
    for endc in result:
        contents_out.AppendText(str(endc) + "\n")
    print("hello RUN button")

# file mode : input is file path
def my_run2(self):
    result = []
    result = parse_uecap.get_uecap(ue_txt_path)
    for endc in result:
        contents_out.AppendText(str(endc) + "\n")
    print("hello RUN button")

def my_paste(self):
    # 取得剪贴板并确保其为打开状态
    text_obj = wx.TextDataObject()
    wx.TheClipboard.Open()
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        # get the text and paste into testcontrol
        if wx.TheClipboard.GetData(text_obj):
            text = text_obj.GetText()
            contents_in.Clear()
            contents_out.Clear()
            contents_in.AppendText(text)
    wx.TheClipboard.Close()


def my_copy(self):
    text_obj = wx.TextDataObject()
    text_obj.SetText(contents_out.GetValue())
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(text_obj)
        wx.TheClipboard.Close()


if __name__ == '__main__':
    print("enter main")
    global ue_txt_path
    global contents_out
    ue_txt_path = r"D:\08_py\uecap_nr.txt"
    # parse_uecap.get_uecap(ue_txt_path)
    # parse_uecap.get_ltedl_com_cc(ue_txt_path)
    # parse_uecap.get_mrdc(ue_txt_path)
    # parse_uecap.get_combination(ue_txt_path)

    # GUI
    app = wx.App()

    win = wx.Frame(None, title="UE Capability of ENDC", size=(500, 450))
    bkg = wx.Panel(win)

    P_Button = wx.Button(bkg, label="Paste")
    C_Button = wx.Button(bkg, label="Copy")
    R_Button = wx.Button(bkg, label="Run")
    P_Button.Bind(wx.EVT_BUTTON, my_paste)
    R_Button.Bind(wx.EVT_BUTTON, my_run)
    C_Button.Bind(wx.EVT_BUTTON, my_copy)
    # filename = wx.TextCtrl(bkg)
    contents_in = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
    contents_out = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)

    hbox = wx.BoxSizer()
    # hbox.Add(filename, proportion=1, flag=wx.EXPAND)
    hbox.Add(P_Button, proportion=0, flag=wx.LEFT, border=5)
    hbox.Add(R_Button, proportion=0, flag=wx.LEFT, border=5)
    hbox.Add(C_Button, proportion=0, flag=wx.LEFT, border=5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(contents_in, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
    vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
    vbox.Add(contents_out, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

    bkg.SetSizer(vbox)
    win.Show()
    app.MainLoop()





