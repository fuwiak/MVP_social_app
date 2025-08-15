import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Business System - Intelligent Business Management',
  description: 'Complete AI-powered business management system with automation, analytics, and insights',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  )
}
