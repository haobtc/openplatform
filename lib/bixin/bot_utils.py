#encoding=utf-8

# action item
def action_item(desc={}, action='', text=''):
    item = {}
    item['desc'] = desc
    item['action'] = action
    item['text'] = text
    return item

def webview_item(desc, url):
    return action_item(desc, url)

# event item
def event_item(desc='', event_name='', kw={}):
    item = {
        'desc': desc,
        'action': "event://{}".format(event_name)
    }
    item.update(kw)

    return item

def image_event_item(desc, event_name, image_url=None,
                      image_width=None, image_height=None):
    image_detail = {
        'image_url': image_url if image_url else '',
        'image_width': image_width if image_width else '',
        'image_height': image_height if image_height else ''
    }
    return event_item(desc, event_name, image_detail)

def select_event_item(desc, event_name):
    return event_item(desc, event_name)


