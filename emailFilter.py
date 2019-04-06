import os
import re
import math

##读取email中的内容   
def readtxt(email_path):
    with open(email_path, 'r', encoding = 'latin-1') as email:
        lines = email.readlines()
    return lines

##清理email中大小写和非英文单词内容
def email_parser(email_path,mode,stopwords=None):
    wordList = []
    lines = readtxt(email_path)
    aString = "".join(lines)
    aString = aString.lower()
    alist = re.split("[^a-zA-Z]",aString)
    
    if mode == 0:
        for word in alist:
            if(len(word) >= 1):
                wordList.append(word)

    elif mode == 1:
        for word in alist:
            if word not in stopwords:
                if(len(word) >= 1):
                    wordList.append(word)
            
    return wordList ##wordList,set(wordList)
    
##归类目录下ham和spam文件并分别处理
def fileParser(path,mode,stopwords=None):
    
    files = os.listdir(path) #得到文件夹下的所有文件名称
    
    ham = 'ham'
    spam = 'spam'
    ham_list = []
    spam_list = []
    ham_num = 0
    spam_num = 0

    for file in files: #遍历文件夹
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
            
            if (ham in file):
                ham_num += 1
                ham_list += email_parser(path + "/" + file, mode, stopwords)
            if (spam in file):
                spam_num += 1
                spam_list += email_parser(path + "/" + file, mode, stopwords)

    ham_doc_prob = ham_num/(ham_num + spam_num)
    spam_doc_prob = spam_num/(ham_num + spam_num)

    return ham_list, spam_list,set(ham_list),set(spam_list), ham_doc_prob, spam_doc_prob


##Building the Model
def set_model(ham_list,spam_list,vocab_set,file_name):

    ham_dic = {}
    spam_dic = {}

    with open(file_name,'w', encoding = 'latin-1') as model:

        ln_ctr = 1
        for word in vocab_set:
            ham_count = ham_list.count(word)
            ham_prob = (ham_count + 0.5) / (len(ham_list) + 0.5*len(vocab_set))
            ham_dic[word] = ham_prob
            spam_count = spam_list.count(word)
            spam_prob = (spam_count + 0.5) / (len(spam_list) + 0.5*len(vocab_set))
            spam_dic[word] = spam_prob
            model.write(str(ln_ctr) + '  ' + word + '  ' + str(ham_count) + '  ' + str(ham_prob) + '  ' + str(spam_count) + '  ' + str(spam_prob) + '\n' )
            ln_ctr += 1
    return ham_dic, spam_dic

def test_model(path,ham_dic,spam_dic,ham_doc_prob,spam_doc_prob, file_name, mode,stopwords=None):

    files = os.listdir(path)
    ham = 'ham'
    spam = 'spam'

    with open(file_name,'w', encoding = 'latin-1') as baseline:

        ln_ctr = 1

        for file in files: 
            if not os.path.isdir(file): 
                
                score_ham, score_spam = math.log10(ham_doc_prob), math.log10(spam_doc_prob)
                file_words = email_parser(path + "/" + file, mode, stopwords)

                for word in file_words:
                    if word in ham_dic:
                        score_ham += math.log10(ham_dic[word])
                    if word in spam_dic: 
                        score_spam += math.log10(spam_dic[word])

                guess = ham if score_ham > score_spam else spam
                real = ham if ham in file else spam
                guess_what = 'right' if guess == real else 'wrong'

                baseline.write(str(ln_ctr) + '  ' + file + '  ' + guess + '  ' + str(score_ham) + '  ' + str(score_spam) + '  ' + real + '  ' + guess_what + '\n')
                ln_ctr += 1

def main():
    # mode 0 for baseline, 1 for stopword, 2 for wordlength
    ham_list, spam_list, ham_set, spam_set, ham_doc_prob, spam_doc_prob = fileParser('train111',0)
    vocab = ham_set.union(spam_set)
    ham_dic, spam_dic = set_model(ham_list,spam_list,vocab,'model.txt')
    test_model('test111', ham_dic, spam_dic, ham_doc_prob, spam_doc_prob, 'baseline-result.txt', 0)

    stopword_lines = readtxt('stopword.txt')
    stop_string = "".join(stopword_lines)
    stop_string = stop_string.lower()
    stop_list = re.split("[^a-zA-Z]",stop_string)
    stopword_ham_list, stopword_spam_list, stopword_ham_set, stopword_spam_set, stopword_ham_doc_prob, stopword_spam_doc_prob = fileParser('train111',1,stop_list)
    stopword_vocab = stopword_ham_set.union(stopword_spam_set)
    stopword_ham_dic, stopword_spam_dic = set_model(stopword_ham_list,stopword_spam_list,stopword_vocab,'stopword-model.txt')
    test_model('test111', stopword_ham_dic, stopword_spam_dic, stopword_ham_doc_prob, stopword_spam_doc_prob, 'stopword-result.txt', 1,stop_list)


if __name__ == '__main__':
    main()