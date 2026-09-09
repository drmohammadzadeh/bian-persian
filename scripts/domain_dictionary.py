"""
BIAN Domain Persian Dictionary and Taxonomy Mapper
Provides Persian titles, descriptions, and Central Bank of Iran system mappings
for all 258 Service Domains of BIAN release 14.0.0.
"""

import re

# Explicit mappings for primary banking service domains
PRIMARY_DOMAIN_MAP = {
    "CurrentAccount": {
        "title": "حساب قرض‌الحسنه جاری",
        "description": "مدیریت حساب جاری، صدور دسته‌چک صیاد/چکاد، مسدودی قضایی سیاح و صورتحساب با تاریخ شمسی.",
        "cbi_system": "CoreBanking / Sayad / Sayyah / Nehab"
    },
    "ConsumerLoan": {
        "title": "تسهیلات خرد و عقود اسلامی",
        "description": "مدیریت پرونده‌های تسهیلات انفرادی در چارچوب قانون عملیات بانکی بدون ربا، استعلام سمات و سفته الکترونیک.",
        "cbi_system": "CoreBanking / Samat"
    },
    "PaymentOrderInitiation": {
        "title": "دستور پرداخت بین‌بانکی",
        "description": "هدایت پرداخت‌های ریالی به سامانه‌های پایا، ساتنا، پل و انتقال داخلی با کنترل سقف‌های روزانه بانک مرکزی.",
        "cbi_system": "Paya / Satna / Pol / CoreBanking"
    },
    "CardAuthorization": {
        "title": "مجوزدهی تراکنش کارت و سوئیچ شتاب",
        "description": "احراز هویت دارنده کارت (رمز پویا، هدی، CVV2)، کنترل مانده و ارتباط با شبکه شتاب و شاپرک.",
        "cbi_system": "Shetab / Shaparak / Shahkar"
    },
    "ATMNetworkOperations": {
        "title": "عملیات شبکه خودپرداز (ATM)",
        "description": "راهبری و پایش ناوگان پایانه‌های خودپرداز بانکی، مدیریت کاست‌های وجه نقد و اتصال به شبکه شتاب.",
        "cbi_system": "Shetab / ATM Network"
    },
    "CardTransactionSwitch": {
        "title": "سوئیچ تبادل تراکنش‌های کارتی",
        "description": "سوئیچینگ تراکنش‌های کارت‌های بانکی، هدایت پیام‌های شتابی ISO 8583 و پایش برخط تراکنش‌ها.",
        "cbi_system": "Shetab / Switch"
    },
    "MerchantAcquiringFacility": {
        "title": "پذیرندگی کارت و شبکه شاپرک",
        "description": "مدیریت پذیرندگان، پایانه‌های فروشگاهی (POS) و درگاه‌های پرداخت اینترنتی (IPG) تحت نظارت شاپرک.",
        "cbi_system": "Shaparak"
    },
    "ChequeProcessing": {
        "title": "پردازش و تسویه چک (سامانه صیاد و چکاد)",
        "description": "عملیات چکاوک، استعلام شناسه صیادی ۱۶ رقمی، اعتبارسنجی صادرکننده، ثبت و انتقال چک الکترونیک.",
        "cbi_system": "Sayad / Chakad / Chakavak"
    },
    "PartyLifecycleManagement": {
        "title": "مدیریت چرخه عمر مشتری و سامانه نهاب",
        "description": "تشکیل پروفایل مشتری (CIF)، تطابق با ثبت احوال و اخذ شناسه ۱۶ رقمی شهاب از سامانه متمرکز نهاب بانک مرکزی.",
        "cbi_system": "Nehab / Registry"
    },
    "PartyAuthentication": {
        "title": "احراز هویت مشتری و سامانه شاهکار",
        "description": "احراز هویت بیومتریک، امضای دیجیتال نماد، و استعلام تطابق کد ملی با شماره همراه در سامانه شاهکار.",
        "cbi_system": "Shahkar / Namad / Identity"
    },
    "BankGuarantee": {
        "title": "ضمانت‌نامه بانکی و سامانه سپام",
        "description": "صدور، تمدید، ابطال و پرداخت ضمانت‌نامه‌های ریالی و ارزی و ثبت در سامانه پیام‌رسانی الکترونیکی مالی (سپام).",
        "cbi_system": "Sepam / TradeFinance"
    },
    "LetterofCredit": {
        "title": "اعتبار اسنادی (LC) و سامانه نیما",
        "description": "گشایش، اصلاح، معامله و تسویه اعتبارات اسنادی وارداتی و صادراتی با ثبت در سامانه ارزی نیما و سپام.",
        "cbi_system": "Nima / Sepam / TradeFinance"
    },
    "SavingsAccount": {
        "title": "حساب قرض‌الحسنه پس‌انداز",
        "description": "مدیریت حساب‌های پس‌انداز، شرکت در قرعه‌کشی سالانه قرض‌الحسنه و افتتاح حساب با شناسه شهاب نهاب.",
        "cbi_system": "CoreBanking / Nehab"
    },
    "TermDeposit": {
        "title": "سپرده سرمایه‌گذاری مدت‌دار",
        "description": "افتتاح سپرده‌های کوتاه‌مدت و بلندمدت، محاسبه سود علی‌الحساب ماهانه مصوب شورای پول و اعتبار و مسدودی سیاح.",
        "cbi_system": "CoreBanking / Sayyah"
    },
    "DirectDebit": {
        "title": "برداشت مستقیم و سامانه مانا",
        "description": "مدیریت مجوزهای برداشت مستقیم دوره‌ای از حساب مشتری با اتصال به سامانه مانا بانک مرکزی.",
        "cbi_system": "Mana / DirectDebit"
    },
    "CreditFacility": {
        "title": "تسهیلات و حد اعتباری",
        "description": "تخصیص حد اعتباری، کارت‌های اعتباری مرابحه، کنترل سقف‌های مجاز و اعتبارسنجی شرکت‌ها و اشخاص.",
        "cbi_system": "Samat / CoreBanking"
    },
    "CorporateLoan": {
        "title": "تسهیلات شرکتی و تسهیلات کلان",
        "description": "اعطای تسهیلات به اشخاص حقوقی در قالب عقود مشارکت مدنی، مضاربه، سلف و استصناع با استعلام سامانه سمات.",
        "cbi_system": "Samat / CorporateBanking"
    },
    "Factoring": {
        "title": "خرید دین و فاکتورینگ",
        "description": "تنزیل اسناد تجاری و خرید دین مطالبات تجاری بر اساس ضوابط فقهی و قانونی بانکداری بدون ربا.",
        "cbi_system": "CoreBanking / TradeFinance"
    },
    "FinancialAccounting": {
        "title": "حسابداری مالی و کل (GL)",
        "description": "دفترکل مالی بانک، ثبت اسناد دوبل حسابداری، بستن حساب‌ها و گزارش‌های مالی ترازنامه.",
        "cbi_system": "GeneralLedger / Financial"
    },
    "CurrencyExchange": {
        "title": "صرافی و عملیات ارزی (سنا و نیما)",
        "description": "خرید و فروش ارزهای خارجی، حوالجات ارزی و ثبت نرخ‌ها در سامانه نظارت ارز (سنا) و سامانه نیما.",
        "cbi_system": "Sana / Nima / FX"
    },
    "CorporateTreasury": {
        "title": "خزانه‌داری بانکی و مدیریت نقدینگی",
        "description": "مدیریت جریان نقدینگی ریالی و ارزی، منابع و مصارف، بازار بین‌بانکی و تسویه تعهدات با بانک مرکزی.",
        "cbi_system": "Treasury / Interbank"
    },
    "CreditRiskOperations": {
        "title": "عملیات مدیریت ریسک اعتباری",
        "description": "پایش ریسک اعتباری سبد تسهیلات، تعیین ذخیره مطالبات مشکوک‌الوصول و انطباق با کفایت سرمایه بال.",
        "cbi_system": "RiskManagement / Samat"
    },
    "FraudEvaluation": {
        "title": "پایش و کشف تقلب‌های مالی",
        "description": "تحلیل رفتار تراکنش‌ها، کشف ناهنجاری‌ها و مسدودسازی آنی تراکنش‌های مشکوک به فیشینگ و کلاهبرداری.",
        "cbi_system": "AntiFraud / Shaparak"
    },
    "RegulatoryCompliance": {
        "title": "تطبیق و نظارت مقرراتی بانک مرکزی",
        "description": "پایش اجرای بخشنامه‌های بانک مرکزی، مبارزه با پولشویی (AML) و پایش الزامات حاکمیتی.",
        "cbi_system": "Compliance / CBI"
    },
    "RegulatoryReporting": {
        "title": "گزارش‌گری نظارتی به بانک مرکزی",
        "description": "تولید و ارسال گزارش‌های آماری، تراز مالی و صورت‌های نظارتی دوره‌ای به بانک مرکزی جمهوری اسلامی ایران.",
        "cbi_system": "Reporting / CBI"
    },
    "DelinquentAccountHandling": {
        "title": "پیگیری و مدیریت مطالبات معوق",
        "description": "مدیریت پرونده‌های سررسیدگذشته، معوق و مشکوک‌الوصول، محاسبه وجه التزام و اقدامات قانونی وصول مطالبات.",
        "cbi_system": "Recovery / Samat"
    }
}

