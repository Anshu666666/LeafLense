---
title: LeafLense - AI-Powered Agricultural Assistant
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# 🌱 LeafLense - AI-Powered Agricultural Assistant

**LeafLense** is an advanced agricultural intelligence platform that combines machine learning, computer vision, and AI agents to provide comprehensive farming solutions. The platform offers plant disease detection, fertilizer recommendations, crop yield predictions, and proactive farming alerts through an intelligent agent system.

## 🌟 Key Features
... (the rest of your great README continues here)

# 🌱 LeafLense - AI-Powered Agricultural Assistant

**LeafLense** is an advanced agricultural intelligence platform that combines machine learning, computer vision, and AI agents to provide comprehensive farming solutions. The platform offers plant disease detection, fertilizer recommendations, crop yield predictions, and proactive farming alerts through an intelligent agent system.

## 🌟 Key Features

### 🔍 **Plant Disease Detection**
- **AI-Powered Diagnosis**: Upload plant leaf images for instant disease identification
- **38+ Disease Classes**: Supports detection across multiple crops (Apple, Tomato, Corn, Grape, etc.)
- **Treatment Recommendations**: Provides organic and chemical treatment options
- **Confidence Scoring**: Reliable predictions with confidence percentages

### 🌾 **FarmAgent - Proactive Farming Assistant**
- **Real-time Weather Integration**: Continuous weather monitoring and analysis
- **Risk Assessment Engine**: Predicts disease and pest risks based on environmental conditions
- **Automated Alerts**: Daily notifications via WhatsApp for farming recommendations
- **Farmer Management**: Complete farmer profile and location management system
- **AI Chat Interface**: Contextual farming advice through intelligent conversations

### 🧪 **Fertilizer Recommendation System**
- **Soil Analysis**: NPK (Nitrogen, Phosphorus, Potassium) level optimization
- **Environmental Factors**: Considers temperature, humidity, and moisture
- **Crop-Specific**: Tailored recommendations for different crop types
- **Natural Language Processing**: Accept recommendations via plain text descriptions

### 📊 **Crop Yield Prediction**
- **Data-Driven Insights**: Predict crop yields based on historical and current data
- **Market Intelligence**: Price prediction and market trend analysis
- **Decision Support**: Help farmers optimize planting and harvesting decisions

### 💬 **Intelligent Chatbot**
- **Multi-language Support**: Communicate in local languages
- **Voice Integration**: Speech-to-text and text-to-speech capabilities
- **Context-Aware**: Understands farmer-specific context and location
- **24/7 Availability**: Always available farming assistance

## 🏗️ System Architecture

### Backend (FastAPI)
```
backend/
├── main.py                 # Main FastAPI application
├── FarmAgent/              # Proactive farming agent
│   ├── app/
│   │   ├── agents/         # Weather, risk, chat agents
│   │   ├── clients/        # Firebase, weather API clients
│   │   └── utils/          # Utility functions
│   └── routes.py           # FarmAgent API endpoints
├── Plant_Disease/          # Disease detection module
│   ├── routes.py           # Disease detection endpoints
│   └── trained_model_savedmodel/  # Pre-trained ML model
├── FertilizerSuggestor/    # Fertilizer recommendation
│   └── routes.py           # Fertilizer API endpoints
└── PricePrediction/        # Crop price prediction
    └── app.py              # Price prediction service
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/         # Reusable UI components
│   │   └── layout/         # Layout components
│   ├── pages/              # Application pages
│   ├── config/             # Configuration files
│   └── assets/             # Static assets
├── public/                 # Public assets
└── package.json            # Dependencies and scripts
```

## 🔧 System Requirements

### Backend Requirements
- **Python**: 3.8+
- **FastAPI**: 0.115.0+
- **TensorFlow**: 2.17+ (for disease detection)
- **Firebase Admin SDK**: For database and authentication
- **Google Generative AI**: For AI-powered responses

### Frontend Requirements
- **Node.js**: 18+
- **React**: 18.3.1+
- **Vite**: 6.0.1+
- **Tailwind CSS**: For styling

### External Services
- **Firebase**: Database and authentication
- **Google Gemini API**: AI language model
- **OpenWeather API**: Weather data
- **WhatsApp Business API**: Alert notifications

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/LeafLense.git
cd LeafLense
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the `backend/` directory:

