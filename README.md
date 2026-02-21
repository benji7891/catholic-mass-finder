# Catholic Mass Finder

A web application to find Catholic parishes, Mass times, confession schedules, and adoration near you.

## Features

- Search by location (zip code, city, or address)
- Use your current location
- Filter by day of the week and service type (Mass, Confession, Adoration)
- Interactive map view with parish markers
- Detailed parish information including phone, website, and full schedule
- Responsive design for mobile and desktop

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```

4. Get a MassTimes API key:
   - Email webmaster@masstimes.org to request an API key
   - Explain your use case and provide your website URL
   - The demo key in their documentation does not work

5. Add your MassTimes API key to the `.env` file:
   ```
   MASSTIMES_API_KEY=your_actual_api_key_here
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack

- React 19 + TypeScript
- Vite
- Tailwind CSS
- Leaflet (maps)
- MassTimes API
- OpenStreetMap Nominatim (geocoding)
- Netlify Functions (serverless API proxy)

## Key Features

### Core Functionality
- **Smart Search**: Geocoded search with input validation and sanitization
- **Current Location**: GPS-based parish finding with improved timeout handling
- **Interactive Map**: Leaflet-powered map with clickable parish markers
- **Advanced Filtering**: Filter by day of week and service type (Mass, Confession, Adoration)
- **Smart Sorting**: Sort by distance, name, or next Mass time
- **Detailed Information**: Full parish details including phone, website, and complete schedule

### Security & Performance
- **✅ Secure API Proxy**: API keys hidden server-side via Netlify Functions
- **✅ Input Sanitization**: XSS protection on all user inputs
- **✅ Request Caching**: localStorage caching with TTL to reduce API calls
- **✅ Retry Logic**: Automatic retry with exponential backoff for failed requests
- **✅ Coordinate Validation**: Server and client-side validation

### User Experience
- **Responsive Design**: Optimized for mobile and desktop
- **Mobile View Sync**: Auto-switch to detail view when selecting parishes on mobile
- **Get Directions**: Direct integration with Google Maps & Apple Maps
- **Empty States**: Helpful messages for no results and filtered results
- **Error Messages**: User-friendly, actionable error messages
- **International Support**: Works worldwide (not US-only)
- **Loading Skeletons**: Animated placeholders for better perceived performance
- **Enhanced Accessibility**: Skip links, ARIA labels, keyboard navigation, and screen reader optimization

## Development

### Prerequisites
- Node.js 20+ (or Node.js 18+)
- npm 9+

### Running Locally

The app uses Netlify Functions for API proxying. To run locally:

```bash
npm run dev
```

This starts:
- Netlify Dev server on port 8888 (handles functions)
- Vite dev server on port 5173 (proxies to Netlify)

Alternatively, run just Vite (without serverless functions):

```bash
npm run dev:vite
```

## Deployment

### Netlify (Recommended)

1. Push your code to GitHub/GitLab/Bitbucket

2. Connect to Netlify:
   - Go to [Netlify](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your repository

3. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Functions directory: `netlify/functions`

4. Add environment variable:
   - Go to Site settings → Environment variables
   - Add `MASSTIMES_API_KEY` with your API key value

5. Deploy!

### Other Platforms

For Vercel, Cloudflare, or other platforms, you'll need to adapt the serverless function to their format.

## Project Structure

```
src/
├── components/      # React components
├── hooks/          # Custom React hooks with caching & retry
├── services/       # API service layers
├── types/          # TypeScript type definitions
└── utils/          # Utilities (validation, caching, sorting, retry)
netlify/
└── functions/      # Serverless API proxy functions
```

## Environment Variables

- `MASSTIMES_API_KEY` - Your MassTimes API key (server-side only)

## Contributing

Contributions welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update documentation

## License

MIT

---

## React + TypeScript + Vite Template

This project was bootstrapped with a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
