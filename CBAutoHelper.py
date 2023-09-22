
import os, cv2, numpy, base64, subprocess, random,threading,time
from lxml import html
class ADB:
    KEYCODE_0 = 0
    KEYCODE_SOFT_LEFT = 1
    KEYCODE_SOFT_RIGHT = 2
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_CALL = 5
    KEYCODE_ENDCALL = 6
    KEYCODE_0_ = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 0xF
    KEYCODE_9 = 0x10
    KEYCODE_STAR = 17
    KEYCODE_POUND = 18
    KEYCODE_DPAD_UP = 19
    KEYCODE_DPAD_DOWN = 20
    KEYCODE_DPAD_LEFT = 21
    KEYCODE_DPAD_RIGHT = 22
    KEYCODE_DPAD_CENTER = 23
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_POWER = 26
    KEYCODE_CAMERA = 27
    KEYCODE_CLEAR = 28
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 0x1F
    KEYCODE_D = 0x20
    KEYCODE_E = 33
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_I = 37
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_M = 41
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_COMMA = 55
    KEYCODE_PERIOD = 56
    KEYCODE_ALT_LEFT = 57
    KEYCODE_ALT_RIGHT = 58
    KEYCODE_SHIFT_LEFT = 59
    KEYCODE_SHIFT_RIGHT = 60
    KEYCODE_TAB = 61
    KEYCODE_SPACE = 62
    KEYCODE_SYM = 0x3F
    KEYCODE_EXPLORER = 0x40
    KEYCODE_ENVELOPE = 65
    KEYCODE_ENTER = 66
    KEYCODE_DEL = 67
    KEYCODE_GRAVE = 68
    KEYCODE_MINUS = 69
    KEYCODE_EQUALS = 70
    KEYCODE_LEFT_BRACKET = 71
    KEYCODE_RIGHT_BRACKET = 72
    KEYCODE_BACKSLASH = 73
    KEYCODE_SEMICOLON = 74
    KEYCODE_APOSTROPHE = 75
    KEYCODE_SLASH = 76
    KEYCODE_AT = 77
    KEYCODE_NUM = 78
    KEYCODE_HEADSETHOOK = 79
    KEYCODE_FOCUS = 80
    KEYCODE_PLUS = 81
    KEYCODE_MENU = 82
    KEYCODE_NOTIFICATION = 83
    KEYCODE_APP_SWITCH = 187
    def GetDevices(self):
        listdevice = []
        devices = str(subprocess.check_output("adb devices", shell=True)).replace("b'List of devices attached\\r\\n", '').replace("'", '').replace('bList of devices attached ', '').split('\\r\\n')
        for device in devices:
            if device != '':
                listdevice.append(device.split('\\tdevice')[0])
        return listdevice
    def OpenApp(self, emulator, package):
        subprocess.check_call(f"adb -s {emulator} shell monkey -p {package} -c android.intent.category.LAUNCHER 1", shell=True)
    def PushFile(self, emulator, pathpc, pathphone):
        subprocess.check_call(f"adb -s {emulator} push {pathpc} {pathphone}", shell=True)
    def InstallApp(self, emulator, path):
        subprocess.check_call(f"adb -s {emulator} -e install {path}", shell=True)
    def GetApk(self, emulator, package):
        path = subprocess.check_output(f"adb -s {emulator} shell pm path {package}", shell=True).split('\n')
        if path == ['']:
            return
        path = path[0].replace('package:', '')
        subprocess.check_call(f"adb -s {emulator} pull {path} {package}.apk", shell=True)
    def KeyEvent(self, emulator, key):
        subprocess.check_call(f"adb -s {emulator} shell input keyevent {str(key)}", shell=True)
    def InpuText(self, emulator, text=None, VN=None):
        if text == None:
            text =  str(base64.b64encode(VN.encode('utf-8')))[1:]
            subprocess.check_call(f"adb -s {emulator} shell ime set com.android.adbkeyboard/.AdbIME", shell=True)
            subprocess.check_call(f"adb -s {emulator} shell am broadcast -a ADB_INPUT_B64 --es msg {text}", shell=True)
            return
        subprocess.check_call(f"adb -s {emulator} shell input text '{text}'", shell=True)
    def Swipe(delf, emulator, x1, y1, x2, y2):
        subprocess.check_call(f"adb -s {emulator} shell input touchscreen swipe {x1} {y1} {x2} {y2}", shell=True)
    def OpenLink(self, emulator, link):
        subprocess.call("adb -s "+emulator+" shell am start -a android.intent.action.VIEW -d '"+link+"'", shell=True)
    def StopApp(self, emulator, package):
        subprocess.call("adb -s "+emulator+f" shell am force-stop {package}", shell=True)
    def ScreenCaptureNoSave(self):
        pipe = subprocess.Popen("adb exec-out screencap -p", stdout=subprocess.PIPE, shell=True)
        img_bytes = pipe.stdout.read()
        img = cv2.imdecode(numpy.frombuffer(img_bytes, numpy.uint8), cv2.IMREAD_COLOR)
        return img
    def ScreenCapture(self, emulator):
        name = emulator
        if ":" in emulator:
            name = emulator.replace(":", "").replace(".", "")
        subprocess.check_call(f"adb -s {emulator} shell screencap /sdcard/Download/{name}.png", shell=True)
        subprocess.check_call(f"adb -s {emulator} pull /sdcard/Download/{name}.png {name}.png", shell=True)
        return f"{name}.png"
    def Pull(self, emulator, path):
        subprocess.check_call(f"adb -s {emulator} pull {path}", shell=True)
    def Push(self, emulator, path, path1):
        subprocess.check_call(f"adb -s {emulator} push {path} {path1}", shell=True)
    def Click(self, emulator, x, y):
        subprocess.check_call(f"adb -s {emulator} shell input tap {int(x)} {int(y)}", shell=True)
    def FindImg(self, emulator, target_pic_name):
        try:
            img = cv2.imread(target_pic_name)
            img2 = cv2.imread(self.ScreenCapture(emulator))
            w, h = img.shape[1], img.shape[0]
            result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED) 
            location = numpy.where(result >= 0.8)
            data = list(zip(*location[::-1]))
            is_match = len(data) > 0
            if is_match:
                x, y = data[0][0], data[0][1]  
                return x + int(w/2), y + int(h/2)
            else:
                return False, False
        except:
            return False, False
    def Grant(self, emulator, package, grant):
        subprocess.check_call(f'adb -s {emulator} shell pm grant {package} android.permission.'+grant)
    def TapImg(self, emulator, img_path):
        x, y = self.FindImg(emulator, target_pic_name=img_path)
        
        if x:
            self.Click(emulator, x, y)
            return True
        else: return False
    def Change_Proxy(self, emulator, proxy):
        subprocess.check_call(f"adb -s {emulator} shell settings put global http_proxy {proxy}", shell=True)
    def Remove_Proxy(self, emulator):
        subprocess.check_call(f"adb -s {emulator} shell settings put global http_proxy :0", shell=True)
    def DeleteCache(self, emulator, package):
        subprocess.check_output(f"adb -s {emulator} shell pm clear {package}", shell=True)
    def SetTextClipbroad(self, emulator, text):
        subprocess.check_call(f'adb -s {emulator} shell am broadcast -a clipper.set -e text "{text}"', shell=True)
    def Paste(self, emulator):
        subprocess.check_call(f"adb -s {emulator} shell input keyevent 279", shell=True)
    def DumXml(self, emulator):
        name = emulator
        if ":" in emulator:
            name = emulator.replace(":", "").replace(".", "")
        subprocess.check_call(f"adb -s {emulator} shell uiautomator dump", shell=True)
        subprocess.check_call(f"adb -s {emulator} pull /sdcard/window_dump.xml {name}.xml", shell=True)
        return f'{name}.xml'
    def GetPosXml(self, emulator, element):
        pos = []
        try:
            path = self.DumXml(emulator)
            if not os.path.exists(path): return pos
            tree = html.parse(path)
            for bound in tree.xpath(element):
                gg = bound.attrib['bounds'].split('][')[0].replace('[', '').split(',')
                pos.append(tuple([int(gg[0]), int(gg[1])]))
            return pos
        except:
            return pos
    def TapXml(self, emulator, xpath):
        pos = self.GetPosXml(emulator, xpath)
        if pos != []:
            pos = pos[-1]
            self.Click(emulator, pos[0], pos[1])

