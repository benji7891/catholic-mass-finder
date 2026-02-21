export default function Header() {
  return (
    <header className="bg-indigo-900 text-white shadow-lg">
      {/* Skip link for keyboard navigation */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:rounded-md focus:bg-white focus:px-4 focus:py-2 focus:text-indigo-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        Skip to main content
      </a>
      <div className="mx-auto max-w-7xl px-4 py-4 flex items-center gap-3">
        <svg
          className="h-8 w-8 text-amber-400 shrink-0"
          viewBox="0 0 24 24"
          fill="currentColor"
          aria-hidden="true"
        >
          <path d="M11 2v5H6v2h5v5h2V9h5V7h-5V2h-2zm-1 14H4v2h6v4h4v-4h6v-2H14h-4z" />
        </svg>
        <div>
          <h1 className="text-xl font-bold leading-tight">Catholic Mass Finder</h1>
          <p className="text-indigo-200 text-sm">Find parishes, Mass times & more near you</p>
        </div>
      </div>
    </header>
  );
}
