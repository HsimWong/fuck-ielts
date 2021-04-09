'''
Eng->Chn: 1
Chn->Eng: 1
Check Eng->Chn: pass 1
Check Chn->Eng: pass 1
'''
daily_items = 50
scanned_words = {}
new_word_list = []   # [split:[words]]
callback_list = {}
today_recited = {}
today_not_remembered = {}
exit_flag_memorize = False
exit_flag_callback = False

import json 
import random

def load_history():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    with open("history.json", 'w+') as f:
        raw_content = str(f.read())
        # print(raw_content)
        if len(raw_content) == 0:
            return 
        scanned_words = json.loads(raw_content)

def generate_new_list():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    with open('wordlist.json', 'r') as f:
        new_word_list = json.loads(f.read())[len(scanned_words):len(scanned_words) + daily_items]


def memorize_new_list():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    for word in new_word_list:
        print()
        print("含义：",word['meaning'], '\t', "词汇：",word['key'], "\t")
        print("发音：",word['pronounciation'])
        refined_word = word['key'][:-1] if word['key'][-1] == '*' else word['key']
        while True:

            word['recited_times'] += 1
            entry = input("请拼写出整个单词：")
            if entry == 'exit':
                global exit_flag_memorize
                exit_flag_memorize = True
                return
            elif entry == refined_word:
                callback_list.update({int(word['index']):word})
                break
            else:
                word['mistakes'] += 1
                today_not_remembered.update({int(word['index']): word})
                callback_list.update({int(word['index']):word})
                print("输入错误，请重新输入")
                continue

        

def generate_callbacks():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    for word_index in scanned_words.keys():
        word = scanned_words[word_index]
        if (word['mistakes'] != 0) and word['corrects'] / word['mistakes'] <= 2:
            callback_list.update({int(word['index']):word})

    

def check_callbacks():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    # englist_list = {}
    while True:
        if len(callback_list) == 0:

            break 
        else:
            keys = list(callback_list.keys())
            random.shuffle(keys)
            for word_index in keys:
                word = callback_list[word_index]
                refined_word = word['key'][:-1] if word['key'][-1] == '*' else word['key']
                while True:
                    word['recited_times'] += 1
                    word['today_recited'] += 1
                    print("含义：",word['meaning'])
                    entry = input("请写出其英文：")
                    if entry == 'exit':
                        global exit_flag_callback
                        exit_flag_callback = True
                        return
                    elif entry == refined_word:
                        word['corrects'] += 1
                        scanned_words.update({int(word['index']): word})
                        if word['today_recited'] >= 2 and (word['mistakes'] == 0 or \
                            (word['mistakes'] != 0 and (word['corrects'] >= 2))):
                            word['today_recited'] = 0

                            scanned_words.update({int(word['index']): word})
                            callback_list.pop(word_index)
                        break 
                    else:
                        word['mistakes'] += 1
                        scanned_words.update({int(word['index']):word})
                        print("输入错误，请重新输入")
                        continue
                continue



def save():
    global daily_items
    global scanned_words
    global new_word_list
    global callback_list
    global today_not_remembered
    global today_recited
    global exit_flag_memorize
    global exit_flag_callback
    if exit_flag_memorize:
        print("在生词没有被浏览完毕的情况下，你的进度将不被保存。")
        # print(scanned_words)
    else:
        print("祝贺！你已经完成了今天的任务")
    history_file = str(json.dumps(scanned_words, ensure_ascii=False).encode('utf-8').decode('utf-8'))
    with open('history.json', 'w') as f:
        f.write(history_file)

    with open('log.txt','w+') as f:
        import datetime
        f.write('\n')
        f.write(str(datetime.datetime.now()))
        f.write('\t')
        if (exit_flag_memorize):
            f.write(str(callback_list))
            f.write('\t')
            f.write('0')
        else:
            f.write(str(daily_items))
            f.wrte('\t')  
            f.write(str(min(daily_items - len(callback_list))))


    

def main():
    global exit_flag_memorize
    load_history()
    generate_callbacks()
    generate_new_list()
    memorize_new_list()

    
    if not exit_flag_memorize:
        print("你已经背完今天的生词了，我们回顾一下他们")
        check_callbacks()

    save()


main()

    

    # wordlist = load_wordlist()
    # recite_history()
    # recite_new_list()
    # update_history()

    
