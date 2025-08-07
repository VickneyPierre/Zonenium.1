**COPY EXACTLY:**

requirements.txt:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
```

main.py:
Action: file_editor view /app/zonenium/deployment_main.py
Observation: /app/zonenium/deployment_main.py:
1|from fastapi import FastAPI, HTTPException
2|from fastapi.middleware.cors import CORSMiddleware
3|from fastapi.responses import HTMLResponse, JSONResponse
4|import os
5|
6|PORT = int(os.environ.get("PORT", 8000))
7|DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
8|
9|app = FastAPI(
10|    title="Zoneium Messenger - Premium Messaging Experience", 
11|    description="Reliable. Private. Beautiful. The most elegant messaging app for modern communication.",
12|    version="3.0.0"
13|)
14|
15|app.add_middleware(
16|    CORSMiddleware,
17|    allow_origins=["*"],
18|    allow_credentials=True,
19|    allow_methods=["*"],
20|    allow_headers=["*"]
21|)
22|
23|@app.get("/")
24|def home():
25|    html_content = """
26|    <!DOCTYPE html>
27|    <html lang="en">
28|    <head>
29|        <meta charset="UTF-8">
30|        <meta name="viewport" content="width=device-width, initial-scale=1.0">
31|        <title>Zoneium - Premium Messaging Experience</title>
32|        <meta name="theme-color" content="#FF6B35">
33|        <link rel="preconnect" href="https://fonts.googleapis.com">
34|        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
35|        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
36|        <style>
37|            :root {
38|                --primary-orange: #FF6B35;
39|                --primary-orange-hover: #E55D2B;
40|                --primary-orange-light: #FF8F66;
41|                --secondary-orange: #FFF4F0;
42|                --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #FF8F66 100%);
43|                --gradient-secondary: linear-gradient(135deg, #FFF4F0 0%, #FFEDE5 100%);
44|                --white: #FFFFFF;
45|                --gray-50: #FAFBFC;
46|                --gray-100: #F3F4F6;
47|                --gray-200: #E5E7EB;
48|                --gray-300: #D1D5DB;
49|                --gray-400: #9CA3AF;
50|                --gray-500: #6B7280;
51|                --gray-600: #4B5563;
52|                --gray-700: #374151;
53|                --gray-800: #1F2937;
54|                --gray-900: #111827;
55|                --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
56|                --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
57|                --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
58|            }
59|
60|            * { margin: 0; padding: 0; box-sizing: border-box; }
61|
62|            body {
63|                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
64|                background: var(--gradient-primary);
65|                min-height: 100vh;
66|                display: flex;
67|                align-items: center;
68|                justify-content: center;
69|                line-height: 1.6;
70|                color: var(--gray-800);
71|                overflow: hidden;
72|                position: relative;
73|            }
74|
75|            .bg-decoration {
76|                position: absolute;
77|                width: 200px;
78|                height: 200px;
79|                border-radius: 50%;
80|                background: rgba(255, 255, 255, 0.1);
81|                animation: float 6s ease-in-out infinite;
82|            }
83|            .bg-decoration:nth-child(1) {
84|                top: 10%;
85|                left: 10%;
86|                animation-delay: 0s;
87|            }
88|            .bg-decoration:nth-child(2) {
89|                top: 70%;
90|                right: 10%;
91|                animation-delay: 2s;
92|                width: 150px;
93|                height: 150px;
94|            }
95|            .bg-decoration:nth-child(3) {
96|                bottom: 20%;
97|                left: 20%;
98|                animation-delay: 4s;
99|                width: 100px;
100|                height: 100px;
101|            }
102|
103|            @keyframes float {
104|                0%, 100% { transform: translateY(0px) rotate(0deg); }
105|                50% { transform: translateY(-20px) rotate(180deg); }
106|            }
107|
108|            .container {
109|                max-width: 420px;
110|                width: 90%;
111|                position: relative;
112|                z-index: 10;
113|            }
114|
115|            .login-card {
116|                background: rgba(255, 255, 255, 0.95);
117|                border-radius: 24px;
118|                padding: 40px 32px;
119|                box-shadow: var(--shadow-large);
120|                backdrop-filter: blur(20px);
121|                border: 1px solid rgba(255, 255, 255, 0.2);
122|                animation: slideUp 0.8s ease-out;
123|            }
124|
125|            @keyframes slideUp {
126|                from {
127|                    opacity: 0;
128|                    transform: translateY(30px);
129|                }
130|                to {
131|                    opacity: 1;
132|                    transform: translateY(0);
133|                }
134|            }
135|
136|            .logo-container {
137|                text-align: center;
138|                margin-bottom: 32px;
139|            }
140|
141|            .logo {
142|                width: 80px;
143|                height: 80px;
144|                margin: 0 auto 16px;
145|                background: var(--gradient-primary);
146|                border-radius: 20px;
147|                display: flex;
148|                align-items: center;
149|                justify-content: center;
150|                box-shadow: var(--shadow-medium);
151|                transition: transform 0.3s ease;
152|                font-size: 32px;
153|                font-weight: 900;
154|                color: white;
155|            }
156|
157|            .logo:hover {
158|                transform: scale(1.05);
159|            }
160|
161|            .app-title {
162|                font-size: 28px;
163|                font-weight: 800;
164|                color: var(--gray-800);
165|                margin-bottom: 8px;
166|                letter-spacing: -0.02em;
167|            }
168|
169|            .app-subtitle {
170|                color: var(--gray-500);
171|                font-size: 16px;
172|                font-weight: 500;
173|                margin-bottom: 32px;
174|            }
175|
176|            .form-group {
177|                margin-bottom: 24px;
178|            }
179|
180|            .form-label {
181|                display: block;
182|                font-size: 14px;
183|                font-weight: 600;
184|                color: var(--gray-700);
185|                margin-bottom: 8px;
186|            }
187|
188|            .form-input {
189|                width: 100%;
190|                padding: 16px 18px;
191|                border: 2px solid var(--gray-200);
192|                border-radius: 12px;
193|                font-size: 16px;
194|                font-weight: 500;
195|                color: var(--gray-800);
196|                background: var(--white);
197|                transition: all 0.3s ease;
198|                outline: none;
199|            }
200|
201|            .form-input:focus {
202|                border-color: var(--primary-orange);
203|                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
204|                transform: translateY(-1px);
205|            }
206|
207|            .form-input::placeholder {
208|                color: var(--gray-400);
209|                font-weight: 400;
210|            }
211|
212|            .primary-button {
213|                width: 100%;
214|                padding: 18px 24px;
215|                background: var(--gradient-primary);
216|                color: var(--white);
217|                border: none;
218|                border-radius: 12px;
219|                font-size: 16px;
220|                font-weight: 700;
221|                cursor: pointer;
222|                transition: all 0.3s ease;
223|                box-shadow: var(--shadow-medium);
224|                margin-bottom: 20px;
225|                text-decoration: none;
226|                display: inline-block;
227|                text-align: center;
228|            }
229|
230|            .primary-button:hover {
231|                background: linear-gradient(135deg, var(--primary-orange-hover) 0%, var(--primary-orange) 100%);
232|                transform: translateY(-2px);
233|                box-shadow: var(--shadow-large);
234|            }
235|
236|            .secondary-button {
237|                width: 100%;
238|                padding: 16px 24px;
239|                background: transparent;
240|                color: var(--gray-600);
241|                border: 2px solid var(--gray-200);
242|                border-radius: 12px;
243|                font-size: 16px;
244|                font-weight: 600;
245|                cursor: pointer;
246|                transition: all 0.3s ease;
247|                margin-bottom: 20px;
248|                text-decoration: none;
249|                display: inline-block;
250|                text-align: center;
251|            }
252|
253|            .secondary-button:hover {
254|                border-color: var(--primary-orange);
255|                color: var(--primary-orange);
256|                background: rgba(255, 107, 53, 0.05);
257|                transform: translateY(-1px);
258|            }
259|
260|            .launch-button {
261|                background: linear-gradient(135deg, #10B981 0%, #059669 100%);
262|                margin-bottom: 16px;
263|            }
264|            
265|            .launch-button:hover {
266|                background: linear-gradient(135deg, #059669 0%, #047857 100%);
267|            }
268|
269|            .divider {
270|                text-align: center;
271|                margin: 24px 0;
272|                position: relative;
273|                color: var(--gray-400);
274|                font-size: 14px;
275|                font-weight: 500;
276|            }
277|
278|            .divider::before {
279|                content: '';
280|                position: absolute;
281|                top: 50%;
282|                left: 0;
283|                right: 0;
284|                height: 1px;
285|                background: var(--gray-200);
286|                z-index: 1;
287|            }
288|
289|            .divider span {
290|                background: var(--white);
291|                padding: 0 16px;
292|                position: relative;
293|                z-index: 2;
294|            }
295|
296|            .features {
297|                margin-top: 32px;
298|                text-align: center;
299|            }
300|
301|            .features-title {
302|                font-size: 18px;
303|                font-weight: 700;
304|                color: var(--gray-800);
305|                margin-bottom: 16px;
306|            }
307|
308|            .features-list {
309|                display: grid;
310|                grid-template-columns: repeat(2, 1fr);
311|                gap: 12px;
312|                font-size: 14px;
313|                color: var(--gray-600);
314|            }
315|
316|            .feature-item {
317|                display: flex;
318|                align-items: center;
319|                gap: 8px;
320|                padding: 8px 12px;
321|                background: var(--secondary-orange);
322|                border-radius: 8px;
323|                font-weight: 500;
324|            }
325|
326|            .feature-icon {
327|                width: 16px;
328|                height: 16px;
329|                background: var(--primary-orange);
330|                border-radius: 50%;
331|                display: flex;
332|                align-items: center;
333|                justify-content: center;
334|                color: white;
335|                font-size: 10px;
336|                font-weight: bold;
337|            }
338|
339|            @media (max-width: 480px) {
340|                .container { width: 95%; }
341|                .login-card { padding: 32px 24px; }
342|                .app-title { font-size: 24px; }
343|                .form-input, .primary-button { font-size: 16px; }
344|                .features-list { grid-template-columns: 1fr; }
345|            }
346|        </style>
347|    </head>
348|    <body>
349|        <div class="bg-decoration"></div>
350|        <div class="bg-decoration"></div>
351|        <div class="bg-decoration"></div>
352|        
353|        <div class="container">
354|            <div class="login-card">
355|                <div class="logo-container">
356|                    <div class="logo">Z</div>
357|                    <h1 class="app-title">Zonenium</h1>
358|                    <p class="app-subtitle">Reliable • Private • Beautiful</p>
359|                </div>
360|
361|                <form id="loginForm">
362|                    <div class="form-group">
363|                        <label class="form-label" for="phone">Phone Number</label>
364|                        <input 
365|                            type="tel" 
366|                            id="phone" 
367|                            name="phone" 
368|                            class="form-input" 
369|                            placeholder="+1 (555) 123-4567"
370|                            required
371|                        />
372|                    </div>
373|
374|                    <div class="form-group">
375|                        <label class="form-label" for="password">Password</label>
376|                        <input 
377|                            type="password" 
378|                            id="password" 
379|                            name="password" 
380|                            class="form-input" 
381|                            placeholder="Enter your password"
382|                            required
383|                        />
384|                    </div>
385|
386|                    <a href="/app" class="primary-button launch-button">
387|                        🚀 Launch App
388|                    </a>
389|
390|                    <button type="submit" class="primary-button">
391|                        Sign In to Zonenium
392|                    </button>
393|                </form>
394|
395|                <div class="divider">
396|                    <span>or</span>
397|                </div>
398|
399|                <a href="/register" class="secondary-button">
400|                    Create New Account
401|                </a>
402|
403|                <div class="features">
404|                    <h3 class="features-title">Why Choose Zonenium?</h3>
405|                    <div class="features-list">
406|                        <div class="feature-item">
407|                            <div class="feature-icon">🔒</div>
408|                            <span>End-to-End Encrypted</span>
409|                        </div>
410|                        <div class="feature-item">
411|                            <div class="feature-icon">⚡</div>
412|                            <span>Lightning Fast</span>
413|                        </div>
414|                        <div class="feature-item">
415|                            <div class="feature-icon">🎵</div>
416|                            <span>Voice Messages</span>
417|                        </div>
418|                        <div class="feature-item">
419|                            <div class="feature-icon">👥</div>
420|                            <span>Group Chats</span>
421|                        </div>
422|                    </div>
423|                </div>
424|            </div>
425|        </div>
426|
427|        <script>
428|            document.getElementById('loginForm').addEventListener('submit', function(e) {
429|                e.preventDefault();
430|                window.location.href = '/app';
431|            });
432|        </script>
433|    </body>
434|    </html>
435|    """
436|    return HTMLResponse(content=html_content)
437|
438|@app.get("/app")
439|def messenger_app():
440|    return HTMLResponse(content="""
441|    <!DOCTYPE html>
442|    <html><head><title>Zonenium - Messaging App</title></head>
443|    <body style="font-family: Arial; text-align: center; padding: 50px; background: #1F2937; color: white;">
444|        <div style="max-width: 400px; margin: 0 auto;">
445|            <div style="width: 60px; height: 60px; margin: 0 auto 20px; background: linear-gradient(135deg, #FF6B35, #FF8F66); border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white;">Z</div>
446|            <h1>Welcome to Zonenium</h1>
447|            <p>Premium messaging experience coming soon!</p>
448|            <div style="margin: 30px 0;">
449|                <h3>Demo Accounts:</h3>
450|                <p>Username: demo_user, Password: demo123</p>
451|                <p>Username: test_user, Password: test123</p>
452|            </div>
453|            <p><a href="/" style="color: #FF6B35;">← Back to Home</a></p>
454|        </div>
455|    </body></html>
456|    """)
457|
458|@app.get("/api/status")
459|def get_status():
460|    return {
461|        "status": "live",
462|        "app": "Zoneium Messenger Premium",
463|        "version": "3.0.0",
464|        "message": "Premium messaging experience with your branding - Reliable. Private. Beautiful.",
465|        "features": [
466|            "Beautiful landing page with your Zonenium branding",
467|            "Launch App button for seamless navigation", 
468|            "Premium UI with glass-morphism effects",
469|            "Mobile responsive design",
470|            "Ready for full messaging features"
471|        ]
472|    }
473|
474|if __name__ == "__main__":
475|    import uvicorn
476|    uvicorn.run(app, host="0.0.0.0", port=PORT)

