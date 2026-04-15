# 🔬 Multi-Agent Research System

An intelligent research system powered by Mistral AI that automates web research, content analysis, and report generation using a multi-agent architecture.

## 🚀 Live Demo

**Try it now**: https://multiagentresech-djmxcyuekqc5fdappufi3ag.streamlit.app/

The app is live and ready to use! Just enter a research topic to get started.

## Features

✨ **Web Search Agent** - Find recent, reliable, detailed information on any topic using Tavily API  
📄 **Reader Agent** - Scrape and analyze content from top web resources  
✍️ **Writer Agent** - Generate structured, professional research reports  
🎯 **Critic Agent** - Evaluate and score reports with constructive feedback  
⏱️ **Rate Limit Handling** - Automatic retry with exponential backoff for API rate limits

## Tech Stack

- **LLM**: Mistral AI (mistral-large-2512)
- **Framework**: LangChain + LanggGraph
- **UI**: Streamlit
- **APIs**: Tavily Search, Mistral AI
- **Python**: 3.13+

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Atharvasayyyy/MultiAgent_Resech.git
cd MultiAgent_Resech

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt
# OR using uv (faster)
uv pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

Get your API keys:
- **Tavily**: https://tavily.com
- **Mistral**: https://console.mistral.ai

## Running Locally

```bash
# Option 1: Using Python module (recommended)
.\.venv\Scripts\python.exe -m streamlit run app.py

# Option 2: Direct executable
.\.venv\Scripts\streamlit.exe run app.py
```

The app will open at `http://localhost:8501`

## Deploying to Streamlit Cloud

### Prerequisites
- GitHub account (you have this ✓)
- Repository pushed to GitHub (done ✓)
- Streamlit account at https://streamlit.io

### Deployment Steps

1. **Create Streamlit Account**
   - Go to https://streamlit.io/cloud
   - Sign up with GitHub (recommended)

2. **Deploy Your App**
   - Click "New App" in Streamlit Cloud
   - Select: Repository: `Atharvasayyyy/MultiAgent_Resech`
   - Select: Branch: `main`
   - Select: Main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to your app
   - Click ⚙️ Settings → Secrets
   - Add your API keys:

```toml
TAVILY_API_KEY = "your_tavily_api_key"
MISTRAL_API_KEY = "your_mistral_api_key"
```

**⚠️ IMPORTANT**: Never commit `.env` or `secrets.toml` with real API keys to GitHub. Streamlit Cloud handles secrets securely through the dashboard.

4. **Access Your App**
   - Your app is now live at: https://multiagentresech-djmxcyuekqc5fdappufi3ag.streamlit.app/

### Auto-Deploy
Each time you push to the `main` branch, Streamlit Cloud automatically redeploys your app.

## Project Structure

```
MultiAgent_Resech/
├── app.py              # Streamlit UI
├── agent.py            # LangChain agent setup
├── tools.py            # Web search & scraping tools
├── pipeline.py         # Research pipeline orchestration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (local only)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## How It Works

1. **User Input**: Enter a research topic in the Streamlit UI
2. **Search**: First agent searches the web for relevant information
3. **Scrape**: Second agent extracts detailed content from top results
4. **Write**: Writer chain generates a structured report
5. **Critique**: Critic agent evaluates and scores the report
6. **Output**: Display final report with feedback

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TAVILY_API_KEY` | API key for web search |
| `MISTRAL_API_KEY` | API key for Mistral AI |

## Rate Limiting

If you encounter Mistral API rate limits:
- The system automatically retries with exponential backoff
- Wait times: 15s → 30s → 60s → 120s → 240s
- Maximum 5 retry attempts

For production use, consider upgrading your Mistral plan.

## Troubleshooting

### "streamlit: command not found"
```bash
# Use the full path or Python module
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### "ModuleNotFoundError: No module named 'langchain_mistralai'"
```bash
# Reinstall dependencies
uv pip install -r requirements.txt
```

### Rate limit errors
- Mistral free tier has strict limits (~1-2 req/min)
- Wait time before retrying, or upgrade your plan
- See https://console.mistral.ai/billing for account options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to your branch
5. Create a Pull Request

## License

MIT License - feel free to use this project!

## Support

For issues or questions:
- Check Streamlit docs: https://docs.streamlit.io
- Mistral docs: https://docs.mistral.ai
- LangChain docs: https://python.langchain.com
