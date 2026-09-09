# BIAN Persian / Iranian Banking Localization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, production-ready Iranian Banking localization for BIAN (Banking Industry Architecture Network) release 14.0.0, including bilingual lexicon, CBI regulatory mappings, shared Iranian core schemas, and 4 pilot OpenAPI 3.0 service domains.

**Architecture:** Layered and modular architecture where a central `common/` module contains reusable Iranian banking components (identity, accounts, Islamic contracts, Shetab/Shaparak error codes) referenced via OpenAPI `$ref` by pilot service domains (`CurrentAccount`, `ConsumerLoan`, `PaymentOrderInitiation`, `CardAuthorization`) in a dedicated `bian-iran/release14.0.0/` workspace, validated by a self-contained Python OpenAPI 3.0 validator.

**Tech Stack:** OpenAPI 3.0 (YAML), Python 3.13 + PyYAML for schema validation and `$ref` resolution, Markdown for architectural standards and lexicons.

## Global Constraints

- **Specification Version:** OpenAPI 3.0.1.
- **Naming Conventions:** JSON property keys and URL paths must be standard English CamelCase (e.g. `nationalId`, `shebaNumber`, `islamicContractType`), while titles, descriptions, enums, error messages, and documentation must be entirely in Persian.
- **Independence:** The original BIAN release folders (`release14.0.0/`, etc.) must remain untouched. All localized specifications belong in `bian-iran/release14.0.0/`.
- **Validation:** All YAML files must pass syntax validation, OpenAPI 3.0 required root element checks, and resolve all relative `$ref` pointers with 0 broken references.

---

### Task 1: Test & Validation Harness (`tests/validate_openapi.py`)

**Files:**
- Create: `tests/validate_openapi.py`
- Create: `tests/test_docs.py`

**Interfaces:**
- Produces: CLI script `python tests/validate_openapi.py` accepting `--path` or `--all` flags, returning exit code 0 on success or 1 with error diagnostic details on failure.

- [ ] **Step 1: Write the failing test / validator script**

Create `tests/validate_openapi.py`:
```python
import os
import sys
import re
import yaml
from pathlib import Path

def resolve_ref(base_file: Path, ref_str: str) -> bool:
    if ref_str.startswith("#/"):
        # Internal reference check
        with open(base_file, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        parts = ref_str.lstrip("#/").split("/")
        curr = content
        for part in parts:
            if not isinstance(curr, dict) or part not in curr:
                return False
            curr = curr[part]
        return True
    else:
        # External file reference check (e.g. ../common/iran-banking-core.yaml#/components/schemas/NationalId)
        if "#" in ref_str:
            file_part, path_part = ref_str.split("#", 1)
        else:
            file_part, path_part = ref_str, ""
        
        target_file = (base_file.parent / file_part).resolve()
        if not target_file.exists():
            return False
        
        if path_part and path_part.startswith("/"):
            with open(target_file, "r", encoding="utf-8") as f:
                target_content = yaml.safe_load(f)
            parts = path_part.lstrip("/").split("/")
            curr = target_content
            for part in parts:
                if not isinstance(curr, dict) or part not in curr:
                    return False
                curr = curr[part]
        return True

def find_refs(data):
    refs = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "$ref" and isinstance(v, str):
                refs.append(v)
            else:
                refs.extend(find_refs(v))
    elif isinstance(data, list):
        for item in data:
            refs.extend(find_refs(item))
    return refs

def validate_openapi_file(file_path: Path) -> list[str]:
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except Exception as e:
        return [f"YAML syntax error in {file_path}: {e}"]

    if not isinstance(doc, dict):
        return [f"Root of {file_path} is not a valid YAML mapping."]

    # Check OpenAPI 3.0 basic requirements if it's a full service domain
    if "service-domains" in str(file_path):
        if "openapi" not in doc or not str(doc["openapi"]).startswith("3.0"):
            errors.append(f"{file_path.name}: Missing or invalid 'openapi: 3.0.x' version header.")
        if "info" not in doc or "title" not in doc.get("info", {}):
            errors.append(f"{file_path.name}: Missing 'info.title'.")
        if "paths" not in doc:
            errors.append(f"{file_path.name}: Missing 'paths' object.")

    # Validate all $ref links
    all_refs = find_refs(doc)
    for ref in all_refs:
        if not resolve_ref(file_path, ref):
            errors.append(f"{file_path.name}: Broken reference '$ref: {ref}'")

    return errors

def main():
    root = Path(__file__).resolve().parent.parent
    target_dir = root / "bian-iran" / "release14.0.0"
    
    if not target_dir.exists():
        print(f"Directory {target_dir} does not exist yet.")
        sys.exit(1)

    yaml_files = list(target_dir.rglob("*.yaml")) + list(target_dir.rglob("*.yml"))
    if not yaml_files:
        print(f"No YAML files found in {target_dir}.")
        sys.exit(1)

    total_errors = 0
    for yf in sorted(yaml_files):
        errs = validate_openapi_file(yf)
        if errs:
            total_errors += len(errs)
            print(f"FAIL: {yf.relative_to(root)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS: {yf.relative_to(root)}")

    if total_errors > 0:
        print(f"\nTotal validation errors: {total_errors}")
        sys.exit(1)
    else:
        print(f"\nAll {len(yaml_files)} OpenAPI specification files passed validation successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

Also create `tests/test_docs.py` to verify required documentation files:
```python
import sys
from pathlib import Path

