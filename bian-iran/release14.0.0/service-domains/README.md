# دامنه‌های سرویس پایلوت اختصاصی (Pilot Service Domains)

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

---
طراحی و توسعه: alimohammadzadeh@ut.ac.ir
