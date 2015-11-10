import os

if os.getenv('APP_NAME'):
    APP_NAME = os.getenv('APP_NAME')
else:
    APP_NAME = 'Nightly'

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


firefox = App(APP_NAME)

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
    type('w', Key.SHIFT + Key.CTRL)
    print('Firefox closed')
    print('TEST COMPLETE!')

def enter_url():
    print('ENTER URL')
    type("l", Key.CTRL) 
    type(URL_TEST_PAGE + Key.ENTER) 

def always_receive_notifications():
    print('PERMISSIONS: <Always Receive Notifications?>')
    if exists(IMG_ALWAYS_RECEIVE_NOTIFICATIONS):
        click(IMG_ALWAYS_RECEIVE_NOTIFICATIONS)

def click_button_pop_notification():
    click(IMG_BTN_POP_NOTIFICATION)
    sleep(2)
    
def verify_pop_notification():
    print "POP NOTIFICATION: ???"
    wait(IMG_WIN_POP_NOTIFICATION)
    print('POP NOTIFICATION: COMPLETE!')
    print('POP NOTIFICATION: WAITING FOR VANISH.....')
    waitVanish(IMG_WIN_POP_NOTIFICATION)
    
setup()

enter_url()
click_button_pop_notification()
always_receive_notifications()
verify_pop_notification()
teardown()