def test_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs_dir = root / "docs"
    required_docs = [
        docs_dir / "bian-iran-lexicon.md",
        docs_dir / "cbi-regulatory-mapping.md",
        docs_dir / "bian-iran-methodology.md"
    ]
    missing = [str(d.name) for d in required_docs if not d.exists()]
    if missing:
        print(f"Missing required documentation: {', '.join(missing)}")
        sys.exit(1)
    print("All required documentation files are present.")
    sys.exit(0)

if __name__ == "__main__":
    test_docs_exist()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python tests/validate_openapi.py`
Expected: FAIL with message that `bian-iran/release14.0.0` does not exist yet.

- [ ] **Step 3: Commit test harness**

```bash
git add tests/validate_openapi.py tests/test_docs.py
git commit -m "test: add OpenAPI and documentation validation test harness"
```

---

### Task 2: High-Level Documentation, Lexicon & Central Bank Mapping

**Files:**
- Create: `docs/bian-iran-lexicon.md`
- Create: `docs/cbi-regulatory-mapping.md`
- Create: `docs/bian-iran-methodology.md`
- Test: `tests/test_docs.py`

**Interfaces:**
- Produces: Complete architectural documentation and bilingual banking terminology guide.

- [ ] **Step 1: Write `docs/bian-iran-lexicon.md`**

Create `docs/bian-iran-lexicon.md` containing:
- Terminology dictionary: Service Domain (دامنه سرویس), Control Record (رکورد کنترلی), Behavior Qualifier (شناسه رفتاری), Functional Pattern (الگوی عملکردی).
- Standard Action Terms: Initiate (افتتاح/آغاز), Update (بروزرسانی), Record (ثبت رویداد), Retrieve (استعلام/دریافت), Execute (اجرا/عملیات), Request (درخواست).
- Iranian Banking Mapping Table:
  - Current Account -> حساب قرض‌الحسنه جاری
  - Savings Account -> حساب قرض‌الحسنه پس‌انداز
  - Term Deposit -> سپرده سرمایه‌گذاری مدت‌دار
  - Consumer Loan -> تسهیلات خرد (عقود اسلامی)
  - Payment Order -> دستور پرداخت (پایا، ساتنا، پل)
  - Card Authorization -> مجوزدهی تراکنش کارت (شتاب / شاپرک)
  - Lien / Block -> مسدودی و انسداد قضایی/بانکی (سیاح)
  - Cheque Processing -> پردازش چک صیادی و چکاد

- [ ] **Step 2: Write `docs/cbi-regulatory-mapping.md`**

Create `docs/cbi-regulatory-mapping.md` containing:
- Central Bank Systems mapping matrix:
  - **نهاب (شهاب):** احراز هویت متمرکز بانکی -> Service Domains: `PartyLifecycleManagement`, `PartyAuthentication`, `CurrentAccount`
  - **سیاح:** سامانه یکپارچه اطلاعات حساب‌ها و مسدودی‌ها -> Service Domain: `CurrentAccount` (Lien/Block)
  - **صیاد / چکاد / سماچک:** مدیریت و اعتبارسنجی چک -> Service Domain: `CurrentAccount` (ChequeFacility)
  - **شتاب:** شبکه تبادل اطلاعات بین‌بانکی کارتی -> Service Domain: `CardAuthorization`, `CardTransactionSwitch`
  - **شاپرک:** شبکه الکترونیکی پرداخت کارت -> Service Domain: `CardAuthorization`, `MerchantAcquiringFacility`
  - **پایا (ACH):** پایاپای الکترونیک -> Service Domain: `PaymentOrderInitiation`, `PaymentExecution`
  - **ساتنا (RTGS):** تسویه ناخالص آنی -> Service Domain: `PaymentOrderInitiation`
  - **پل:** پرداخت لحظه‌ای بین‌بانکی -> Service Domain: `PaymentOrderInitiation`
  - **سمات / مکنا:** سامانه متمرکز اطلاعات تسهیلات و تعهدات -> Service Domain: `ConsumerLoan`, `CreditFacility`
  - **شاهکار:** تطبیق کدملی و سیم‌کارت -> Service Domain: `PartyAuthentication`, `CardAuthorization`

- [ ] **Step 3: Write `docs/bian-iran-methodology.md`**

Create `docs/bian-iran-methodology.md` containing:
- 5-step methodology for localizing any BIAN Service Domain for Iran:
  1. تحلیل دامنه بین‌المللی BIAN و استخراج دارایی کنترلی (Control Record).
  2. بررسی الزامات و بخشنامه‌های ناظر بانک مرکزی ایران (CBI Regulations).
  3. استفاده از مدل‌های داده مشترک (`common/iran-banking-core.yaml` و...).
  4. طراحی مشخصات OpenAPI 3.0 با کلیدهای CamelCase انگلیسی و مستندات فارسی.
  5. اعتبارسنجی با تست اتوماتیک `validate_openapi.py`.

- [ ] **Step 4: Run test to verify documentation is valid**

Run: `python tests/test_docs.py`
Expected: PASS with "All required documentation files are present."

- [ ] **Step 5: Commit documentation**

```bash
git add docs/bian-iran-lexicon.md docs/cbi-regulatory-mapping.md docs/bian-iran-methodology.md
git commit -m "docs: add BIAN Persian lexicon, CBI mapping, and localization methodology"
```

---

### Task 3: Common Core Components (`bian-iran/release14.0.0/common/`)

**Files:**
- Create: `bian-iran/release14.0.0/common/iran-banking-core.yaml`
- Create: `bian-iran/release14.0.0/common/islamic-contracts.yaml`
- Create: `bian-iran/release14.0.0/common/error-codes.yaml`
- Test: `tests/validate_openapi.py`

**Interfaces:**
- Produces:
  - `iran-banking-core.yaml#/components/schemas/NationalId`
  - `iran-banking-core.yaml#/components/schemas/LegalEntityId`
  - `iran-banking-core.yaml#/components/schemas/ShahabId`
  - `iran-banking-core.yaml#/components/schemas/IbanNumber`
  - `iran-banking-core.yaml#/components/schemas/InternalAccountNumber`
  - `iran-banking-core.yaml#/components/schemas/CardPan`
  - `iran-banking-core.yaml#/components/schemas/SayadChequeId`
  - `iran-banking-core.yaml#/components/schemas/Currency`
  - `iran-banking-core.yaml#/components/schemas/JalaliDate`
  - `iran-banking-core.yaml#/components/schemas/FinancialAmount`
  - `islamic-contracts.yaml#/components/schemas/ContractType`
  - `islamic-contracts.yaml#/components/schemas/IslamicContractDetails`
  - `islamic-contracts.yaml#/components/schemas/CollateralDetails`
  - `islamic-contracts.yaml#/components/schemas/InstallmentSchedule`
  - `error-codes.yaml#/components/schemas/ProblemDetails`
  - `error-codes.yaml#/components/schemas/ShetabResponseCode`

