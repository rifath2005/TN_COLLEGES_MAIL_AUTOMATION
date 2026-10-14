# Multi-runtime Dockerfile (Node.js 20 + Python 3) for TN Outreach Automation
FROM node:20-slim

# Install Python 3 and build utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy root package files
COPY package*.json ./
COPY AUTO_LAND/package*.json ./AUTO_LAND/

# Install root & AUTO_LAND dependencies
RUN npm install && cd AUTO_LAND && npm install

# Copy application source code and institutional dataset
COPY contacts.csv ./
COPY email_template.json ./
COPY run_outreach.py ./
COPY AUTO_LAND ./AUTO_LAND

# Build frontend production assets
RUN cd AUTO_LAND && npm run build

# Expose port (default 3000)
ENV PORT=3000
ENV NODE_ENV=production
EXPOSE 3000

# Start production server
CMD ["node", "--loader", "tsx", "AUTO_LAND/server.ts"]
