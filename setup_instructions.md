# 🤖 NeuralSprint - Local Setup Instructions

## Quick Start Guide

### 1. Prerequisites
- **Python 3.8+** (download from python.org)
- **LM Studio** (download from lmstudio.ai)
- **RTX 2050+ GPU** recommended for optimal AI performance

### 2. Install Dependencies
```bash
# Navigate to project folder
cd neuralsprint

# Install Python dependencies
pip install streamlit plotly requests pandas

# Alternative using requirements:
pip install -r requirements.txt
```

### 3. Setup LM Studio (For AI Features)
1. Download and install LM Studio from https://lmstudio.ai
2. Launch LM Studio
3. Download the Qwen3 4B model from the model library
4. Start the local server (default: localhost:1234)

### 4. Run NeuralSprint
```bash
streamlit run app.py --server.port 5000
```

### 5. Access the Application
Open your browser and go to: http://localhost:5000

## Configuration

### Environment Variables (Optional)
```bash
# Set custom LM Studio URL if different from default
export LM_STUDIO_URL="http://localhost:1234"

# Set custom model name if using different model
export MODEL_NAME="qwen2.5-3b-instruct"
```

### AI Features
- **With LM Studio**: Full AI automation including story estimation, sprint planning, and insights
- **Without LM Studio**: Manual mode - all features work except AI-powered automation

## Features Overview

### 🚀 Sprint Planning
- Create and manage sprints
- AI-assisted story selection
- Capacity planning and optimization

### 📝 Backlog Management  
- Create and organize user stories
- AI-powered story point estimation
- Bulk operations and filtering

### 🎯 Daily Standups
- Team progress tracking
- Blocker identification
- AI-generated summaries

### 🔄 Retrospectives
- Sprint analysis and feedback
- Action item tracking
- AI insights and recommendations

### 📊 Analytics
- Velocity tracking
- Burndown charts
- Predictive insights and bottleneck detection

## Troubleshooting

### AI Not Working
- Ensure LM Studio is running on localhost:1234
- Check that a model is loaded in LM Studio
- Verify firewall/antivirus isn't blocking connections

### Performance Issues
- Close unnecessary applications
- Ensure sufficient RAM (8GB minimum)
- Use GPU acceleration in LM Studio settings

### Port Conflicts
```bash
# Use different port if 5000 is busy
streamlit run app.py --server.port 8501
```

## Data Storage
- All data stored locally in `data/` folder as JSON files
- No external services or cloud dependencies
- Easy backup by copying the data folder

## Support
For issues or questions, refer to the documentation in replit.md or create an issue in the project repository.