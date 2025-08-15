/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['localhost'],
  },
  // Disable strict mode for better Docker compatibility
  reactStrictMode: false,
  swcMinify: true,
  poweredByHeader: false,
}

module.exports = nextConfig
