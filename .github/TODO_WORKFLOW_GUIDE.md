# 📚 دليل استخدام GitHub Action لإنشاء Issues من TODO

## 🎯 نظرة عامة

هذا الـ Action يقوم تلقائياً بـ:
- 🔍 فحص جميع ملفات الكود بحثاً عن تعليقات TODO, FIXME, HACK, XXX, BUG, NOTE
- ✨ إنشاء GitHub Issues تلقائياً لكل تعليق
- 🏷️ إضافة Labels مناسبة حسب نوع التعليق وأولويته
- 👤 تعيين المهمة للمطور الذي أضاف التعليق
- ✅ إغلاق الـ Issue تلقائياً عند حذف التعليق
- 🔄 إعادة فتح الـ Issue إذا عاد التعليق مرة أخرى

---

## 📝 أنواع التعليقات المدعومة

### 1. TODO (مهام عادية)
```python
# TODO: Add caching mechanism for policy evaluation results
```
- **Label:** `type:enhancement`, `priority:medium`
- **الوصف:** مهام تحسينية أو ميزات جديدة مطلوبة
- **الأيقونة:** 📝

### 2. FIXME (مشاكل تحتاج إصلاح)
```python
# FIXME: Need to handle race conditions in concurrent evaluations
```
- **Label:** `type:bug`, `priority:high`, `needs-fix`
- **الوصف:** مشاكل معروفة تحتاج إصلاح عاجل
- **الأيقونة:** 🔥

### 3. HACK (حلول مؤقتة)
```python
# HACK: Hardcoded policy logic, should be loaded from config
```
- **Label:** `type:technical-debt`, `priority:medium`, `refactor`
- **الوصف:** كود يحتاج إعادة هيكلة أو تحسين
- **الأيقونة:** ⚠️

### 4. XXX (تحذيرات مهمة)
```python
# XXX: This code is critical and needs careful review
```
- **Label:** `type:attention-needed`, `priority:high`
- **الوصف:** أجزاء من الكود تحتاج انتباه خاص
- **الأيقونة:** ❗

### 5. BUG (أخطاء حرجة)
```python
# BUG: Memory leak in this function under high load
```
- **Label:** `type:bug`, `priority:critical`
- **الوصف:** أخطاء حرجة تحتاج إصلاح فوري
- **الأيقونة:** 🐛

### 6. NOTE (ملاحظات توثيقية)
```python
# NOTE: This algorithm was optimized for performance
```
- **Label:** `type:documentation`, `priority:low`
- **الوصف:** ملاحظات توثيقية أو تذكيرات
- **الأيقونة:** 📄

---

## 🚀 متى يتم تشغيل الـ Action؟

### 1. عند Push إلى الـ branches الرئيسية
```yaml
on:
  push:
    branches:
      - main
      - master
```

### 2. عند فتح أو تحديث Pull Request
```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

### 3. يدوياً (Manual Trigger)
- اذهب إلى: `Actions` → `Create Issues from TODOs` → `Run workflow`

### 4. جدولة أسبوعية (كل يوم اثنين الساعة 9 صباحاً)
```yaml
schedule:
  - cron: '0 9 * * 1'
```

---

## 🎨 تنسيق الـ Issues المُنشأة

كل Issue يتم إنشاؤه بالشكل التالي:

```markdown
### 📋 Summary
**Type:** TODO
**Priority:** medium
**File:** `policy_evaluator.py`
**Line:** 6

### 💬 Comment
```
Add caching mechanism for policy evaluation results
```

### 📦 Code Context
```python
class PolicyEvaluator:
    # TODO: Add caching mechanism for policy evaluation results
    def __init__(self):
        self.engine = WasmEngine()
```

### 🔗 References
- Commit: abc123
- Author: @username
- Date: 2025-10-02

### ✅ Acceptance Criteria
- [ ] Review the code section
- [ ] Implement the solution
- [ ] Add tests if needed
- [ ] Update documentation
- [ ] Remove the TODO comment

---
*This issue was automatically created from a TODO comment in the code.*
*It will be automatically closed when the TODO comment is removed.*
```

---

## ⚙️ الإعدادات المتقدمة

### 🏷️ Labels التلقائية

| نوع التعليق | Labels المضافة |
|-------------|----------------|
| TODO | `todo`, `automated`, `type:enhancement`, `priority:medium` |
| FIXME | `todo`, `automated`, `type:bug`, `priority:high`, `needs-fix` |
| HACK | `todo`, `automated`, `type:technical-debt`, `priority:medium`, `refactor` |
| XXX | `todo`, `automated`, `type:attention-needed`, `priority:high` |
| BUG | `todo`, `automated`, `type:bug`, `priority:critical` |
| NOTE | `todo`, `automated`, `type:documentation`, `priority:low` |

### 📂 المسارات المستثناة

الـ Action يتجاهل تلقائياً:
- `node_modules/`
- `dist/`
- `build/`
- `__pycache__/`
- `.git/`
- `opa-wasm-env/`

### 🔄 الإدارة التلقائية

| الميزة | الوصف |
|--------|--------|
| ✅ AUTO_ASSIGN | تعيين المهمة للمطور الذي أضاف التعليق |
| ✅ CLOSE_ISSUES | إغلاق الـ Issue عند حذف التعليق |
| ✅ REOPEN_CLOSED_ISSUES | إعادة فتح الـ Issue إذا عاد التعليق |
| ✅ AUTO_P | تنسيق HTML تلقائي |
| ✅ ESCAPE | حماية من الأحرف الخاصة |

---

## 📖 أمثلة على الاستخدام

### ✍️ كتابة TODO بشكل صحيح

#### ❌ خطأ (لن يتم التعرف عليه)
```python
# todo add caching  # بدون نقطتين
# To do: add caching  # مسافة في TODO
//TODO add caching  # بدون مسافة بعد //
```

#### ✅ صحيح
```python
# TODO: Add caching mechanism for policy evaluation results
# FIXME: Handle race conditions in concurrent evaluations
# HACK: Hardcoded values, should be configurable
```

### 🎯 TODO مع سياق أفضل

```python
# TODO: Implement retry logic with exponential backoff
#       - Add max retry count (default: 3)
#       - Add backoff multiplier (default: 2)
#       - Add timeout between retries
#       - Log retry attempts for debugging
def execute_policy():
    pass
