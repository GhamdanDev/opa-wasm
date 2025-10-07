# ✅ قائمة المهام المطلوبة على GitHub - خطوة بخطوة

> **كل ما يجب عليك القيام به على GitHub لتشغيل Slack workflows**

---

## 📝 المهام المطلوبة على GitHub

### ✅ المهمة 1: إضافة السر الأساسي (SLACK_BOT_TOKEN)

**هذا إجباري ولن تعمل الـ workflows بدونه!**

#### الخطوات:

1. **افتح مستودعك في GitHub**
   ```
   اذهب إلى: https://github.com/YOUR-USERNAME/YOUR-REPO
   ```

2. **اذهب إلى الإعدادات**
   ```
   اضغط على تبويب "Settings" في الأعلى
   ```

3. **افتح صفحة الأسرار**
   ```
   من القائمة الجانبية اليسرى:
   اضغط "Secrets and variables" → ثم اضغط "Actions"
   ```

4. **أضف سر جديد**
   ```
   اضغط الزر الأخضر "New repository secret"
   ```

5. **أدخل معلومات السر**
   ```
   Name: SLACK_BOT_TOKEN
   
   Secret: (الصق هنا الـ Token من Slack)
   ملاحظة: يبدأ الـ Token بـ xoxb- ويكون طويلاً
   ```

6. **احفظ**
   ```
   اضغط "Add secret"
   ```

**✅ تم! السر الأساسي جاهز**

---

### ⚠️ المهمة 2: إضافة أسرار القنوات (اختياري)

**هذه اختيارية - إذا لم تضفها، سيستخدم النظام القنوات الافتراضية**

إذا كنت تريد استخدام أسماء قنوات مخصصة (غير `#critical-todos`, `#dev-todos`, `#dev-reports`)، أضف هذه الأسرار:

#### كرر نفس الخطوات السابقة لكل سر:

**السر 1:**
```
Name: SLACK_CRITICAL_CHANNEL
Secret: #your-critical-channel-name
```

**السر 2:**
```
Name: SLACK_GENERAL_CHANNEL
Secret: #your-general-channel-name
```

**السر 3:**
```
Name: SLACK_REPORTS_CHANNEL
Secret: #your-reports-channel-name
```

**ملاحظة:** أسماء القنوات يجب أن تبدأ بـ `#`

---

### ✅ المهمة 3: التحقق من وجود ملفات Workflows

**تأكد أن هذه الملفات موجودة في مستودعك:**

#### افتح مستودعك وتحقق من:

```
.github/
  └── workflows/
      ├── create-todo-issues.yml        ← يجب أن يكون موجود
      ├── slack-notifications.yml       ← يجب أن يكون موجود
      └── slack-notifications-advanced.yml  ← يجب أن يكون موجود
```

**كيف تتحقق:**
1. في صفحة مستودعك على GitHub
2. اضغط على مجلد `.github`
3. ثم اضغط على مجلد `workflows`
4. يجب أن ترى الملفات الثلاثة

**إذا لم تكن موجودة:**
- الملفات موجودة محلياً على جهازك
- تحتاج لعمل `git push` لرفعها لـ GitHub

---

### ✅ المهمة 4: تفعيل GitHub Actions

**تأكد أن GitHub Actions مُفعّل:**

1. **اذهب إلى تبويب Actions**
   ```
   في صفحة المستودع، اضغط "Actions"
   ```

2. **تحقق من الحالة**
   - إذا رأيت قائمة بالـ workflows → **مُفعّل ✅**
   - إذا رأيت رسالة "Workflows are disabled" → **غير مُفعّل ❌**

3. **لتفعيل GitHub Actions (إذا كان معطلاً):**
   ```
   اضغط الزر الأخضر "I understand my workflows, go ahead and enable them"
   ```

---

### ✅ المهمة 5: منح الأذونات المطلوبة

**تأكد أن الـ workflows تملك الأذونات الكافية:**

1. **اذهب إلى Settings**
   ```
   Settings → Actions → General
   ```

2. **انزل إلى "Workflow permissions"**

3. **اختر أحد الخيارين:**
   - **الخيار المُوصى به:** "Read and write permissions"
   - **أو:** ابقِ على "Read repository contents and packages permissions" وفعّل:
     - ✅ "Allow GitHub Actions to create and approve pull requests"

4. **احفظ**
   ```
   اضغط "Save"
   ```

---

### ✅ المهمة 6: إجراء اختبار يدوي

**الآن اختبر أن كل شيء يعمل:**

1. **اذهب إلى Actions**
   ```
   في صفحة المستودع، اضغط "Actions"
   ```

2. **اختر الـ workflow**
   ```
   من القائمة الجانبية اليسرى، اختر:
   "🔔 Advanced Slack Notifications for TODOs"
   ```

3. **شغّل يدوياً**
   ```
   اضغط "Run workflow" (الزر الأزرق على اليمين)
   ```

4. **اختر نوع الإشعار**
   ```
   في القائمة المنسدلة:
   notification_type → اختر "test_notification"
   ```

5. **شغّل**
   ```
   اضغط "Run workflow" الأخضر
   ```

6. **راقب التنفيذ**
   ```
   انتظر 10-30 ثانية
   يجب أن ترى:
   - نقطة صفراء 🟡 (قيد التشغيل)
   - ثم علامة خضراء ✅ (نجح)
   
   إذا رأيت علامة حمراء ❌:
   - اضغط عليها
   - اقرأ رسالة الخطأ
   - راجع قسم "حل المشاكل" أدناه
   ```

