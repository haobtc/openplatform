#encoding=utf-8

import os
import logging
from django.core.management.base import BaseCommand, CommandError

from bixin.bot import Bot
from bixin.bot_utils import webview_item, action_item

class Command(BaseCommand):

    def handle(self, *args, **options):

        bot = Bot()
        menu_data = self.get_menu_data()
        bot.send_set_bot_menu(menu_data)

        logging.info('success !!')

    def get_menu_data(self):
        return [
            self.get_webview_item_data(),
            self.get_action_item_data(),
        ]

    def get_webview_item_data(self):
        desc = {
            'en_US': 'app website demo',
            'zh_Hans': '应用网站',
        }
        url = 'https://platformapidemo.bixin.im/'
        return webview_item(desc, url)

    def get_action_item_data(self):
        desc = {
            'en_US': 'action item demo',
            'zh_Hans': '事件Demo',
        }
        event_name = 'action_demo'
        return action_item(desc, event_name)
