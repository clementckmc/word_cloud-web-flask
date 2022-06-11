import os
import docx2txt
import PyPDF2
import urllib
import jieba
import MeCab
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image

script_dir = os.path.dirname(__file__)
rel_path = "static\\tmp"
UPLOAD_FOLDER = os.path.join(script_dir, rel_path)

# generate word cloud (without mask)
def gen_wc(text, lang):
    if lang == "Jpn":
        stop_words = ["の", "こと", "年", "月", "日"] + list(STOPWORDS)
        cloud = WordCloud(font_path="PATH/FONT_YOU_INTENDED_TO_USE", stopwords=stop_words).generate(text) #TODO
    elif lang == "Chi":
        stop_words = ["的", "在", "於", "及", "年", "月", "日"] + list(STOPWORDS)
        cloud = WordCloud(font_path="PATH/FONT_YOU_INTENDED_TO_USE", stopwords=stop_words).generate(text) #TODO
    else:
        stop_words = ["said", "will"] + list(STOPWORDS)
        cloud = WordCloud(stopwords=stop_words).generate(text)
    os.chdir(UPLOAD_FOLDER) #TODO
    cloud.to_file("output.png")

# generate word cloud (with mask)
def gen_wc_m(text, maskname, lang):
    # get mask
    mask = np.array(Image.open(os.path.join(UPLOAD_FOLDER, maskname))) #TODO

    # get background color
    r = mask[0][0][0]
    g = mask[0][0][1]
    b = mask[0][0][2]

    # generate word cloud
    if lang == "Jpn":
        stop_words = ["の", "こと", "年", "月", "日"] + list(STOPWORDS)
        cloud = WordCloud(mask=mask, background_color= (r, g, b), stopwords=stop_words).generate(text) #TODO
        image_color = ImageColorGenerator(mask)
        cloud.recolor(color_func= image_color)
    elif lang == "Chi":
        stop_words = ["的", "在", "於", "及", "年", "月", "日"] + list(STOPWORDS)
        cloud = WordCloud(mask=mask, background_color= (r, g, b), font_path="PATH/FONT_YOU_INTENDED_TO_USE", stopwords=stop_words).generate(text) #TODO
        image_color = ImageColorGenerator(mask)
        cloud.recolor(color_func= image_color)
    else:
        stop_words = ["said", "will"] + list(STOPWORDS)
        cloud = WordCloud(mask=mask, background_color= (r, g, b), stopwords=stop_words).generate(text)
        image_color = ImageColorGenerator(mask)
        cloud.recolor(color_func= image_color)
    
    os.chdir(UPLOAD_FOLDER)
    cloud.to_file("output.png")



# txt file
def wc_txt(filename, maskname=None, lang="Eng"):
    text = open(os.path.join(UPLOAD_FOLDER, filename), "r", encoding="utf-8").read() #TODO
    if lang == "Chi":
        text = ' '.join(jieba.cut(text))
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)
    
    elif lang == "Jpn":
        # MeCabの準備
        tagger = MeCab.Tagger("-Owakati")
        tagger.parse(text)
        node = tagger.parseToNode(text)

        # 名詞を取り出す
        word_list = []
        while node:
            word_type = node.feature.split(',')[0]
            if word_type == '名詞':
                word_list.append(node.surface)
            node = node.next

        # リストを文字列に変換
        word_chain = ' '.join(word_list)

        if maskname == None:
            gen_wc(word_chain, lang)
        else:
            gen_wc_m(word_chain, maskname, lang)
    
    # English
    else:
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)



# docx file
def wc_doc(filename, maskname=None, lang="Eng"):
    text = docx2txt.process(os.path.join(UPLOAD_FOLDER, filename)) #TODO
    if lang == "Chi":
        text = ' '.join(jieba.cut(text))
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)
    elif lang == "Jpn":
        tagger = MeCab.Tagger("-Owakati")
        tagger.parse(text)
        node = tagger.parseToNode(text)
        word_list = []
        while node:
            word_type = node.feature.split(',')[0]
            if word_type == '名詞':
                word_list.append(node.surface)
            node = node.next
        word_chain = ' '.join(word_list)
        if maskname == None:
            gen_wc(word_chain, lang)
        else:
            gen_wc_m(word_chain, maskname, lang)
    else:
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)



# pdf file
def wc_pdf(filename, maskname=None, lang="Eng"):
    File = open(os.path.join(UPLOAD_FOLDER, filename),'rb') #TODO
    pdf = PyPDF2.PdfFileReader(File)
    textlst = []
    for page in pdf.pages:
        textlst.append(page.extractText())
    text = " ".join(textlst)
    if lang == "Chi":
        text = ' '.join(jieba.cut(text))
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)
    elif lang == "Jpn":
        tagger = MeCab.Tagger("-Owakati")
        tagger.parse(text)
        node = tagger.parseToNode(text)
        word_list = []
        while node:
            word_type = node.feature.split(',')[0]
            if word_type == '名詞':
                word_list.append(node.surface)
            node = node.next
        word_chain = ' '.join(word_list)
        if maskname == None:
            gen_wc(word_chain, lang)
        else:
            gen_wc_m(word_chain, maskname, lang)
    else:
        if maskname == None:
            gen_wc(text, lang)
        else:
            gen_wc_m(text, maskname, lang)


def apology(message, code=400):
    print(message)