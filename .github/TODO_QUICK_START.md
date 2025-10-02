# 🤖 GitHub Actions - TODO to Issue Automation

## 🚀 البداية السريعة

### 1. إعداد الـ Labels (مرة واحدة فقط)

```bash
# اذهب إلى Actions → Setup Labels for TODO Action → Run workflow
```

أو يدوياً من تبويب Issues → Labels وأنشئ:
- `todo`, `automated`
- `type:enhancement`, `type:bug`, `type:technical-debt`
- `priority:critical`, `priority:high`, `priority:medium`, `priority:low`

### 2. كتابة TODO في الكود

```python
# TODO: Add input validation for user data
# FIXME: Handle timeout errors properly
# HACK: Temporary solution, needs refactoring
```

### 3. Push إلى main/master

```bash
git add .
git commit -m "Add TODO comments"
git push origin main
```

### 4. شاهد الـ Issues تُنشأ تلقائياً! ✨

---

## 📋 الأوامر المتاحة

| تعليق | الأولوية | النوع | الأيقونة |
|-------|----------|-------|----------|
| `TODO:` | Medium | Enhancement | 📝 |
| `FIXME:` | High | Bug | 🔥 |
| `HACK:` | Medium | Technical Debt | ⚠️ |
| `XXX:` | High | Attention | ❗ |
| `BUG:` | Critical | Bug | 🐛 |
| `NOTE:` | Low | Documentation | 📄 |

---

## 🎯 أمثلة عملية

### Python
```python
# TODO: Implement caching mechanism
class MyClass:
    pass

# FIXME: Race condition in multi-threading
def process_data():
    pass
```

### JavaScript/TypeScript
```javascript
// TODO: Add error boundaries
function App() {
  // FIXME: Memory leak in useEffect
  return <div>Hello</div>;
}
```

### YAML/Config
```yaml
# TODO: Add production configuration
config:
  debug: true
```

---

## 📊 عرض الـ Issues

### حسب الأولوية
```
is:issue is:open label:priority:critical
is:issue is:open label:priority:high
```

### حسب النوع
```
is:issue is:open label:type:bug
is:issue is:open label:type:enhancement
```

### جميع TODOs المفتوحة
```
is:issue is:open label:todo
```

---

## ⚙️ متى يعمل الـ Action؟

✅ Push إلى main/master  
✅ فتح/تحديث Pull Request  
✅ يدوياً من تبويب Actions  
✅ كل يوم اثنين 9 صباحاً (جدولة)

---

## 🔄 دورة الحياة

1. **كتابة TODO** → يتم إنشاء Issue تلقائياً
2. **حل المشكلة** → احذف تعليق TODO من الكود
3. **Push** → يتم إغلاق الـ Issue تلقائياً
4. **إذا عاد TODO** → يُعاد فتح الـ Issue

---

## 🛠️ استكشاف الأخطاء

### لا يتم إنشاء Issues؟

1. تحقق من صيغة TODO:
   ```python
   # ✅ TODO: description
   # ❌ todo description
   # ❌ TODO description
   ```

2. تحقق من الصلاحيات في `create-todo-issues.yml`
3. راجع Logs في تبويب Actions

---

## 📖 التوثيق الكامل

راجع: [TODO_WORKFLOW_GUIDE.md](.github/TODO_WORKFLOW_GUIDE.md)

---

## 🎓 نصائح الخبراء

1. **كن محدداً:** `TODO: Add retry logic with 3 attempts` أفضل من `TODO: fix this`
2. **أضف تقدير:** `TODO: [2 hours] Implement OAuth2`
3. **اربط بالوثائق:** `TODO: See architecture.md for details`
4. **حدد المسؤول:** `FIXME: @john-doe review this logic`

---

## 📈 الإحصائيات

بعد إعداد الـ Action، يمكنك تتبع:
- 📊 عدد TODOs النشطة
- ⏱️ متوسط وقت الحل
- 👥 التوزيع على المطورين
- 🎯 الأولويات المفتوحة

---

**الإعداد:** تم ✅  
**الاستخدام:** سهل ✅  
**التتبع:** تلقائي ✅

🚀 ابدأ الآن بكتابة أول TODO!
