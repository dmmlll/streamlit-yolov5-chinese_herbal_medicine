from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
from PIL import Image

@st.cache
def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)


if __name__ == '__main__':

    #标题
    st.set_page_config(page_title="中药饮片的检测识别",
                       #page_icon=":D:\\dongmiaomiao\\YOLOV5\\yolov5-streamlit-main\\data\\images\\中药饮片.png:",
                       page_icon=":herb:",
                       layout="wide"
                       )
    #source,source2,source3=st.text_area()
    st.title('*中药饮片的检测识别*:tulip:')
    st.header('***YOLOv5 实现中药饮片的检测识别***:four_leaf_clover:')

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default='weights/yolov5s-zhongyao.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.35, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='',
                        help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true',
                        help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true',
                        help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--project', default='runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp',
                        help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)

    #第一个框检测视频图片
    source = ("图片检测", "视频检测")
    #下拉选框，侧边栏
    source_index = st.sidebar.selectbox("检测方式", range(
        len(source)), format_func=lambda x: source[x])
    #0代表图片检测，选择图片检测
    if source_index == 0:
        #选择文件
        uploaded_file = st.sidebar.file_uploader(
            "上传图片", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='资源加载中...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                opt.source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False
    #这个是1，1代表视频检测
    else:
        uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='资源加载中...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                opt.source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    if is_valid:
        print('valid')
        if st.button('开始检测'):

            detect(opt)

            if source_index == 0:
                with st.spinner(text='Preparing Images'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

                    st.balloons()
            else:
                with st.spinner(text='Preparing Video'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(str(Path(f'{get_detection_folder()}') / vid))

                    st.balloons()
    #第二个选择，查询中药饮片
    source2 = ('安息香', '白扁豆', '白矾', '白芥子', '白蔹', '白茅根', '白前', '白芍', '白术', '柏子仁',
               '板蓝根', '北沙参', '荜拨', '荜澄茄', '薄荷', '苍术', '草豆蔻', '柴胡', '陈皮', '沉香',
               '赤芍', '赤石脂', '川楝子', '川木香', '川牛膝', '川穹', '大腹皮', '淡豆豉', '当归', '丹参',
               '稻芽', '大青叶', '地龙', '防风', '番泻叶', '蜂房', '茯苓', '甘草', '干姜', '甘松',
               '公丁香', '桂枝', '谷精草', '谷芽', '海螵蛸', '蒿本', '合欢皮', '黄柏', '黄芪', '黄芩',
               '藿香', '僵蚕', '鸡冠花', '锦灯笼', '荆芥穗', '金银花', '九香虫', '橘核', '苦地丁', '莱菔子',
               '连翘', '莲须', '莲子', '莲子心', '灵芝', '荔枝核', '龙眼', '芦根', '路路通', '麻黄',
               '麦冬', '牛蒡子', '羌活', '千年健', '青蒿', '秦皮', '忍冬藤', '人参', '肉豆蔻', '桑寄生',
               '桑螵蛸', '桑葚', '山慈菇', '山奈', '山药', '沙苑子', '射干', '鸡内金', '瓦楞子', '石榴皮',
               '丝瓜络', '酸枣仁', '苏木', '太子参', '天花粉', '天麻', '土荆皮', '五加皮', '杏仁', '细辛',
               '银柴胡', '薏仁', '郁金', '浙贝母', '枳壳', '竹茹', '猪牙皂')

    source2_index = st.sidebar.radio("查询", range(
        len(source2)), format_func=lambda x: source2[x])
    #st.empty(source2_index)2
    if source2_index == 0:
        #加载图片
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\安息香.jpg')
        #image = Image.open('https://www.yuxiblog.com/wp-content/uploads/2020/05/%E5%AE%89%E6%81%AF%E9%A6%99%E7%B2%BE%E6%B2%B9-300x168.jpg')
        st.image(image, caption='安息香')
        #显示信息（安息香）
        st.markdown('''
                    中文名：安息香\n
                    拼音：an xi xiang\n
                    性状：本品为不规则的小块，稍扁平，常粘结成团块。表面橙黄色，具蜡样光泽（自然出脂）；或为不规则的圆柱状、扁平块状，表面灰白色至淡黄白色（人工割脂）。质脆，易碎，断面平坦，白色,放置后逐渐变为淡黄棕色至红棕色。加热则软化熔融。气芳香，味微辛，嚼之有砂粒感。\n
                    功能主治：开窍，辟秽，行气血。治卒中暴厥，心腹疼痛，产后血晕，小儿惊痫，风痹腰痛。\n
                    性味：辛苦，温。\n
                    用法用量：内服：研末，1～5分；或入丸、散。外用：烧烟熏。0.6～1.5g，多入丸散用。\n
                    服用禁忌：阴虚火旺者慎服。\n
                    来自:[中医百科](https://zhongyibaike.com/wiki/%E4%B8%AD%E8%8D%AF%E5%A4%A7%E5%85%A8)
                     ''')
        # Download an image:
        # with open("D:\\dongmiaomiao\\images21\\images2\\anxixiang.jpg", "rb") as file:
        # btn = st.download_button(
        # label="Download image",
        # data=file,
        # file_name="anxixiang.jpg",
        # mime="image/jpg"
        # )
    #显示信息（白扁豆）
    elif source2_index==1:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白扁豆.jpg')
        st.image(image, caption='白扁豆')
        st.markdown('''
        中文名：白扁豆\n
        拼音：bai bian dou\n
        性状：种子扁椭圆形或扁卵圆形，长0.8~1.3cm，宽6~9mm，厚约7mm。表面淡黄白色或淡黄色，平滑，稍有光泽，有的可见棕褐色斑点，一侧边缘有隆起的白色半月形种阜。长7~10mm，剥去后可见凹陷的种脐，紧接种阜的一端有珠孔，另端有种脊。质坚硬，种皮薄而脆，子叶2片，肥厚，黄白色。气微，味淡，嚼之有豆腥气。以粒大、饱满、色白者为佳。\n
        功能主治：健脾化湿，和中消暑。用于脾胃虚弱，食欲不振，大便溏泻，白带过多，暑湿吐泻，胸闷腹胀。 炒扁豆：健脾化湿。用于脾虚泄泻，白带过多。\n
        性味：甘淡；微温；平。\n
        用法用量：内服：煎汤，10~15g；或生品捣研水绞汁；或入丸、散。\n
        外用：适量，捣敷。\n
        服用禁忌：一般人群均可食用。适宜脾胃虚弱、食欲不振、大更溏泻、白带过多、暑湿吐泻、胸闷腹胀症状的患者食用。患寒热病者，患冷气人，患冷气人不可食。
        ''')
    elif source2_index==2:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白矾.jpg')
        st.image(image, caption='白矾')
        st.markdown('''
        中文名：白矾\n
        拼音：bai fan\n
        性状：呈不规则的块状或粒状。无色或淡黄白色，透明或半透明。表面略平滑或凹凸不平，具细密纵棱，有玻璃样光泽。质硬而脆。气微，味酸、微甘而极涩。\n
        功能主治：消痰，燥湿，止泻，止血，解毒，杀虫。治癫痫，喉痹，疚涎壅甚，肝炎，黄疸，黄肿，胃、十二指肠溃疡，子宫脱垂，白带，泻痢，衄血，口舌生疮，疮痔疥癣，水、火、虫伤。\n
        性味：酸涩；寒；\n
        用法用量：0.6～1.5g。外用适量，研末敷或化水洗患处。\n
        服用禁忌：阴虚胃弱，无湿热者忌服。
        ''')
    elif source2_index==3:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白芥子.jpg')
        st.image(image, caption='白芥子')
        st.markdown('''
        中文名：白芥子\n
        拼音：bai jie zi\n
        性状：种子呈圆球形，直径1.1～2.5毫米，较黄芥子为大。表面类白色至淡黄色，光滑。在扩大镜下观察，可见细微的网纹及一暗色小点状的种脐。种皮脆薄易压碎，剥去后有薄膜状的胚乳粘着于种皮内表面。胚黄白色，袖质，二子叶相叠，并于中脉处折起呈马鞍状，胚根亦折转而藏于其间。气无，味先觉油样而后微酸，继感辛辣。以个大、饱满、色白、纯净者为佳。\n
        功能主治：利气豁痰，温中散寒，通络止痛。治痰饮咳喘，胸胁胀满疼痛，反胃呕吐，中风不语，肢体痹痛麻木，脚气，阴疽，肿毒，跌打肿痛。\n
        性味：辛，温。\n
        用法用量：内服：煎汤，1～3钱；或入丸、散。外用：研末调敷。\n
        服用禁忌：肺虚久咳及阴虚火旺者禁服。
        ''')
    elif source2_index==4:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白蔹.jpg')
        st.image(image, caption='白蔹')
        st.markdown('''
        中文名：白蔹\n
        拼音：bai lian \n
        性状：块根长圆形或纺锤形，多纵切成瓣或斜片。完整者长5-12cm，直径1.5-3.5cm。表面红棕色或红褐色，有纵皱纹、细横纹及横长皮孔，栓皮易层层脱落，脱落处显淡红棕色，剖面类白色或淡红棕色，皱缩不平。斜片呈卵圆形，长2.5-5cm，宽2-3cm，切面类白色或浅红棕色，可见放射状纹理，周边较厚，微翘起或略弯曲。体轻，质硬脆，粉性。气微，味微甜。以肥大、断面粉红色、粉性足者为佳。\n
        功能主治：清热，解毒，散结，生肌，止痛，治痈肿，疔疮，瘰疬，烫伤，温疟，惊痫，血痢，肠风，痔漏。\n
        性味：苦；辛；性微寒。\n
        用法用量：用量4.5～9克，水煎服；鲜品捣烂或干品研细粉外敷。用治痈疽发背、疔疮、瘰疬、水火烫伤等。\n
        服用禁忌：脾胃虚寒及无实火者，痈疽已溃者均不宜服。阴疽色淡不起，胃气弱者，也不宜服用。
        ''')
    elif source2_index==5:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白茅根.jpg')
        st.image(image, caption='白茅根')
        st.markdown('''
        中文名：白茅根\n
        拼音：bai mao gen\n
        性状：长圆柱形。表面黄白色或淡黄色，微有光泽，具纵皱纹，节明显，稍突起，节间长短不等。体轻，质略脆，断面皮部白色，多有裂隙，放射状排列，中柱淡黄色，易与皮部剥离。无臭，味微甜。\n
        功能主治：凉血止血，清热利尿。属止血药下属中的凉血止血药。\n
        性味：味甘，性寒。\n
        用法用量：用量9～30克，煎服；或鲜品30～60克，捣汁外用。\n
        服用禁忌：脾胃虚寒、溲多不渴者禁服。
        ''')
    elif source2_index==6:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白前.jpg')
        st.image(image, caption='白前')
        st.markdown('''
        中文名：白前\n
        拼音：bai qian \n
        性状：根茎圆柱形，较短小，或略呈块状；表面灰绿色或淡黄色，平滑或有细纵纹。节明显，节间长1～2厘米，质地较坚硬，折断面中空，髓腔较小。节上簇生纤细弯曲的根，细根稍粗长，直径约1毫米，分枝的细根少，质脆，易折断。\n
        功能主治：降气、消痰、止咳。\n
        性味：性微温，味辛、苦。\n
        用法用量：用量3～9克，煎服；或入丸、散。\n
        服用禁忌：阴虚火旺、肺肾气虚咳嗽者慎服。
        ''')
    elif source2_index == 7:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白芍.jpg')
        st.image(image, caption='白芍')
        st.markdown('''
        中文名：白芍\n
        拼音：bai shao\n
        性状：圆柱形，粗细均匀，大多顺直。长5～20厘米，直径1～2.5厘米。表面棕色或浅棕色，外皮未去尽处显棕褐色斑痕，较粗糙，有明显的纵皱纹及细根痕，偶见横向皮孔。质坚实而重，不易折断，切断面灰白色或微带棕色，角质样，木质部呈放射状。气无，味微苦而酸。\n
        功能主治：养血柔肝，缓中止痛，敛阴收汗。治胸腹胁肋疼痛，泻痢腹痛，自汗盗汗，阴虚发热，月经不调，崩漏，带下。\n
        性味：苦酸，凉。\n
        用法用量：内服：煎汤，2～4钱；或入丸、散。\n
        服用禁忌：虚寒腹痛泄泻者慎服。
        ''')
    elif source2_index == 8:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\白术.jpg')
        st.image(image, caption='白术')
        st.markdown('''
        中文名：白术\n
        拼音：bai zhu\n
        性状：根茎略呈圆柱状块形，下部两侧膨大，长3~12厘米，直径2~7厘米。表面灰黄色或灰棕色，有瘤状突起及断续的纵皱纹和沟纹，并有须根痕，顶端有残留的茎基和芽痕。质坚实，不易折断，断面不平坦，淡黄色至淡棕色，并有棕色油室散在，烘干者断面角质样，色较深，有裂隙。气清香，味甜微辛，嚼之略带黏液性。\n
        功能主治：健脾、益气、燥湿利水、止汗、安胎。\n
        性味：性温，味甘、苦。\n
        用法用量：用量6~12克，煎服；或入丸、散；或熬膏。\n
        服用禁忌：阴虚内热、津液亏耗者慎服;内有实邪雍滞者禁服。
        ''')
    elif source2_index == 9:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\柏子仁.jpg')
        st.image(image, caption='柏子仁')
        st.markdown('''
        中文名：柏子仁\n
        拼音：bai zi ren\n
        性状：种仁呈长卵圆形至长椭圆形，亦有呈长圆锥形者，长3～7毫米，径1.5～3毫米。新鲜品淡黄色或黄白色，久置则颜色变深而呈黄棕色，并有油渗出。外面常包有 薄膜质的内种皮，顶端略尖，圆三棱形，并有深褐色的点，基部钝圆，颜色较浅。断面乳白色至黄白色，胚乳较多，子叶2枚或更多，均含丰富的油质。气微香，味淡而有油腻感。以粒饱满、黄白色、油性大而不泛油、无皮壳杂质者为佳。\n
        功能主治：养心安神，润肠通便。治惊悸，失眠，遗精，盗汗，便秘。\n
        性味：性平，味甘。\n
        用法用量：内服：煎汤，10~15g；便溏者制霜用；或入丸、散。外用：适量，研末调敷；或鲜品捣敷。\n
        服用禁忌：便溏及痰多者忌服。
        ''')
    elif source2_index == 10:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\板蓝根.jpg')
        st.image(image, caption='板蓝根')
        st.markdown('''
        中文名：板蓝根\n
        拼音：ban lan gen\n
        性状：本品呈圆形的厚片。外表皮淡灰黄色至淡棕黄色，有纵皱纹。切面皮部黄白色，木部黄色。气微，味微甜后苦涩。\n
        功能主治：清热解毒，凉血，利咽。外感发热，温病初起，咽喉肿痛，温毒发斑，痄腮，丹毒，痈肿疮毒。\n
        性味：味苦，性寒。\n
        用法用量：煎服，9-15g。\n
        服用禁忌：体虚而无实火热毒者忌服，脾胃虚寒者慎用。
        ''')
    elif source2_index == 11:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\北沙参.jpg')
        st.image(image, caption='北沙参')
        st.markdown('''
        中文名：北沙参\n
        拼音：bei sha shen\n
        性状：本品呈细长圆柱形，偶有分枝，长15～45cm，直径0.4～1.2cm。表面淡黄白色，略粗糙，偶有残存外皮，不去外皮的表面黄棕色。全体有细纵皱纹及纵沟，并有棕黄色点状细根痕。顶端常留有黄棕色根茎残基；上端稍细，中部略粗，下部渐细。质脆，易折断，断面皮部浅黄白色，木部黄色。气特异，味微甘。\n
        功能主治：养阴清肺，益胃生津。用于肺热燥咳，劳嗽痰血，热病津伤口渴。\n
        性味： 甘、微苦，微寒。\n
        用法用量：内服：煎汤，5-10g；或入丸、散、膏剂。\n
        服用禁忌：风寒作嗽及肺胃虚寒者忌服。
        ''')
    elif source2_index == 12:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\荜拨.jpg')
        st.image(image, caption='荜拨')
        st.markdown('''
        中文名：荜拨\n
        拼音：bi bo\n
        性状：果穗圆柱形，稍弯曲，由多数小浆果集合而成，长1.5~3.5cm，直径0.3~0.5cm。表面黑褐色或棕色，有斜向排列整齐的小突起，基部有果穗梗残余或脱落痕；质硬而脆，易折断，断面不整齐，颗粒状。小浆果球形，直径约1mm。有特异香气，味辛辣。 以肥大、饱满、坚实、色黑褐、气味浓者为佳。\n
        功能主治：温中，散寒，下气，止痛。治心腹冷痛，呕吐吞酸，肠鸣泄泻，冷痢，阴疝，头痛，鼻渊，齿痛。\n
        性味：辛，热。\n
        用法用量：内服：煎汤，1.5~3g，或入丸、散。外用：研末鼻吸或置蛀牙孔中，适量。\n
        服用禁忌：实热郁火、阴虚火旺者均忌服。
        ''')
    elif source2_index == 13:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\荜澄茄.jpg')
        st.image(image, caption='荜澄茄')
        st.markdown('''
        中文名：荜澄茄\n
        拼音：bi cheng jia\n
        性状：类球形，直径4～6毫米。表面棕褐色至黑褐色，有网状皱纹。基部偶有宿萼及细果梗。除去外皮可见硬脆的果核，种子1粒，子叶2，黄棕色，富油性。气芳香，味稍辣而微苦。用量1.5~3克，内服煎汤。\n
        功能主治：温中散寒，行气止痛。属温里药。\n
        性味：性温，味辛。\n
        用法用量：用量1.5～3克，内服煎汤。\n
        服用禁忌：阴虚血分有热，发热咳嗽禁用。
        ''')
    elif source2_index == 14:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\薄荷.jpg')
        st.image(image, caption='薄荷')
        st.markdown('''
        中文名：薄荷\n
        拼音：bo he \n
        性状: 茎方柱形，长60～90厘米，直径2～8毫米；表面紫棕色或淡绿色，棱角处具茸毛，节间长1～5厘米，有对生分枝，质脆，断面中空或白色。叶对生，有短柄；叶片皱缩卷曲，湿润后展开，叶披针形、卵状披针形、长圆状披针形至椭圆形，两面均有柔毛及腺鳞(放大镜下观察呈凹点状)。茎上部轮伞花序腋生，疏离，花萼钟状，先端5齿裂，花冠多数存在，黄棕色。搓揉后有特殊香气，味辛凉。\n
        功能主治：宣散风热、清头目、透疹。\n
        性味：性凉，味辛。\n
        用法用量：用量3～6克，宜后下，外用适量。\n
        服用禁忌：阴虚血燥，肝阳偏亢，表虚汗多者忌服。
        ''')
    elif source2_index == 15:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\苍术.jpg')
        st.image(image, caption='苍术')
        st.markdown('''
        中文名：苍术\n
        拼音：cang zhu\n
        性状：不规则连珠状或结节状圆柱形，略弯曲，偶有分枝，长3～10厘米，直径1～2厘米。表面灰棕色，有皱纹、横曲纹及残留须根，顶端具茎痕或残留茎基。质坚实，断面黄白色或灰白色，散有多数橙黄色或棕红色油室，暴露稍久，可析出白色细针状结晶。\n
        功能主治：健脾，燥湿，解郁，辟秽。治湿盛困脾，倦怠嗜卧，脘痞腹胀，食欲不振，呕吐，泄泻，痢疾，疟疾，痰饮，水肿，时气感冒，风寒湿痹，足痿，夜盲。\n
        性味：性温，味辛、苦。\n
        用法用量：用量3～10克，水煎服。\n
        服用禁忌：能过量服用。忌与酸味食物同服。孕妇禁用。
        ''')
    elif source2_index == 16:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\草豆蔻.jpg')
        st.image(image, caption='草豆蔻')
        st.markdown('''
        中文名：草豆蔻\n
        拼音：cao dou kou\n
        性状：草豆蔻药材类球形。表面灰褐色，中间有黄白色的隔膜，将种子团分成3瓣，每瓣有种子多数，粘连紧密，种子团略光滑。种子为卵圆状多面体，外被淡棕色膜质假种皮，种背一端有种脐。质硬，将种子沿种背纵剖两瓣，纵断面观呈斜心形，种皮沿种脊向内伸入部分约占整个表面积的1/2；胚乳灰白色。\n
        功能主治：用于寒湿内阻，脘腹胀满冷痛，嗳气呕逆，不思饮食等证。\n
        性味：味辛，性温。\n
        用法用量：用量3～6克，煎服。\n
        服用禁忌：不宜久煎。阴虚血少，津液不足者禁服，无寒湿者慎服。
        ''')
    elif source2_index == 17:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\柴胡.jpg')
        st.image(image, caption='柴胡')
        st.markdown('''
        中文名：柴胡\n
        拼音：chai hu \n
        性状：根较细，圆锥形，顶端有多数细毛状枯叶纤维，下部多不分枝或稍分枝。表面红棕色或黑棕色，靠近根头处多具细密环纹。质稍软，易折断，断面略平坦，不显纤维性。具败油气。\n
        功能主治：和解表里，疏肝，升阳。用于感冒发热，寒热往来，胸胁胀痛，月经不调，子宫脱垂，脱肛。\n
        性味：性微寒，味苦。\n
        用法用量：用量3～9克，水煎服；或入丸、散。外用：适量，煎水洗；或研末调敷。\n
        服用禁忌：真阴亏损，肝阳上亢及肝风内动之证禁服。
        ''')
    elif source2_index == 18:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\陈皮.jpg')
        st.image(image, caption='陈皮')
        st.markdown('''
        中文名：陈皮\n
        拼音：chen pi\n
        性状：常3瓣相连，形状整齐，厚度均匀。点状油室较大，对光照视，透明清晰。质较柔软。\n
        功能主治：理气开胃，燥湿化痰，治脾胃病。用治胸脘胀满、食少呕吐、咳嗽痰多。\n
        性味：味辛、味苦，性温。\n
        用法用量：用量3～9克，煎服。\n
        服用禁忌：阴虚燥咳，咯血、吐血或内有实热者慎用。
        ''')
    elif source2_index == 19:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\沉香.jpg')
        st.image(image, caption='沉香')
        st.markdown('''
        中文名：沉香\n
        拼音：chen xiang\n
        性状：\n
        功能主治：行气止痛，温中止呕，纳气平喘。用于胸腹胀闷疼痛，胃寒呕吐呃逆，肾虚气逆喘急。治气逆喘息，呕吐呃逆，脘腹胀痛，腰膝虚冷，大肠虚秘，小便气淋，男子精冷。\n
        性味：味辛、苦，性微温。\n
        用法用量：治气逆喘息，呕吐呃逆，脘腹胀痛，腰膝虚冷，大肠虚秘，小便气淋，男子精冷。\n
        服用禁忌：阴亏火旺，气虚下陷者慎服。
        ''')
    elif source2_index == 20:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\赤芍.jpg')
        st.image(image, caption='赤芍')
        st.markdown('''
        中文名：赤芍\n
        拼音：chi shao\n
        性状：干燥根呈圆柱形，两端粗细近于相等，稍弯曲，长10～36厘米，径约6～19毫米。表面暗褐色或暗棕色，粗糙，有横向凸起的皮孔及根痕，具粗而深的纵皱纹， 手搓之则外皮易脱落，显出白色或淡棕色的皮层。质硬而脆，易折断。断面平坦，粉白色或黄白色，皮层窄，呈类粉红色，中央髓部小，木质部射线明显，有时具有 裂隙。气微香，味微苦涩。以根条粗长，外皮易脱落，皱纹粗而深，断面白色，粉性大者为佳。\n
        功能主治：行瘀，止痛，清热凉血，消肿。治瘀滞经闭，疝瘕积聚，腹痛，胁痛，衄血，血痢，肠风下血，目赤，痈肿。\n
        性味：苦，微寒。\n
        用法用量：内服：煎汤，4~10g；或入丸、散。\n
        服用禁忌：不宜与藜芦同用。血虚无瘀之症及痈疽已溃者慎服。
        ''')
    elif source2_index == 21:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\赤石脂.jpg')
        st.image(image, caption='赤石脂')
        st.markdown('''
        中文名：赤石脂\n
        拼音：chi shi zhi\n
        性状：本品为块状集合体，呈不规则的块状。粉红色、红色至紫红色，或有红白相间的花纹。质软，易碎，断面有的具蜡样光泽。吸水性强。具黏土气，味淡，嚼之无沙粒感。\n
        功能主治：涩肠，止血，收湿，生肌。治久泻，久痢，便血，脱肛，遗精，崩漏，带下，溃疡不敛。\n
        性味：甘、酸、涩，温。\n
        用法用量：9～12g。外用适量，研末敷患处。\n
        服用禁忌：不宜与肉桂同用。 有湿热积滞者忌服。孕妇慎服。
        ''')
    elif source2_index == 22:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\川楝子.jpg')
        st.image(image, caption='川楝子')
        st.markdown('''
        中文名：川楝子\n
        拼音：chuan lian zi\n
        性状：本品呈类球形，直径2～3.2cm。表面金黄色至棕黄色，微有光泽，少数凹陷或皱缩，具深棕色小点。顶端有花柱残痕，基部凹陷，有果梗痕。外果皮革质，与果 肉间常成空隙，果肉松软，淡黄色，遇水润湿显黏性。果核球形或卵圆形，质坚硬，两端平截，有6～8条纵棱，内分6～8室，每室含黑棕色长圆形的种子1粒。 气特异，味酸、苦。\n
        功能主治：舒肝行气，止痛，驱虫。用于胸胁、脘腹胀痛，疝痛，虫积腹痛。\n
        性味：苦，寒；有小毒。\n
        用法用量：内服：煎汤，3~10g；或入丸、散。外用：适量，研末调涂。行气止痛炒用，杀虫生用。\n
        服用禁忌：脾胃虚寒者忌服。
        ''')
    elif source2_index == 23:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\川木香.jpg')
        st.image(image, caption='川木香')
        st.markdown('''
        中文名：川木香\n
        拼音：chuan mu xiang\n
        性状： 本品呈圆柱形或有纵槽的半圆柱形，稍弯曲，长10～30cm，直径1～3cm。表面黄褐色或棕褐色，具皱纵纹，外皮脱落处可见丝瓜络状细筋脉；根头偶有黑色发黏的胶状物，习称“油头”。体较轻，质硬脆，易折断，断面黄白色或黄色，有深黄色稀疏油点及裂隙，木部宽广，有放射状纹理；有的中心呈枯朽状。气微香，味苦，嚼之粘牙。\n
        功能主治：行气止痛。用于脘腹胀痛，肠鸣腹泻，里急后重，两胁不舒，肝胆疼痛。\n
        性味： 辛、苦，温。\n
        用法用量：内服：煎汤，1.5～9克，宜后下；研末，每次0.5～0.9克。用于胸胁、脘腹胀痛，肠鸣腹泻，里急后重。\n
        服用禁忌：脏腑燥热，气虚、阴虚者禁服。芳香不宜久煎。
        ''')
    elif source2_index == 24:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\川牛膝.jpg')
        st.image(image, caption='川牛膝')
        st.markdown('''
        中文名：川牛膝\n
        拼音：chuan niu xi\n
        性状：本品呈近圆柱形，微扭曲，向下略细或有少数分枝，长30～60cm，直径0.5～3cm。表面黄棕色或灰褐色，具纵皱纹、支根痕和多数横向突起的皮孔。质韧，不易折断，断面浅黄色或棕黄色，维管束点状，排列成数轮同心环。气微，味甜。以条粗壮、质柔韧、分枝少、断面浅黄色者为佳。\n
        功能主治：祛风，利湿，通经，活血祛瘀。治风湿腰膝疼痛，脚痿筋挛，血淋，尿血，妇女经闭，癥瘕，胞衣不下，跌扑损伤。\n
        性味：甘、微苦，平。\n
        用法用量：内服，煎汤，6～10g;或入丸、散；或泡酒。\n
        服用禁忌：《四川中药志》：妇女月经过多，妊娠，梦遗滑精者忌用。
        ''')
    elif source2_index == 25:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\川穹.jpg')
        st.image(image, caption='川穹')
        st.markdown('''
        中文名：川穹\n
        拼音：chuan qiong\n
        性状：\n
        功能主治：活血化瘀；镇静安神；祛风除湿；\n
        性味：辛温\n
        用法用量：\n
        服用禁忌：
        ''')
    elif source2_index == 26:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\大腹皮.jpg')
        st.image(image, caption='大腹皮')
        st.markdown('''
        中文名：大腹皮\n
        拼音：da fu pi\n
        性状：干燥果皮，通常纵剖为二。未打松者呈椭圆形瓢状。长6～7厘米，宽约3厘米，厚约1厘米；外果皮灰棕黄色，有褐色斑点及纵裂纹。已打松者，外果皮脱落，中果 皮为黄白色至灰黄色的纤维，纤维纵向排列，外层松散成缕，内层纤维较粗，现棕毛状。内壁凹陷，褐色或深棕色。表面光滑呈硬壳状。体轻松，质柔韧，易纵向撕 裂。无臭，味淡。以色黄白、质柔韧、无杂质者为佳。\n
        功能主治：下气宽中，行水消肿。用于湿阻气滞，脘腹胀闷，大便不爽，水肿胀满，脚气浮肿，小便不利。\n
        性味：辛，微温。\n
        用法用量：内服：煎汤，5~10g；或入丸、散。外用：适量，煎水洗；或研末调敷。\n
        服用禁忌：气虚体弱者慎服。
        ''')
    elif source2_index == 27:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\淡豆豉.jpg')
        st.image(image, caption='淡豆豉')
        st.markdown('''
        中文名：淡豆豉\n
        拼音：dan dou chi\n
        性状：本品呈椭圆形略扁，长0.6-1cm，直径0.5-0.7cm。表面黑色，皱缩不平，无光泽，一侧有棕色的条状种脐，珠孔不明显。子叶2片，肥厚。质柔软，断面棕黑色。气微，味微甘。以粒大、饱满、色黑者为佳。\n
        功能主治：解表，除烦，宣郁，解毒。治伤寒热病，寒热，头痛，烦躁，胸闷。\n
        性味：苦；辛；平\n
        用法用量：内服：煎汤，5~15g；或入丸剂。外用：适量，捣敷；或炒焦研末调敷。\n
        服用禁忌：《本草经疏》：凡伤寒传入阴经与夫直中三阴者，皆不宜用。
        ''')
    elif source2_index == 28:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\当归.jpg')
        st.image(image, caption='当归')
        st.markdown('''
        中文名：当归\n
        拼音：dang gui\n
        性状：本品略呈圆柱形，下部有支根3～5条或更多，长15～25cm。表面黄棕色至棕褐色，具纵皱纹及横长皮孔。根头（归头）直径1.5～4cm,具环纹，上端圆 钝，有紫色或黄绿色的茎及叶鞘的残基；主根（归身）表面凹凸不平；支根（归尾）直径0.3～1cm,上粗下细，多扭曲，有少数须根痕。质柔韧，断面黄白色 或淡黄棕色，皮部厚，有裂隙及多数棕色点状分泌腔，木部色较淡，形成层环黄棕色。有浓郁的香气，味甘、辛、微苦。柴性大、干枯无油或断面呈绿褐色者不可供药用。\n
        功能主治：补血活血，调经止痛，润肠通便。用于血虚萎黄，眩晕心悸，月经不调，经闭痛经，虚寒腹痛，肠燥便秘，风湿痹痛，跌扑损伤，痈疽疮疡。酒当归活血通经，用于经闭痛经，风湿痹痛，跌扑损伤。当归身功效为补血，用于血虚萎黄，经少，眩晕，经络不利，崩漏。当归尾功效为活血祛瘀，用于瘀血阻滞，经少经闭，经行腹痛，跌扑损伤，瘀滞经络，痈疽疮疡。\n
        性味：味甘；辛；苦；性温\n
        用法用量：内服：煎汤，6~12g；或入丸、散；或浸酒；或敷膏。\n
        服用禁忌：湿阻中满及大便溏泄者慎服。
        ''')
    elif source2_index == 29:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\丹参.jpg')
        st.image(image, caption='丹参')
        st.markdown('''
        中文名：丹参\n
        拼音：dan shen\n
        性状：干燥根茎顶部常有茎基残余，根茎上生1至多数细长的榀。根略呈长圆柱形，微弯曲，有时分支，其上生多数细须根，根长约10～25厘米，直径约0.8～1.5 厘米，支根长约5～8厘米，直径约2～5毫米，表面棕红色至砖红色，粗糙，具不规则的纵皱或栓皮，多呈鳞片状剥落.质坚脆，易折断，断面不平坦，带角质或 纤维性，皮部色较深，呈紫黑色或砖红色，木部维管束灰黄色或黄白色，放射状排列。气弱，味甘微苦。以条粗、内紫黑色，有菊花状白点者为佳。\n
        功能主治：祛瘀止痛，活血通经，清心除烦。治心绞痛，月经不调，痛经，经闭，血崩带下，癥瘕，积聚，瘀血腹痛，骨节疼痛，惊悸不眠，恶疮肿毒。\n
        性味：苦，微温。\n
        用法用量：内服：煎汤，9～15g；或入丸、散。熬膏涂，或煎水熏洗。\n
        服用禁忌：无瘀血者慎服。
        ''')
    elif source2_index == 30:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\稻芽.jpg')
        st.image(image, caption='稻芽')
        st.markdown('''
        中文名：稻芽\n
        拼音：dao ya\n
        性状：呈稍扁的长椭圆形，两端略尖，长7～9毫米，宽3～4毫米，外稃坚硬，表面黄色，具短细毛，有脉5条。一端有2枚对称的白色条形桨片，长约2毫米，淡黄色，膜质，于一个桨片内侧伸出淡黄色弯曲的初生根，长0.5～1.2厘米。内稃薄膜质，光滑，黄白色，内含果实，质坚，断面白色，有粉性。气无，味微甜。\n
        功能主治：和中消食、健脾开胃。属消食药。\n
        性味：性温，味甘。\n
        用法用量：用量9～15克；大剂量可用30克。用治米面薯芋等淀粉类食物所致的食滞、脘腹胀满，或脾虚食少等。\n
        服用禁忌：尚不明确。
        ''')
    elif source2_index == 31:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\大青叶.jpg')
        st.image(image, caption='大青叶')
        st.markdown('''
        中文名：大青叶\n
        拼音：da qing ye\n
        性状：本品多皱缩卷曲，有的破碎。完整叶片展平后呈长椭圆形至长圆状倒披针形，长5～20cm，宽2～6cm；上表面暗灰绿色，有的可见色较深稍突起的小点；先端钝，全缘或微波状，基部狭窄下延至叶柄呈翼状；叶柄长4～10cm，淡棕黄色。质脆。气微，味微酸、苦、涩。\n
        功能主治：清热解毒，凉血止血。治温病热盛烦渴，流行性感冒，急性传染性肝炎，菌痢，急性胃肠炎，急性肺炎，丹毒，吐血，衄血，黄疸，痢疾，喉痹，口疮，痈疽肿毒。\n
        性味：苦；寒\n
        用法用量：内服：煎汤，10~15g，鲜品30~60g；或捣汁服。外用：捣敷；煎水洗。\n
        服用禁忌：脾胃虚寒者忌服。
        ''')
    elif source2_index == 32:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\地龙.jpg')
        st.image(image, caption='地龙')
        st.markdown('''
        中文名：地龙\n
        拼音：di long\n
        性状：（1）广地龙，呈长条状薄片，弯曲，边缘略卷，长15~20cm，宽1~2cm。全体具环节，背部棕褐色至紫灰色，腹部浅黄棕色； 第14~16环节为生殖带，习称白颈，较光亮。体前端稍尖，尾端钝圆，刚毛圈粗糙而硬，色稍浅。雄生殖孔在第18节腹侧刚毛圈一小孔突上，外缘有数圈环绕 的浅皮褶，内侧刚毛圈隆起，前面两边有横排（一排或二排）小乳突，每边10~20个不等。受精囊孔3对，位于6~9节间一椭圆形突起上，约占节周 5/11。体轻，略呈革质，不易折断。气腥，味微咸。\n
       （2）沪地龙，长8~15cm，宽 0.5~1.5cm。全体具环节，背部棕褐色至黄褐色，腹部浅黄棕色；受精囊孔3对，在6-7，7-8，8-9节间。第14~16节为生殖带，较光亮。第 18节有1对雄生殖孔。通谷环毛蚓的雄交配腔孔呈纵向裂缝状；栉盲环毛蚓的雄生殖孔内侧有1个或多个小乳突。\n
        功能主治：清势止痉，平肝熄风，通经活络，平喘利尿。主热病发热狂燥，惊痫抽搐，肝阳头痛，中风偏瘫，风湿痹痛，肺热喘咳，小便不通。\n
        性味：味咸；性寒\n
        用法用量：内服：煎汤，5~10g；或末，每次1~2g；或入丸、散；或鲜品拌糖或盐化水服。外用：适量，鲜品捣烂敷或取汁涂敷；研末撒或调涂。\n
        服用禁忌：脾胃虚寒不宜服，孕妇禁服。
        ''')
    elif source2_index == 33:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\防风.jpg')
        st.image(image, caption='防风')
        st.markdown('''
        中文名：防风\n
        拼音：fang feng\n
        性状：根呈长圆锥形或长圆柱形，下部渐细，有的略弯曲，长15~30cm，直径0.5~2cm。表面灰棕色，粗糙，有纵皱纹、多数横长皮孔及点状突起的细根痕。根 头部有明显密集的环纹，有的部有明显密集的环纹，有的五纹上残存棕褐色毛状叶基。体轻，质松，易折断，断面不平坦，皮部浅棕色，有裂隙，散生黄棕色油点， 木部浅黄色。气特异，味微甘。 以条粗壮、断面皮部色浅棕、木部色浅黄者为佳。\n
        功能主治：发表，祛风，胜湿，止痛。治外感风寒，头痛，目眩，项强，风寒湿痹，骨节酸痛，四肢挛急，破伤风。\n
        性味：辛、甘，温。\n
        用法用量：内服：煎汤，5~10g；或入丸、散。 外用：适量，煎水熏洗。 一般生用，止泻炒用，止血炒炭用。\n
        服用禁忌：血虚痉急或头痛不因风邪者忌服。
        ''')
    elif source2_index == 34:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\番泻叶.jpg')
        st.image(image, caption='番泻叶')
        st.markdown('''
        中文名：番泻叶\n
        拼音：fan xie ye\n
        性状：（1）狭叶番泻叶：小叶片多完整平坦。卵状披针形至线状披针形，长2~6cm，宽0．4~1.5cm；主脉突出，叶端尖突出成棘尖，全缘，基部略不对称，上面黄绿色，下面浅黄绿色，两面均有稀毛茸，下表面主脉突出，羽状网脉。叶片革质。气微弱而特异，味微苦而稍有粘性。\n
       （2）尖叶番泻叶：小叶片呈广披针形或长卵形，长2~4cm，宽0.7~1.2cm；叶端尖或微凸，全线，叶基不对称，上面浅绿色，下面灰绿色，微有短毛，质地较薄脆，微呈革质状。气味同上。以叶片大、完整、色绿、梗少、无泥沙杂质者为佳。\n
        功能主治：泻热通便，消积导滞，止血。主热结便秘，习惯性便秘，积滞腹胀，水肿臌胀，胃、十二指肠溃疡出血。\n
        性味：甘苦；寒凉\n
        用法用量：内服：煎汤，3~6g，后下；或泡茶；或研末，1.5~3g。\n
        服用禁忌：体虚、妇女哺乳期、月经期及孕妇忌用。《饮片新参》：中寒泄泻者忌用。
        ''')
    elif source2_index == 35:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\蜂房.jpg')
        st.image(image, caption='蜂房')
        st.markdown('''
        中文名：蜂房\n
        拼音：feng fang\n
        性状：本品呈圆盘状或不规则的扁块状，有的似莲房状，大小不一。表面灰白色或灰褐色。腹面有多数整齐的六角形房孔，孔径3～4mm或6～8mm；背面有1个或数个黑色短柄。体轻，质韧，略有弹性。气微，味辛淡。质酥脆或坚硬者不可供药用。\n
        功能主治：祛风，攻毒，杀虫。治惊痫，风痹，瘾疹瘙痒，乳痈，疔毒，瘰疬，痔漏，风火牙痛，头癣，蜂螫肿疼。\n
        性味：甘，平。\n
        用法用量：内服：煎汤，5~10g；研末服，2~5g。外用：适量，煎水洗、研末掺或调敷。\n
        服用禁忌：气虚弱及肾功能不全者慎服。
        ''')
    elif source2_index == 36:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\茯苓.jpg')
        st.image(image, caption='茯苓')
        st.markdown('''
        中文名：茯苓\n
        拼音：fu ling\n
        性状：茯苓块：为去皮后切制的茯苓，呈块片状，大小不一。白色、淡红色或淡棕色。\n
        功能主治：渗湿利水，益脾和胃，宁心安神。治小便不利，水肿胀满，痰饮咳逆，呕哕，泄泻，遗精，淋浊，惊悸，健忘。\n
        性味：甘；淡；平\n
        用法用量：内服：煎汤，10~15g；或入丸散。宁心安神用朱砂拌。\n
        服用禁忌：虚寒精滑或气虚下陷者忌服。
        ''')
    elif source2_index == 37:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\甘草.jpg')
        st.image(image, caption='甘草')
        st.markdown('''
        中文名：甘草\n
        拼音：gan cao\n
        性状：干燥根呈长圆柱形，不分枝，多截成长30～120厘米的段，直径0.6～3.3厘米。带皮的甘草，外皮松紧不等，显红棕色、棕色或灰棕色，具显著的皱纹、沟纹及稀疏的细根痕，皮孔横生，微突起，呈暗黄色。
             两端切面平齐，切面中央稍陷下。质坚实而重。断面纤维性，黄白色，粉性，有一明显的环纹和菊花心，常形成裂隙.微具特异的香气，味甜而特殊。根状茎形状与根相似，但表面有芽痕，横切面中央有髓。
             粉草外表平坦，淡黄色，纤维性，有纵裂纹。带皮甘草以外皮细紧、有皱沟、红棕色、质坚实、粉性足、断面黄白色者为佳；外皮粗糙，灰棕色、质松、粉性小、断面深黄色者为次；外皮棕黑色、质坚硬、断面棕黄色、味苦者不可入药。粉草较带皮甘草为佳。\n
        功能主治：和中缓急，润肺，解毒，调和诸药。炙用，治脾胃虚弱，食少，腹痛便溏，劳倦发热，肺痿咳嗽，心悸，惊痫；生用，治咽喉肿痛，消化性溃疡，痈疽疮疡，解药毒及食物中毒。\n
        性味：甘，平。\n
        用法用量：内服：煎汤，2~6g，调和诸药用量宜小，作为主药用量宜稍大，可用10g左右；用于中毒抢救，可用30~60g。凡入补益药中宜炙用，入清泻药中宜生用。外用：适量，煎水洗、渍；或研末敷。\n
        服用禁忌：不宜与甘遂、大戟、芫花、海藻同用。
        ''')
    elif source2_index == 38:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\干姜.jpg')
        st.image(image, caption='干姜')
        st.markdown('''
        中文名：干姜\n
        拼音：gan jiang\n
        性状：干燥根茎为扁平、不规则的块状，有指状分枝。长4～6厘米，厚0.4～2厘米。表面灰白色或灰黄色，粗糙，具纵皱纹及明显的环节；在分枝处，常有鳞叶残存。质坚实，断面颊粒性，灰白色或淡黄色，质松者则显筋脉，有细小的油点及一明显的环纹。气芳香，味辛辣。以质坚实，外皮灰黄色、内灰白色、断面粉性足、少筋脉者为佳。\n
        功能主治：温中逐寒，回阳通脉。治心腹冷痛，吐泻，肢冷脉微，寒次喘咳，风寒湿痹，阳虚吐、衄、下血。\n
        性味：辛、热。\n
        用法用量：内服：煎汤，3~10g；或入丸散。外用：适量，煎汤洗；或研末调敷。\n
        服用禁忌：阴虚内热、血热妄行者禁服。
        ''')
    elif source2_index == 39:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\甘松.jpg')
        st.image(image, caption='甘松')
        st.markdown('''
        中文名：甘松\n
        拼音：gan song\n
        性状：本品多弯曲，上粗下细，长5~18cm。根茎短，上端有残留茎基，外被多层枯叶殖基，呈膜质片状或纤维状，外层棕黑色，内层棕色或黄色。根单一，有的数条交结，并列或分枝，长6~16cm，直径0.3~1cm；表面皱缩，棕褐色，有细根和须根。质松脆，易折断，断面粗糙，皮部深棕色，常成裂片状，木部黄白 色。气特异，叶苦、辛，有清凉感。以条长、根粗、香气浓者为佳。\n
        功能主治：理气止痛，醒脾健胃。治胃痛，胸腹胀满，头痛，癔病，脚气，食欲不振。\n
        性味：味辛；甘；性温\n
        用法用量：内服：煎汤，3~6g；或入丸、散。外用：适量，研末敷；或泡水含漱；或煎汤外洗。\n
        服用禁忌：气虚血热者忌服。
        ''')
    elif source2_index == 40:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\公丁香.jpg')
        st.image(image, caption='公丁香')
        st.markdown('''
        中文名：公丁香\n
        拼音：gong ding xiang\n
        性状：干燥的花蕾略呈短棒状，长1.5～2厘米，红棕色至暗棕色。下部为圆柱状略扁的萼管，长1～1.3厘米，宽约5毫米，厚约3毫米，基部渐狭小，表面粗糙，刻 之有油渗出，萼管上端有4片三角形肥厚的萼。上部近圆球形；径约6毫米，具花瓣4片，互相抱合。将花蕾剖开，可见多数雄蕊，花丝向中心弯曲，中央有一粗壮 直立的花柱。质坚实而重，入水即沉；断面有油性，用指甲划之可见油质渗出。气强烈芳香，味辛。以个大，粗壮、鲜紫棕色、香气强烈、油多者为佳。\n
        功能主治：温中降逆，温肾助阳。主呃逆，脘腹冷痛，食少吐泻，肾虚阳痿，腰膝酸冷，阴疽。\n
        性味：辛，温。\n
        用法用量：内服，煎汤，2~5g；或入丸、散。外用：适量，感想末敷贴。\n
        服用禁忌：不宜与郁金同用。热病及阴虚内热者忌服。
        ''')
    elif source2_index == 41:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\桂枝.jpg')
        st.image(image, caption='桂枝')
        st.markdown('''
        中文名：桂枝\n
        拼音：gui zhi\n
        性状：枝长圆柱形，多分枝，长30~70cm，粗端直径0.3~1cm。表面棕色或红棕色，有细皱纹及小疙瘩状叶痕、枝痕和芽痕，皮孔点状或点状椭圆形。制裁硬而 脆，易折断，断面皮部红棕色，可见一淡黄色石细胞环带，木部黄白色至浅黄棕色，髓部略呈方形。有特异香气，味甜、微辛，皮部味较浓。以枝条嫩细均匀，色红棕，香气浓者为佳。\n
        功能主治：发汗解肌，温经通脉。治风寒表证，肩背肢节酸疼，胸痹痰饮，经闭癥瘕。\n
        性味：辛；甘；性温\n
        用法用量：内服：煎汤1.5~6g，大剂量，可用至15~30g；或入丸、散。\n
        服用禁忌：热病高热，阴虚火旺，血热妄行者禁服。
        ''')
    elif source2_index == 42:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\谷精草.jpg')
        st.image(image, caption='谷精草')
        st.markdown('''
        中文名：谷精草\n
        拼音：gu jing cao \n
        性状：为带花茎的头状花序。花序呈扁圆形，直径4～5毫米；底部有鳞片状浅黄色的总苞片，紧密排列呈盘状；小花30～40朵，灰白色，排 列甚密，表面附有白色的细粉；用手搓碎后，可见多数黑色小粒及灰绿色小形种子。花序下连一细长的花茎，长约15～18厘米，黄绿色，有光泽；质柔，不易折 断。臭无，味淡，久嚼则成团。以珠大而紧、灰白色，花茎短、黄绿色，无根、叶及杂质者为佳。\n
        功能主治：祛风散热，明目退翳。治目翳，雀盲，头痛，齿痛，喉痹，鼻衄。\n
        性味：辛甘，凉。\n
        用法用量：内服：煎汤，9～12克；或入丸、散。外用：烧存性研末撒。\n
        服用禁忌：《得配本草》：血虚病目者禁用。
        ''')
    elif source2_index == 43:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\谷芽.jpg')
        st.image(image, caption='谷芽')
        st.markdown('''
        中文名：谷芽\n
        拼音：gu ya\n
        性状：类圆形，直径约2毫米，顶端钝圆，基部略尖。外壳为革质的稃片，淡黄色，具点状皱纹，下端有初生的细须根，长2～5毫米，剥去稃片，内含淡黄色或黄白色颖果(小米)1粒。无臭，味微甘。 出芽率不得少于85%。\n
        功能主治：消食和中、健脾开胃。属消食药。\n
        性味：性温，味甘。\n
        用法用量：用量9～15克。用治食积不消、腹胀口臭、脾胃虚弱、不饥食少等。\n
        服用禁忌：胃下垂者忌用。
        ''')
    elif source2_index == 44:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\海螵蛸.jpg')
        st.image(image, caption='海螵蛸')
        st.markdown('''
        中文名：海螵蛸\n
        拼音：hai piao shao\n
        性状：无针乌贼:呈扁长椭圆形，中间厚，边缘薄，长9～14cm,宽2.5～3.5cm，厚约1.3cm 。背面有磁白色脊状隆起，两侧略显微红色，有不甚明显的细小疣点；腹面白色，自尾端到中部有细密波状横层纹；角质缘半透明，尾部较宽平，无骨针。体轻，质 松，易折断，断面粉质，显疏松层纹。气微腥，味微咸。\n
        金乌贼:长13～23cm，宽约至6.5cm。背面疣点明显，略呈层状排列；腹面的细密波状横层纹占全体大部分，中间有纵向浅槽；尾部角质缘渐宽，向腹面翘起，末端有1骨针，多已断落。\n
        功能主治：收敛止血，固精止带，制酸止痛，收湿敛疮。主吐血，呕血，崩漏，便血，衄血，创伤出血，肾虚遗精滑精，赤白带下，胃痛嘈杂，嗳气泛酸，湿疹溃疡。\n
        性味：咸、涩，温。\n
        用法用量：内服：煎汤，10~30g；研末，1.5~3g。外用：适量，研末撒；或调敷；或吹耳、鼻。\n
        服用禁忌：阴虚多热者不宜多服；久服易致便秘，可适当配润肠药同用。
        ''')
    elif source2_index == 45:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\蒿本.jpg')
        st.image(image, caption='蒿本')
        st.markdown('''
        中文名：蒿本\n
        拼音：hao ben\n
        性状：\n
        功能主治：具有祛风散寒、胜湿止痛的功效。此药在临床上可以用来治疗外感风寒，巅顶头痛、头痛、鼻塞等疾病。还可以用来治疗风寒湿痹等疾病。\n
        性味：辛、温\n
        用法用量：3--10克，外用适量。\n
        服用禁忌：对于阴血亏虚，肝阳上亢，以及火热内盛导致的头痛患者慎服
        ''')
    elif source2_index == 46:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\合欢皮.jpg')
        st.image(image, caption='合欢皮')
        st.markdown('''
        中文名：合欢皮\n
        拼音：he huan pi\n
        性状：本品呈卷曲筒状或半筒状，长40～80cm，厚0.1～0.3cm。外表面灰棕色至灰褐色，稍有纵皱纹，有的成浅裂纹，密生明显的椭圆形横向皮孔，棕色或棕红色，偶有突起的横棱或较大的圆形枝痕，常附有地衣斑；内表面淡黄棕色或黄白色，平滑，有细密纵纹。质硬而脆，易折断，断面呈纤维性片状，淡黄棕色或黄白 色。气微香，味淡、微涩、稍刺舌，而后喉头有不适感。\n
        功能主治：解郁安神，活血消肿。用于心神不安，忧郁失眠，肺痈，疮肿，跌扑伤痛。\n
        性味：甘；平\n
        用法用量：内服：煎汤，10~15g；或入丸、散。外用：适量，研末调敷。\n
        服用禁忌：
        ''')
    elif source2_index == 47:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\黄柏.jpg')
        st.image(image, caption='黄柏')
        st.markdown('''
        中文名：黄柏\n
        拼音：huang bai\n
        性状：为植物黄皮树及其变型变种的干燥树皮。呈稍弯曲的板片状，边缘不整齐，长宽不一，厚约3～5毫米，栓皮多已剥离。外表面深黄色，较平坦，有纵棱线及棕色皮孔；内表面灰黄色或黄色。质坚硬而轻，易折断，折断面纤维性，呈片状分裂，鲜黄色。气微，味苦，嚼之有粘滑性，能使水染黄色。以片张厚大、鲜黄色、无栓皮者为佳。\n
        功能主治：清热。燥湿，泻火，解毒。治热痢，泄泻，消渴，黄疸，痿躄，梦遗，淋浊，痔疮，便血，亦白带下，骨蒸劳热，目赤肿痛，口舌生疮，疮疡肿毒。\n
        性味：苦，寒。\n
        用法用量：内服：煎汤，3~9g；或入丸、散。外用：适量，研末调敷，或煎水浸洗。\n
        服用禁忌：脾虚泄泻，胃弱食少者忌服。
        ''')
    elif source2_index == 48:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\黄芪.jpg')
        st.image(image, caption='黄芪')
        st.markdown('''
        中文名：黄芪\n
        拼音：huang qi\n
        性状：本品呈圆柱形，有的有分枝，上端较粗，长30～90cm，直径1～3.5cm。表面淡棕黄色或淡棕褐色，有不整齐的纵皱纹或纵沟。质硬而韧，不易折断，断面 纤维性强，并显粉性，皮部黄白色，木部淡黄色，有放射状纹理及裂隙，老根中心偶有枯朽状，黑褐色或呈空洞。气微，味微甜，嚼之微有豆腥味。\n
        功能主治：补气固表，利尿托毒，排脓，敛疮生肌。用于气虚乏力，食少便溏，中气下陷，久泻脱肛，便血崩漏，表虚自汗，气虚水肿，痈疽难溃，久溃不敛，血虚痿黄，内热消渴；慢性肾炎蛋白尿，糖尿病。\n
        性味：甘，温。\n
        用法用量：内服：煎汤，9～30g。\n
        服用禁忌：
        ''')
    elif source2_index == 49:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\黄芩.jpg')
        st.image(image, caption='黄芩')
        st.markdown('''
        中文名：黄芩\n
        拼音：huang qin\n
        性状：干燥根呈倒圆锥形，扭曲不直，长7～27厘米，径约1～2厦米。表面深黄色或黄棕色。上部皮较粗糙，有扭曲的纵皱纹或不规则的网纹，下部皮细，有顺纹或细皱纹，上下均有稀疏的疣状支根痕。质硬而脆，易折断；断面深黄色，中间有棕红色圆心。老根断面中央呈暗棕色或棕黑色朽片状，习称枯黄芩或枯芩；或因中空而不 坚硬，呈劈破状者，习称黄芩瓣。根遇潮湿或冷水则变为黄绿色。无臭，味苦。以条粗长、质坚实、色黄、除净外皮者为佳。条短、质松、色深黄、成瓣状者质次。\n
        功能主治：泻实火，除湿热，止血，安胎。治壮热烦渴，肺热咳嗽，湿热泻痢，黄疸，热淋，吐、衄、崩、漏，目赤肿痛，胎动不安，痈肿疔疮。\n
        性味：苦，寒。\n
        用法用量：内服：煎汤，3~9g；或入丸、散。外用：适量，煎水洗；或研末调敷。\n
        服用禁忌：凡中寒作泄，中寒腹痛，肝肾虚而少腹痛，血虚腹痛，脾虚泄泻，肾虚溏泻，脾虚水肿，血枯经闭，气虚小水不利，肺受寒邪喘咳，及血虚胎不安，阴虚淋露，法并禁用。
        ''')
    elif source2_index == 50:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\藿香.jpg')
        st.image(image, caption='藿香')
        st.markdown('''
        中文名：藿香\n
        拼音：huo xiang\n
        性状：又名：土藿香(《滇南本草》)，杜藿香。干燥全草长约60～90厘米。茎呈四方柱形，四角有棱脊，直径约3～10毫米，表面黄绿色或灰黄色，毛茸稀少，或近于无毛;质轻脆，断面中央有白色髓。老茎坚硬，木质化，断面中空。叶多已脱落，剩余的叶灰绿色，皱缩或破碎，两面微具毛;薄而脆。有时枝端有圆柱形的花序，土棕色，小花具短柄，花冠多脱落，小坚果藏于萼内。气清香，味淡。以茎枝青绿、叶多、香浓者为佳。\n
        功能主治：快气，和中，辟秽，祛湿。治感冒暑湿，寒热，头痛，胸脘痞闷，呕吐泄泻，疟疾，痢疾，口臭。\n
        性味：味辛；性微温。\n
        用法用量：内服：煎汤，1.5～3钱；或入丸、散。外用：煎水含漱；或烧存性研末调敷。\n
        服用禁忌：1. 适宜外感风寒、内伤湿滞、头痛昏重、呕吐腹泻者、胃肠型感冒患者、中暑、晕车、船、消化不良致腹胀、腹泻、腹痛者、宿醉未醒者。\n
        2. 阴虚火旺、邪实便秘者禁服。
        ''')
    elif source2_index == 51:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\僵蚕.jpg')
        st.image(image, caption='僵蚕')
        st.markdown('''
        中文名：僵蚕\n
        拼音：jiang can\n
        性状：呈圆柱形，多弯曲而皱缩。长约2～5厘米，直径4～7毫米。表面灰白色或现浅棕色，多被有白色粉霜。头、足及各节均清晰可辨。体外常杂有丝团缠绕。头部黄褐色，类圆形。足8对，呈突起状。质硬而脆，易折断；断面平坦，色棕、黑不一，多光亮，外层为白色，显粉性，内有4个褐色的亮圈。微有腐臭气，味微咸。以条直肥壮，质坚，色白，断面光者为佳。\n
        功能主治：祛风解痉，化痰散结。治中风失音，惊痫，头风，喉风，喉痹，瘰疬结核，风疮瘾疹，丹毒，乳腺炎。\n
        性味：辛咸，平。\n
        用法用量：内服：煎汤，3~10g ；研末，1~3g；或入丸、散。外用：适量，煎水洗；研末撒或调敷。\n
        服用禁忌：①《药性论》：恶桑螵蛸、桔梗、茯苓、茯神、萆薢。②《本草经疏》：凡中风口噤，小儿惊痫夜啼，由于心虚神魂不宁，血虚经络劲急所致，而无外邪为病者忌之。女子崩中，产后余痛，非风寒客入者，亦不宜用。
        ''')
    elif source2_index == 52:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\鸡冠花.jpg')
        st.image(image, caption='鸡冠花')
        st.markdown('''
        中文名：鸡冠花\n
        拼音：ji guan hua\n
        性状：为带有短茎的花序，形似鸡冠，或为穗状、卷冠状，上缘呈鸡冠状的部分，密生线状的绒毛，即未开放的小花，一般颜色较深，有红、浅红、白等颜色；中部以下密生许多小花，各小花有膜质灰白色的苞片及花被片。蒴果盖裂；种子黑色，有光泽。气无，味淡。以朵大而扁、色泽鲜艳的白鸡冠花较佳，色红者次之。\n
        功能主治：收敛止血，止带，止痢。治痔漏下血，赤白下痢，吐血，咳血，血淋，妇女崩中，赤白带下。\n
        性味：甘；凉；无毒\n
        用法用量：内服：煎汤，6~12克；或入丸、散。外用：煎水熏洗。\n
        服用禁忌：
        ''')
    elif source2_index == 53:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\锦灯笼.jpg')
        st.image(image, caption='锦灯笼')
        st.markdown('''
        中文名：锦灯笼\n
        拼音：jin deng long\n
        性状：本品略呈灯笼状，多压扁，长3～4.5cm，宽2.5～4cm。表面橙红色或橙黄色，有5条明显的纵棱，棱间有网状的细脉纹。顶端渐尖，微5裂，基部略平截，中心凹陷有果梗。体轻，质柔韧，中空，或内有棕红色或橙红色果实。果实球形，多压扁，直径1～1.5cm，果皮皱缩，内含种子多数。气微，宿萼味苦， 果实味甘、微酸。\n
        功能主治：清热，解毒，利尿。治骨蒸劳热，咳嗽，咽喉肿痛，黄疸，水肿，天泡湿疮。\n
        性味：苦，寒。\n
        用法用量：5～9g。外用适量，捣敷患处。\n
        服用禁忌：
        ''')
    elif source2_index == 54:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\荆芥穗.jpg')
        st.image(image, caption='荆芥穗')
        st.markdown('''
        中文名：荆芥穗\n
        拼音：jing jie sui\n
        性状：干燥的全草，茎方形，四面有纵沟，上部多分枝，长45～90厘米，直径3～5毫米；表面淡紫红色，被有短柔毛。质轻脆，易折断，断面纤维状，黄白色，中心有白色疏松的髓。叶对生，叶片分裂，裂片细长，呈黄色，皱缩卷曲，破碎不全；质脆易脱落。枝顶着生穗状轮伞花序，呈绿色圆柱形，长7～10厘米；花冠多已脱 落，只留绿色的萼筒，内有4个棕黑色的小坚果。气芳香，味微涩而辛凉。以浅紫色、茎细、穗多而密者为佳。\n
        功能主治：发表祛风，理血；炒炭后可止血。治感冒发热，头痛，咽喉肿痛，中风口噤，吐血，衄血，便血；崩漏，产后血晕；痈肿，疮疥，瘰疬。荆芥穗效用相同，但发散之力较强。\n
        性味：辛，温。\n
        用法用量：内服：煎汤，3~10g；或临丸、散。 外用：适量，煎水熏洗；捣敷；或研末调散。\n
        服用禁忌：表虚自汗、阴虚头痛忌服。
        ''')
    elif source2_index == 55:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\金银花.jpg')
        st.image(image, caption='金银花')
        st.markdown('''
        中文名：金银花\n
        拼音：jin yin hua\n
        性状：干燥花蕾呈长棒状，略弯曲，长约2～3厘米，上部较粗，直径约1.5～3毫米。外表黄色或黄褐色，被有短柔毛及腺毛。基部有绿色细小的花萼，5裂，裂片三角形，无毛。剖开花蕾，则见5枚雄蕊及1枚雌蕊。花冠唇形，雌雄蕊呈须状伸出。气芳香，味微苦。以花未开放、色黄白、肥大者为佳。\n
        功能主治：清热，解毒。治温病发热，热毒血痢，痈疡，肿毒，瘰疬，痔漏。\n
        性味：甘；寒\n
        用法用量：内服：煎汤，10~20g；或入丸散。外用：适量，捣敷。\n
        服用禁忌：脾胃虚寒及气虚疮疡脓清者忌服。
        ''')
    elif source2_index == 56:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\九香虫.jpg')
        st.image(image, caption='九香虫')
        st.markdown('''
        中文名：九香虫\n
        拼音：jiu xiang chong\n
        性状：本品略呈六角状扁椭圆形，长1.6~2cm，宽约1cm。表面棕褐色或棕黑色，略有光泽。头部小，与胸部略呈三角形，复眼突出，卵圆状，单眼1对，触角1对各5节，多已脱落。腹部棕红色至棕黑色，每节近边缘外有突起的小点。质脆，折断后腹面有浅棕色的内含物。气特异味微咸。以个均匀、棕褐色、油性大、无虫蛀者为佳。\n
        功能主治：理气止痛，温中助阳。用于胃寒胀痛，肝胃气痛，肾虚阳痿，腰膝酸痛。\n
        性味：味咸；性温\n
        用法用量：内服：煎汤，3~9g；或入丸、散，0.6~1.2g。\n
        服用禁忌：凡阴虚内热者禁服。
        ''')
    elif source2_index == 57:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\橘核.jpg')
        st.image(image, caption='橘核')
        st.markdown('''
        中文名：橘核\n
        拼音：ju he\n
        性状：干燥种子呈卵形或卵圆形，一端常成短嘴状突起，长约7～10毫米，短径约5～7毫米。外种皮淡黄白色至淡灰白色，光滑，一侧有种脊棱线，自种脐延至合点，质脆易剥落。内种皮膜质，淡棕色，紧贴于外种皮之内。种仁两片，肥厚，富油质。微有油气，味苦。以色白，饱满、子粒均匀者为佳。\n
        功能主治：理气，止痛。治疝气，睾丸肿痛，乳痈，腰痛，膀胱气痛。\n
        性味：苦，平。\n
        用法用量：内服：煎汤，3~9g；或入丸、散。\n
        服用禁忌：《本草逢原》：惟实证为宜，虚者禁用。以其味苦，大伤胃中冲和之气也。
        ''')
    elif source2_index == 58:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\苦地丁.jpg')
        st.image(image, caption='苦地丁')
        st.markdown('''
        中文名：苦地丁\n
        拼音：ku di ding\n
        性状：皱缩成团，长10～30厘米。主根圆锥形，表面棕黄色。茎细，多分枝，表面灰绿色或黄绿色，具5纵棱，质软，断面中空。叶多皱缩破碎，暗绿色或灰绿色，完整叶片二至三回羽状全裂。花少见，花冠唇形，有距，淡紫色。蒴果扁长椭圆形，呈荚果状。种子扁心形，黑色，有光泽。气微，味苦。\n
        功能主治：清热解毒，散结消肿。\n
        性味：性寒，味苦。\n
        用法用量：用量9～15g，煎汤内服，外用适量，煎汤洗患处。用治时疫感冒，咽喉肿痛，疔疮肿痛，痈疽发背，痄腮丹毒。\n
        服用禁忌：体虚者忌之，孕妇慎用。
        ''')
    elif source2_index == 59:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\莱菔子.jpg')
        st.image(image, caption='莱菔子')
        st.markdown('''
        中文名：莱菔子\n
        拼音：lai fu zi\n
        性状：干燥种子呈椭圆形或近卵圆形而稍扁，长约3毫米，宽2.5毫米。表面红棕色，一侧有数条纵沟，一端有种脐，呈褐色圆点状突起。用放大镜观察，全体均有致密的网纹。质硬，破开后可见黄白色或黄色的种仁；有油性。无臭，味甘，微辛。以粒大、饱满、油性大者为佳。\n
        功能主治：下气定喘，消食化痰。治咳嗽痰喘，食积气滞，胸闷腹胀，下痢后重。\n
        性味：味辛；甘；性平\n
        用法用量：内服，煎汤5~10g，或入丸、散。外用研末调敷。气虚及无食积、痰滞者慎用；脾虚而无食积者，不宜与人参同用，以免降低人参补气效力。\n
        服用禁忌：
        ''')
    elif source2_index == 60:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\连翘.jpg')
        st.image(image, caption='连翘')
        st.markdown('''
        中文名：连翘\n
        拼音：lian qiao\n
        性状：本品呈长卵形至卵形，稍扁，长1.5～2.5cm，直径0.5～1.3cm。表面有不规则的纵皱纹及多数凸起的小斑点，两面各有1条明显的纵沟。顶端锐尖， 基部有小果梗或已脱落。青翘多不开裂，表面绿褐色，凸起的灰白色小斑点较少，质硬；种子多数，黄绿色，细长，一侧有翅。老翘自顶端开裂或裂成两瓣，表面黄 棕色或红棕色，内表面多为浅黄棕色，平滑，具一纵隔；质脆；种子棕色，多已脱落。气微香，味苦。\n
        功能主治：清热，解毒，散结，消肿。治温热，丹毒，斑疹，痈疡肿毒，瘰疬，小便淋闭。\n
        性味：苦，微寒。\n
        用法用量：内服：煎汤，6~15g；或入丸、散。\n
        服用禁忌：脾胃虚弱，气虚发热，痈疽已溃、脓稀色淡者忌服。
        ''')
    elif source2_index == 61:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\莲须.jpg')
        st.image(image, caption='莲须')
        st.markdown('''
        中文名：莲须\n
        拼音：lian xu\n
        性状：本品为干燥雄蕊，线状，常螺旋状扭曲，花药长1.2-1.5cm，淡黄色棕色，2室，纵裂，内有多数黄色花粉；花丝丝状略扁，稍弯曲，长1-1.5cm，棕黄色或棕褐色，质轻。气微，味微涩。\n
        功能主治：清心，益肾，涩精，止血。治梦遗滑泄，吐、衄、崩、带，泻痢。\n
        性味：甘；涩；平\n
        用法用量：内服：煎汤，3~9g；或入丸、散。\n
        服用禁忌：1.《日华子本草》：忌地黄、葱、蒜。\n
        2.《本草从新》：小便不利者勿服。
        ''')
    elif source2_index == 62:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\莲子.jpg')
        st.image(image, caption='莲子')
        st.markdown('''
        中文名：莲子\n
        拼音：lian zi\n
        性状：本品略呈椭圆形或类球形，长1.2～1.8cm，直径0.8～1.4cm。表面浅黄棕色至红棕色，有细纵纹和较宽的脉纹。一端中心呈乳头状突起，深棕色，多有裂口，其周边略下陷。质硬，种皮薄，不易剥离。子叶2，黄白色，肥厚，中有空隙，具绿色莲子心。无臭，味甘、微涩；莲子心味苦。\n
        功能主治：补脾止泻，益肾固精，养心安神。主脾虚久泻久痢，肾虚遗精，滑泄，小便不禁，妇人崩漏带下，心神不宁，惊悸，不眠。\n
        性味：甘；涩；平\n
        用法用量：内服：煎汤，6~15g；或入丸、散。\n
        服用禁忌：中满痞胀及大便燥结者，忌服。
        ''')
    elif source2_index == 63:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\莲子心.jpg')
        st.image(image, caption='莲子心')
        st.markdown('''
        中文名：莲子心\n
        拼音：lian zi xin\n
        性状：干燥的莲心，略成棒状，长1.2～1.6厘米。顶端膏绿色，有2个分歧，一长一短，先端反折，紧密互贴，用水浸软后展开，可见2片盾状卷曲的幼叶。中央的胚 芽直立，长约2毫米。基部胚根黄绿色，略呈圆柱形，长2～4毫米。质脆，易折断，断面有多数小孔。气无，味苦。以个大、色青绿。未经煮者为佳。\n
        功能主治：清心火，安神，去热，止血，涩精。治心烦，口渴，吐血，遗精，目赤肿痛。\n
        性味：苦，寒。\n
        用法用量：内服：煎汤，1.5~3g；或入散剂。\n
        服用禁忌：
        ''')
    elif source2_index == 64:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\灵芝.jpg')
        st.image(image, caption='灵芝')
        st.markdown('''
        中文名：灵芝\n
        拼音：ling zhi\n
        性状：1.赤芝：外形呈伞状，菌盖肾形、半圆形或近圆形，直径10～18cm，厚1～2cm。皮壳坚硬，黄褐色至红褐色，有光泽，具环状棱纹和辐射状皱纹，边缘薄而平截，常稍内卷。菌肉白色至淡棕色。菌柄圆柱形，侧生，少偏生，长7～15cm，直径1～3.5cm，红褐色至紫褐色，光亮。孢子细小，黄褐色。气微香，味苦涩。\n
        2.紫芝：皮壳紫黑色，有漆样光泽。菌肉锈褐色。菌柄长17～23cm。\n
        功能主治：益气血，安心神，健脾胃。主虚劳，心悸失眠，头晕，神疲乏力，久咳气喘，冠心病，矽肺，肿瘤。\n
        性味：甘；平；无毒\n
        用法用量：内服：煎汤，10~15g；研末，2~6g；或浸酒。\n
        服用禁忌：实证慎服。 《本草经集注》：恶恒山。畏扁青、茵陈蒿。
        ''')
    elif source2_index == 65:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\荔枝核.jpg')
        st.image(image, caption='荔枝核')
        st.markdown('''
        中文名：荔枝核\n
        拼音：li zhi he\n
        性状：本品呈长圆形或卵圆形，略扁，长1.5～2.2cm，直径1～1.5cm。表面棕红色或紫棕色，平滑，有光泽，略有凹陷及细波纹。一端有类圆形黄棕色的种脐，直径约7mm。质硬，子叶2，棕黄色。气微，味微甘、苦、涩。\n
        功能主治：温中，理气，散寒止痛。治胃脘痛，睾丸肿痛，疝气痛，妇女血气刺痛。\n
        性味：甘、微苦，温。\n
        用法用量：内服：煎汤，6~10g；研末，1.5~3g；或入丸、散。外用：适量，研末调敷。\n
        服用禁忌：《本草从新》:无寒湿滞气者勿服。
        ''')
    elif source2_index == 66:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\龙眼.jpg')
        st.image(image, caption='龙眼')
        st.markdown('''
        中文名：龙眼\n
        拼音：long yan\n
        性状：生药为由顶端纵向裂开的不规则块片，长约1.5厘米，宽1.5～3.5厘米，厚不及1毫米，表面黄棕色，半透明；靠近果皮的一面皱缩不平，粗糙；靠近种皮的 一面光亮而有纵皱纹。质柔韧而微有粘性，常粘结呈块状。气香，味浓甜而特殊。以片大、肉厚、质细软、色棕黄、半透明、味浓甜者为佳。\n
        功能主治：益心脾，补气血，安神。治虚劳羸弱，失眠，健忘，惊悸，怔忡。\n
        性味：甘，温。\n
        用法用量：内服：煎汤，10~15g，大剂量30~60g；或熬膏；或浸酒；或入丸、散。\n
        服用禁忌：内有痰火及湿滞停饮者忌服。
        ''')
    elif source2_index == 67:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\芦根.jpg')
        st.image(image, caption='芦根')
        st.markdown('''
        中文名：芦根\n
        拼音：lu gen\n
        性状：呈压扁的长圆柱形。表面有光泽，黄白色，节部较硬，显红黄色，节间有纵皱纹。质轻而柔韧，不易折断，气无，味微甘。均以条粗壮、黄白色、有光泽、无须根、质嫩者为佳。\n
        功能主治：清热，生津，除烦，止呕。治热病烦渴，胃热呕吐，噎膈，反胃，肺痿，肺痈。并解河豚鱼毒。\n
        性味：甘；寒\n
        用法用量：内服：煎汤，15~30g，鲜品60~120g；或鲜品捣汁。外用：适量，煎汤洗。\n
        服用禁忌：脾胃虚寒者慎服。
        ''')
    elif source2_index == 68:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\路路通.jpg')
        st.image(image, caption='路路通')
        st.markdown('''
        中文名：路路通\n
        拼音：lu lu tong\n
        性状：果序圆球形，直径2~3cm。表面灰棕色至棕褐色，有多数尖刺状宿存萼齿及鸟嘴状花柱，常折断或弯曲，除去后则现多数蜂窝小孔；基部有圆柱形果柄，长3~4.5cm，常折断或仅具果柄痕。小蒴果顶部开裂形成空洞状，可见种子多数，发育不完全者细小，多角形，直径约1mm，黄棕色亚棕褐色，发育完全者少 数，扁平长圆形，具翅，褐色。体轻，质硬，不易破开。气微香,味淡。以个大、色黄、无泥、无果柄者为佳。\n
        功能主治：祛风通络，利水除湿。治肢体痹痛，手足拘挛，胃痛，水肿，胀满，经闭，乳少，痈疽，痔漏，疥癣，湿疹。\n
        性味：苦；平\n
        用法用量：内服：煎汤；3~10g；或煅存性研末服。外用：适量，研末敷；或烧烟闻嗅。\n
        服用禁忌：孕妇忌服。
        ''')
    elif source2_index == 69:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\麻黄.jpg')
        st.image(image, caption='麻黄')
        st.markdown('''
        中文名：麻黄\n
        拼音：ma huang\n
        性状：茎呈细长圆柱形而微扁，少分枝，直径约1～2毫米，通常切成长约2～3厘米的小段。表面淡绿色至黄绿色，有细纵走棱线，手触之微有粗糙感，节 明显，节间长2.5～6厘米。节上有膜质鳞叶2片（稀3片），长约3～4毫米，上部灰白色，锐长，三角形，尖端反曲，基部棕红色，连合成筒状。茎质脆，易 折断，断面略纤维性，外圈为绿黄色，中央髓部呈红棕色。\n
        功能主治：发汗，平喘，利水。治伤寒表实，发热恶寒无汗、头痛鼻塞、骨节疼痛；咳嗽气喘；风水浮肿，小便不利；风邪顽痹，皮肤不仁，风疹瘙痒。\n
        性味：辛、微苦，温。\n
        用法用量：内服：煎汤，1.5~10g；或入丸、散。外用：适量，研末(口搐)鼻或研末敷。生用：发汗力强，发汗，利水用之；炙用：发汗力弱，密炙兼能润肺，止咳平喘多用。\n
        服用禁忌：凡素体虚弱而自汗、盗汗、气喘者，均忌服。
        ''')
    elif source2_index == 70:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\麦冬.jpg')
        st.image(image, caption='麦冬')
        st.markdown('''
        中文名：麦冬\n
        拼音：mai dong\n
        性状：本品呈纺锤形，两端略尖，长1.5～3cm，直径0.3～0.6cm。表面黄白色或淡黄色，有细纵纹。质柔韧，断面黄白色，半透明，中柱细小。气微香，味甘、微苦。\n
        功能主治：养阴润肺，清心除烦，益胃生津。治肺燥干咳，吐血，咯血，肺痿，肺痈，虚劳烦热，消渴，热病津伤，咽干口燥，便秘。\n
        性味：甘，微苦，微寒。\n
        用法用量：内服：煎汤，6~15g；或入丸、散、膏。外用：适量，研末调敷；煎汤涂；或鲜品捣汁搽。\n
        服用禁忌：凡脾胃虚寒泄泻，胃有痰饮湿浊及暴感风寒咳嗽者均忌服。
        ''')
    elif source2_index == 71:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\牛蒡子.jpg')
        st.image(image, caption='牛蒡子')
        st.markdown('''
        中文名：牛蒡子\n
        拼音：niu bang zi\n
        性状：瘦果呈长扁卵形，长约6毫米，中部直径约3毫米。外皮灰褐色，有数条微突起的纵纹，中间一条较明显，全体有稀疏的斑点，又似致密的网纹.一端略窄，微弯曲，顶上有一浅色小点；另一端钝圆，稍宽，有一小凹窝。纵面稍隆起，边缘光圆而厚。外皮较坚硬，破开后种仁两瓣，灰白色，富有油性。无臭，味微苦。以粒大、饱满、外皮灰褐色者佳。\n
        功能主治：疏散风热，宣肺透疹，消肿解毒。治风热咳嗽，咽喉肿痛，斑疹不透，风疹作痒，痈肿疮毒。\n
        性味：辛苦，凉。\n
        用法用量：内服：煎汤，5~10g；或入散剂。外用：适量，煎汤含漱。\n
        服用禁忌：《本草经疏》：若气虚色白大便自利或泄泻者，慎勿服之；痈疽已溃，非便秘不宜服。
        ''')
    elif source2_index == 72:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\羌活.jpg')
        st.image(image, caption='羌活')
        st.markdown('''
        中文名：羌活\n
        拼音：qiang huo\n
        性状：为圆柱形略弯曲的根茎，长4~13cm，直径0.6~2.5cm。顶端具茎痕。表面棕褐色至黑褐色，外皮脱落处呈黄色。节间缩短，呈紧密隆起的环状，形似蚕（习称蚕羌）；或节是延长，形如竹节状（习称竹节羌）。节上有多数点状或瘤状突起的根良及色破碎鳞片。体轻，质脆，易折断。断面不平整，有多数裂隙，皮部黄棕色至暗棕色，油润，有棕色油点，木部黄白色，射线明显，髓部黄色至黄棕色。\n
        功能主治：散表寒，祛风湿，利关节。治感冒风寒，头痛无汗，风寒湿痹，项强筋急，骨节酸疼，风水浮肿，痈疽疮毒。用于阳痿遗精，遗尿尿频，腰膝冷痛，肾虚作喘，五更泄泻；外用治白癜风，斑秃。\n
        性味：辛苦，温。\n
        用法用量：内服：煎汤，3~10g；或入丸、散。\n
        服用禁忌：血虚痹痛忌服。
        ''')
    elif source2_index == 73:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\千年健.jpg')
        st.image(image, caption='千年健')
        st.markdown('''
        中文名：千年健\n
        拼音：qian nian jian\n
        性状：干燥根茎呈长圆柱形，弯曲，长短不等，通常长约40厘米，直径6～8毫米，棕红色或棕黄色，表面粗糙，有多数扭曲的深纵沟纹及黄白色的针状突出物，沟纹成层排列，每层长约1.5厘米，末端即成针刺突出。质脆，易折断，折断面不平，树脂样，有很多粗韧的针状纤维群，并散布去除纤维后所留下的针眼状小孔。横切面淡棕色至棕红色，纤维群成黄色点状散列。气芳香，久闻有不悦感，味微辛辣。以棕红色、条祖、香浓者为佳。\n
        功能主治：祛风湿，壮筋骨，消肿止痛。治风湿痹痛，肢节酸痛，筋骨痿软，胃痛，痈疽疮肿。\n
        性味：味苦；辛；性温；小毒\n
        用法用量：内服：煎汤，9~15g；或浸酒。外用：适量，研末，调敷。\n
        服用禁忌：①《柑园小识》：忌莱菔。\n
        ②《饮片新参》：阴虚内热者慎用。
        ''')
    elif source2_index == 74:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\青蒿.jpg')
        st.image(image, caption='青蒿')
        st.markdown('''
        中文名：青蒿\n
        拼音：qing hao\n
        性状：茎圆柱形，上部多分枝，长30~80cm，直径0.2~0.6cm，表面黄绿色或棕黄色，具纵棱线；质略硬，易折断，断面中部有髓。叶互生，暗绿色或棕绿 色，卷缩，碎，完整者展平后为三回羽状深裂，裂片及小裂片矩圆形或长椭圆形，两面被短毛。气香特异，味微苦。以色绿、叶多、香气浓者为佳。\n
        功能主治：清热，解暑，除蒸，截疟。治温病，暑热，骨蒸劳热，疟疾，痢疾，黄疸，疥疮，瘙痒。\n
        性味：味苦；微辛；性寒\n
        用法用量：内服：煎汤，6~15g，治疟疾可用20~40g，不宜久煎；鲜品用量加倍，水浸绞汁饮；或入丸、散。外用：适量，研末调敷；或鲜品捣敷；或煎水洗。\n
        服用禁忌：1.《本草经疏》：产后血虚，内寒作泻，及饮食停滞泄泻者，勿用。凡产后脾胃薄弱。\n
        2.《本草通玄》：胃虚者，不敢投也。
        ''')
    elif source2_index == 75:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\秦皮.jpg')
        st.image(image, caption='秦皮')
        st.markdown('''
        中文名：秦皮\n
        拼音：qin pi\n
        性状：为长条状块片，厚3～6mm。外表面灰棕色，具龟裂状沟纹及红棕色圆形或横长的皮孔。质坚硬，断面纤维性较强。\n
        功能主治：清热燥湿，平喘止咳，明目。治细菌性痢疾，肠炎，白带，慢性气管炎，目赤肿痛，迎风流泪，牛皮癣。\n
        性味：苦，寒。\n
        用法用量：内服：煎汤，6～12克；或入丸剂。外用：煎水洗。\n
        服用禁忌：脾胃虚寒者忌服。
       ''')
    elif source2_index == 76:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\忍冬藤.jpg')
        st.image(image, caption='忍冬藤')
        st.markdown('''
        中文名：忍冬藤\n
        拼音：ren dong teng\n
        性状：本品常捆成束或卷成团。茎枝长圆本形，多分枝，直径1.5~6mm，节间长3~6cm，有殖叶及叶痕。表面棕红色或暗棕色，有细 纵纹，老枝光滑，细枝有淡黄色毛茸；外皮易剥落露出灰白色同皮。质硬脆，易折断，断面黄白色，中心空洞。气微，老枝味微苦，嫩枝味淡。以表面色棕红、质嫩 者为佳。\n
        功能主治：清热，解毒，通络。治温病发热，热毒血痢，传染性肝炎，痈肿疮毒，筋骨疼痛。\n
        性味：味甘；性寒\n
        用法用量：内服：煎汤，10~30g；或入丸、散；或浸酒。外用：适量，煎水熏洗，或熬膏贴，或研末调敷衍，赤可用鲜品捣敷。\n
        服用禁忌：脾胃虚寒，泄泻不止者禁用。
        ''')
    elif source2_index == 77:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\人参.jpg')
        st.image(image, caption='人参')
        st.markdown('''
        中文名：人参\n
        拼音：ren shen\n
        性状：\n
        功能主治：大补元气，固脱生津，安神。治劳伤虚损，食少，倦怠，反胃吐食，大便滑泄，虚咳喘促，自汗暴脱，惊悸，健忘，眩晕头痛，阳痿，尿频，消渴，妇女崩漏，小儿慢惊，及久虚不复，一切气血津液不足之证。\n
        性味：甘微苦，温。\n
        用法用量：3～9g，另煎兑入汤剂服；野山参若研粉吞服，一次2g，一日2次。不宜与藜芦同用。\n
        服用禁忌：实证、热证忌服。
        ''')
    elif source2_index == 78:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\肉豆蔻.jpg')
        st.image(image, caption='肉豆蔻')
        st.markdown('''
        中文名：肉豆蔻\n
        拼音：rou dou kou\n
        性状：种仁卵圆形或椭圆形，长2~3.5cm，宽1.5~2.5cm。表面灰棕色至暗棕色，有网状沟纹，常被有白色石灰 粉；宽端有浅色圆形隆起（种脐的部位）。狭端有暗色下陷处（合点的部位），两端间有明显的纵沟（种脊的部位）。质坚硬，难破碎，碎断面可见棕黄或暗棕色外 胚乳向内伸入，与类白色的内胚乳交错，形成大理石样纹理。纵切时可见宽端有小形腔隙，内藏小型干缩的胚，子叶卷曲。气强烈芳香，味辛辣、微苦。以个大、体 重、坚实、破开后香气浓者为佳。\n
        功能主治：温中行气，消食，涩肠止泻。用于心腹胀痛，虚泻，冷痢，呕吐，宿食不消，食少呕吐。\n
        性味：辛；苦；温\n
        用法用量：内服：煎汤，1.5~6g；或入丸、散。\n
        服用禁忌：①《雷公炮炙论》：凡使，勿令犯铜。\n
        ②《本草经疏》：大肠素有火热及中暑热泄暴注，肠风下血，胃火齿痛及湿热积滞方盛，滞下初起，皆不宜服。
        ''')
    elif source2_index == 79:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\桑寄生.jpg')
        st.image(image, caption='桑寄生')
        st.markdown('''
        中文名：桑寄生\n
        拼音：sang ji sheng\n
        性状：带叶茎枝圆柱形，有分枝，长30~40cm，粗枝直径0.5~1cm，细枝或枝梢直径2~3mm。表面粗糙，嫩枝顶端被有锈色毛绒，红褐色或灰褐色，有多数圆点状、黄褐色或灰黄色皮孔和纵向细皱纹，粗枝表面红褐色或灰褐色，有突起的枝痕和叶痕。质坚脆，易折断，断面不平坦，皮部薄，深棕褐色，易与木部分离；木部宽阔，几占茎的大部，淡红棕色；髓射线明显，放射状；髓部小形，色稍深。叶易脱落，仅少数残留茎上，叶片常卷缩、破碎，完整者卵圆形至长卵形，长3~6cm，宽2.5~4cm，先端钝圆，基部圆形成宽楔形，茶褐色或黄褐色，全缘，侧脉3-4对，略明显，幼叶有锈色绒毛，近革质而脆，易破碎；叶柄长 0.5~1cm。花、果常脱落；花蕾管状，稍弯，顶部卵圆形，被锈色绒毛；浆果长间形，红褐色，密生小瘤体。气微，味淡、微涩以枝细、质嫩。红褐色、叶多者为佳。\n
        功能主治：补肝肾，强筋骨，除风湿，通经络，益血，安胎。治腰膝酸痛，筋骨痿弱，偏枯，脚气，风寒湿痹，胎漏血崩，产后乳汁不下。\n
        性味：苦；甘；性平\n
        用法用量：内服：煎汤，10~15g；或入丸、散；或浸酒；或捣汁服。外用：适量，捣烂外敷。\n
        服用禁忌：
        ''')
    elif source2_index == 80:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\桑螵蛸.jpg')
        st.image(image, caption='桑螵蛸')
        st.markdown('''
        中文名：桑螵蛸\n
        拼音：sang piao shao\n
        性状：1.团螵蛸：略呈圆柱形或半圆形，由多层膜状薄片叠成，长2.5～4cm，宽2～3cm。表面浅黄褐色，上面带状隆起不明显，底面平坦或有凹沟。体轻，质松而 韧，横断面可见外层为海绵状，内层为许多放射状排列的小室，室内各有一细小椭圆形卵，深棕色，有光泽。气微腥，味淡或微咸。\n
        2.长螵蛸：略呈长条形，一端较细，长2.5～5cm，宽1～1.5cm。表面灰黄色，上面带状隆起明显，带的两侧各有一条暗棕色浅沟及斜向纹理。质硬而脆。\n
        3.黑螵蛸：略呈平行四边形，长2～4cm，宽1.5～2cm。表面灰褐色，上面带状隆起明显，两侧有斜向纹理，近尾端微向上翘。质硬而韧。\n
        功能主治：补肾助阳，固精缩尿。治肾虚遗精，白浊，小便频数，遗尿，赤白带下，阳痿，早泄。\n
        性味：甘、咸，平。\n
        用法用量：内服：煎汤，5~10g；研末，3~5g；或入丸剂。外用：适量，研末撒或油调敷。\n
        服用禁忌：阴虚火旺或膀胱有热者慎服。
        ''')
    elif source2_index == 81:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\桑葚.jpg')
        st.image(image, caption='桑葚')
        st.markdown('''
        中文名：桑葚\n
        拼音：sang shen\n
        性状：干燥果穗呈长圆形，长1～2厘米，直径6～10毫米。基部具柄，长1～1.5厘米。表面紫红色或紫黑色。果穗由30～60个瘦果聚合而成；瘦果卵圆形，稍 扁，长2～5毫米，外具膜质苞片4枚。胚乳白色。质油润，富有糖性。气微，味微酸而甜。以个大、肉厚、紫红色、糖性大者为佳。\n
        功能主治：滋阴养血，生津，润肠。主肝肾不足和血虚精亏的头晕目眩，腰酸耳鸣，须发早白，失眠多梦，津伤口渴，消渴，肠燥便秘。\n
        性味：甘、酸，寒。\n
        用法用量：内服：煎汤，10～15g；或熬膏、浸酒、生啖；或入九、散。外用：适量，浸水洗。\n
        服用禁忌：脾胃虚寒便溏者禁服。
        ''')
    elif source2_index == 82:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\山慈菇.jpg')
        st.image(image, caption='山慈菇')
        st.markdown('''
        中文名：山慈菇\n
        拼音：shan ci gu\n
        性状：毛慈菇：呈不规则扁球形或圆锥形，顶端渐突起，基部有须根痕。长1.8～3cm，膨大部直径1～2cm。表面黄棕色或棕褐色，有纵皱纹或纵沟，中部有2～3 条微突起的环节，节上有鳞片叶干枯腐烂后留下的丝状纤维。质坚硬，难折断，断面灰白色或黄白色，略呈角质。气微，味淡，带黏性。\n
        功能主治：消肿，散结，化痰，解毒。治痈疽疔肿，瘰疬，喉痹肿痛，蛇、虫、狂犬伤。\n
        性味：味甘；微辛；性寒；小毒\n
        用法用量：内服：煎汤，3~6g；或磨汁；或入丸、散。外用：适量，磨汁涂；或研末调敷。\n
        服用禁忌：正虚体弱患者慎服。
        ''')
    elif source2_index == 83:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\山奈.jpg')
        st.image(image, caption='山奈')
        st.markdown('''
        中文名：山奈 又名：沙姜\n
        拼音：shan nai\n
        功能主治：行气止痛、健脾和胃、促进消化、治疗胃寒、心腹冷痛、治疗牙痛。\n
        性味：辛\n
        用法用量：\n
        服用禁忌：婴儿应少吃沙姜，因为沙姜辣味比较重，对肠胃有一定的刺激作用。更要警惕的是，阴虚血亏人群不宜食用沙姜，会使体质更加虚弱;如果是肝气郁结所致的内火旺人群，也不宜食用沙姜，容易产生口感、咽痛、便秘等上火症状。\n
        ''')
    elif source2_index == 84:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\山药.jpg')
        st.image(image, caption='山药')
        st.markdown('''
        中文名：山药\n
        拼音：shan yao\n
        性状：（1）毛山药 略呈圆柱形，稍扁而弯曲，长15~30cm，直径1.5~6cm。表面黄白色或浅棕黄色，有明显纵皱及栓皮未除尽的痕迹，并可见少数须根痕，两头不整齐。质坚实，不易折断，断面白色，颗粒状，粉性，散有浅棕黄色点状物。无臭，味甘，微酸，嚼之发粘。\n
       （2）光山药 呈圆柱形，两端齐平，长7~16cm，直径1.5~3cm，粗细均匀，挺直。表面光滑，洁白，粉性足。均以条粗、质坚实、粉性足、色洁白者为佳。\n
        功能主治：补脾养胃，生津益肺，补肾涩精。用于脾虚食少、久泻不止、肺虚喘咳、肾虚遗精、白带过多、尿频、虚热消渴。\n
        性味：甘；平\n
        用法用量：内服：煎汤，15~30g，大剂量60~250g；或入丸、散。外用：适量，捣敷。补阴，宜生用；健脾止泻，宜炒黄用。\n
        服用禁忌：有实邪者忌服。
        ''')
    elif source2_index == 85:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\沙苑子.jpg')
        st.image(image, caption='沙苑子')
        st.markdown('''
        中文名：沙苑子\n
        拼音：sha yuan zi\n
        性状：①扁茎黄芪的干燥种子呈肾脏形而稍扁，长约2毫米，宽约1.5毫米，厚不足1毫米。表面灰褐色或绿褐色，光滑。一边微向内凹陷。在凹入处有明显的种脐。质坚 硬不易破碎。子叶2枚淡黄色，略为椭圆形，胚根弯曲。无臭，味淡，嚼之有豆腥气。以饱满、均匀者为佳。 主产陕西、山西等地.\n
        ②华黄芪的干燥种子呈较规则的肾形，颗粒饱满，长2～2.8毫米，宽1.8～2毫米。表面暗绿色或棕绿色，光滑。腹面中央微凹陷处有种脐。质坚硬，不易破碎。气微，味淡。 主产河北。\n
        功能主治：补肝，益肾，明目，固精。治肝肾不足，腰膝酸痛，目昏，遗精早泄，小便频数，遗尿，尿血，白带。\n
        性味：甘，温。\n
        用法用量：内服，煎汤，9~15克。或入丸、散。\n
        服用禁忌：相火炽盛，阳强易举者忌服。
        ''')
    elif source2_index == 86:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\射干.jpg')
        st.image(image, caption='射干')
        st.markdown('''
        中文名：射干\n
        拼音：she gan\n
        性状：本品呈不规则结节状，长3～10cm，直径1～2cm。表面黄褐色、棕褐色或黑褐色，皱缩，有较密的环纹。上面有数个圆盘状凹陷的茎痕，偶有茎基残存；下面有残留细根及根痕。质硬，断面黄色，颗粒性。气微，味苦、微辛。\n
        功能主治：降火，解毒，散血，消痰。治喉痹咽痛，咳逆上气，痰涎壅盛，瘰疬结核，疟母，妇女经闭，痈肿疮毒。\n
        性味：苦，寒，有毒。\n
        用法用量：内服：煎汤，5~10g；入丸、散；或鲜品捣汁。外用：适量，或研末吹喉；或捣烂敷。\n
        服用禁忌：无实火及脾虚便溏者不宜。孕妇忌服。
        ''')
    elif source2_index == 87:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\鸡内金.jpg')
        st.image(image, caption='鸡内金')
        st.markdown('''
        中文名：鸡内金\n
        拼音：sheng ji nei jin\n
        性状：为不规则的长椭圆形的片状物，有明显的波浪式皱纹，长约5厘米，宽约3厘米，表面金黄色、黄褐色或黄绿色，老鸡的鸡内金则微黑。质薄脆，易折断，断面呈胶质状，有光泽。气微腥，味淡微苦。以干燥、完整、个大、色黄者为佳。\n
        功能主治：健胃消食，涩精止遗。治食积胀满，呕吐反胃，泻痢，疳积，消渴，遗溺，喉痹乳蛾，牙疳口疮。\n
        性味：味甘；性平\n
        用法用量：内服：煎汤，3~10g；研末，每次1.5~3g；或入丸、散。外用：适量，研末调敷或生贴。\n
        服用禁忌：脾虚无积者慎服。
        ''')
    elif source2_index == 88:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\瓦楞子.jpg')
        st.image(image, caption='瓦楞子')
        st.markdown('''
        中文名：瓦楞子\n
        拼音：sheng wa leng zi\n
        性状：毛蚶：略呈三角形或扇形，长4～5cm，高3～4cm。壳外面隆起，有棕褐色茸毛或已脱落；壳顶突出，向内卷曲；自壳顶至腹面有延伸的放射肋30～34条。壳内面平滑，白色，壳缘有与壳外面直楞相对应的凹陷，铰合部具小齿1列。质坚。无臭，味淡。\n
        泥蚶：长2.5～4cm，高2～3cm。壳外面无棕褐色茸毛，放射肋18～21条，肋上有颗粒状突起。\n
        魁蚶：长7～9cm，高6～8cm。壳外面放射肋42～48条。\n
        功能主治：化痰，软坚，散瘀，消积。治痰积，胃痛，嘈杂，吐酸，癥瘕，瘰疬，牙疳。\n
        性味：咸，平。\n
        用法用量：内服：煎汤，9~15g，宜打碎行煎；研末，每次1~3g；或入丸、散。外用：适量，煅后研末调敷。\n
        服用禁忌：
        ''')
    elif source2_index == 89:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\石榴皮.jpg')
        st.image(image, caption='石榴皮')
        st.markdown('''
        中文名：石榴皮\n
        拼音：shi liu pi\n
        性状：果皮半圆形或不规则块片，大小不一，厚1.5~3mm。外表面黄棕色、暗红色或棕红色，稍具光泽，粗糙，有棕色小点，有的有突起的筒状宿萼或粗短果柄。内表面黄色或红棕色，有种子脱落后的凹窝，呈网状隆起。质硬而脆，断面黄色，略显颗粒状。气微，味苦涩。以皮厚、棕红色者为佳。\n
        功能主治：涩肠，止血，驱虫。治久泻，久痢，便血，脱肛，滑精，崩漏，带下，虫积腹痛，疥癣。\n
        性味：味酸；涩；性温；小毒\n
        用法用量：内服：煎汤，3~10g；或入丸、散。外用：适量，煎水熏洗，研末撒或调敷。\n
        服用禁忌：《本草从新》：能恋膈成痰，痢积未尽者，服之太早，反为害也。
        ''')
    elif source2_index == 90:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\丝瓜络.jpg')
        st.image(image, caption='丝瓜络')
        st.markdown('''
        中文名：丝瓜络\n
        拼音：si gua luo\n
        性状：丝状维管束纵横交织而成的细密坚韧的网络状物。全体呈压扁的长圆筒状或长棱形，两端细，略弯曲，长25～70厘米，直径5～10厘米，表面黄白色至暗黄色，有时残存果皮及膜状的果肉，体轻，质韧，富弹性，难折断，横切面可见子房3室，空洞状，偶有残留种子。气无，味淡。\n
        功能主治：活血、通络、祛风。属活血化瘀药下分类的活血止痛药。\n
        性味：性平，味甘。\n
        用法用量：用量3～12克。用治各种原因引起的气血瘀滞、脉络不通的胸胁疼痛、腹痛、腰痛、睾丸疼痛、妇人经痛、乳汁不通等；肺热咳嗽、痔瘘、崩漏等。\n
        服用禁忌：脾胃虚寒者少用丝瓜络。
        ''')
    elif source2_index == 91:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\酸枣仁.jpg')
        st.image(image, caption='酸枣仁')
        st.markdown('''
        中文名：酸枣仁\n
        拼音：suan zao ren\n
        性状：种子扁圆形或扁椭圆形，长5~9mm，宽5~7mm，厚约3mm。表面紫红色或紫褐色，平滑有光泽，有的具纵裂纹。一面较平坦，中间有1条隆起的纵线纹；另一面稍凸起。一端凹陷，可见线形种脐；另端有细小凸起的合点。种皮较脆，胚乳白色，子叶2，浅黄色，富油性。气微、味淡。以粒大、饱满、有光泽、外皮红棕 色、种仁色黄白者为佳。\n
        功能主治：养肝，宁心，安神，敛汗。治虚烦不眠，惊悸怔忡，烦渴，虚汗。\n
        性味：甘；平\n
        用法用量：内服：煎汤，6~15g；研末，每次3~5g；或入丸、散。\n
        服用禁忌：凡有实邪郁火及患有滑泄症者慎服。
        ''')
    elif source2_index == 92:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\苏木.jpg')
        st.image(image, caption='苏木')
        st.markdown('''
        中文名：苏木\n
        拼音：su mu\n
        性状：干燥心材呈圆柱形，有的连接根部，呈不规则稍弯曲的长条状，长8～100厘米，直径3～10厘米。表面暗棕色或黄棕色，可见红黄色 相间的纵走条纹，有刀削痕及细小的凹入油孔。横断面有显著的年轮，有时中央可见黄白色的髓，并具点状闪光。质致密，坚硬而重，无臭，味微涩。将本品投入热水中，水染成鲜艳的桃红色，加醋则变为黄色，再加碱又变为红色。以粗大、坚实、色红黄者为佳。苏木刨片为不规则的长条形，厚约0.5毫米，宽狭不一，通常宽约1厘米左右，全体呈红黄色或黄棕色，少数带有黄白色的边材；表面有纵纹。质脆，易断。\n
        功能主治：行血，破瘀，消肿，止痛。治妇人血气心腹痛，经闭，产后瘀血胀痛喘急，痢疾，破伤风，痈肿，扑损瘀滞作痛。\n
        性味：甘、咸，平。\n
        用法用量：内服：煎汤，3~9g,或研末。外用：适量，研末撒。\n
        服用禁忌：1.血虚无瘀者不宜，孕妇忌服。\n
        2.《本草纲目》：忌铁。\n
        3.《本草经疏》：产后恶露已净，由血虚腹痛者不宜用。\n
        4.《本经逢原》：大便不实者禁用。
        ''')
    elif source2_index == 93:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\太子参.jpg')
        st.image(image, caption='太子参')
        st.markdown('''
        中文名：太子参\n
        拼音：tai zi shen\n
        性状：干燥块根呈细长条形或长纺锤形，长约2～6厘米；直径约3～6毫米左右。表面黄白色，半透明，有细皱纹及凹下的须根痕，根头钝圆，其上常有残存的茎痕，下端渐细如鼠尾。质脆易折断，断面黄白色而亮，直接晒干的断面为白色，有粉性。气微，味微甘。以肥润、黄白色、无须根者为佳。\n
        功能主治：益气健脾，生津润肺。用于脾虚体倦，食欲不振，病后虚弱，气阴不足，自汗口渴，肺燥干咳。\n
        性味：甘苦，微温。\n
        用法用量：内服：煎汤，9～30g。\n
        服用禁忌：表实邪盛者不宜用。
        ''')
    elif source2_index == 94:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\天花粉.jpg')
        st.image(image, caption='天花粉')
        st.markdown('''
        中文名：天花粉\n
        拼音：tian hua fen\n
        性状：干燥根呈不规则的圆柱形，长5～10厘米，直径2～5厘米，表面黄白色至淡棕色，皱缩不平，具有陷下的细根痕迹。质结实而重，粉质，不易折断。纵剖面白色，有黄色条状的维管束；横断面白色，散有淡棕色导管群条痕。气微，味淡后微苦。以色洁白、粉性足、质细嫩、体肥满者为佳；色棕、纤维多者为次。以河南产量大、质量优，习称安阳花粉。\n
        功能主治：生津，止渴，降火，润燥，排脓，消肿。治热病口渴，消渴，黄疸，肺燥咳血，痈肿，痔瘘。\n
        性味：甘苦酸，凉。\n
        用法用量：内服：煎汤，9~15g；或入丸、散。外用：适量，研末撒布或调敷。\n
        服用禁忌：脾胃虚寒大便滑泄者忌服。
        ''')
    elif source2_index == 95:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\天麻.jpg')
        st.image(image, caption='天麻')
        st.markdown('''
        中文名：天麻\n
        拼音：tian ma\n
        性状：干燥根茎为长椭圆形，略扁，皱缩而弯曲，一端有残留茎基，红色或棕红色，俗称鹦哥嘴，另一端有圆形的根痕，长6～10厘米，直径2～5厘米，厚0.9～2厘米。表面黄白色或淡黄棕色，半透明，常有浅色片状的外皮残留，多纵皱，并可见数行不甚明显的须根痕排列成环。冬麻皱纹细而少，春麻皱纹粗大。质坚硬，不易折断。断面略平坦，角质，黄白色或淡棕色，有光泽。嚼之发脆，有粘性。气特异，味甘。以色黄白、半透明、肥大坚实者为佳。色灰褐、外皮未去净、体轻、断面 中空者为次。\n
        功能主治：息风止痉，平肝阳；祛风通络。主急慢惊风，抽搐拘挛，眩晕，头痛，半身不遂，肢麻，风湿痹痛。\n
        性味：甘，平。\n
        用法用量：内服：煎汤，3~10g；或入丸、散、研末吞服，每次1~1.5g。\n
        服用禁忌：《雷公炮炙论》：使御风草根，勿使天麻，二件若同用，即令人有肠结之患。 气血虚甚者慎服。
        ''')
    elif source2_index == 96:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\土荆皮.jpg')
        st.image(image, caption='土荆皮')
        st.markdown('''
        中文名：土荆皮\n
        拼音：tu jing pi\n
        性状：①根皮:呈不规则的长条块片状，长短大小不一，扭曲而稍卷，厚约3～6毫米。外表面粗糙有皱纹及横向灰白色皮孔。木栓灰黄色，常呈鳞片状剥落，显出红棕色皮部。内表面红棕色或黄白色，较平坦，有纵向纹理。质脆，易断，断面红褐色，外皮颗粒性，内皮纤维性。气微弱，味苦而涩。\n
        ②树皮:大多呈条状或片状，厚约1厘米，外表暗棕色，作龟裂状，外皮甚厚；内表面较根皮为祖糙。以形大、黄褐色、有纤维质而无栓皮者为佳。\n
        功能主治：祛风除湿；杀虫止痒。。用于疥癣瘙痒。《药材资料汇编》：治癣疥。\n
        性味：辛，温；有毒。\n
        用法用量：外用适量，醋或酒浸涂擦，或研末调涂患处。\n
        服用禁忌：
        ''')
    elif source2_index == 97:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\五加皮.jpg')
        st.image(image, caption='五加皮')
        st.markdown('''
        中文名：五加皮\n
        拼音：wu jia pi\n
        性状：本品呈不规则卷筒状，长5～15cm，直径0.4～1.4cm，厚约0.2cm。外表面灰褐色，有稍扭曲的纵皱纹及横长皮孔；内表面淡黄色或灰黄色，有细纵纹。体轻，质脆，易折断，断面不整齐，灰白色。气微香，味微辣而苦。\n
        功能主治：祛风湿，壮筋骨，活血去瘀。治风寒湿痹，筋骨挛急，腰痛，阳痿，脚弱，小儿行迟，水肿，脚气，疮疽肿毒，跌打劳伤。\n
        性味：辛、苦，温。\n
        用法用量：内服：煎汤，6~9g，鲜品加倍；浸酒或入丸、散。外用：适量，煎水熏洗或为末敷。\n
        服用禁忌：阴虚火旺者慎服。
        ''')
    elif source2_index == 98:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\杏仁.jpg')
        st.image(image, caption='杏仁')
        st.markdown('''
        中文名：杏仁\n
        拼音：xing ren\n
        性状：\n
        功能主治：止咳平喘、润肠通便，可治疗肺病、咳嗽等疾病。\n
        性味：苦；温；有毒\n
        用法用量：内服：煎汤，3-10g；或入丸、散。外用：捣敷。\n
        服用禁忌：阴虚咳嗽及大便溏泄者忌服。
        ''')
    elif source2_index == 99:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\细辛.jpg')
        st.image(image, caption='细辛')
        st.markdown('''
        中文名：细辛\n
        拼音：xi xin\n
        性状：根茎细长,长5~15cm，直径1~3mm，节间长0.2~1cm；叶片较薄，心形。气味较弱。\n
        功能主治：祛风，散寒，行水，开窍。治风冷头痛，鼻渊，齿痛，痰饮咳逆，风湿痹痛。\n
        性味：辛；温；小毒\n
        用法用量：内服：煎汤，1.5~9g；研末，1~3g。 外用：适量，研末吹鼻、塞耳、敷脐；或煎水含漱。\n
        服用禁忌：气虚多汗，血虚头痛，阴虚咳嗽等忌服。
        ''')
    elif source2_index == 100:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\银柴胡.jpg')
        st.image(image, caption='银柴胡')
        st.markdown('''
        中文名：银柴胡\n
        拼音：yin chai hu\n
        性状：干燥的根呈圆柱形，长15～40厘米，直径1～2.5厘米。根头顶瑞有多数细小疣状突起，为地上茎痕，密集而发白，习称珍珠盘。下端略细，少数有分歧。表面 黄棕或带灰棕色，有扭曲的纵纹及支根痕，并可见多数圆形小孔，习称沙眼，近根头处尤多，自此处折断，断面有棕色花纹。质松脆，折断时有粉尘飞出，断面粗 糙，有空隙，中有大形黄白色相间的放射状花纹。气微，味甘、微苦。以条长、外皮淡黄棕色、断面黄白色者为佳。\n
        功能主治：清虚热，除疳热。治虚劳骨蒸，阴虚久疟，小儿疳热羸瘦。\n
        性味：甘；性微寒\n
        用法用量：内服：煎汤，5~9g；或入丸、散。\n
        服用禁忌：外感风寒及血虚无热者忌服。
        ''')
    elif source2_index == 101:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\薏仁.jpg')
        st.image(image, caption='薏仁')
        st.markdown('''
        中文名：薏仁\n
        拼音：yi ren\n
        性状：长圆形，长5-8毫米，宽4-6毫米，厚3-4毫米，腹面具宽沟，基部有棕色种脐，质地粉性坚实，白色或黄白色。\n
        功能主治：利水渗湿，健脾止泻，除痹，排脓，解毒散结。用于水肿，脚气，小便不利，脾虚泄泻，湿痹拘挛，肺痈，肠痈，赘疣，癌肿。\n
        性味：甘、淡，凉。\n
        用法用量：9～30g\n
        服用禁忌：孕妇慎用。
        ''')
    elif source2_index == 102:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\郁金.jpg')
        st.image(image, caption='郁金')
        st.markdown('''
        中文名：郁金\n
        拼音：yv jin\n
        性状：①黄郁金:又名：黄丝郁金、广玉金。为植物姜黄的干燥块根，呈卵圆形或长卵圆形，两端稍尖，中部微满，长2～4厘米，中部直径1～2厘米。表面灰黄色或淡棕色，有灰白色细皱纹及凹下的小点，一端显折断的痕迹，呈鲜黄色，另一端稍尖。质坚实，横断面平坦光亮，呈角质状，杏黄色或橙黄色，中部有一颜色较浅的圆心。微有姜香 气，味辛而苦。以个大、肥满、外皮皱纹细、断面橙黄色者为佳。主产四川。\n
        ②黑郁金:又名：温郁金、川玉金。为植物郁金的干燥 块根。长纺锤形，稍扁，多弯曲，两端钝尖，有折断痕而呈灰黑色，长3～6厘米，中部直径1～1.5厘米。表面灰褐色，外皮皱缩或有细皱纹。横断面暗灰色发亮，中部有l条颜色较浅的环纹，中心扁圆形。气无，味淡而辛凉。以个大、外皮少皱缩、断面灰黑色者为佳。主产浙江。\n
        ③白丝郁金:亦为植物郁金的干燥块根。外形较黄郁金瘦长。断面内心呈白色（姜黄色素含量较少），内圈与外层之间有1条黄白色的环纹，质地模糊不透明。味微辛，香气亦较差。以个大、皮细、断面结实者为佳。主产四川。\n
        ④绿丝郁金:为植物莪术的干燥块根。形状质地同黄郁金，但表皮较粗，断面色暗淡，深浅不一，少透明。味辛而重，香气不显。产四川。\n
        功能主治：行气解郁，活血止痛，利胆退黄。治胸腹胁肋诸痛，失心癫狂，热病神昏，吐血，衄血，尿血，血淋，妇女倒经，黄疸。\n
        性味：味辛；苦；性寒\n
        用法用量：内服：煎汤，3~10g；或入丸散。\n
        服用禁忌：阴虚失血及无气滞血瘀者忌服，孕妇慎服。
        ''')
    elif source2_index == 103:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\浙贝母.jpg')
        st.image(image, caption='浙贝母')
        st.text('''
        中文名：浙贝母\n
        拼音：zhe bei mu\n
        性状：（1）珠贝:为完整的鳞茎，呈扁球形，直径1~2.5cm。表面类白色，外层两枚鳞叶肥厚，对合，内有小鳞叶2~3枚及残茎。质结实而脆，易折断，断面白色，富粉性。气微，味苦。\n
             （2）元宝贝（大贝）:为单瓣肥厚鳞叶，呈元宝形或菱肉形，长2~4cm，高1~2.5cm，厚0.6~1.5cm；外表面类白色至淡黄白色，有淡棕色斑痕，内表类白色至淡黄白色。以鳞叶肥厚、质坚实、粉性足、断面色白者为佳。\n
        功能主治：清热化痰，散结解毒。治风热咳嗽，肺痈喉痹，瘰疬，疮疡肿毒。\n
        性味：味苦；性寒\n
        用法用量：内服：煎汤，3~10g；或入丸、散。外用：适量，研末撒。\n
        服用禁忌：寒痰、湿痰及脾胃虚寒者慎服。反乌头。
        ''')
    elif source2_index == 104:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\枳壳.jpg')
        st.image(image, caption='枳壳')
        st.markdown('''
        中文名：枳壳\n
        拼音：zhi qiao\n
        性状：果实呈半球形，直径3~5.5cm。外皮绿褐色或棕褐色，略粗糙，散有众多小油点，中央有明显的花柱基痕或圆形果柄痕。切面中果皮厚0.6~1.2cm，黄白色较光滑，略向外翻，有维管束散布，边缘有棕黄色油点l~2列。质坚硬，不易折断，瓤囊7~12瓣，少数至15瓣，囊内汁胞干缩，棕黄色或暗棕色，质软，内藏种子。中轴坚实，宽5~9mm，黄白色，有一圈断续环列的维管束点。气香，味苦、微酸。以外果皮色绿褐、果肉厚、质坚硬、香气浓者为佳。\n
        功能主治：破气，行痰，消积。治胸膈痰滞，胸痞，胁胀，食积，噫气，呕逆，下痢后重，脱肛，子宫脱垂。\n
        性味：苦；酸；性微寒\n
        用法用量：内服：煎汤，3~9g；或入丸、散。外用：适量，煎水洗或炒热熨。\n
        服用禁忌：脾胃虚弱及孕妇慎服。
        ''')
    elif source2_index == 105:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\竹茹.jpg')
        st.image(image, caption='竹茹')
        st.markdown('''
        中文名：竹茹\n
        拼音：zhu ru\n
        性状：本品呈不规则的丝状或薄带状，常卷曲扭缩而缠结成团或作创花状，长短不一，宽0.5~0.7cm，厚0.3~0.5cm。全体淡黄白色、浅绿色、青黄色、灰黄色、灰黄绿色、黄而韧，有弹性。气稍清香，味微甜。\n
        功能主治：清热化痰，凉血，除烦止呕。治烦热呕吐、呃逆，痰热咳喘，吐血，衄血，崩漏，恶阻，眙动，惊痫。\n
        性味：甘；微寒\n
        用法用量：内服：煎汤，5~10g；或入丸、散。外用：适量，熬膏贴。\n
        服用禁忌：寒痰咳喘、胃寒呕逆及脾虚泄泻者禁服。
        ''')
    else:
        image = Image.open('C:\\Users\\dongmiaomiao\\Desktop\\web\\猪牙皂.jpg')
        st.image(image, caption='猪牙皂')
        st.markdown('''
        中文名：猪牙皂\n
        拼音：zhu ya zao\n
        性状：干燥荚果呈圆柱形，略扁，弯曲作镰形，长5～10厘米，宽5～12毫米。表面紫棕色或紫黑色，被灰白色粉霜，擦去后有光泽，并有细小的疣状突起及线状裂纹，腹缝线突起呈棱脊状，背缝线突起不显著而有棕黄色纵纹。先端有喙状的花柱残基，基部有果柄残痕。质硬而脆，易折断，断面外层棕黄色，中间黄白色，中心较软，有淡绿或淡棕黄色的丝状物与斜向网纹，纵向剖开可见排列整齐的凹窝，很少见种子。臭微，有刺激性，嗅其粉末则作喷嚏，味先甜后辣。以个小饱满、色紫黑、有光泽、无果柄、质坚硬、肉多而粘、断面淡绿色者为佳。\n
        功能主治：通窍，涤痰，搜风，杀虫。治中风口噤，头风，风痼，喉痹，痰喘，痞满积滞，关格不通，痈肿，疥癞，癣疾，头疮。\n
        性味：辛咸，温，有毒。\n
        用法用量：1～1.5g，多入丸散用。外用适量，研末吹鼻取嚏或研末调敷患处。\n
        服用禁忌：体弱者及孕妇忌服。
        ''')

    #第三个框，处方
    source3 = ('感冒', '发烧')
    # sidebar侧边栏
    source3_index = st.sidebar.radio("处方", range(
        len(source3)), format_func=lambda x: source3[x])
    if source3_index == 0:
        st.write('''
            感冒用药：*********************************

            ''')