KEYWORD_MAP = {
    'Account': 'حساب',
    'Accounts': 'حساب‌ها',
    'Reconciliation': 'مغایرت‌گیری',
    'Recovery': 'وصول مطالبات',
    'Receivable': 'دریافتنی‌ها',
    'Payable': 'پرداختنی‌ها',
    'Advanced': 'پیشرفته',
    'Voice': 'صوتی',
    'Services': 'خدمات',
    'Management': 'مدیریت',
    'Operations': 'عملیات',
    'Advertising': 'تبلیغات',
    'Archive': 'آرشیو',
    'Asset': 'دارایی',
    'Liability': 'بدهی',
    'Securitization': 'اوراق‌بهادارسازی',
    'ATM': 'خودپرداز',
    'Network': 'شبکه',
    'Bank': 'بانکی',
    'Drafts': 'حواله‌جات',
    'Guarantee': 'ضمانت‌نامه',
    'Branch': 'شعبه',
    'Currency': 'اسکناس و ارز',
    'Distribution': 'توزیع',
    'Location': 'موقعیت مکانی',
    'Brand': 'برند',
    'Brokered': 'کارگزاری',
    'Product': 'محصول',
    'Proxy': 'وکالت',
    'Business': 'کسب‌وکار',
    'Development': 'توسعه',
    'Unit': 'واحد',
    'Card': 'کارت',
    'Authorization': 'مجوزدهی',
    'Case': 'پرونده',
    'Clearing': 'پایاپای',
    'Collections': 'وصول مطالبات',
    'Financial': 'مالی',
    'Settlement': 'تسویه',
    'Participant': 'مشارکت‌کننده',
    'Facility': 'تسهیلات',
    'Terminal': 'پایانه',
    'Administration': 'راهبری',
    'Operation': 'عملیات',
    'Transaction': 'تراکنش',
    'Capture': 'دریافت داده',
    'Switch': 'سوئیچینگ',
    'Tracking': 'پیگیری',
    'eCommerce': 'تجارت الکترونیک',
    'Gateway': 'درگاه',
    'Root': 'ریشه',
    'Cause': 'علت',
    'Analysis': 'تحلیل',
    'Cash': 'وجه نقد',
    'Concentration': 'تمرکز وجوه',
    'Central': 'مرکزی',
    'Handling': 'مدیریت',
    'Channel': 'کانال',
    'Activity': 'فعالیت',
    'History': 'سوابق',
    'Cheque': 'چک',
    'Lock': 'مسدودی',
    'Box': 'صندوق',
    'Processing': 'پردازش',
    'Claim': 'خسارت',
    'Assessment': 'ارزیابی',
    'Collateral': 'وثایق',
    'Allocation': 'تخصیص',
    'Commission': 'کارمزد',
    'Agreement': 'قرارداد',
    'Commissions': 'کارمزدها',
    'Competitor': 'رقبا',
    'Compliance': 'تطبیق مقررات',
    'Reporting': 'گزارش‌دهی',
    'Consumer': 'مشتریان خرد',
    'Advisory': 'مشاوره',
    'Investments': 'سرمایه‌گذاری',
    'Loan': 'تسهیلات',
    'Contact': 'ارتباط',
    'Center': 'مرکز',
    'Handler': 'مدیریت',
    'Routing': 'مسیریابی',
    'Contractor': 'پیمانکار',
    'Supplier': 'تامین‌کننده',
    'Corporate': 'شرکتی',
    'Action': 'اقدامات',
    'Current': 'جاری',
    'Finance': 'تامین مالی',
    'Lease': 'لیزینگ',
    'Payroll': 'حقوق و دستمزد',
    'Tax': 'مالیات',
    'Treasury': 'خزانه‌داری',
    'Trust': 'امانی',
    'Correspondence': 'مکاتبات',
    'Correspondent': 'کارگزاری بین‌بانکی',
    'Directory': 'دفتر راهنما',
    'Relationship': 'روابط با مشتری',
    'Counterparty': 'طرف معامله',
    'Credit': 'اعتباری',
    'Models': 'مدل‌ها',
    'Risk': 'ریسک',
    'Exchange': 'مبادلات',
    'Custody': 'حفاظت اسناد',
    'Customer': 'مشتری',
    'Access': 'دسترسی',
    'Entitlement': 'مجوزها',
    'Behavior': 'رفتاری',
    'Insights': 'بینش و تحلیل',
    'Billing': 'صورتحساب',
    'Campaign': 'کمپین',
    'Design': 'طراحی',
    'Execution': 'اجرا',
    'Rating': 'رتبه‌بندی',
    'Event': 'رویداد',
    'Offer': 'پیشنهاد',
    'Portfolio': 'پورتفوی',
    'Position': 'موقعیت',
    'Service': 'سرویس',
    'Eligibility': 'احراز شرایط',
    'Proposition': 'پیشنهاد ارزش',
    'Surveys': 'نظرسنجی',
    'Workbench': 'میز کار',
    'Dealer': 'معاملاتگر',
    'Desk': 'میز',
    'Delinquent': 'معوق',
    'Direct': 'مستقیم',
    'Debit': 'برداشت مستقیم',
    'Mandate': 'مجوز',
    'Disbursement': 'پرداخت تسهیلات',
    'Document': 'اسناد',
    'ECM': 'بازار سهام',
    'DCM': 'بازار بدهی',
    'Enterprise': 'سازمانی',
    'Architecture': 'معماری',
    'Factoring': 'خرید دین',
    'Fiduciary': 'وکالت امانی',
    'Accounting': 'حسابداری',
    'Instrument': 'ابزار مالی',
    'Reference': 'داده مرجع',
    'Data': 'داده‌ها',
    'Valuation': 'ارزش‌گذاری',
    'Market': 'بازار',
    'Research': 'تحقیقات',
    'Statement': 'صورت‌های مالی',
    'Fraud': 'کشف تقلب',
    'Diagnosis': 'تشخیص',
    'Evaluation': 'ارزیابی',
    'Model': 'مدل',
    'Resolution': 'رسیدگی',
    'Funeral': 'بیمه عمر',
    'Policy': 'بیمه‌نامه',
    'Guideline': 'دستورالعمل',
    'Hedge': 'پوشش ریسک',
    'Fund': 'صندوق',
    'IT': 'فناوری اطلاعات',
    'Standards': 'استانداردها',
    'Guidelines': 'رهنمودها',
    'Incentive': 'مشوق و پاداش',
    'Program': 'برنامه',
    'Information': 'اطلاعات',
    'Provider': 'تامین‌کننده',
    'Intellectual': 'مالکیت فکری',
    'Property': 'دارایی',
    'Interactive': 'تعاملی',
    'Help': 'پشتیبانی',
    'Interbank': 'بین‌بانکی',
    'Internal': 'داخلی',
    'Investment': 'سرمایه‌گذاری',
    'Planning': 'برنامه‌ریزی',
    'Issued': 'صادره',
    'Certificate': 'گواهی‌نامه',
    'Device': 'تجهیزات و توکن',
    'Knowledge': 'مدیریت دانش',
    'Lead': 'سرنخ فروش',
    'Opportunity': 'فرصت تجاری',
    'Leasing': 'لیزینگ',
    'Item': 'قلم دارایی',
    'Legal': 'حقوقی',
    'Entity': 'شخصیت حقوقی',
    'Letter': 'اعتبار اسنادی',
    'Syndication': 'سندیکای بانکی',
    'Syndicated': 'سندیکایی',
    'Order': 'سفارش',
    'Partner': 'شریک تجاری',
    'Party': 'مشتری و ذینفع',
    'Lifecycle': 'چرخه عمر',
    'Profile': 'پروفایل',
    'Payment': 'پرداخت',
    'Rail': 'بستر پرداخت',
    'Point': 'پایانه فروشگاهی',
    'Keeping': 'نگهداری پوزیشن',
    'Placement': 'عرضه اوراق',
    'Combination': 'ترکیب محصولات',
    'Deployment': 'استقرار',
    'Expert': 'کارشناسی تخصصی',
    'Sales': 'فروش',
    'Support': 'پشتیبانی',
    'Inventory': 'موجودی انبار',
    'Matching': 'انطباق',
    'Quality': 'کیفیت',
    'Assurance': 'تضمین کیفیت',
    'Agency': 'نمایندگی',
    'Training': 'آموزش',
    'Production': 'محیط عملیاتی',
    'Release': 'انتشار نسخه',
    'ProgramTrading': 'معاملات الگوریتمی',
    'Project': 'پروژه',
    'Promotional': 'ترویجی',
    'Events': 'رویدادها',
    'Prospect': 'مشتری بالقوه',
    'Public': 'عمومی',
    'Offering': 'پذیره‌نویسی',
    'Quote': 'استعلام نرخ',
    'Regulatory': 'مقرراتی',
    'Authority': 'نهاد ناظر',
    'Reward': 'وفاداری و پاداش',
    'Points': 'امتیازات',
    'Awards': 'جوایز',
    'Redemption': 'مصرف جوایز',
    'Delivery': 'تحویل',
    'Menu': 'منو',
    'Savings': 'قرض‌الحسنه پس‌انداز',
    'Securities': 'اوراق بهادار',
    'Fails': 'خطاهای تسویه اوراق',
    'Segment': 'بخش‌بندی بازار',
    'Direction': 'جهت‌گیری',
    'Servicing': 'ارائه خدمت',
    'Issue': 'رسیدگی به مسائل',
    'Session': 'نشست',
    'Dialogue': 'گفتگو و تعامل',
    'Special': 'ویژه',
    'Pricing': 'قیمت‌گذاری',
    'Conditions': 'شرایط',
    'Standing': 'دستور پرداخت ثابت',
    'Stock': 'سهام',
    'Lending': 'قرض‌دهی سهام',
    'Repos': 'قرارداد ریپو',
    'Sub': 'فرعی',
    'Custodian': 'امین اسناد',
    'Suitability': 'تناسب‌سنجی',
    'Checking': 'کنترل و بررسی',
    'System': 'سامانه',
    'Systems': 'سامانه‌ها',
    'Term': 'مدت‌دار',
    'Deposit': 'سپرده',
    'Framework': 'چارچوب',
    'Trade': 'معاملات',
    'Confirmation': 'تاییدیه معامله',
    'Trader': 'معامله‌گر',
    'Trading': 'معاملاتی',
    'Book': 'دفتر معاملات',
    'Oversight': 'نظارت',
    'Engine': 'موتور پردازش',
    'Underwriting': 'تعهد پذیره‌نویسی',
    'Virtual': 'مجازی',
    'eBranch': 'شعبه مجازی',
    'eTrading': 'معاملات برخط'
}

