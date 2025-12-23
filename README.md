## Darkman yt-dlp API

Backend بسيط مبني على Flask + yt-dlp لاستخراج معلومات وصيغ الصوت/الفيديو من روابط يوتيوب (وعدد كبير من المواقع الأخرى) على شكل JSON، ليتم استهلاكها من تطبيق أندرويد أو أي عميل آخر.

- المطوّر: **darkman**  
- تيليجرام: [t.me/darkman_bin](https://t.me/darkman_bin)

## المميزات
- إرجاع معلومات الفيديو (العنوان، المدة، الصورة المصغرة، رابط الصفحة، القناة).
- إرجاع قائمة كاملة بالصيغ المتاحة:
  - صيغ صوت فقط (Audio only).
  - صيغ فيديو فقط (Video only).
  - دقة الفيديو، نوع الكودك، الامتداد، الحجم التقريبي، معدل البت.


## هيكلة المشروع
```
api/
  index.py        - كود Flask + yt-dlp
requirements.txt  - حزم Python المطلوبة
vercel.json       - إعدادات نشر المشروع على Vercel
```
## الاستخدام

### نقطة التحقق الأساسية
``GET /``

الرد:
```
{
  "name": "Darkman yt-dlp API",
  "author": "darkman",
  "contact": "t.me/darkman_bin",
  "status": "ok"
}
```


### نقطة جلب معلومات الفيديو

```
GET /info?url=VIDEO_URL
```

مثال:
```
curl "https://YOUR_PROJECT_NAME.vercel.app/info?url=https://www.youtube.com/watch?v=XXXXXXXXXXX"
```
الرد يكون JSON مشابه للتالي (مختصر):

```
{
  "id": "XXXXXXXXXXX",
  "title": "...",
  "thumbnail": "https://i.ytimg.com/vi/XXXXXXXXXXX/maxresdefault.jpg",
  "duration": 2092,
  "webpage_url": "https://www.youtube.com/watch?v=XXXXXXXXXXX",
  "uploader": "...",
  "channel": "...",
  "formats": [
    {
      "format_id": "140",
      "ext": "m4a",
      "vcodec": "none",
      "acodec": "mp4a.40.2",
      "resolution": null,
      "fps": null,
      "filesize": 33860903,
      "tbr": 129.0,
      "url": "https://...audio-stream-url..."
    },
    {
      "format_id": "137",
      "ext": "mp4",
      "vcodec": "avc1.640028",
      "acodec": "none",
      "resolution": "1920x1080",
      "fps": 30,
      "filesize": 977482421,
      "tbr": 3737.7,
      "url": "https://...video-stream-url..."
    }
  ]
}
```

## تنبيه قانوني

هذا المشروع يعتمد على yt-dlp، واستخدامه يخضع لشروط خدمة المواقع التي تتعامل معها (مثل YouTube) والقوانين في بلدك.  
المطوّر غير مسؤول عن أي استخدام غير قانوني أو مخالف لتلك الشروط.
