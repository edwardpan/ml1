"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字典顺序排序后输出。
"""

def is_saler_phone(phone):
    """判断是否是电话促销员的号码
    :param phone: 电话号码,字符串
    :return: True:是电话促销员,False:不是
    """
    return str(phone).startswith("140")

def all_text_and_receive_phone():
    """找出所有发送和接收过短信，接过电话的号码"""
    phones = set()
    for text in texts:
        phones.add(text[0])
        phones.add(text[1])
    for call in calls:
        phones.add(call[1])
    return phones

def get_saller_phones():
    """获取所有可能的推销员号码"""
    maybe_not_saller_phones = all_text_and_receive_phone()
    maybe_saller_phones = set()
    for call in calls:
        from_call = call[0]
        if is_saler_phone(from_call) and from_call not in maybe_not_saller_phones: # 号码以140开头且没有发送/接收过短信，没有接过电话
            maybe_saller_phones.add(from_call)
    maybe_saller_phones_list = list(maybe_saller_phones)
    maybe_saller_phones_list.sort()
    return maybe_saller_phones_list

print("These numbers could be telemarketers: ")
saller_phones = get_saller_phones()
for phone in saller_phones:
    print(phone)