ACTION_TRANSLATIONS = {
    'InCR': 'افتتاح / آغاز رکورد کنترلی',
    'UpCR': 'بروزرسانی رکورد کنترلی',
    'ReCR': 'استعلام / دریافت رکورد کنترلی',
    'CoCR': 'کنترل و پایش رکورد کنترلی',
    'ExCR': 'تبادل اطلاعات رکورد کنترلی',
    'EcCR': 'اجرا / عملیات رکورد کنترلی',
    'RqCR': 'درخواست در رکورد کنترلی',
    'RcCR': 'ثبت رویداد رکورد کنترلی',
    'EvCR': 'ارزیابی رکورد کنترلی',
    'AuCR': 'مجوزدهی رکورد کنترلی',
    'NoCR': 'اعلان در رکورد کنترلی',
    'InBQ': 'آغاز شناسه رفتاری',
    'UpBQ': 'بروزرسانی شناسه رفتاری',
    'ReBQ': 'استعلام شناسه رفتاری',
    'CoBQ': 'کنترل شناسه رفتاری',
    'ExBQ': 'تبادل شناسه رفتاری',
    'EcBQ': 'اجرای شناسه رفتاری',
    'RqBQ': 'درخواست شناسه رفتاری',
    'RcBQ': 'ثبت رویداد شناسه رفتاری',
    'EvBQ': 'ارزیابی شناسه رفتاری',
    'AuBQ': 'مجوزدهی شناسه رفتاری',
    'NoBQ': 'اعلان شناسه رفتاری'
}

