FROM node:20-alpine AS builder
WORKDIR /app
COPY api/package*.json ./
RUN npm ci

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app

# Install Python and yt-dlp
RUN apk add --no-cache python3 py3-pip ffmpeg && \
    pip3 install --break-system-packages yt-dlp

# Install production dependencies only
COPY api/package*.json ./
RUN npm ci --omit=dev

# Copy source code
COPY api/src/ ./src/

# Copy data files
COPY data/ ./data/

# Create local storage directory
RUN mkdir -p ./data/local/audio ./data/local/pdf ./data/local/youtube

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV LOCAL_STORAGE_ENABLED=true
ENV LOCAL_STORAGE_PATH=./data/local
ENV AUTO_DOWNLOAD_ON_START=true
ENV LOG_LEVEL=info

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# Start server
CMD ["node", "src/index.js"]
