# Node.js 기반 이미지
FROM node:20-alpine

# 작업 디렉토리 설정
WORKDIR /app

# package.json 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# 앱 코드 복사
COPY . .

# 포트 노출
EXPOSE 3000

# 앱 실행
CMD ["npm", "start"]
