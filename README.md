# Restaurant Recommendation System 🍽️

> A smart, AI-powered restaurant discovery platform for European cities

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node-v18+-green.svg)](https://nodejs.org/)
[![React](https://img.shields.io/badge/react-v18+-blue.svg)](https://reactjs.org/)

## 🎯 Project Overview

An intelligent restaurant recommendation system that helps users discover their perfect dining experience in London, Paris, and Rome. Using machine learning algorithms and user preference analysis, it provides personalized restaurant suggestions tailored to individual tastes, dietary requirements, and dining priorities.

### ✨ Key Features
- **Smart Recommendations**: AI-powered matching based on user preferences
- **Multi-City Support**: London, Paris, and Rome restaurant databases
- **Personalized Experience**: Learns from user feedback and selections
- **Rich Restaurant Data**: Photos, ratings, reviews, and detailed information
- **Intuitive Interface**: Modern, responsive web application

## 🏗️ Architecture

```
res-rec-system/
├── frontend/          # React TypeScript application
├── backend/           # Flask Python API
├── LICENSE           # MIT License
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/res-rec-system.git
   cd res-rec-system
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   flask run
   ```

4. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Open your browser** to `http://localhost:5173`

## 📚 Documentation

For detailed documentation, setup instructions, and technical details, see:
- [Frontend Documentation](./frontend/README.md) - Complete project documentation
- [Backend API Documentation](./backend/) - API endpoints and backend architecture

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **TailwindCSS** for styling
- **Vite** for build tooling
- Custom hooks for API integration

### Backend
- **Flask** Python web framework
- **MongoDB** for data persistence
- **scikit-learn** for ML algorithms
- **NumPy/Pandas** for data processing

## 📈 What Makes This Special

- **Production-Ready**: Comprehensive error handling and user feedback
- **Scalable Architecture**: Clean separation of concerns and modular design  
- **AI Integration**: Real machine learning for personalized recommendations
- **Modern Stack**: Latest versions of React, TypeScript, and Python frameworks
- **User-Centered**: Intuitive interface with accessibility considerations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for food lovers everywhere** 