'''
@Date: 2020-03-23 23:34:17
@LastEditors: code
@Author: code
@LastEditTime: 2020-04-07 22:45:40
'''

import nonebot
import config
from os import path

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()



