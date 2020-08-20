import re

convertUnsignedTable = {'a': r'á|à|ạ|ả|ã|â|ấ|ầ|ậ|ẩ|ẫ|ă|ắ|ằ|ặ|ẳ|ẵ',
                'A': r'Á|À|Ạ|Ả|Ã|Â|Ấ|Ầ|Ậ|Ẩ|Ẫ|Ă|Ắ|Ằ|Ặ|Ẳ|Ẵ',
                'e': r'é|è|ẹ|ẻ|ẽ|ê|ế|ề|ệ|ể|ễ',
                'E': r'É|È|Ẹ|Ẻ|Ẽ|Ê|Ế|Ề|Ệ|Ể|Ễ',
                'o': r'ó|ò|ọ|ỏ|õ|ô|ố|ồ|ộ|ổ|ỗ|ơ|ớ|ờ|ợ|ở|ỡ',
                'O': r'Ó|Ò|Ọ|Ỏ|Õ|Ô|Ố|Ồ|Ộ|Ổ|Ỗ|Ơ|Ớ|Ờ|Ợ|Ở|Ỡ',
                'u': r'ú|ù|ụ|ủ|ũ|ư|ứ|ừ|ự|ử|ữ',
                'U': r'Ú|Ù|Ụ|Ủ|Ũ|Ư|Ứ|Ừ|Ự|Ử|Ữ',
                'i': r'í|ì|ị|ỉ|ĩ',
                'I': r'Í|Ì|Ị|Ỉ|Ĩ',
                'd': r'đ',
                'D': r'Đ',
                'y': r'ý|ỳ|ỵ|ỷ|ỹ',
                'Y': r'Ý|Ỳ|Ỵ|Ỷ|Ỹ'}

combineWordTable = {
                    'xe bus': 'xe_bus',
                    'thanh pho': 'thanh_pho',
                    'thoi gian': 'thoi_gian',
                    'da nang': '<VAR>da_nang',
                    'ho chi minh': '<VAR>ho_chi_minh',
                    'xuat phat': 'xuat_phat',
                    'hue': '<VAR>hue',
                    'b1': '<VAR>B1',
                    'b2': '<VAR>B2',
                    'b3': '<VAR>B3',
                    'b4': '<VAR>B4',
                    'b5': '<VAR>B5',
                    'b6': '<VAR>B6',
                    'b7': '<VAR>B7'}

class Tokenize():
    def __init__(self, str: str):
        self._str = str.lower()
        self.unsignedStr = ""

    def parse(self):
        output = self._str
        for key in convertUnsignedTable:
            output = re.sub(convertUnsignedTable[key], key, output)

        for words in combineWordTable:
            output = output.replace(words, combineWordTable[words])

        m = re.search("(\d+)\:(\d+)", output)
        if m is not None:
            output = output[: m.start()] + "<VAR>" + output[m.start():]
        return output.split()

# print(Tokenize("Những xe nào xuất phát từ thành phố Hồ Chí Minh ?").parse())