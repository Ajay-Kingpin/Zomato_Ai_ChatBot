# Zomato AI Recommendation System - Complete Commands Guide

## 🚀 **Complete Application Commands**

### **1. Web Frontend (Recommended)**
```bash
# Start the web application
python phase6/app.py
```
*Opens modern web interface at http://localhost:5000*

### **2. Command Line Interface**
```bash
# Interactive CLI application
python phase5/main.py
```

### **3. Demo Scripts**
```bash
# Complete system demo
python simple_demo.py

# LLM-only demo
python demo_llm_recommendations.py
```

### **4. Testing Commands**
```bash
# Run all tests (97 tests total)
python -m pytest -v

# Run specific phase tests
python -m pytest phase6/tests/ -v  # Web frontend
python -m pytest phase5/tests/ -v  # Complete integration
python -m pytest phase4/tests/ -v  # LLM recommendations
python -m pytest phase3/tests/ -v  # Data integration
python -m pytest phase2/tests/ -v  # User input
python -m pytest phase1/tests/ -v  # Data loading

# Quick test run
python -m pytest --tb=short -q
```

---

## 🌐 **Web Frontend Features**

### **Main Interface** (http://localhost:5000)
- ✅ **Modern UI**: Beautiful Tailwind CSS design
- ✅ **Real-time Stats**: Dataset overview and system status
- ✅ **Smart Form**: City suggestions, validation, error handling
- ✅ **AI Integration**: Real LLM recommendations
- ✅ **Responsive**: Works on desktop and mobile

### **API Endpoints**
```
GET  /                    # Main web interface
GET  /health              # Health check
GET  /api/cities          # Available cities
GET  /api/stats           # Dataset statistics
POST /api/recommendations  # Get AI recommendations
```

### **API Usage Example**
```bash
# Get recommendations via API
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"city": "Bangalore", "price": 800, "diet": "veg"}'
```

---

## 📊 **System Overview**

### **6 Complete Phases**
1. **Phase 1**: Data Loading (51,717 restaurants)
2. **Phase 2**: User Input Processing
3. **Phase 3**: Data Integration & Filtering
4. **Phase 4**: LLM Recommendations (Groq AI)
5. **Phase 5**: Complete System Integration
6. **Phase 6**: Web Frontend Interface

### **Test Results**
```
======================= 97 passed in 107.06s ==============================
Phase 1: 10 tests ✅
Phase 2: 24 tests ✅
Phase 3: 20 tests ✅
Phase 4: 23 tests ✅
Phase 5: 10 tests ✅
Phase 6: 10 tests ✅
```

---

## 🎯 **Recommended Usage**

### **For Users**
1. **Web Interface**: `python phase6/app.py`
   - Visit http://localhost:5000
   - Fill in city, budget, and dietary preferences
   - Get AI-powered recommendations instantly

### **For Developers**
1. **Run Tests**: `python -m pytest -v`
2. **API Development**: Use REST endpoints at `/api/`
3. **Integration**: Import from `phase5.main.ZomatoRecommendationApp`

### **For Demo**
1. **Complete Demo**: `python simple_demo.py`
2. **Web Demo**: `python phase6/app.py`

---

## 🔧 **Setup Requirements**

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Environment Setup**
- ✅ API key configured in `phase4/.env`
- ✅ All dependencies installed
- ✅ Tests passing (97/97)

---

## 🎉 **System Status: PRODUCTION READY**

The complete Zomato AI Recommendation System is fully operational with:

- ✅ **6 Complete Phases** working seamlessly
- ✅ **97 Passing Tests** with comprehensive coverage
- ✅ **Modern Web Interface** with real AI integration
- ✅ **RESTful API** for programmatic access
- ✅ **Command Line Interface** for power users
- ✅ **Real AI Recommendations** powered by Llama 3.1

**Choose any command above to start using the system!** 🚀
