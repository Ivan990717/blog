def get_validCode_img(request):
    def get_random_color():
        import random
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # pip install pillow 用磁盘读取很慢
    from PIL import Image, ImageDraw, ImageFont
    import random
    valid_code = ""
    img = Image.new("RGB", (270, 40), color=get_random_color())
    draw = ImageDraw.Draw(img)
    ttf = ImageFont.truetype('static/font/kumo.ttf', size=40)  # 添加字体库
    for i in range(5):
        random_number = str(random.randint(0, 9))
        random_lower_alp = chr(random.randint(97, 122))
        random_upper_alp = chr(random.randint(65, 90))
        random_char = random.choice([random_number, random_lower_alp, random_upper_alp])

        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=ttf)
        valid_code += str(random_char)

    # 补充噪点，干扰线
    width = 270
    height = 40
    for i in range(10):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(5):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    from io import BytesIO  # 内存管理工具
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    request.session["valid_code"] = valid_code

    '''

    首先生成一个随机字符串，然后生成cookie键值对
    存入django-session数据库，
    {session_key:session_data}
    '''

    # with open('validCode.png','wb') as f:
    #     img.save(f,'png')
    #
    # with open('validCode.png','rb') as f:
    #     data = f.read()
    return  data