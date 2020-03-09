if __name__=="__main__":
    with open("vca/main_window_layout.py","r+",encoding="utf-8") as f:
        content=f.read()
        if "DragableQListView" not in content:
            f.seek(0,0)
            content="import vca.dragable_QListView \n"+content
            content=content.replace("QtWidgets.QListView","vca.dragable_QListView.DragableQListView")
            f.write(content)
            f.flush()
            print("替换完成")
        else:
            print("无需替换")
