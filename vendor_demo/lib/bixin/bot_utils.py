from urllib import urlencode

def select_event_item(desc, text, event, input = None, **kw):
    params = {}
    params['text'] = text.encode('utf-8')
    params['event'] = event
    if input:
        params['input'] = input

    params.update(dict(kw))

    uri = 'bixin://postevent/'
    uri = '%s?%s'%(uri, urlencode(params))

    item = {}
    item['desc'] = desc
    item['action'] = uri
    return item

def select_action_item(desc, action):
    item = {}
    item['desc'] = desc
    item['action'] = action
    return item

def select_webview_item(desc, text, url):
    params = {}
    params['url'] = url

    uri = 'bixin://webview'
    uri = '%s?%s'%(uri, urlencode(params))

    item = {}
    item['desc'] = desc
    item['action'] = uri
    return item

def image_action_item(desc, action, image_url=None,
                      image_width=None, image_height=None):
    item = {'desc': desc,
            'action': action,
            'image_url': image_url if image_url else '',
            'image_width': image_width if image_width else '',
            'image_height': image_height if image_height else ''
           }
    return item
