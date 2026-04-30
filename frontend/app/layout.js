import './globals.css';

export const metadata = {
  title: 'Curio AI',
  description: 'Minimal Next.js frontend for Curio AI',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap" rel="stylesheet" />
      </head>
      <body>
        <div className="mesh-bg" />
        {children}
      </body>
    </html>
  );
}