class LDPlayer:
    def __init__(self):
        self.pathLD = "C:\LDPlayer\LDPlayer9"
    def Info(self, param, NameOrId):
        self.param, self.NameOrId = param, NameOrId
    def ExecuteLD(self, shell):
        return str(subprocess.Popen(f"ldconsole {shell}", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, shell=True, cwd=self.pathLD).stdout.read())
    def ChangeProxy(self, proxy):
        self.AdbLd(f"shell settings put global http_proxy {proxy}")
    def RemoveProxy(self):
        self.ChangeProxy(":0")
    def DumXml(self):
        self.AdbLd('shell uiautomator dump')
        path = "\"\"%s\"\""%os.path.join(os.getcwd(), f"window_dump_{self.NameOrId}.xml")
        self.AdbLd(f"pull /sdcard/window_dump.xml {path}")
        return f'window_dump_{self.NameOrId}.xml'
    def GetPosXml(self, element):
        name = self.DumXml()
        tree = html.parse(name)
        pos = []
        for bound in tree.xpath(element):
            gg = bound.attrib['bounds'].split('][')[0].replace('[', '').split(',')
            pos.append(tuple([int(gg[0]), int(gg[1])]))
        return pos
    def Click(self, x, y):
        return self.AdbLd(f'shell input tap {x} {y}')
    def SendText(self, text, VN=True):
        if VN:
            text =  str(base64.b64encode(text.encode('utf-8')))[1:]
            self.AdbLd(f"shell ime set com.android.adbkeyboard/.AdbIME")
            self.AdbLd(f"shell am broadcast -a ADB_INPUT_B64 --es msg {text}")
            return
            
        self.AdbLd(f"shell input text '{text}'")
    def Swipe(self, x1, y1, x2, y2, delay=0):
        if delay == 0: delay = ""
        self.AdbLd(f"shell input touchscreen swipe {x1} {y1} {x2} {y2} {delay}")
    def PushImg(self, path):
        self.AdbLd(f"push {path} /sdcard/Pictures/avatar.png")
        self.AdbLd("shell am broadcast -a android.intent.action.BOOT_COMPLETED -n com.android.providers.media/.MediaScannerReceiver")
        self.AdbLd("shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///mnt/sdcard/Pictures/")
        self.AdbLd("shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard/Pictures")
    def ScreenCapture(self):
        path = "\"\"%s\"\""%os.path.join(os.getcwd(), f"screenshot_{self.NameOrId}.png")
        self.AdbLd(f"shell screencap /sdcard/Download/screenshot_{self.NameOrId}.png")
        self.AdbLd(f"pull /sdcard/Download/screenshot_{self.NameOrId}.png {path}")
        return f"screenshot_{self.NameOrId}.png"
    def FindImg(self, target_pic_name):
        img = cv2.imread(target_pic_name)
        img2 = cv2.imread(self.ScreenCapture())
        w, h = img.shape[1], img.shape[0]
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED) 
        location = numpy.where(result >= 0.8)
        data = list(zip(*location[::-1]))
        is_match = len(data) > 0
        if is_match:
            x, y = data[0][0], data[0][1]  
            return x + int(w/2), y + int(h/2)
        else:
            return False, False
    def TapImage(self, pathImg):
        x, y = self.FindImg(pathImg)
        if x:
            print(x,y)
            self.Click(x, y)
    def TapXml(self, xpath, index=0):
        pos = self.GetPosXml(xpath)
        if pos != []:
            pos = pos[index]
            self.Click(pos[0], pos[1])
    def KeyEvent(self, key):
        self.AdbLd(f"shell input keyevent {str(key)}")
    def DeleteCache(self, package):
        self.AdbLd(f"shell pm clear {package}")
    def OpenTikTokLite(self):
        print(self.AdbLd('shell am start -a android.intent.action.VIEW -d snssdk1233://notification com.zhiliaoapp.musically.go'))
        # while True:
        #     print("Đang mở")
        #     open = self.AdbLd('shell am start -a android.intent.action.VIEW -d snssdk1233://notification com.zhiliaoapp.musically.go')
        #     print(open)
        #     if 'error' in open:
        #         if 'error' not in self.AdbLd('shell am start -a android.intent.action.VIEW -d snssdk1233://notification com.zhiliaoapp.musically.go'): return
        #     else:
        #         break
        # print("Mở App")
    def ChangeInfo(self):
        model = random.choice(['Samsung E2100B', 'Samsung B5702', 'Samsung B520', 'Samsung C5212', 'Samsung W259 Duos', 'Samsung SCH-W699', 'Samsung S3030 Tobi', 'Samsung W299 Duos', 'Samsung S9402 Ego', 'Samsung U810 Renown', 'Samsung i770 Saga', 'Samsung A867 Eternity', 'Samsung A777', 'Samsung T919 Behold', 'Samsung T459 Gravity', 'Samsung E2510', 'Samsung T219', 'Samsung E1410', 'Samsung T119', 'Samsung E1117', 'Samsung i907 Epix', 'Samsung E1110', 'Samsung C6620', 'Samsung A767 Propel', 'Samsung C510', 'Samsung M3200 Beat s', 'Samsung S3600', 'Samsung M7500 Emporio Armani', 'Samsung F270 Beat', 'Samsung i7110', 'Samsung F275', 'Samsung M8800 Pixon', 'Samsung T339', 'Samsung T229', 'Samsung A637', 'Samsung A837 Rugby', 'Samsung B210', 'Samsung A237', 'Samsung B320', 'Samsung M3510 Beat b', 'Samsung P270', 'Samsung M200', 'Samsung F268', 'Samsung B2700', 'Samsung T109', 'Samsung E200 ECO', 'Samsung D980', 'Samsung B510', 'Samsung E215', 'Samsung B130', 'Samsung i8510 INNOV8', 'Samsung S7330', 'Samsung i740', 'Asus PadFone 2', 'ZTE Blade V', "HTC EndeavorU", "Samsung GT-P3100", "Asus ME173X", "Sony C5302"]).replace(" ", "_")
        dauso = """8486+8496+8497+8498+8432+8433+8434+8435+8436+8437+8438+8439""".split("+")
        # self.Change_Property('--cpu 1 --memory 1024 --manufacturer %s --model %s --imei auto --pnumber %s --androidid auto --mac auto --simserial auto --imsi auto')
        print("Change")
        print(self.ChangeProperty(f'--cpu 2 --memory 4096 --manufacturer {model.split("_")[0]} --model {model} --resolution 360,600,160 --imei auto --pnumber +"{random.choice(dauso)}{random.randint(1000000, 9999999)}" --androidid auto --mac auto --simserial auto --imsi auto'))
        string = ""
        char = "qwertyuiopasdfghmcnvxbcz"
        for i in range(10):
            string += char[random.randint(0, len(char)-1)]
        self.Rename(string)
        return self.GetDevices()[int(self.NameOrId)]
    def Start(self):
        self.ExecuteLD(f"launch --{self.param} {self.NameOrId}")
    def OpenApp(self, Package_Name):
       self.ExecuteLD(f"launchex --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def StopApp(self, Package_Name):
       self.ExecuteLD(f"killapp --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def Close(self):
        self.ExecuteLD(f"quit --{self.param} {self.NameOrId}")
    def CloseAll(self):
        self.ExecuteLD(f"quitall")
    def Reboot(self):
        self.ExecuteLD(f"reboot --{self.param} {self.NameOrId}")
    def Create(self, Name):
        print(self.ExecuteLD(f"add --name {Name}"))
    def Copy(self, Name, From_NameOrId):
        self.ExecuteLD(f"copy --name {Name} --from {From_NameOrId}")
    def Remove(self):
        self.ExecuteLD(f"remove --{self.param} {self.NameOrId}")
    def Rename(self, title_new):
        self.ExecuteLD(f"rename --{self.param} {self.NameOrId} --title {title_new}")
    def InstallAppFile(self, path):
        self.AdbLd(f'-e install {path}')
        # self.ExecuteLD(f'installapp --{self.param} {self.NameOrId} --filename "{path}"')
    def CheckInstalled(self, package):
        if package in str(self.AdbLd("shell pm list packages")): return True
        return False
    def InstallAppPackage(self, Package_Name):
        
        self.ExecuteLD(f"installapp --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def UnInstallApp(self, Package_Name):
        self.ExecuteLD(f"uninstallapp --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def RunApp(self, Package_Name):
        self.ExecuteLD(f"runapp --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def KillApp(self, Package_Name):
        self.ExecuteLD(f"killapp --{self.param} {self.NameOrId} --packagename {Package_Name}")
    def Locate(self, Lng, Lat):
        self.ExecuteLD(f"locate --{self.param} {self.NameOrId} --LLI {Lng},{Lat}")
    def ChangeProperty(self, cmd):
        return self.ExecuteLD(f"modify --{self.param} {self.NameOrId} {cmd}")
    def SetProp(self, key, value):
        self.ExecuteLD(f"setprop --{self.param} {self.NameOrId} --key {key} --value {value}")
    def InstallAGetPropppPackage(self, key):
        return self.ExecuteLD(f"getprop --{self.param} {self.NameOrId} --key {key}")
    def AdbLd(self, cmd):
        return self.ExecuteLD(f'adb --{self.param} {self.NameOrId} --command "{cmd}"')
    def DownCPU(self, rate):
        self.ExecuteLD(f"downcpu --{self.param} {self.NameOrId} --rate {rate}")
    def IsDevice_Running(self):
        a = self.ExecuteLD(f"isrunning --{self.param} {self.NameOrId}")
        if "running"  in str(a):
            return True
        else:
            return False
    def DownCPU(self, audio, fast_play, clean_mode):
        self.ExecuteLD(f"globalsetting --{self.param} {self.NameOrId} --audio {audio} --fastplay {fast_play} --cleanmode {clean_mode}")
    def GetDevices(self):
        list = str(self.ExecuteLD(f"list")).replace("b'","").replace("'","").replace('\n', '').split("\\r\\n")
        return list
    def GetDevices2(self):
        list2 = str(self.ExecuteLD(f"list2")).replace("b'","").replace("'","").replace('\n', '').split("\\r\\n")
        Info_Devices = []
        for i in list2:
            if i == "":
                continue
            item = i.split(",")
            Info_Devices.append({"name":item[1],"index":item[0],"id":"-1"})
        return Info_Devices
    def kk(index):
        l = LDPlayer()
        for i in range(10):
            l.Info('index', index)
            l.ChangeInfo()
            time.sleep(10)

    threading.Thread(target=kk, args=("0",)).start()
