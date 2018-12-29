# coding:utf-8
# coding:utf-8


class Node(object):
    def __init__(self, id, text, children):
        self.id = id
        self.text = text
        # self.isMenu = True
        # self.menuLinkUrl = menuLinkUrl
        # self.menuIcoUrl = menuIcoUrl
        self.children = children

    def __delattr__(self, item):
        # del self[item]
        pass

    def get(self):
        # menuIcoUrl=self.menuIcoUrl, menuLinkUrl=self.menuLinkUrl, # isMenu=self.isMenu,
        if self.children:
            dicts = dict(menuId=self.id, text=self.text,
                         children=[])
            for nextNode in self.children:
                data = nextNode.get()
                if data:
                    dicts["children"].append(data)
        else:
            dicts = dict(menuId=self.id, text=self.text, )
        return dicts


def set_menus(id, menus):
    try:
        _subMenus = []
        for menu in menus:
            if menu.oz_pid == id:
                menuNode = Node(menu.id, menu.oz_name, [])
                _subMenus.append(menuNode)
        for sub in _subMenus:
            menu2 = _query_sub_menu_info(sub.id, menus)
            if len(menu2):
                sub.children = set_menus(sub.id, menus)
            else:
                sub.__delattr__('children')
        # 子菜单列表不为空
        if len(_subMenus):
            return _subMenus
        else:  # 没有子菜单了
            return None
    except Exception as e:
        print e
        return []


def _query_sub_menu_info(id, menus):
    menuList = []
    for menu in menus:
        if menu.oz_pid == id:
            menuList.append(menu)
    return menuList
