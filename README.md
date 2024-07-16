![image](https://github.com/user-attachments/assets/eb527e7e-ca11-4309-af16-16db306e1d50)

# ربات تراکنش اتوماتیک برای Sonic Odyssey با سرعت بالا و بدون فلگ شدن.
## این ربات بر اساس پایتون کار میکند و برای استفاده میتوانید مراحل زیر را انجام بدهید .


## 1. ابتدا پایتون را نصب کنید
```
sudo apt install python3
```
## 2. حالا پیشنیاز های اون رو نصب کنید
```
pip install solana==0.18.0
pip install requests
pip install bip39
pip install base58
pip install colorama
pip install pynacl
pip install bip32utils
```

## 3. با دستورات زیر فایل را دانلود کنید
```
git clone https://github.com/xONEIROS/Sonic-Odyssey-auto-transaction-bot.git
cd Sonic-Odyssey-auto-transaction-bot
```

## 4. حالا با دستور زیر فایل های پرایوت کی و سیدفریز را ادیت کنید ( یکیش کافیه )
برای پریاویت کی کافیه کپی کنید و داخل فایل پیست کنید ( هر خط یک والت سپس با کلید ctrl + x و بعدش Y بیاید بیرون
```
nano privateKeys.txt
```
برای سید فریز ها هم برای هر والت توی یک خط قرار بدید و مثل بالا سیو کنید
```
nano accounts.txt
```

## 5. حالا با دستور زیر برنامه رو ران کنید ، بعد از ران کردن ازتون میپرسه برای استفاده از سیدفریز عدد 0 رو وارد کنید و برای پرایویت کی عدد 1 هر کدوم رو در مرحله 4 وارد کردید رو بزنید و بزنید اینتر ، بقیه رو نمیخواد تغییر بدید و فقط بزنید اینتر تا فرایند براتون شروع شه .
```
python3 main.py
```
> -------------------------------

# اگر میخواهید با استفاده از سایت [replit](https://replit.com/) این مراحل رو انجام بدید کافیه این ویدئو آموزشی رو ببینید

https://github.com/user-attachments/assets/f65e06bf-2a79-445a-a8ec-70cab31a231a


