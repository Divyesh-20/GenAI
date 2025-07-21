/** next.config.js */
module.exports = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    return [
      {
        source: "/api/generate-video",
        destination: "http://localhost:6000/generate-video",
      },
      {
        source: "/api/health",
        destination: "http://localhost:6000/health",
      },
    ];
  },
};
