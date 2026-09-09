![image](https://user-images.githubusercontent.com/75980500/109956689-d6e5d280-7cdb-11eb-86be-c853000a5b7e.png)


https://bian.org/

https://portal.bian.org/ 

شبکه معماری صنعت بانکداری (BIAN) یک شرکت غیرانتفاعی و مشارکتی است که شامل بانک‌های پیشرو، ارائه‌دهندگان فناوری، مشاوران و دانشگاهیان از سراسر جهان می‌شود.

این شبکه از متخصصان با هم به کاهش هزینه های بانکداری و افزایش سرعت نوآوری در صنعت اختصاص دارد. اعضا تخصص صنعت خود را ترکیب می‌کنند تا چارچوب فناوری بانکداری انقلابی را تعریف کنند که معماری اصلی بانکداری را که معمولاً پیچیده و قدیمی است، استاندارد و ساده می‌کند. بر اساس اصول معماری سرویس‌گرا، مدل جامع راه‌حلی برای بانک‌ها برای آینده ارائه می‌کند که همکاری صنعت را تقویت می‌کند.


**پرتال BIAN**

پورتال BIAN با دسترسی به مدل ها و API ها در آدرس زیر قابل دسترسی است: https://portal.bian.org/


---

## 🇮🇷 نسخه بومی‌سازی شده برای صنعت بانکداری ایران (BIAN-Iran)

در این مخزن، استاندارد بین‌المللی BIAN برای اولین بار بر اساس الزامات، مقررات و سامانه‌های متمرکز **بانک مرکزی جمهوری اسلامی ایران**، قانون عملیات بانکی بدون ربا و شبکه پرداخت کشور بومی‌سازی شده است.

### مستندات مرجع و راهنماها:
1. **[واژه‌نامه تخصصی و اصطلاح‌نامه BIAN به فارسی](docs/bian-iran-lexicon.md):** معادل‌های استاندارد مفاهیم دامنه‌های سرویس، رکوردهای کنترلی و افعال عملیاتی.
2. **[ماتریس انطباق با سامانه‌های بانک مرکزی](docs/cbi-regulatory-mapping.md):** نگاشت دامنه‌ها با سامانه‌های نهاب، شتاب، شاپرک، پایا، ساتنا، پل، صیاد، چکاد، سیاح و سمات.
3. **[متدولوژی و راهنمای بومی‌سازی دامنه‌ها](docs/bian-iran-methodology.md):** فرآیند ۵ مرحله‌ای بومی‌سازی سایر دامنه‌های سرویس BIAN برای ایران.

### ساختار فایل‌های بومی‌سازی شده نسخه ۱۴.۰.۰ (`bian-iran/release14.0.0/`):
تمامی **۱۰۳۲ فایل مشخصات فنی (OpenAPI و AsyncAPI)** به همراه مولفه‌های مشترک هسته بانکداری ایران به زبان فارسی و با تگ‌های نظارتی بانک مرکزی بومی‌سازی شده‌اند:

* **مولفه‌های پایه و مشترک (`common/`):**
  * [`iran-banking-core.yaml`](bian-iran/release14.0.0/common/iran-banking-core.yaml): کد ملی، شناسه حقوقی، شناسه شهاب (نهاب)، شماره شبا، شماره کارت، شناسه صیادی، تقویم جلالی و مبالغ ریالی.
  * [`islamic-contracts.yaml`](bian-iran/release14.0.0/common/islamic-contracts.yaml): عقود اسلامی (مرابحه، مضاربه، جعاله، قرض‌الحسنه و...)، تضامین، سفته الکترونیک و جداول اقساط.
  * [`error-codes.yaml`](bian-iran/release14.0.0/common/error-codes.yaml): کدهای خطای شبکه شتاب و شاپرک و قالب استاندارد ProblemDetails.

* **مجموعه دامنه‌های بومی‌سازی شده (۱۰۳۲ فایل):**
  1. **APIهای معنایی OpenAPI 3.x:** ۲۵۸ دامنه سرویس بومی‌شده در مسیر [`bian-iran/release14.0.0/semantic-apis/oas3/yamls/`](bian-iran/release14.0.0/semantic-apis/oas3/yamls/)
  2. **APIهای معنایی AsyncAPI 3.x:** ۲۵۸ فایل رویدادمحور در مسیر [`bian-iran/release14.0.0/semantic-apis/asyncapi-3.x/yamls/`](bian-iran/release14.0.0/semantic-apis/asyncapi-3.x/yamls/)
  3. **APIهای توسعه‌یافته ISO 20022 (OpenAPI):** ۲۵۸ دامنه سرویس در مسیر [`bian-iran/release14.0.0/apis-iso20022_ext-ddd/oas3/yamls/`](bian-iran/release14.0.0/apis-iso20022_ext-ddd/oas3/yamls/)
  4. **APIهای توسعه‌یافته ISO 20022 (AsyncAPI):** ۲۵۸ دامنه سرویس در مسیر [`bian-iran/release14.0.0/apis-iso20022_ext-ddd/asyncapi-3.x/yamls/`](bian-iran/release14.0.0/apis-iso20022_ext-ddd/asyncapi-3.x/yamls/)

* **دامنه‌های پایلوت با پیاده‌سازی عمیق اختصاصی (`service-domains/`):**
  * [`CurrentAccount.yaml`](bian-iran/release14.0.0/service-domains/CurrentAccount.yaml): **حساب قرض‌الحسنه جاری** (نهاب، صیاد، چکاد، سیاح).
  * [`ConsumerLoan.yaml`](bian-iran/release14.0.0/service-domains/ConsumerLoan.yaml): **تسهیلات خرد** (عقود اسلامی، سمات، سفته الکترونیک، تقسیط).
  * [`PaymentOrderInitiation.yaml`](bian-iran/release14.0.0/service-domains/PaymentOrderInitiation.yaml): **دستور پرداخت** (انتقال داخلی، سامانه پل، پایا و ساتنا).
  * [`CardAuthorization.yaml`](bian-iran/release14.0.0/service-domains/CardAuthorization.yaml): **مجوزدهی تراکنش کارت** (رمز دوم پویا، شاهکار، سوئیچ شتاب/شاپرک).

### ابزارهای اعتبارسنجی و بومی‌سازی:
```bash
# اعتبارسنجی سینتکس و ساختار تمام فایل‌ها
python tests/validate_openapi.py
python tests/test_docs.py

# خط‌لوله بازتولید و بومی‌سازی
python scripts/localize_release14.py
```

---

**دانلود - ارتباط برنامه‌نویسی معنایی BIAN*


نسخه 14.0.0:
1. نسخه 14.0.0 - API های توسعه یافته BOM (OAS 3.x): https://github.com/bian-official/public/tree/main/release14.0.0/semantic-apis/oas3%20/yamls
2. نسخه 14.0.0 - API توسعه یافته ISO20022 و حاشیه نویسی برای DD (OAS 3.x): https://github.com/bian-official/public/tree/main/release14.0.0/apis-iso20022_ext-ddd/oas3/ya
3. نسخه 14.0.0 - API های توسعه یافته BOM (Async 3.x): https://github.com/bian-official/public/tree/main/release14.0.0/semantic-apis/asyncapi-3.x/yamls
4. نسخه 14.0.0 - API های توسعه یافته ISO20022 و حاشیه نویسی شده برای DDD (Async 3.x): https://github.com/bian-official/public/tree/main/release14.0.0/apis-iso20022_ext-dd-s/asyncapi


نسخه 13.0.0:
1. نسخه 13.0.0 - API های توسعه یافته BOM (OAS 3.x): https://github.com/bian-official/public/tree/main/release13.0.0/semantic-apis/oas3/yamls
2. نسخه 13.0.0 - API توسعه یافته ISO20022 و حاشیه نویسی برای DD (OAS 3.x): https://github.com/bian-official/public/tree/main/release13.0.0/apis-iso20022_ext-ddd/oas3/ya
3. نسخه 13.0.0 - API های توسعه یافته BOM (Async 3.x): https://github.com/bian-official/public/tree/main/release13.0.0/semantic-apis/asyncapi-3.x/yamls
4. نسخه 13.0.0 - ISO20022 توسعه API و حاشیه نویسی برای DDD (Async 3.x): https://github.com/bian-official/public/tree/main/release13.0.0/apis-iso20022_ext-ddd/asyncapi-s


نسخه 12.0.0:
1. نسخه 12.0.0 - API های توسعه یافته BOM (OAS 3.x): https://github.com/bian-official/public/tree/main/release12.0.0/semantic-apis/oas3/yamls
2. نسخه 12.0.0 - API توسعه یافته ISO20022 و حاشیه‌نویسی برای DD (OAS 3.x): https://github.com/bian-official/public/tree/main/release12.0.0/apis-iso20022_ext-ddd/oas3/ya
3. نسخه 12.0.0 - API های توسعه یافته BOM (Async 3.x): https://github.com/bian-official/public/tree/main/release12.0.0/semantic-apis/asyncapi-3.x/yamls
4. نسخه 12.0.0 - ISO20022 توسعه API و حاشیه نویسی برای DDD (Async 3.x): https://github.com/bian-official/public/tree/main/release12.0.0/apis-iso20022_ext-ddd/asyncapi-s

انتشارات قبلی:
1. نسخه 11.0.0 (OAS 3.x): https://github.com/bian-official/public/tree/main/release11.0.0/semantic-apis/oas3/yamls
2. نسخه 10.0.0 (OAS 3.x): https://github.com/bian-official/public/tree/main/release10.0.0/semantic-apis/oas3/yamls
3. نسخه 9.1.0 (Swagger 2.x): https://github.com/bian-official/public/tree/main/release9.1/semantic-apis/swaggers

هر یک از مشخصات API نشان دهنده یک دامنه خدمات BIAN است.




**مشارکت کنید**

1. با نام کاربری خود وارد GitHub شوید _
2. روی دکمه "Fork" در گوشه سمت راست بالا کلیک کنید. این یک کپی از مخزن ایجاد می کند که می توانید آن را دانلود و تغییر دهید.
3. ابزارهای کلاینت Git لازم را نصب کنید، برای مثال، کلاینت گیت را برای سیستم عامل خود از اینجا دانلود کنید https://git-scm.com/downloads و اجرا کنید.
4. از دستور git clone برای کلون کردن مخزن فورکی که ایجاد کرده است در رایانه محلی خود استفاده کنید. چیزی شبیه به این خواهد بود:
    گیت کلون https://github.com/username/bian-official _myrepository_
    که در آن _username_ نام کاربری GitHub شما و _myrepository_ نامی است که برای مخزن در رایانه خود انتخاب کنید.
5. یک شعبه برای اضافه کردن هر ویژگی جدید ایجاد کنید:
    git checkout -b _mybranch_
    محل که _mybranch_ شاخه جدید شماست.
6. هر ویژگی جدید را به _mybranch_ اضافه کنید
7. مرحله بعدی مرحله بندی، commit کردن و هل دادن فایل های اصلاح شده به مخزن "forked" خود در GitHub است. می توانید از دستورات _git add_، _commit_ و _push_ استفاده کنید. اطلاعات دقیق را می توانید در اینجا بیابید: https://git-scm.com/docs
8. به مخزن فورک خود در GitHub مراجعه کنید و با کلیک بر روی دکمه "درخواست کشش" یک درخواست ارسال کنید.
9. BIAN پیشنهادی در درخواست کشش شما را در گروه های کاری BIAN با اعضای خود بررسی می کند. BIAN ممکن است از آن با سوالات / شفاف سازی ها / پیشنهاداتی برای اصلاحات به شما مراجعه کنید. اگر این تغییرات در گروه‌های کاری BIAN ممکن است، برای ارتقای استانداردهای BIAN استفاده می‌شود و به عنوان بخشی از نسخه‌های برنامه‌ریزی شده آینده منتشر می‌شود.
10. اگر می توانید از چنگال خود به عنوان طعم خود در اجرای استاندارد BIAN استفاده کنید.

---
طراحی و توسعه: alimohammadzadeh@ut.ac.ir
