import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://curriculum.hust.edu.cn/")

ACCOUNT = "U201813423"
PASSWORD = "z.528086118"


def login(): 
    driver.find_element_by_class_name('login_box_landing_btn').click()
    account = driver.find_element_by_id("username_text")
    account.send_keys(ACCOUNT)
    password = driver.find_element_by_id("password_text")
    password.send_keys(PASSWORD)
    driver.find_element_by_class_name('login_box_landing_btn').click()
    driver.find_elements_by_class_name('buttonDivLeft')[2].click()
    print("\nlogin success!\n")

def pingJiaoAll(): #遍历page
    pageNum = 1
    nextBtn = driver.find_element_by_class_name('buttonRight')
    while(nextBtn.get_attribute('style') == "cursor: pointer;"):
        pingJiaoPage(pageNum)
        nextBtn.click()
        pageNum += 1
        nextBtn = driver.find_element_by_class_name('buttonRight')
    pingJiaoPage(pageNum)

def pingJiaoPage(pageNum): #获取page中课程列表
    print("page:" + str(pageNum))

    time.sleep(0.5)
    items = driver.find_elements_by_xpath('//td[@class = "tableSM"]/div')

    for item in items:
        itemName = driver.find_elements_by_class_name('tableTitleDIV_green')[items.index(item)].text
        if(item.text == "评价"):
            print(itemName + "开始评教")
            itemId = item.get_attribute('onclick')[13:20]
            pingJiao(itemId,pageNum)
            print(itemName + "评教已完成")
        else:
            print(itemName + "评教已完成")
    print("\n")
    return

def pingJiao(itemId,page): #对某课程进行评教

    itemIdStr = "http://curriculum.hust.edu.cn/wspj/awspj.jsp?jsid=&kcdm=" + str(itemId) + "&xnxq=20182&pjlc=2018201&page=" + str(page)
    js='window.open( \"' + itemIdStr + '\")'

    driver.execute_script(js)
    driver.switch_to.window(driver.window_handles[-1])
    
    time.sleep(0.3)
    for i in range(7):
        tempStr = '//td[@id = \"pjxx' + str(i)  + '\"]/input'
        item = driver.find_elements_by_xpath(tempStr)
        if(len(item) != 0):
            item[0].click()
            time.sleep(0.1)
    driver.find_elements_by_class_name('buttonDivLeft')[1].click()
    driver.switch_to.alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    

login()
pingJiaoAll()