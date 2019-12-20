import os

# 转换文件格式和编码方式
def to_lf(path, isLF, encoding = 'utf-8'):
    """
    :param path: 文件路径
    :param isLF: True 转为Unix(LF)  False 转为Windows(CRLF)
    :param encoding: 编码方式，默认utf-8
    :return:
    """
    newline = '\n' if isLF else '\r\n'
    tp = 'Unix(LF)' if isLF else 'Windows(CRLF)'
    with open(path, 'r', newline=None, encoding=encoding) as infile:
        str = infile.readlines()
        with open(path, 'w', newline=newline, encoding=encoding) as outfile:
            outfile.writelines(str)
            print("文件转换成功，格式：{0} ;编码：{1} ;路径：{2}".format(tp, encoding, path))
            outfile.close()
        infile.close()

if __name__ == "__main__":
    rootdir = r'E:\git_project\models'
    isLF = True  # True 转为Unix(LF)  False 转为Windows(CRLF)
    path_list = [rootdir, ]
    #path_list.sort(key=lambda x:int(x[:-4])) #对读取的路径进行排序
    while len(path_list) > 0:
        root_path = path_list.pop(0)
        if os.path.isdir(root_path):
            file_list = os.listdir(root_path)
            for file in file_list:
                path_list.append(os.path.join(root_path, file))
            continue
        if '.sh' in root_path:
            to_lf(root_path, isLF)