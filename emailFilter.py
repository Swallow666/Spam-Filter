

import os
import numpy as np
import re  ##正则匹配包
import math



##读取email中的内容   
def readtxt(email_path):
    with open(email_path, 'r', encoding = 'latin-1') as email:
        lines = email.readlines()
    return lines

##清理email中大小写和非英文单词内容
def email_parser(email_path):
    wordList = []
    lines = readtxt(email_path)
    aString = "".join(lines)
    aString = aString.lower()
    list = re.split("[^a-zA-Z]",aString)
    
    for word in list:
        if(len(word) >= 1):
            wordList.append(word)
            
    return wordList ##wordList,set(wordList)
    
##归类目录下ham和spam文件并分别处理
def fileParser(path):
    
    files = os.listdir(path) #得到文件夹下的所有文件名称
    
    ham = 'ham'
    spam = 'spam'
    ham_list = []
    spam_list = []
    
    for file in files: #遍历文件夹
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
            
            if (ham in file ):
                ham_list += email_parser(path + "/" + file)
            if (spam in file):
                spam_list += email_parser(path + "/" + file)

    return ham_list, spam_list,set(ham_list),set(spam_list)

    
##计算出各自的frequency, 不过这个frequency我不太确定是怎么算一次.............
def count_word(ham_list,spam_list,vocab_set):
    ham_word_count = {}
    spam_word_count = {}
    
    for word in vocab_set:
        counter = 0
        if (word in ham_list):
            counter = ham_list.count(word)
            ham_word_count[word] = counter
        if (word in spam_list):
            counter = spam_list.count(word)
            spam_word_count[word] = counter
     
    return ham_word_count,spam_word_count
            
##Building the Model
def set_model(ham_list,spam_list,ham_set,spam_set,file_name):
    vocab_set = ham_set.union(spam_set)
    with open(file_name,'a', encoding = 'latin-1') as model:
        
        for word in vocab_set:
            ham_count = ham_list.count(word)
            ham_prob = ( ham_list.count(word) + 0.5) / (len(ham_list) + 0.5*len(vocab_set))
            spam_count = (spam_list.count(word))
            spam_prob = ( spam_list.count(word) + 0.5) / (len(spam_list) + 0.5*len(spam_set))
            model.write(word + '  ' + str(ham_count) + '  ' + str(ham_prob) + '  ' + str(spam_count) + '  ' + str(spam_prob) + '\n' )
            
## Building and Evaluating the Classifier        
def test_model(test_files_name,model_name):
    
    
    files = os.listdir(test_files_name)
   
    ham = 'ham'
    spam = 'spam'
    ham_count = 0
    spam_count = 0
    
    for file in files: #遍历文件夹
        
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
            
            if (ham in file ):
                ham_count += 1
            if (spam in file):
                spam_count += 1
    
    
    with open('baseline-result.txt','a', encoding = 'latin-1') as test:
        
        number = 0
        result = ''
        key = 0
        
        with open("model.txt", "r") as model:
            model_set = [[x for x in line.split()] for line in model] ## this line of the code, I search stackoverflow to find this method, and it works:)
        
            for file in files:
                number +=1
                ##email_list = email_parser(file)
                test.write(str(number) + '  ' + str(file) + '  ')
                
                email_list = email_parser(test_files_name + "/" + file)
                
                score_ham = math.log( (ham_count)/(spam_count + ham_count),10)
                score_spam = math.log( (spam_count)/(spam_count + ham_count),10)
                
                    
                for word in email_list:
                    
                    for record in model_set:
                        for data in record:
                            if data == word:
                                score_ham += math.log(float(model_set[model_set.index(record)][2]), 10)
                                score_spam += math.log(float(model_set[model_set.index(record)][4]), 10)
                             
                        
                test.write(str(score_ham) + '  ' + str(score_spam) + '  ')
    
    
        
                if (ham in file ):
                    test.write(ham + '  ')
                    
                if (spam in file):
                    test.write(spam + '  ')
            
                test.write('\n')
            
                
              
        
        
        
        
                
    


def main():
    ham_list, spam_list,ham_set,spam_set = fileParser('train111')
    print(len(ham_set))
    print(len(spam_set))
    vocab = ham_set.union(spam_set)
    print(len(vocab))
    
    ham_word_count,spam_word_count = count_word(ham_list,spam_list,vocab)
    print (ham_list.count('a') + spam_list.count('a'))
    print (ham_word_count['a'])
    print (spam_word_count['a'])
    
    ##set_model(ham_list,spam_list,ham_set,spam_set,'model.txt')
    test_model('test111', 'model.txt')
    
if __name__ == '__main__':
		main()	

