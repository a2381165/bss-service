# coding:utf-8


class Node:
    def __init__(self, id, text, menuLinkUrl, menuIcoUrl, children):
        self.id = id
        self.text = text
        self.menuLinkUrl = menuLinkUrl
        self.menuIcoUrl = menuIcoUrl
        self.children = children

    def __delattr__(self, item):
        # del self[item]
        pass

    def get(self):
        if self.children:
            dicts = dict(id=self.id, text=self.text, menuIcoUrl=self.menuIcoUrl, menuLinkUrl=self.menuLinkUrl,
                         children=[])
            for nextNode in self.children:
                dicts["children"].append(nextNode.get())
        else:
            dicts = dict(id=self.id, text=self.text, menuIcoUrl=self.menuIcoUrl, menuLinkUrl=self.menuLinkUrl)
        return dicts


def set_menus(id, menus):
    try:
        _subMenus = []
        for menu in menus:
            if menu.menu_parent_id == id:
                menuNode = Node(menu.menu_id, menu.menu_title, menu.menu_link_url, menu.menu_ico_url, [])
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
        if menu.menu_parent_id == id:
            menuList.append(menu)
    return menuList

def set_menu2(id, menus):
    try:
        _subMenus = []
        for menu in menus:
            if menu.menu_parent_id == id:
                # menuNode = Node(menu.menu_id, menu.menu_title, menu.menu_link_url, menu.menu_ico_url, [])
                _subMenus.append(menu)
        for sub in _subMenus:
            menu2 = _query_sub_menu_info(sub.menu_id, menus)
            if len(menu2):
                sub.children = set_menus(sub.menu_id, menus)
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
