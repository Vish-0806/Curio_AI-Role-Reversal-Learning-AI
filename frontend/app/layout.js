import './globals.css';

export const metadata = {
  title: 'Curio AI',
  description: 'Minimal Next.js frontend for Curio AI',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
