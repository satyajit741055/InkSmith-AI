# InkSmith AI Blog Generator - Frontend

React + TypeScript + Tailwind CSS frontend for the InkSmith AI blog generation platform.

## Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

## Project Structure

```
src/
├── api/              # API client functions
│   ├── client.ts     # Axios instance with auth interceptor
│   ├── auth.ts       # Authentication endpoints
│   └── blog.ts       # Blog generation endpoints
├── components/       # Reusable components
│   ├── Layout.tsx    # Main layout with navbar
│   ├── ProtectedRoute.tsx  # Route guard for authenticated pages
│   ├── BlogForm.tsx  # Form to submit blog topic
│   ├── ProgressPanel.tsx   # Shows generation progress
│   └── MarkdownPreview.tsx # Renders markdown content
├── context/          # React context
│   └── AuthContext.tsx     # Authentication state management
├── pages/            # Page components
│   ├── LandingPage.tsx     # Home page
│   ├── LoginPage.tsx       # Login/Register
│   ├── DashboardPage.tsx   # User dashboard
│   └── NewBlogPage.tsx     # Create new blog
├── App.tsx          # Main app with routing
└── main.tsx         # Entry point
```

## Features

- **Authentication**: Login/Register with JWT tokens
- **Blog Creation**: Submit a prompt to generate a blog
- **Real-time Progress**: Poll backend for generation status
- **Progress Tracking**: Visual progress panel showing current step
- **PDF Download**: Download generated blog as PDF

## Environment

Make sure the backend is running on `http://localhost:8001`

## Development

- Hot reload enabled with Vite
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- TypeScript for type safety
