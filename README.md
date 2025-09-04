# 🪷 Equanimity: AI-Powered Buddhist Mindfulness App

A beautiful full-stack application that combines FastAPI backend with Streamlit frontend to provide personalized equanimity practices using Google's Gemini AI.

## ✨ Features

- **Deep Psychological Assessment**: 5 carefully crafted questions that reveal emotional patterns
- **AI-Generated Practices**: Personalized 3-day equanimity practices using Gemini AI
- **Buddhist-Inspired Design**: Authentic aesthetic with earth tones and lotus symbolism
- **Modern Architecture**: FastAPI backend + Streamlit frontend for optimal performance
- **Easy Deployment**: Multiple deployment options included

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
2. **Google Gemini API Key** - Get yours at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Local Development Setup

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd equanimity-app
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Start the Backend (Terminal 1)**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Start the Frontend (Terminal 2)**
   ```bash
   streamlit run app.py --server.port 8501
   ```

5. **Visit the App**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 🐳 Docker Deployment

### Option 1: Single Container (Simplest)
```bash
docker build -t equanimity-app .
docker run -p 8000:8000 -p 8501:8501 -e GEMINI_API_KEY=your_key_here equanimity-app
```

### Option 2: Docker Compose (Recommended)
```bash
# Set your API key in .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment Options

### 1. **Render (Easiest - Free Tier Available)**

**For FastAPI Backend:**
1. Create new Web Service on [Render](https://render.com)
2. Connect your GitHub repo
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `GEMINI_API_KEY`

**For Streamlit Frontend:**
1. Create another Web Service
2. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment Variables**: Add `API_BASE_URL=https://your-fastapi-url.onrender.com`

### 2. **Railway (Very Easy)**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add --service backend
railway add --service frontend

# Deploy backend
railway up --service backend

# Deploy frontend  
railway up --service frontend
```

### 3. **Google Cloud Run (Scalable)**

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/equanimity-app

# Deploy to Cloud Run
gcloud run deploy equanimity --image gcr.io/YOUR_PROJECT/equanimity-app \
  --platform managed --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

### 4. **Heroku (Classic)**

```bash
# Install Heroku CLI and login
heroku create equanimity-backend
heroku create equanimity-frontend

# Deploy backend
git subtree push --prefix=backend heroku main

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here -a equanimity-backend
```

### 5. **Vercel (Frontend) + Railway (Backend)**

**Backend on Railway:**
```bash
railway init --template fastapi
# Push your FastAPI code
```

**Frontend on Vercel:**
```bash
npm i -g vercel
vercel --build-env API_BASE_URL=https://your-railway-backend.up.railway.app
```

## 📁 Project Structure

```
equanimity-app/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend  
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Multi-service setup
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes |
| `API_BASE_URL` | FastAPI backend URL for frontend | Development only |

### API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /generate-technique` - Generate personalized practice

## 🎨 Customization

### Styling
The app uses custom CSS in the Streamlit frontend (`app.py`). Modify the `st.markdown()` sections to change colors, fonts, or layout.

### Questions
Update the `QUESTIONS` list in `app.py` to modify the assessment questions.

### AI Prompts
Enhance the Gemini prompt in `main.py` to adjust the generated practices.

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure FastAPI is running on port 8000
   - Check `API_BASE_URL` in Streamlit app

2. **Gemini AI Errors**
   - Verify your API key is correct
   - Check API quotas and limits

3. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Ensure Python 3.11+ is being used

### Development Tips

```bash
# Check FastAPI is running
curl http://localhost:8000/health

# View FastAPI logs
uvicorn main:app --reload --log-level debug

# View Streamlit in development mode
streamlit run app.py --logger.level debug
```

## 📖 Architecture

- **Frontend**: Streamlit with custom CSS for Buddhist aesthetic
- **Backend**: FastAPI with Pydantic models for type safety  
- **AI**: Google Gemini Pro for generating personalized practices
- **Deployment**: Docker + various cloud options for scalability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Acknowledgments

- Buddhist wisdom traditions for the foundational teachings
- Google for Gemini AI capabilities
- Streamlit and FastAPI communities for excellent frameworks

---

**May this app bring peace and equanimity to all who use it** 🧘‍♀️✨