- [ ] **Step 1: Write `iran-banking-core.yaml`**

Create `bian-iran/release14.0.0/common/iran-banking-core.yaml` defining schemas:
- `NationalId`: string, pattern `^[0-9]{10}$`, example `"0012345678"`, Persian title and description.
- `LegalEntityId`: string, pattern `^[0-9]{11}$`, example `"10100000000"`.
- `ForeignNationalId`: string, pattern `^[0-9]{9,12}$`.
- `ShahabId`: string, pattern `^[0-9]{16}$`, example `"1000000000000001"`.
- `IbanNumber`: string, pattern `^IR[0-9]{24}$`, example `"IR000000000000000000000000"`.
- `InternalAccountNumber`: string, pattern `^[0-9A-Za-z\.\-]{5,30}$`.
- `CardPan`: string, pattern `^[0-9]{16}$`, example `"6037990000000000"`.
- `SayadChequeId`: string, pattern `^[0-9]{16}$`, example `"1234567890123456"`.
- `Currency`: string, enum `["IRR", "IRT"]`, default `"IRR"`.
- `JalaliDate`: string, pattern `^[1-4][0-9]{3}[/-](0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])$`, example `"1403/06/19"`.
- `FinancialAmount`: object with `amount` (integer/number) and `currency` (ref to `Currency`).

- [ ] **Step 2: Write `islamic-contracts.yaml`**

