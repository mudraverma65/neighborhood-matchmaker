import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/neighborhoods',
        destination: 'http://localhost:8000/neighborhoods',
      },
      {
        source: '/amenities',
        destination: 'http://localhost:8000/amenities',
      },
      {
        source: '/search-neighborhoods',
        destination: 'http://localhost:8000/search-neighborhoods',
      },
    ];
  },
};

export default nextConfig;
