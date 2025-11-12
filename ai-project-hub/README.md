# AI Project Hub

A simple Next.js application for managing AI project documentation and code prototypes.

## Features

- 📝 Markdown documentation repository
- 💻 Code prototype viewer
- 🎨 Clean, minimal UI
- 🌙 Dark mode support

## Setup Instructions

### Prerequisites

You need to have Node.js installed (version 18 or higher). If you don't have it:

1. **Install Node.js:**
   - Visit [nodejs.org](https://nodejs.org/)
   - Download and install the LTS version
   - Verify installation: `node --version` and `npm --version`

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd ai-project-hub
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   - Navigate to [http://localhost:3000](http://localhost:3000)
   - You should see the AI Project Hub interface

## Project Structure

```
ai-project-hub/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main page
├── docs/                  # Markdown documentation files
│   ├── sample-prd.md
│   └── getting-started.md
├── prototypes/            # Code prototype directories
│   ├── simple-calculator/
│   └── data-processor/
└── package.json
```

## Adding Content

### Adding Markdown Documentation

1. Create a new `.md` file in the `docs/` directory
2. Write your documentation in Markdown format
3. The app will automatically detect and display it in the sidebar

### Adding Code Prototypes

1. Create a new directory in `prototypes/`
2. Add your code files (`.js`, `.ts`, `.py`, etc.)
3. Name the main file one of:
   - `index.js` or `index.ts`
   - `main.js` or `main.ts`
   - Or any `.js`, `.ts`, or `.py` file
4. The app will automatically detect and display it

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Next Steps

- Add more documentation files to `docs/`
- Create more prototypes in `prototypes/`
- Customize the UI in `app/page.tsx`
- Add features like search, filtering, or editing

## Troubleshooting

**Port 3000 already in use?**
- Use a different port: `npm run dev -- -p 3001`

**Dependencies not installing?**
- Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Files not showing up?**
- Make sure files are in the correct directories (`docs/` or `prototypes/`)
- Check file extensions (`.md` for docs, `.js/.ts/.py` for code)
- Restart the dev server