Create `bian-iran/release14.0.0/common/islamic-contracts.yaml` defining schemas:
- `ContractType`: string, enum: `["Morabaha", "Mozaraba", "Jaala", "GharzOlHasaneh", "Salaf", "CivilPartnership", "FinancialLease", "Istisna"]` with Persian descriptions for each contract.
- `IslamicContractDetails`: object containing contract number, type, profit rate, penalty rate, total principal, number of installments.
- `CollateralType`: string, enum: `["ElectronicPromissoryNote", "OfficialGuarantor", "DepositPledge", "RealEstateMortgage", "StockPledge"]`.
- `CollateralDetails`: object containing collateral ID, type, assessed value, owner national ID.
- `InstallmentSchedule`: object with installment number, dueDate (JalaliDate), principalAmount, profitAmount, remainingBalance.

- [ ] **Step 3: Write `error-codes.yaml`**

Create `bian-iran/release14.0.0/common/error-codes.yaml` defining schemas:
- `ProblemDetails`: RFC 7807 compliant object with `type`, `title`, `status`, `detail`, `errorCode`, `messageFa`, `cbiSystem`, `timestamp`.
- `ShetabResponseCode`: string, enum `["00", "51", "55", "57", "61", "68", "91", "92", "96"]` with Persian descriptions for each code.

- [ ] **Step 4: Run validation test on common components**

Run: `python tests/validate_openapi.py`
Expected: PASS for all 3 common YAML files with 0 errors.

- [ ] **Step 5: Commit common components**

```bash
git add bian-iran/release14.0.0/common/
git commit -m "feat: add Iranian banking common core OpenAPI components"
```

---

### Task 4: Pilot Service Domains - CurrentAccount & ConsumerLoan

**Files:**
- Create: `bian-iran/release14.0.0/service-domains/CurrentAccount.yaml`
- Create: `bian-iran/release14.0.0/service-domains/ConsumerLoan.yaml`
- Test: `tests/validate_openapi.py`

**Interfaces:**
- Consumes: Models from `../common/iran-banking-core.yaml`, `../common/islamic-contracts.yaml`, `../common/error-codes.yaml`.
- Produces: Complete OpenAPI 3.0.1 specs for CurrentAccount and ConsumerLoan.

- [ ] **Step 1: Write `CurrentAccount.yaml`**

Create `bian-iran/release14.0.0/service-domains/CurrentAccount.yaml`:
- OpenAPI 3.0.1 header with Persian title: "دامنه سرویس حساب جاری بانکی ایران (Current Account)".
- Endpoints:
  - `POST /CurrentAccount/Initiate`: افتتاح حساب جاری با استعلام نهاب، ثبت شهاب، تخصیص شماره حساب متمرکز و صدور شبا.
  - `POST /CurrentAccount/{accountId}/ChequeFacility/Request`: درخواست دسته چک صیادی و استعلام سامانه سماچک/صیاد.
  - `POST /CurrentAccount/{accountId}/Lien/Apply`: اعمال مسدودی برخط حساب متصل به سامانه سیاح بانک مرکزی.
  - `DELETE /CurrentAccount/{accountId}/Lien/{lienId}/Release`: رفع مسدودی حساب.
  - `GET /CurrentAccount/{accountId}/Statement`: دریافت گردش حساب با تاریخ‌های جلالی.
- All request/response bodies and parameters must accurately `$ref` schemas from `../common/iran-banking-core.yaml` and `../common/error-codes.yaml`.

- [ ] **Step 2: Write `ConsumerLoan.yaml`**

Create `bian-iran/release14.0.0/service-domains/ConsumerLoan.yaml`:
- OpenAPI 3.0.1 header with Persian title: "دامنه سرویس تسهیلات خرد و عقود اسلامی (Consumer Loan)".
- Endpoints:
  - `POST /ConsumerLoan/Initiate`: ثبت پرونده درخواست تسهیلات خرد بر اساس عقود اسلامی (مرابحه، قرض‌الحسنه و...).
  - `POST /ConsumerLoan/{loanId}/CreditAssessment`: استعلام سامانه سمات بانک مرکزی و ارزیابی نسبت درآمد به تعهدات.
  - `POST /ConsumerLoan/{loanId}/Collateral/Register`: ثبت تضامین، سفته الکترونیک و ضامنین معتبر.
  - `POST /ConsumerLoan/{loanId}/Disbursement`: واریز مبلغ تسهیلات و تولید جدول بازپرداخت اقساط شمسی.
  - `GET /ConsumerLoan/{loanId}/InstallmentSchedule`: دریافت جدول اقساط و مانده بدهی.
- References `../common/islamic-contracts.yaml`, `../common/iran-banking-core.yaml`, and `../common/error-codes.yaml`.

