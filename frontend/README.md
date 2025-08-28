# TxVoc Frontend

A modern, responsive Next.js frontend for the TxVoc text-to-speech synthesis application.

## Features

- 🎨 **Modern Design**: Clean, minimal UI with cool color palette and smooth animations
- 📱 **Fully Responsive**: Works seamlessly on mobile, tablet, and desktop
- 🎯 **Interactive Elements**: Drag-and-drop file upload, custom audio player, smooth transitions
- 🌙 **Dark Theme**: Beautiful dark theme with glassmorphism effects
- ⚡ **Fast Performance**: Built with Next.js 15 and optimized for speed
- 🧩 **Component Library**: Uses shadcn/ui for consistent, accessible components

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS v4 with custom design system
- **Components**: shadcn/ui
- **Icons**: Lucide React
- **Animations**: CSS animations and smooth transitions

## Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn package manager

### Installation

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:3000
   ```

## Backend Integration

The frontend is configured to connect to the backend API at `http://localhost:8000`. Make sure your backend server is running before testing the full functionality.

### API Endpoints Used

- `GET /voices` - Fetch available voices
- `POST /voices` - Upload new voice samples (.wav files)
- `POST /synthesize` - Generate speech from text

## Features Overview

### 🎤 Text Input

- Large, responsive textarea for text input
- Real-time validation
- Smooth focus transitions

### 🎵 Voice Selection

- Dropdown populated with available voices from backend
- Clean, accessible select component
- Dynamic voice list updates

### 📁 File Upload

- Drag-and-drop interface for WAV files
- Visual feedback for drag states
- File validation and error handling
- Smooth upload animations

### 🔊 Audio Player

- Custom-styled audio controls
- Play/pause functionality
- Download generated audio
- Browser-native audio controls

### 🎨 Design Features

- **Glassmorphism**: Frosted glass effects on cards and navigation
- **Gradient Text**: Beautiful gradient text effects for headings
- **Smooth Animations**: Hover effects, loading states, and transitions
- **Responsive Design**: Optimized for all screen sizes
- **Dark Theme**: Carefully crafted dark color palette

## Build for Production

```bash
npm run build
npm start
```
