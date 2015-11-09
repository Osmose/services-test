import os

if os.getenv('APP_NAME'):
    APP_NAME = os.getenv('APP_NAME')
else:
    APP_NAME = 'Nightly'

PATH_PROFILE = "C:/Jenkins/workspace/services-test/autopush/e2e-test/tests/prefs/prefs.js"
               
NIGHTLY64 = "C:/Program Files/%s/firefox.exe -height 768 -width 1024" % (APP_NAME)
PATH_FIREFOX = NIGHTLY64

OS_VERSION = Settings.getOSVersion()

if Settings.isWindows():
    OS = "WIN"
    if OS_VERSION == "10.0" or OS_VERSION == "6.3":
        print('OS: %s - %s' % (OS, OS_VERSION))
        if APP_NAME == 'Nightly':
            PATH_IMGS = '../images_nightly64/'
        else:
            PATH_IMGS = '../images_release32/'
            print('TBD -> need images for GR32!!')
            exit(1) 
    else:
        print "Not windows 10"
        exit(1)

elif Settings.isLinux():
    print "is Linux!"
    exit(1)

elif Settings.isMac():
    print "is Mac"
    exit(1)

else:
    print "System not recognized"
    exit(2)

URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

IMG_REFRESH = PATH_IMGS + "btn_refresh.png" # 
URL_ENTRY_POINT_1 = Pattern(PATH_IMGS + "url_entry_moz.png").targetOffset(110,-4)
URL_ENTRY_POINT_2 = PATH_IMGS + "url_entry_search.png" 
URL_ENTRY_POINT_3 = Pattern(PATH_IMGS + "url_entry_nightly.png").targetOffset(59,0)
URL_ENTRY_POINT_4 = Pattern(PATH_IMGS + "url_entry_green_padlock.png").targetOffset(59,1)
IMG_WIN_MAXIMIZE = PATH_IMGS + "win_maximize.png" 
IMG_ALWAYS_RECEIVE_NOTIFICATIONS = PATH_IMGS + "btn_always_receive.png"
IMG_BTN_POP_NOTIFICATION = PATH_IMGS + "btn_pop_notification.png" 
IMG_WIN_POP_NOTIFICATION = PATH_IMGS + "win_pop_notification.png" 
LINE = '--------------------------'


firefox = App(APP_NAME)

def header(label):
    return '%s\n%s\n%s' % (LINE, label, LINE)
    
def setup():
    # firefox.close()
    
    print header('SETUP')
    firefox.open(PATH_FIREFOX)
    if exists(IMG_REFRESH):
        print('REFRESH NIGHTLY: TRYING....!')
        click(IMG_REFRESH)
        click("1446188189853.png")
        
    firefox.focus()

def teardown():

    #print('%s\n%s\n%s' % (LINE, 'TEARDOWN', LINE))
    print header('TEARDOWN')
    print('closing browser now')
    type('w', Key.SHIFT + Key.CTRL)
    print('Firefox closed')
    
setup()

print header('TEST')

if exists(URL_ENTRY_POINT_1):
    print('URL ENTRY POINT: <Mozilla Foundation>')
    click(URL_ENTRY_POINT_1)
elif exists(URL_ENTRY_POINT_2):
    print('URL ENTRY POINT: <Search or enter address>')
    click(URL_ENTRY_POINT_2)
elif exists(URL_ENTRY_POINT_3):
    print('URL ENTRY POINT: <Nightly...>')
    click(URL_ENTRY_POINT_3)
elif exists(URL_ENTRY_POINT_4):
    print('URL ENTRY POINT: <green padlock>')
    click(URL_ENTRY_POINT_4)
else:
    print('ERROR: can\'t find URL bar!')
    exit(1)
type(URL_TEST_PAGE + Key.ENTER)

click(IMG_BTN_POP_NOTIFICATION)

sleep(2)

print('PERMISSIONS: <Always Receive Notifications?>')
if exists(IMG_ALWAYS_RECEIVE_NOTIFICATIONS):
    click(IMG_ALWAYS_RECEIVE_NOTIFICATIONS)

print "POP NOTIFICATION: ???"
wait(IMG_WIN_POP_NOTIFICATION)
print('POP NOTIFICATION: COMPLETE!')
print('POP NOTIFICATION: WAITING FOR VANISH.....')
waitVanish(IMG_WIN_POP_NOTIFICATION)
print('TEST COMPLETE!')

teardown()