- [ ] **Step 3: Run validation test**

Run: `python tests/validate_openapi.py`
Expected: PASS for `CurrentAccount.yaml` and `ConsumerLoan.yaml` with all `$ref` pointers successfully resolved.

- [ ] **Step 4: Commit**

```bash
git add bian-iran/release14.0.0/service-domains/CurrentAccount.yaml bian-iran/release14.0.0/service-domains/ConsumerLoan.yaml
git commit -m "feat: add CurrentAccount and ConsumerLoan localized OpenAPI specs"
```

---

### Task 5: Pilot Service Domains - PaymentOrderInitiation & CardAuthorization

**Files:**
- Create: `bian-iran/release14.0.0/service-domains/PaymentOrderInitiation.yaml`
- Create: `bian-iran/release14.0.0/service-domains/CardAuthorization.yaml`
- Test: `tests/validate_openapi.py`

**Interfaces:**
- Consumes: Models from `../common/iran-banking-core.yaml`, `../common/error-codes.yaml`.
- Produces: Complete OpenAPI 3.0.1 specs for PaymentOrderInitiation and CardAuthorization.

- [ ] **Step 1: Write `PaymentOrderInitiation.yaml`**

Create `bian-iran/release14.0.0/service-domains/PaymentOrderInitiation.yaml`:
- OpenAPI 3.0.1 header with Persian title: "دامنه سرویس دستور پرداخت بین‌بانکی (Payment Order Initiation)".
- Endpoints:
  - `POST /PaymentOrder/Initiate`: ثبت دستور انتقال وجه با تشخیص هوشمند مسیر (انتقال داخلی، سامانه پل، پایا، ساتنا).
  - `POST /PaymentOrder/ValidateLimits`: بررسی سقف مجاز انتقال وجه بر اساس کانال و استعلام وضعیت مشتری.
  - `GET /PaymentOrder/{paymentId}/Status`: استعلام وضعیت انتقال بر اساس شناسه تراکنش، `TraceNo` یا `RRN`.
- Complete schemas with Persian descriptions and examples.

- [ ] **Step 2: Write `CardAuthorization.yaml`**

Create `bian-iran/release14.0.0/service-domains/CardAuthorization.yaml`:
- OpenAPI 3.0.1 header with Persian title: "دامنه سرویس مجوزدهی تراکنش کارت و سوئیچ شتاب (Card Authorization)".
- Endpoints:
  - `POST /CardAuthorization/Authorize`: اعتبارسنجی تراکنش کارتی (رمز دوم پویا/هدی، CVV2، تاریخ انقضا، سامانه شاهکار).
  - `POST /CardAuthorization/VerifyBalance`: کنترل موجودی و سقف مجاز برداشت روزانه شتاب/شاپرک.
  - `POST /CardAuthorization/Reverse`: عملیات اصلاحیه / برگشت تراکنش (Reversal) طبق ضوابط شتاب.
- References `../common/iran-banking-core.yaml` and `../common/error-codes.yaml`.

- [ ] **Step 3: Run validation test**

Run: `python tests/validate_openapi.py`
Expected: PASS for all service domains with 0 errors.

- [ ] **Step 4: Commit**

```bash
git add bian-iran/release14.0.0/service-domains/PaymentOrderInitiation.yaml bian-iran/release14.0.0/service-domains/CardAuthorization.yaml
git commit -m "feat: add PaymentOrderInitiation and CardAuthorization localized OpenAPI specs"
```

---

### Task 6: End-to-End Verification, Documentation Links & README Update

**Files:**
- Modify: `README.md`
- Test: `tests/validate_openapi.py` and `tests/test_docs.py`

**Interfaces:**
- Produces: Fully integrated repository presentation with usage instructions and Swagger UI testing instructions.

- [ ] **Step 1: Run complete validation suite**

Run: `python tests/validate_openapi.py` and `python tests/test_docs.py`
Expected: 100% PASS for all files and documentation.

- [ ] **Step 2: Update `README.md`**

Update `README.md` to feature the new `bian-iran/` localized release 14.0.0, outlining:
- راهنمای پروژه بومی‌سازی BIAN ایران
- پیوند به اسناد معماری، اصطلاح‌نامه و ماتریس انطباق با بانک مرکزی
- فهرست ۴ دامنه سرویس پایلوت پیاده‌سازی شده
- راهنمای تست مشخصات OpenAPI در ابزارهای Swagger Editor و Postman

- [ ] **Step 3: Final Commit**

```bash
git add README.md
git commit -m "docs: update README with BIAN Iranian localization guide and pilot domains"
```
