# Step-by-step: Replace Supabase Edge Functions with Django (for your Vite + React + Capacitor app)

## 1) Configure the backend
- Unzip `django-backend.zip`
- Create and activate a virtualenv
- `pip install -r requirements.txt`
- Copy `.env.example` to `.env`, adjust `API_KEYS` and DB settings if needed
- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`

## 2) Create a frontend API helper
Add a file `src/services/api.ts`:

```ts
export const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

const authHeader = () => ({
  Authorization: `Bearer ${import.meta.env.VITE_API_KEY ?? "dev-key-123"}`,
  "Content-Type": "application/json"
});

export async function aiDiagnosis(cropType: string, symptoms: string) {
  const res = await fetch(`${API_BASE}/ai-diagnosis`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify({ cropType, symptoms })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ diagnosis: string, treatment: string, confidence: number }>;
}

export async function farmingAdvice(location: {lat: number, lng: number}, cropType: string, season: string) {
  const res = await fetch(`${API_BASE}/farming-advice`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify({ location, cropType, season })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ advice: string, plantingDate: string }>;
}

export async function marketAnalysis(cropType: string, district: string, quantity: number) {
  const res = await fetch(`${API_BASE}/market-analysis`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify({ cropType, district, quantity })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ predictedPrice: number, trend: string }>;
}
```

Then in your pages/components, replace the Supabase URLs with calls to these helpers.

## 3) Add a `.env` for Vite
Create `.env.local` in your frontend root:

```env
VITE_API_BASE=http://localhost:8000/api/v1
VITE_API_KEY=dev-key-123
```

## 4) Test end-to-end
- Start backend: `python manage.py runserver`
- Start frontend: `bun dev` or `npm run dev`
- Use your app's UI pages to verify responses

## 5) Production hardening (recommended)
- Switch to Postgres and set `DEBUG=false`
- Set `CORS_ALLOW_ALL=false` and declare allowed origins
- Rotate `API_KEYS` and store in DB (consider `djangorestframework-api-key`)
- Add Celery+Redis if you want long-running AI jobs
- Add request rate limiting (e.g., `django-ratelimit`)

## 6) OpenAPI / Swagger
Visit `http://localhost:8000/api/docs/` for live docs. You can generate a Postman collection from the OpenAPI schema at `/api/schema/`.
