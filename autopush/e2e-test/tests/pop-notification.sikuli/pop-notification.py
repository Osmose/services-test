import os

if os.getenv('APP_NAME'):
    APP_NAME = os.getenv('APP_NAME')
    BUILD_NUMBER = os.getenv('BUILD_NUMBER')
else:
    APP_NAME = 'Nightly'
    BUILD_NUMBER = '000'

OS_VERSION = Settings.getOSVersion()

if Settings.isWindows():
    OS = 'WIN'
    if OS_VERSION == '10.0' or OS_VERSION == '6.3':
        print('OS: %s - %s' % (OS, OS_VERSION))
        if APP_NAME == 'Nightly':
            PATH_IMGS = '../images_nightly64/'
            PATH_BIN = 'C:/Program Files'
        else:
            PATH_IMGS = '../images_release32/'
            PATH_BIN = 'C:/Program Files (x86)'
            print "no images found for this OS - ABORTING!"
            exit(1) 
    else:
        print 'Not windows 10'
        exit(1)

elif Settings.isLinux():
    OS = "LINUX"
    print('OS: %s - %s' % (OS, OS_VERSION))
    print "no images found for this OS - ABORTING!"
    exit(1)

elif Settings.isMac():
    OS = 'OSX'
    print('OS: %s - %s' % (OS, OS_VERSION))
    print 'no images found for this OS - ABORTING!'
    exit(1)

else:
    print 'OS not recognized - ABORTING!'
    exit(1)

URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

PATH_PROFILE = 'C:/Jenkins/workspace/autopush_e2e-test_prod/services-test/autopush/e2e-test/tests/prefs/prefs.js'             
NIGHTLY64 = '%s/%s/firefox.exe -height 768 -width 1024' % (PATH_BIN, APP_NAME)
PATH_FIREFOX = NIGHTLY64
IMG_REFRESH = PATH_IMGS + 'btn_refresh.png'
IMG_ALWAYS_RECEIVE_NOTIFICATIONS = PATH_IMGS + 'btn_always_receive.png'
IMG_BTN_POP_NOTIFICATION = PATH_IMGS + 'btn_pop_notification.png' 
IMG_WIN_POP_NOTIFICATION = PATH_IMGS + 'win_pop_notification.png' 
LINE = '--------------------------'

BIN_MINICAP = 'C:\\Program Files (x86)\\MiniCap\MiniCap.exe'
PATH_SCREENSHOTS = 'C:\\Jenkins\\workspace\\screenshots'
URL_SCREENSHOTS = 'https://services-qa-jenkins.stage.mozaws.net:8443/job/screenshots/ws'
firefox = App(APP_NAME)

screenshot_counter = 0

def screenshot():
    from subprocess import Popen, PIPE
    global screenshot_counter
    print('taking screenshot')
    suffix = '%s_%s' % (BUILD_NUMBER, screenshot_counter)
    name_screenshot = '%s\\screenshot_%s.jpg' % (PATH_SCREENSHOTS, suffix)
    cmd = [BIN_MINICAP, '-capturescreen', '-exit', '-closeapp', '-save', name_screenshot] 
    print('%s/screenshot_%s.jpg' % (URL_SCREENSHOTS, suffix))
    proc = Popen(cmd, stdout=PIPE)
    output = proc.communicate()[0]
    print output
    screenshot_counter += 1
    
   
   

def print_header(label):
    print '%s\n%s\n%s' % (LINE, label, LINE)
    
def setup():
    print_header('SETUP')
    firefox.open(PATH_FIREFOX)
    sleep(3)
    firefox.focus()
    print_header('TEST')

def teardown():
    print_header('TEARDOWN')
    print('closing browser now')
    try:
        type('w', Key.SHIFT + Key.CTRL)
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)
    print('Firefox closed')
    print('TEST COMPLETE!')

def enter_url():
    print('ENTER URL')
   
    type("l", Key.CTRL) 
    
    try:
        type(URL_TEST_PAGE + Key.ENTER) 
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)

def always_receive_notifications():
    print('PERMISSIONS: <Always Receive Notifications?>')
    try:
        if exists(IMG_ALWAYS_RECEIVE_NOTIFICATIONS):
            click(IMG_ALWAYS_RECEIVE_NOTIFICATIONS)
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)

def click_button_pop_notification():
  
    try:
        click(IMG_BTN_POP_NOTIFICATION)
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)
    sleep(2)
    
def verify_pop_notification():
    print "POP NOTIFICATION: ???"
    # wait(Pattern(IMG_WIN_POP_NOTIFICATION).similar(50), 10)
    try:
        wait(IMG_WIN_POP_NOTIFICATION, 10)
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)
    
    print('POP NOTIFICATION: COMPLETE!')
    print('POP NOTIFICATION: WAITING FOR VANISH.....')

    try:
        waitVanish(IMG_WIN_POP_NOTIFICATION, 10)
    except FindFailed as e:
        screenshot()
        print 'ERROR: %s' % e
        exit(1)

setup()

enter_url()
click_button_pop_notification()
always_receive_notifications()
verify_pop_notification()
teardown()