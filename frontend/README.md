# GRACE Frontend

The frontend is a desktop-first responsive institutional administration client built with React, TypeScript, Vite, and Material UI.

```bash
cp .env.example .env
npm install
npm run dev
npm run build
```

`VITE_API_URL` defaults to `http://localhost:8000/api/v1`. Access tokens are attached through the shared API client and refreshed using the JWT refresh endpoint. Authorization is always enforced by the backend; UI visibility is not a security boundary.

The interface includes explicit loading, error, and empty states, consistent status labels, a dynamic risk heat map, aggregate dashboard, working CSV exports, AI generation, and human review controls.