```env
# Google APIs
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# OpenWeather API
OPENWEATHER_API_KEY=your_openweather_api_key

# Application Settings
PORT=8000
ENVIRONMENT=development

# Database
DATABASE_URL=your_database_url_if_needed
```

#### Firebase Setup
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Generate a service account key
4. Save the key as `serviceAccountKey.json` in the `backend/` directory

#### Run Backend Server
```bash
# From the backend directory
python main.py
```

The backend server will start at: `http://localhost:8000`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=your_firebase_config
VITE_FIREBASE_AUTH_DOMAIN=your_firebase_config
VITE_FIREBASE_PROJECT_ID=your_firebase_config
VITE_FIREBASE_STORAGE_BUCKET=your_firebase_config
VITE_FIREBASE_MESSAGING_SENDER_ID=your_firebase_config
VITE_FIREBASE_APP_ID=your_firebase_config
```

#### Run Frontend Development Server
```bash
# From the frontend directory
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## 📡 API Endpoints

### FarmAgent Endpoints
- `GET /farm/farmagent/` - Service status
- `POST /farm/farmagent/run-now` - Trigger immediate pipeline execution
- `POST /farm/farmagent/farmers` - Register new farmer
- `GET /farm/farmagent/farmers` - Get all farmers
- `GET /farm/farmagent/alerts` - Get all alerts
- `GET /farm/farmagent/alerts/{farmer_id}` - Get farmer-specific alerts
- `POST /farm/farmagent/api/chat` - Chat with AI assistant

### Plant Disease Detection
- `POST /plant/disease/predict` - Upload image for disease detection

### Fertilizer Recommendation
- `POST /fertilizer/predict` - Get fertilizer recommendation (structured data)
- `POST /fertilizer/predict_from_text` - Get recommendation from natural language

## 🏃‍♂️ Running the Application

### Development Mode
1. **Start Backend**: 
   ```bash
   cd backend && python main.py
   ```

2. **Start Frontend**: 
   ```bash
   cd frontend && npm run dev
   ```

3. **Access Application**: Open `http://localhost:3000` in your browser

### Production Build

#### Backend (using Gunicorn)
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### Frontend (Build & Serve)
```bash
cd frontend
npm run build
npm run preview
```

## 🔧 Configuration

### Model Setup
The plant disease detection requires a trained TensorFlow model:

1. Ensure the model is in `backend/Plant_Disease/trained_model_savedmodel/`
2. The model should support 38 plant disease classes
3. Expected input shape: (None, 128, 128, 3)

### Firebase Configuration
1. Set up Firestore collections:
   - `farmers`: Farmer profiles and locations
   - `alerts`: Generated alerts and recommendations
   - `chat_messages`: Chat history

### Weather Integration
- Register at [OpenWeatherMap](https://openweathermap.org/api)
- Add your API key to the `.env` file
- The system fetches weather data every 6 hours

## 📱 Features Walkthrough

### Disease Detection
1. Navigate to `/disease-detection`
2. Upload a clear image of a plant leaf
3. Get instant diagnosis with confidence score
4. Receive treatment recommendations

### Fertilizer Recommendations
1. Go to `/fertilizer`
2. Input soil conditions and crop information
3. Receive NPK recommendations
4. Alternative: Use natural language input

### Farm Monitoring
1. Register farmers through `/farm/farmagent/farmers`
2. System automatically monitors weather conditions
3. Receives daily alerts at 6:00 AM IST
4. Chat interface available for real-time advice

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Recommendations
- **Backend**: Deploy on Google Cloud Run, AWS Lambda, or Heroku
- **Frontend**: Deploy on Vercel, Netlify, or AWS S3 + CloudFront
- **Database**: Use Firebase Firestore or MongoDB Atlas
- **File Storage**: Google Cloud Storage or AWS S3

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

For support, email support@leaflense.com or join our [Discord community](https://discord.gg/leaflense).

## 🙏 Acknowledgments

- TensorFlow team for the machine learning framework
- Google for Gemini AI and Firebase services
- OpenWeatherMap for weather data
- The agricultural research community for disease datasets

---

**Built with ❤️ for the farming community** 🌾