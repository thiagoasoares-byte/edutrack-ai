# EduTrack AI - Frontend (Next.js/Vercel)

This is the frontend migration of the EduTrack AI application from Streamlit to Next.js/Vercel.

## Overview

This frontend application connects to the existing Xano backend (no changes made to backend/API logic as requested).

## Features

- User authentication (login/logout/profile)
- Subject management (CRUD operations)
- Task management (CRUD operations with filtering)
- Dashboard with metrics and progress tracking
- Reports and analytics
- Responsive design matching original Streamlit theme

## Technology Stack

- Next.js 13.4.19
- React 18.2.0
- JavaScript (ES2020)
- Tailwind-inspired CSS (custom implementation)
- HTTP client: axios
- Cookie management: js-cookie
- Date handling: date-fns

## Environment Variables

Create a `.env.local` file in the root directory with:

```
NEXT_PUBLIC_XANO_URL=https://x8ki-letl-twmt.n7.xano.io/api
```

This should match your Xano instance URL.

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deployment to Vercel

1. Push this repository to GitHub/GitLab/Bitbucket
2. Import the project in Vercel
3. Vercel will automatically detect it's a Next.js project and configure the build settings
4. Add the `NEXT_PUBLIC_XANO_URL` environment variable in Vercel project settings
5. Deploy!

## Project Structure

```
/frontend
  /components       # Reusable React components (empty for now - using inline components)
  /contexts         # React context providers (AuthContext)
  /lib              # Utility functions
    api.js          # HTTP client for Xano API
    auth.js         # Authentication helpers
  /pages            # Next.js pages
    _app.js         # App wrapper with auth checking
    index.js        # Dashboard/home page
    login.js        # Login page
    profile.js      # User profile page
    subjects.js     # Subject management
    tasks.js        # Task management
    reports.js      # Reports and analytics
  /styles           # CSS styles
    globals.css     # Global styles and CSS variables
```

## Backend Integration

This frontend connects to the existing Xano backend with these endpoints:

### Authentication
- POST `/auth/login` - User login
- POST `/auth/signup` - User registration
- POST `/auth/logout` - User logout
- PATCH `/auth/update_profile` - Update user profile

### Subjects
- GET `/subjects/list` - Get all subjects
- POST `/subjects` - Create new subject
- PATCH `/subjects/{id}` - Update subject
- DELETE `/subjects/{id}` - Delete subject

### Tasks
- GET `/academic_tasks/list` - Get all tasks
- POST `/academic_tasks` - Create new task
- PATCH `/academic_tasks/{id}` - Update task
- DELETE `/academic_tasks/{id}` - Delete task

All requests include authentication via Bearer token in cookies.

## Design

The UI maintains the original Streamlit theme:
- Dark navy background (`#0f1724`)
- Card background (`#0b1220`)
- Accent colors (teal: `#6ee7b7`, blue: `#7dd3fc`)
- Consistent border-radius, shadows, and spacing

## Notes

- No changes were made to the backend/Xano API logic as requested
- All functionality mirrors the original Streamlit application
- Authentication is handled via cookies (js-cookie) to match original behavior
- Date handling uses date-fns for consistency
- Responsive design works on mobile and desktop

## Troubleshooting

If you encounter CORS issues, make sure your Xano instance has CORS enabled for your Vercel domain.

For authentication issues, check that cookies are being set correctly and that the Xano auth endpoints are working properly.