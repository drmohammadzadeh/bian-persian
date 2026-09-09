"""
Script to generate comprehensive Persian README.md files for bian-iran and all its subdirectories.
"""

import sys
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

READMES = {
    ROOT / "bian-iran" / "README.md": """# بومی‌سازی BIAN برای صنعت بانکداری ایران (BIAN-Iran)

به بخش بومی‌سازی شده **شبکه معماری صنعت بانکداری (BIAN)** برای اکوسیستم بانکی و مالی جمهوری اسلامی ایران خوش آمدید.

---

## 🎯 هدف و مأموریت
استاندارد بین‌المللی BIAN یک چارچوب معماری سرویس‌گرا (SOA) و استاندارد تعاریف معنایی برای بانک‌ها است. در این بخش، این استاندارد متناسب با:
1. **قوانین و مقررات بانک مرکزی جمهوری اسلامی ایران (CBI):** اتصال و انطباق با سامانه‌های حاکمیتی متمرکز (شتاب، شاپرک، پایا، ساتنا، پل، صیاد، نهاب، سیاح، سمات، چکاد و مانا).
2. **قانون عملیات بانکی بدون ربا:** تعریف و مدل‌سازی عقود اسلامی (مرابحه، مضاربه، جعاله، قرض‌الحسنه، مشارکت مدنی و...) به جای بهره سنتی.
3. **ساختارهای داده‌ای بومی:** پشتیبانی از کد ملی، شناسه ملی حقوقی، شناسه شهاب، شماره شبا، تاریخ هجری شمسی (جلالی) و مبالغ ریالی.

---

## 📁 ساختار پوشه‌های این بخش:
* **[`release14.0.0/`](release14.0.0/README.md):** جدیدترین نسخه BIAN (نسخه ۱۴.۰.۰) با بومی‌سازی جامع بیش از ۱۰۴۰ فایل مشخصات فنی (OpenAPI و AsyncAPI) و مولفه‌های مشترک هسته بانکداری ایران.

---

## 📚 پیوندهای اسناد بالادستی:
* [واژه‌نامه تخصصی BIAN به فارسی](../docs/bian-iran-lexicon.md)
* [ماتریس نگاشت با سامانه‌های بانک مرکزی](../docs/cbi-regulatory-mapping.md)
* [متدولوژی ۵ مرحله‌ای بومی‌سازی دامنه‌ها](../docs/bian-iran-methodology.md)
""",

    ROOT / "bian-iran" / "release14.0.0" / "README.md": """# نسخه ۱۴.۰.۰ بومی‌سازی شده BIAN (Release 14.0.0)

این پوشه شامل نسخه کامل و بومی‌سازی‌شده **BIAN Release 14.0.0** برای شبکه بانکی ایران است.

---

## 📦 محتویات این نسخه:

1. **[`common/`](common/README.md):**
   مولفه‌های مشترک هسته بانکداری ایران (انواع داده هویتی نهاب، شماره شبا، تاریخ جلالی، عقود اسلامی، کدهای خطای شتاب و شاپرک).
2. **[`service-domains/`](service-domains/README.md):**
   دامنه‌های سرویس پایلوت با بازمهندسی عمیق و اختصاصی برای Core Banking ایران (حساب جاری، تسهیلات خرد، دستور پرداخت و کارت).
3. **[`semantic-apis/`](semantic-apis/README.md):**
   مشخصات رابط‌های برنامه‌نویسی معنایی BIAN (شامل ۲۵۸ فایل OpenAPI 3.x و ۲۵۸ فایل رویدادمحور AsyncAPI 3.x).
4. **[`apis-iso20022_ext-ddd/`](apis-iso20022_ext-ddd/README.md):**
   مشخصات فنی توسعه‌یافته بر اساس استاندارد جهانی پیام‌های مالی ISO 20022 و طراحی دامنه‌محور (DDD) شامل ۵۱۶ فایل.

---

## 🔍 نحوه اعتبارسنجی فایل‌ها:
تمامی فایل‌های این پوشه با ابزارهای اعتبارسنجی پایتون از نظر سینتکس YAML و ارجاعات `$ref` بررسی و تایید شده‌اند:
```bash
python tests/validate_openapi.py
```
""",

    ROOT / "bian-iran" / "release14.0.0" / "common" / "README.md": """# مولفه‌های پایه و مشترک سیستم بانکی ایران (Common Components)

این دایرکتوری شامل انواع داده، اسکیماها و تعاریف پایه‌ای است که به عنوان بلوک‌های سازنده مشترک (Reusable Core Components) در سراسر دامنه‌های سرویس BIAN مورد ارجاع (`$ref`) قرار می‌گیرند.

---

## 📄 فایل‌های موجود در این پوشه:

### ۱. [`iran-banking-core.yaml`](iran-banking-core.yaml)
شامل انواع داده‌های پایه هویتی، حسابی و زمانی کشور:
* `NationalId`: کد ملی ۱۰ رقمی با الگوریتم کنترلی ثبت احوال.
* `LegalEntityId`: شناسه ملی ۱۱ رقمی اشخاص حقوقی و شرکت‌ها.
* `ShahabId`: شناسه ۱۶ رقمی هویت الکترونیکی بانکی تحت نظارت سامانه نهاب بانک مرکزی.
* `IbanNumber`: شماره ۲۶ کاراکتری شبا (`^IR[0-9]{24}$`).
* `InternalAccountNumber`: شماره حساب داخلی متمرکز.
* `CardPan`: شماره کارت ۱۶ رقمی شتاب با الگوریتم لان (Luhn).
* `SayadChequeId`: شناسه ۱۶ رقمی چک صیادی.
* `Currency`: ریال ایران (`IRR`) و تومان (`IRT`).
* `JalaliDate`: تاریخ تقویم رسمی هجری شمسی (`YYYY/MM/DD`).
* `FinancialAmount`: ساختار نگهداری مبالغ پولی ریالی صحیح.

### ۲. [`islamic-contracts.yaml`](islamic-contracts.yaml)
مدل داده عقود قانون عملیات بانکی بدون ربا و تسهیلات اعتباری:
* `ContractType`: انوم عقود شرعی (مرابحه، مضاربه، جعاله، قرض‌الحسنه، سلف، مشارکت مدنی، اجاره به شرط تملیک، استصناع).
* `IslamicContractDetails`: نرخ سود مصوب، وجه التزام تأخیر تأدیه و اقساط.
* `CollateralType` و `CollateralDetails`: سفته الکترونیک، ضامنین، ترهین ملک و توثیق سپرده/سهام.
* `InstallmentSchedule`: جدول اقساط و سررسیدهای پرداخت شمسی.

### ۳. [`error-codes.yaml`](error-codes.yaml)
کدها و پاسخ‌های استاندارد شبکه تبادل اطلاعات بانکی:
* `ShetabResponseCode`: کدهای استاندارد سوئیچ شتاب و شاپرک (`00` موفق، `51` مانده ناکافی، `55` رمز نامعتبر و...).
* `ProblemDetails`: قالب خطای وب‌سرویس منطبق بر RFC 7807 همراه با شرح فارسی خطای کاربر (`messageFa`).
""",

    ROOT / "bian-iran" / "release14.0.0" / "service-domains" / "README.md": """# دامنه‌های سرویس پایلوت اختصاصی (Pilot Service Domains)

این پوشه شامل دامنه‌های کلیدی Core Banking است که به صورت عمیق، مستقل و منطبق با سامانه متمرکز بانکداری و سامانه‌های حاکمیتی بانک مرکزی ایران طراحی و پیاده‌سازی شده‌اند.

---

## 🏛️ دامنه‌های سرویس پیاده‌سازی شده:

### ۱. [`CurrentAccount.yaml`](CurrentAccount.yaml) - حساب قرض‌الحسنه جاری
* **سامانه‌های متصل:** سامانه نهاب (شهاب) + سامانه صیاد/چکاد + سامانه سیاح (مسدودی حساب).
* **عملیات اصلی:**
  * افتتاح حساب جاری (`POST /CurrentAccount/Initiate`) با استعلام نهاب و تخصیص شبا.
  * درخواست دسته چک صیادی (`POST /CurrentAccount/{accountId}/ChequeFacility/Request`).
  * اعمال مسدودی قضایی سیاح (`POST /CurrentAccount/{accountId}/Lien/Apply`).
  * رفع مسدودی حساب (`DELETE /CurrentAccount/{accountId}/Lien/{lienId}/Release`).
  * دریافت صورتحساب با تاریخ شمسی (`GET /CurrentAccount/{accountId}/Statement`).

### ۲. [`ConsumerLoan.yaml`](ConsumerLoan.yaml) - تسهیلات خرد بانکی
* **سامانه‌های متصل:** عقود اسلامی + سامانه سمات بانک مرکزی + سفته الکترونیک خزانه‌داری.
* **عملیات اصلی:**
  * ثبت پرونده تسهیلاتی بر مبنای عقود اسلامی (`POST /ConsumerLoan/Initiate`).
  * استعلام سوابق و بدهی‌های معوق از سمات (`POST /ConsumerLoan/{loanId}/CreditAssessment`).
  * ثبت تضامین و سفته الکترونیک (`POST /ConsumerLoan/{loanId}/Collateral/Register`).
  * واریز وجه تسهیلات و تقسیط (`POST /ConsumerLoan/{loanId}/Disbursement`).
  * دریافت جدول اقساط شمسی (`GET /ConsumerLoan/{loanId}/InstallmentSchedule`).

### ۳. [`PaymentOrderInitiation.yaml`](PaymentOrderInitiation.yaml) - دستور پرداخت بین‌بانکی
* **سامانه‌های متصل:** سامانه‌های پایا، ساتنا، پل و انتقال وجه داخلی.
* **عملیات اصلی:**
  * ثبت و هدایت هوشمند پرداخت بر بستر شبا (`POST /PaymentOrder/Initiate`).
  * کنترل سقف‌های مجاز تراکنش روزانه بانک مرکزی (`POST /PaymentOrder/ValidateLimits`).
  * استعلام وضعیت انتقال با کد پیگیری یکتا (`GET /PaymentOrder/{paymentId}/Status`).

### ۴. [`CardAuthorization.yaml`](CardAuthorization.yaml) - مجوزدهی تراکنش کارت
* **سامانه‌های متصل:** سوئیچ صادرکنندگی شتاب + شبکه شاپرک + سامانه شاهکار.
* **عملیات اصلی:**
  * احراز هویت دارنده کارت با رمز پویا/هدی و تطابق شاهکار (`POST /CardAuthorization/Authorize`).
  * کنترل موجودی و بررسی سقف برداشت روزانه (`POST /CardAuthorization/VerifyBalance`).
  * پردازش عملیات برگشت تراکنش / اصلاحیه شتابی (`POST /CardAuthorization/Reverse`).
""",

    ROOT / "bian-iran" / "release14.0.0" / "semantic-apis" / "README.md": """# رابط‌های برنامه‌نویسی معنایی BIAN (Semantic APIs)

این پوشه شامل رابط‌های برنامه‌نویسی استاندارد معنایی **BIAN BOM (Business Object Model)** نسخه ۱۴ است که برای تمامی دامنه‌های عملکردی بانکداری بومی‌سازی شده‌اند.

---

## 📂 زیرشاخه‌ها:
* **[`oas3/`](oas3/README.md):** مشخصات مبتنی بر پروتکل وب و RESTful در قالب OpenAPI 3.x.
* **[`asyncapi-3.x/`](asyncapi-3.x/README.md):** مشخصات رویدادمحور بر بستر صف‌های پیام در قالب AsyncAPI 3.x.
""",

    ROOT / "bian-iran" / "release14.0.0" / "semantic-apis" / "oas3" / "README.md": """# مشخصات OpenAPI 3.x برای APIهای معنایی BIAN

این پوشه حاوی مشخصات رابط‌های برنامه‌نویسی وب RESTful استاندارد BIAN نسخه ۱۴ منطبق با استاندارد **OpenAPI 3.0** است.

---

## 📂 زیرشاخه‌ها:
* **[`yamls/`](yamls/README.md):** شامل ۲۵۸ فایل مشخصات فنی دامنه‌های سرویس در قالب فایل‌های YAML معتبر، همراه با عناوین، توضیحات و اکستنشن‌های بومی ایران.
""",

    ROOT / "bian-iran" / "release14.0.0" / "semantic-apis" / "oas3" / "yamls" / "README.md": """# مشخصات YAML دامنه‌های معنایی OpenAPI 3.x

این پوشه شامل **۲۵۸ دامنه سرویس معنایی BIAN نسخه ۱۴.۰.۰** در قالب فایل‌های OpenAPI 3.x (YAML) است.

---

## 🌟 ویژگی‌های بومی‌سازی در این فایل‌ها:
1. **عناوین دوزبانه:** هدر `info.title` با معادل استاندارد فارسی غنی‌سازی شده است.
2. **توضیحات و نقش بانکی:** شرح کارکرد هر دامنه در سیستم بانکی ایران به `info.description` اضافه شده است.
3. **اکستنشن‌های نظارتی:**
   * `x-persian-title`: عنوان رسمی فارسی دامنه.
   * `x-persian-description`: شرح کارکرد دامنه به فارسی.
   * `x-cbi-system`: سامانه متمرکز مرتبط در بانک مرکزی ایران (شتاب، شاپرک، نهاب، صیاد، پایا، ساتنا، سمات، سیاح و...).
   * `x-bian-standard`: شناسه استاندارد بومی `BIAN-Iran v14.0.0`.
4. **بومی‌سازی ترم‌های عملیاتی:** درج ترجمه افعال استاندارد (`Initiate`، `Execute`، `Control`، `Retrieve` و...) در خلاصه عملیات‌ها.
""",

    ROOT / "bian-iran" / "release14.0.0" / "semantic-apis" / "asyncapi-3.x" / "README.md": """# مشخصات رویدادمحور AsyncAPI 3.x برای APIهای معنایی BIAN

این پوشه شامل مشخصات معماری رویدادمحور (Event-Driven Architecture) استاندارد BIAN نسخه ۱۴ منطبق با مشخصات **AsyncAPI 3.x** است.

---

## 📂 زیرشاخه‌ها:
* **[`yamls/`](yamls/README.md):** شامل ۲۵۸ فایل مشخصات کانال‌ها، رویدادها و پیام‌های ناهمگام دامنه‌های سرویس بانکی.
""",

    ROOT / "bian-iran" / "release14.0.0" / "semantic-apis" / "asyncapi-3.x" / "yamls" / "README.md": """# مشخصات YAML رویدادمحور AsyncAPI 3.x

این دایرکتوری حاوی **۲۵۸ فایل رویدادمحور AsyncAPI 3.x (YAML)** برای تبادل ناهمگام پیام‌ها در زیرساخت‌های صف و گذرگاه داده (Message Brokers مانند Apache Kafka, RabbitMQ) در بانکداری ایران است.

---

## 🌟 ویژگی‌های بومی‌سازی:
* عناوین دوزبانه فارسی و انگلیسی در کانال‌های پیام.
* الصاق اکستنشن‌های `x-persian-title`، `x-persian-description` و `x-cbi-system`.
* تشریح کانال‌های انتشار و اشتراک رویدادهای مالی و تغییرات موجودی.
""",

    ROOT / "bian-iran" / "release14.0.0" / "apis-iso20022_ext-ddd" / "README.md": """# مشخصات توسعه‌یافته ISO 20022 و طراحی دامنه‌محور (DDD)

این پوشه شامل مشخصات فنی BIAN نسخه ۱۴ است که بر پایه استاندارد بین‌المللی پیام‌رسانی مالی **ISO 20022** توسعه یافته و بر اساس متدولوژی **طراحی دامنه‌محور (Domain-Driven Design - DDD)** حاشیه‌نویسی شده است.

---

## 📂 زیرشاخه‌ها:
* **[`oas3/`](oas3/README.md):** مشخصات OpenAPI 3.x منطبق با ساختار پیام‌های ISO 20022.
* **[`asyncapi-3.x/`](asyncapi-3.x/README.md):** مشخصات AsyncAPI 3.x منطبق با ساختار پیام‌های ISO 20022.
""",

    ROOT / "bian-iran" / "release14.0.0" / "apis-iso20022_ext-ddd" / "oas3" / "README.md": """# مشخصات OpenAPI 3.x توسعه‌یافته با ISO 20022

این بخش شامل مشخصات وب‌سرویس‌های همگام (RESTful) است که مدل‌های داده‌ای پیام‌های مالی ISO 20022 (مانند استانداردهای پایا و ساتنا) را به ساختارهای BIAN متصل می‌کند.

---

## 📂 زیرشاخه‌ها:
* **[`yamls/`](yamls/README.md):** شامل ۲۵۸ فایل مشخصات فنی دامنه‌های سرویس توسعه‌یافته با ISO 20022.
""",

    ROOT / "bian-iran" / "release14.0.0" / "apis-iso20022_ext-ddd" / "oas3" / "yamls" / "README.md": """# مشخصات YAML دامنه‌های توسعه‌یافته با ISO 20022 (OpenAPI 3.x)

این دایرکتوری شامل **۲۵۸ دامنه سرویس BIAN** است که با مدل داده‌های استاندارد پیام‌رسانی بین‌المللی ISO 20022 غنی‌سازی شده و برای سیستم بانکی ایران بومی‌سازی شده‌اند.

---

## 🌟 ویژگی‌های بومی‌سازی:
* تلفیق استانداردهای پیام‌رسانی بین‌بانکی پایا و ساتنا (ISO 20022 pacs/pain) با مدل‌های داده BIAN.
* درج عناوین و توضیحات فارسی تخصصی به همراه تگ سامانه ناظر بانک مرکزی.
* سازگاری ۱۰۰٪ با ابزارهای تولید کد و Swagger UI.
""",

    ROOT / "bian-iran" / "release14.0.0" / "apis-iso20022_ext-ddd" / "asyncapi-3.x" / "README.md": """# مشخصات AsyncAPI 3.x توسعه‌یافته با ISO 20022

این بخش مشخصات تبادل رویدادهای مالی بر بستر پیام‌های استاندارد ISO 20022 را به صورت ناهمگام (AsyncAPI) ارائه می‌کند.

---

## 📂 زیرشاخه‌ها:
* **[`yamls/`](yamls/README.md):** شامل ۲۵۸ فایل مشخصات کانال‌ها و پیام‌های رویدادمحور ISO 20022.
""",

    ROOT / "bian-iran" / "release14.0.0" / "apis-iso20022_ext-ddd" / "asyncapi-3.x" / "yamls" / "README.md": """# مشخصات YAML رویدادمحور ISO 20022 (AsyncAPI 3.x)

این دایرکتوری حاوی **۲۵۸ فایل مشخصات فنی AsyncAPI 3.x** است که پیام‌ها و رویدادهای ناهمگام بانکی را با ساختار پیام‌های ISO 20022 و متدولوژی DDD در اختیار تیم‌های معماری و توسعه سیستم‌های متمرکز و پرداخت کشور قرار می‌دهد.

---

## 🌟 ویژگی‌های بومی‌سازی:
* ترجمه و بومی‌سازی تعاریف کانال‌ها و پیام‌های بانکی.
* الصاق تگ‌های سامانه‌های پایا، ساتنا و سپام در هدرهای مشخصات.
"""
}

def main():
    print(f"Generating {len(READMES)} README.md files across bian-iran hierarchy...")
    for path, content in READMES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Check if Readme.md (different case) exists in the directory, and overwrite it cleanly
        target_name = path.name
        existing_files = list(path.parent.glob("readme.md")) + list(path.parent.glob("Readme.md")) + list(path.parent.glob("README.md"))
        for ef in existing_files:
            if ef.name != target_name:
                try:
                    ef.unlink()
                except Exception:
                    pass

        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"  + Created: {path.relative_to(ROOT)}")

    print(f"\nAll {len(READMES)} README.md files generated successfully!")

if __name__ == "__main__":
    main()
