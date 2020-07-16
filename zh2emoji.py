#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import sys
import getopt
from PIL import Image, ImageDraw, ImageFont

PY3 = sys.version_info[0] == 3
if not PY3:
    range = xrange


def word2image(word, debug=False, width=400, fontpath='PingFangBold.ttf'):
    '''
    @brief 将一个中文字符转为图片
    @params word: 一个中文字,__len__长度为1
    @params width: 返回的图片宽的数字,默认400,高根据宽自动调节
    @params fontpath: 字体文件的路径
    @return image
    '''
    # assert len(word) == 1
    page_width, page_height = (400 * len(word), 450)
    word_color = '#000000'  # 文字颜色,黑色
    bg_color = '#ffffff'  # 背景颜色,白色

    img = Image.new('RGBA', (page_width, page_height), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontpath, 400)
    draw.text((0, -50), word, word_color, font)

    height = int(width * 1.0 / page_width * page_height)
    img = img.resize((width, height), Image.NEAREST)
    if debug:
        img.save('test.png')
    # img.show()
    return img


def image2print(img, char, width=40):
    '''
    @brief 将图片转化为字符串,字符串可以在终端打印出来
    @params img: 待打印的白底黑字的图片.
    @params char: 替换图片的字符
    @params width: 由于像素点转为打印字符占用屏幕宽度挺大的, 所以需要对图片进行相应缩小.
    @return string
    '''
    ascii_char = [char, '  ']

    def select_ascii_char(r, g, b):
        ''' 在灰度图像中,灰度值最高为255,代表白色,最低为0,代表黑色 '''
        gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)  # 'RGB－灰度值'转换公式
        unit = 256.0 / len(ascii_char)  # ascii_char中的一个字符所能表示的灰度值区间
        return ascii_char[int(gray/unit)]

    txt = ""
    old_width, old_height = img.size
    height = int(width * 1.0 / old_width * old_height)
    img = img.resize((width, height), Image.NEAREST)

    for h in range(height):
        for w in range(width):
            txt += select_ascii_char(*img.getpixel((w, h))[:3])
        txt += '\n'
    return txt


WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

def widen(s):
    """
    Convert all ASCII characters to the full-width counterpart.
    [https://gist.github.com/jcayzac/1485005]
    """
    return str(s).translate(WIDE_MAP)



def usage():
    print('''NAME
       zh2emoji - create Chinese character banners

SYNOPSIS
       zh2emoji.py [-b <BIG-text>] [-s <small-char>] [-w <width>] [-d --debug] [--widen]

DESCRIPTION
       Just similar to figlet, but making chinese figlet, making emoji's figlet.

       -b
              The string to generate a banner of

       -s
              The character to draw the banner

       -w
              The width of the banner

       -d, --debug

              Turn on debug mode. A preview image named test.png will be saved

       --widen

              Force the banner text to be full-width characters
''')
    sys.exit(2)


if __name__ == '__main__':
    ''' demo
    使用不同的填充方法显示来展示"茴"字
    其中, 对于ascii 建议后面多一个空格填充;
    对于emoji表情, 可能跟终端的打印方式有关, 对比后自行决定后面需不需要加上空格填充;
    对于中文,输出正好;
    '''
    big_text = 'A'
    small_char = 'a'
    w = 40
    wide = False
    debug = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'b:s:w:d', ['debug', 'widen'])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-b':
            big_text = arg
        elif opt == '-s':
            small_char = arg
        elif opt == '-w':
            w = int(arg)
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt == '--widen':
            wide = True
        else:
            usage()
    if wide:
        big_text = widen(big_text)
    print(image2print(word2image(big_text, debug), widen(small_char), w))
