# Quick Setup Guide

## Step-by-Step Instructions

### Step 1: Install Node.js (if not already installed)

1. Go to [https://nodejs.org/](https://nodejs.org/)
2. Download the LTS (Long Term Support) version
3. Run the installer
4. Verify installation by opening terminal and running:
   ```bash
   node --version
   npm --version
   ```
   Both commands should show version numbers.

### Step 2: Navigate to Project Directory

Open terminal and navigate to the project:
```bash
cd "/Users/shaminder/Desktop/AI Projects/stock_shorts_tracker/ai-project-hub"
```

### Step 3: Install Dependencies

Run this command to install all required packages:
```bash
npm install
```

This will take a few minutes. You'll see progress in the terminal.

### Step 4: Start the Development Server

Run this command:
```bash
npm run dev
```

You should see output like:
```
▲ Next.js 14.2.0
- Local:        http://localhost:3000
```

### Step 5: Open in Browser

1. Open your web browser
2. Go to: [http://localhost:3000](http://localhost:3000)
3. You should see the AI Project Hub interface!

## What You'll See

- **Left Sidebar**: List of all your projects (docs and prototypes)
- **Main Area**: Content viewer (shows markdown or code when you click a project)

## Adding Your Own Content

### Add a Markdown Document:
1. Create a new file in `docs/` folder
2. Name it something like `my-project.md`
3. Write your content in Markdown
4. Refresh the browser - it will appear in the sidebar!

### Add a Code Prototype:
1. Create a new folder in `prototypes/` folder
2. Name it something like `my-prototype`
3. Add a code file (`.js`, `.ts`, or `.py`)
4. Name it `index.js`, `main.js`, or any name with proper extension
5. Refresh the browser - it will appear in the sidebar!

## Troubleshooting

**"command not found: npm"**
- Node.js is not installed or not in PATH
- Reinstall Node.js and restart terminal

**"Port 3000 is already in use"**
- Another app is using port 3000
- Run: `npm run dev -- -p 3001`
- Then go to http://localhost:3001

**"Cannot find module" errors**
- Run `npm install` again
- Delete `node_modules` folder and `package-lock.json`, then run `npm install`

**Files not showing up**
- Make sure files are in `docs/` or `prototypes/` folders
- Check file extensions (`.md` for docs)
- Restart the dev server (Ctrl+C, then `npm run dev` again)

## Next Steps

- Add your own markdown files to `docs/`
- Create your own prototypes in `prototypes/`
- Customize the UI by editing `app/page.tsx`
- Explore the code structure!