def split_camel_case(s: str) -> list[str]:
    """Splits CamelCase into individual words."""
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\b)|[0-9]+', s)

def get_domain_info(domain_name: str) -> dict:
    """Returns Persian title, description, and CBI system for a BIAN domain name."""
    if domain_name in PRIMARY_DOMAIN_MAP:
        return PRIMARY_DOMAIN_MAP[domain_name]

    words = split_camel_case(domain_name)
    translated_words = []
    for w in words:
        if w in KEYWORD_MAP:
            translated_words.append(KEYWORD_MAP[w])
        elif w.lower() in ('and', 'for', 'of', 'to', 'in', 'on', 'with'):
            continue
        else:
            translated_words.append(w)
    
    fa_title = " ".join(translated_words)
    eng_spaced = " ".join(words)

    # Determine probable Iranian banking system
    cbi_system = "CoreBanking"
    name_lower = domain_name.lower()
    if 'card' in name_lower or 'atm' in name_lower or 'terminal' in name_lower or 'switch' in name_lower:
        cbi_system = "Shetab / Shaparak"
    elif 'payment' in name_lower or 'clearing' in name_lower or 'settlement' in name_lower or 'directdebit' in name_lower:
        cbi_system = "Paya / Satna / Pol"
    elif 'cheque' in name_lower:
        cbi_system = "Sayad / Chakad"
    elif 'loan' in name_lower or 'credit' in name_lower or 'collateral' in name_lower or 'mortgage' in name_lower:
        cbi_system = "Samat / CoreBanking"
    elif 'party' in name_lower or 'customer' in name_lower:
        cbi_system = "Nehab / Shahkar"
    elif 'regulatory' in name_lower or 'compliance' in name_lower or 'fraud' in name_lower:
        cbi_system = "CBI / Compliance"
    elif 'treasury' in name_lower or 'market' in name_lower or 'currency' in name_lower:
        cbi_system = "Treasury / Nima / Sana"

    return {
        "title": fa_title,
        "description": f"مدیریت حوزه {fa_title} ({eng_spaced}) در چارچوب استاندارد BIAN نسخه ۱۴ منطبق با سیستم بانکی ایران.",
        "cbi_system": cbi_system
    }