```

### 🔗 TODO مع إشارة لـ Issue آخر

```python
# TODO: Refactor this function (related to #42)
# FIXME: This breaks when input is None (see #15)
```

---

## 🛠️ تخصيص الـ Action

### تغيير الـ Labels

```yaml
TODO_LABELS: "enhancement,priority:low,backend"
FIXME_LABELS: "bug,priority:critical,security"
```

### تغيير العنوان

```yaml
TODO_TITLE_PREFIX: "🎯 Task:"
FIXME_TITLE_PREFIX: "🚨 Bug:"
```

### إضافة Milestones

```yaml
ADD_MILESTONES: true
MILESTONE_NAME: "v2.0.0"
```

### إضافة إلى GitHub Projects

```yaml
ADD_PROJECTS: true
PROJECT_NAME: "Development Board"
PROJECT_COLUMN_NAME: "To Do"
```

### وضع الاختبار (Dry Run)

```yaml
DRY_RUN: true  # لن يتم إنشاء Issues فعلية
```

---

## 📊 متابعة الـ Issues

### عرض جميع TODO Issues
```
is:issue is:open label:todo
```

### عرض حسب الأولوية
```
is:issue is:open label:priority:critical
is:issue is:open label:priority:high
is:issue is:open label:priority:medium
```

### عرض حسب النوع
```
is:issue is:open label:type:bug
is:issue is:open label:type:enhancement
is:issue is:open label:type:technical-debt
```

---

## 🎓 أفضل الممارسات

### 1. كتابة TODO واضح ومحدد
```python
# ❌ TODO: fix this
# ✅ TODO: Add input validation for email field (RFC 5322 compliant)
```

### 2. إضافة تقدير الوقت
```python
# TODO: Implement caching layer [Est: 4 hours]
```

### 3. تحديد الأولوية في التعليق
```python
# FIXME: [CRITICAL] Memory leak in connection pool
# TODO: [Low Priority] Add dark mode support
```

### 4. ربط بالوثائق
```python
# TODO: Implement OAuth2 (see docs/authentication.md)
```

### 5. إضافة اسم المسؤول
```python
# FIXME: @john-doe please review this authentication logic
```

---

## 🔍 استكشاف الأخطاء

### المشكلة: لا يتم إنشاء Issues

**الحلول:**
1. تحقق من وجود صلاحيات `issues: write` في الـ workflow
2. تأكد من أن التعليق يتبع الصيغة الصحيحة: `# TODO: description`
3. تحقق من أن الملف ليس في المسارات المستثناة
4. راجع logs الـ Action في تبويب Actions

### المشكلة: تكرار Issues

**الحلول:**
1. تأكد من أن `CLOSE_ISSUES: true`
2. راجع أن التعليق تم حذفه من الكود
3. انتظر تشغيل الـ Action التالي (أو شغله يدوياً)

### المشكلة: عدم تعيين المطور الصحيح

**الحلول:**
1. تأكد من أن `AUTO_ASSIGN: true`
2. تحقق من أن المطور لديه صلاحيات على الـ repo
3. استخدم `ASSIGN_EACH: false` لتعيين المطور الأخير

---

## 📈 إحصائيات وتقارير

بعد كل تشغيل، يمكنك رؤية:
- عدد الـ TODOs الجديدة المكتشفة
- عدد الـ Issues المُنشأة
- عدد الـ Issues المُغلقة
- التوزيع حسب النوع والأولوية

يتم عرض الملخص في تبويب `Summary` بعد تشغيل الـ Action.

---

## 🤝 المساهمة

لتحسين الـ workflow:
1. عدّل ملف `.github/workflows/create-todo-issues.yml`
2. اختبر التغييرات باستخدام `DRY_RUN: true`
3. أنشئ Pull Request مع شرح للتغييرات

---

## 📚 مصادر إضافية

- [alstr/todo-to-issue-action Documentation](https://github.com/alstr/todo-to-issue-action)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Issues Best Practices](https://docs.github.com/en/issues)

---

**تم إنشاء هذا الدليل بواسطة GitHub Copilot** 🤖
