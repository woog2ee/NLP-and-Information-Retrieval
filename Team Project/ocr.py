import os 
from pykospacing import spacing
from hanspell import spell_checker
import cv2
import pytesseract
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'     # tensorflow 오류 제거용
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'



def ocr_read(imPath):
    # 이미지 텍스트화
    config = ('-l kor --oem 3 --psm 4')
    img_gray = cv2.imread(imPath, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.imread(imPath, cv2.IMREAD_GRAYSCALE)
    string = pytesseract.image_to_string(img_gray, config=config)
    
    # 띄어쓰기
    spacing = spacing()
    no_space_string = string.replace(' ','').replace('\n','')
    newstring = spacing(no_space_string) 
    result = spell_checker.check(newstring).checked
    return result