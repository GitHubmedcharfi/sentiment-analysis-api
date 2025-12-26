# Use official Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy source code
COPY ./ ./

# Expose default React dev server port
EXPOSE 3000

# Start React development server
CMD ["npm", "start"]