7. **تحقق من Slack**
   ```
   يجب أن تظهر رسالة في #dev-todos:
   "✅ Slack Integration Test Successful!"
   ```

---

## 📋 قائمة التحقق النهائية

تأكد من إكمال كل خطوة:

### على GitHub:
- [ ] ✅ أضفت سر `SLACK_BOT_TOKEN` في Settings → Secrets → Actions
- [ ] ✅ (اختياري) أضفت أسرار القنوات المخصصة
- [ ] ✅ ملفات workflows موجودة في `.github/workflows/`
- [ ] ✅ GitHub Actions مُفعّل
- [ ] ✅ أذونات Workflow صحيحة (Read and write permissions)
- [ ] ✅ أجريت اختبار يدوي ونجح

### على Slack (يجب أن تكون جاهزة):
- [ ] ✅ أنشأت Slack App
- [ ] ✅ منحت الصلاحيات (chat:write, chat:write.public, channels:read)
- [ ] ✅ حصلت على Bot Token (يبدأ بـ xoxb-)
- [ ] ✅ أنشأت القنوات (#critical-todos, #dev-todos, #dev-reports)
- [ ] ✅ دعوت البوت للقنوات (/invite @BotName)

---

## ❌ حل المشاكل الشائعة على GitHub

### مشكلة: السر غير موجود

**الأعراض:**
```
Error in workflow: SLACK_BOT_TOKEN secret not found
```

**الحل:**
1. تحقق من الاسم بالضبط: `SLACK_BOT_TOKEN` (كل الحروف كبيرة)
2. تحقق أنك في المستودع الصحيح
3. أعد إضافة السر بدقة

---

### مشكلة: Workflow لا يظهر في Actions

**الأعراض:**
- لا ترى الـ workflows في تبويب Actions

**الحل:**
1. تأكد أن الملفات في المسار الصحيح: `.github/workflows/`
2. تأكد أن امتداد الملفات `.yml` (وليس `.txt`)
3. تأكد أنك عملت `git push` للملفات
4. تحقق من وجود أخطاء YAML:
   ```
   يمكنك استخدام: https://www.yamllint.com/
   ```

---

### مشكلة: Workflow يفشل عند التشغيل

**الأعراض:**
- علامة حمراء ❌ بعد تشغيل workflow

**الحل:**
1. **افتح تفاصيل الخطأ:**
   - اضغط على الـ workflow الفاشل
   - اضغط على الـ job الفاشل
   - اقرأ رسالة الخطأ

2. **أخطاء شائعة:**

   **خطأ: "channel_not_found"**
   ```
   الحل: البوت غير مدعو للقناة
   في Slack: /invite @TODO Bot
   ```

   **خطأ: "not_authed"**
   ```
   الحل: Token خاطئ أو منتهي
   أعد نسخ Token من Slack وحدّث السر
   ```

   **خطأ: "missing_scope"**
   ```
   الحل: أضف الصلاحية المطلوبة في Slack App
   ثم أعد تثبيت App وحدّث Token
   ```

---

### مشكلة: الأذونات غير كافية

**الأعراض:**
```
Error: Resource not accessible by integration
```

**الحل:**
1. Settings → Actions → General
2. Workflow permissions
3. اختر "Read and write permissions"
4. Save

---

## 🎯 ملخص سريع: ما يجب عليك فعله على GitHub

```
1️⃣ إضافة SLACK_BOT_TOKEN في Secrets
   └─> Settings → Secrets → Actions → New secret

2️⃣ (اختياري) إضافة أسرار القنوات المخصصة
   └─> نفس الخطوات لـ SLACK_*_CHANNEL

3️⃣ التحقق من وجود ملفات workflows
   └─> .github/workflows/*.yml موجودة

4️⃣ تفعيل GitHub Actions
   └─> Actions → Enable workflows

5️⃣ منح الأذونات
   └─> Settings → Actions → Workflow permissions

6️⃣ اختبار
   └─> Actions → Run workflow → test_notification
```

**الوقت المطلوب:** 5 دقائق فقط على GitHub

---

## 🔗 روابط مساعدة

- **إضافة Secrets:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **تفعيل Actions:** https://docs.github.com/en/actions/managing-workflow-runs/disabling-and-enabling-a-workflow
- **Workflow Permissions:** https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token

---

## ✅ بعد الانتهاء

عندما تكمل كل الخطوات:

1. **شغّل اختبار:**
   ```
   Actions → Advanced Slack Notifications → Run workflow → test_notification
   ```

2. **انتظر النتيجة:**
   ```
   ✅ رسالة في Slack → نجح!
   ❌ خطأ → راجع قسم حل المشاكل
   ```

3. **استمتع:**
   ```
   الآن ستحصل على:
   - تنبيهات حرجة فورية
   - ملخص يومي الساعة 9 صباحاً
   - تقارير أسبوعية (يدوية)
   ```

---

**إذا أكملت كل هذه الخطوات ولا يزال لا يعمل:**
راجع [الدليل الكامل لحل المشاكل](.github/SLACK_INTEGRATION_GUIDE_AR.md#-استكشاف-الأخطاء-وإصلاحها)

---

**آخر تحديث:** 2025-10-07  
**الصعوبة:** سهل جداً 🟢  
**الوقت:** 5 دقائق
