src/
│
├── app/
│   ├── layouts/
│   │   ├── AppLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── BlankLayout.tsx
│   │
│   ├── providers/
│   │   ├── MantineProvider.tsx
│   │   └── QueryProvider.tsx
│   │
│   ├── router/
│   │   ├── AppRouter.tsx
│   │   ├── ProtectedRoute.tsx
│   │   ├── RoleRoute.tsx
│   │   └── routes.ts
│   │
│   └── theme/
│       ├── theme.ts
│       └── globals.css
│
├── modules/
│   ├── auth/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── types.ts
│   │
│   ├── customer/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── types.ts
│   │
│   ├── owner/
│   ├── delivery/
│   ├── admin/
│   └── health/
│
├── shared/
│   ├── api/
│   │   ├── axios.ts
│   │   └── interceptors.ts
│   │
│   ├── components/
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── PageHeader/
│   │   ├── Loader/
│   │   └── EmptyState/
│   │
│   ├── constants/
│   ├── hooks/
│   ├── stores/
│   │   ├── auth.store.ts
│   │   ├── cart.store.ts
│   │   ├── ui.store.ts
│   │   └── warmup.store.ts
│   │
│   ├── types/
│   ├── utils/
│   └── lib/
│
├── assets/
│
├── App.tsx
├── main.tsx
└── vite-env.d.ts