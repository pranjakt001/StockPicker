# 📈 AI-Powered Stock Investment Advisor

An intelligent multi-agent system that researches trending companies and provides personalized stock investment recommendations. Powered by CrewAI, this application uses specialized AI agents that work together like a professional investment team.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.28.0+-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0.0+-orange.svg)

## Live Demo : https://huggingface.co/spaces/pranjakt/StockPicker


## 🌟 Features

- **Multi-Agent AI System**: Specialized agents work collaboratively to analyze stocks
- **Real-Time Research**: Searches latest news and market data using web tools
- **Comprehensive Analysis**: Deep dive into market position, future outlook, and investment potential
- **Email Delivery**: Beautifully formatted HTML reports sent directly to your inbox
- **User-Friendly Interface**: Simple Gradio web interface for easy interaction
- **Hierarchical Workflow**: Manager agent coordinates tasks for optimal results

## 🤖 The AI Crew

The system employs 4 specialized AI agents:

1. **👨‍💼 Trending Company Finder**
   - Searches latest financial news
   - Identifies 2-3 trending companies in specified sector
   - Uses: Perplexity Sonar AI + Web Search Tools

2. **🔬 Financial Researcher**
   - Conducts deep analysis on each company
   - Evaluates market position, growth prospects, and investment potential
   - Uses: Perplexity Sonar AI + Web Research Tools

3. **🎯 Stock Picker**
   - Reviews all research findings
   - Selects the best investment opportunity
   - Provides detailed rationale
   - Uses: Perplexity Sonar AI

4. **📋 Manager**
   - Coordinates the entire workflow
   - Delegates tasks to appropriate agents
   - Ensures quality and completeness
   - Uses: Perplexity Sonar AI

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- API Keys:
  - OpenAI API Key
  - Serper API Key (for web search)
  - SendGrid API Key (for email delivery)
  - Perplexity API Key (optional, for Sonar model)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-stock-picker.git
cd ai-stock-picker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=your_verified_sender@email.com
PERPLEXITY_API_KEY=your_perplexity_key_here  # Optional
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to: `http://localhost:7860`

## 📁 Project Structure

```
ai-stock-picker/
│
├── app.py                      # Gradio web interface
├── crew.py                     # CrewAI agents and tasks definition
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
│
├── config/
│   ├── agents.yaml            # Agent configurations
│   └── tasks.yaml             # Task definitions
│
└── output/                    # Generated reports (auto-created)
    ├── trending_companies.json
    ├── research_report.json
    └── decision.md
```

## 🔧 Configuration

### `agents.yaml` - Agent Personalities

Defines the role, goal, backstory, and AI model for each agent:

```yaml
trending_company_finder:
  role: Financial News Analyst
  goal: Find 2-3 trending companies in the news
  llm: perplexity/sonar

financial_researcher:
  role: Senior Financial Researcher
  goal: Provide comprehensive analysis
  llm: openai/gpt-4o-mini

stock_picker:
  role: Stock Picker from Research
  goal: Select the best investment opportunity
  llm: openai/gpt-4o-mini

manager:
  role: Manager
  goal: Coordinate all agents effectively
  llm: openai/gpt-4o
```

### `tasks.yaml` - Task Definitions

Specifies what each agent should do:

```yaml
find_trending_companies:
  description: Find top trending companies in {sector}
  agent: trending_company_finder
  output_file: output/trending_companies.json

research_trending_companies:
  description: Deep analysis of trending companies
  agent: financial_researcher
  context: [find_trending_companies]
  output_file: output/research_report.json

pick_best_company:
  description: Select best investment and explain why
  agent: stock_picker
  context: [research_trending_companies]
  output_file: output/decision.md
```

## 🌐 Deployment

### Hugging Face Spaces

1. **Create a new Space**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as SDK
   - Set Python version to 3.10

2. **Upload files**
   - Upload all project files
   - Make sure to include `config/` folder

3. **Set environment variables**
   - Go to Space Settings → Variables and secrets
   - Add your API keys as secrets:
     - `OPENAI_API_KEY`
     - `SERPER_API_KEY`
     - `SENDGRID_API_KEY`
     - `FROM_EMAIL`
     - `PERPLEXITY_API_KEY` (optional)

4. **Deploy**
   - Space will automatically build and deploy
   - Access your app at: `https://huggingface.co/spaces/your-username/your-space-name`

### Local Development

```bash
# Run with hot reload
python app.py

# Or specify custom port
python app.py --server-port 8080
```

## 📧 Email Configuration

### SendGrid Setup

1. **Create SendGrid Account**
   - Sign up at [SendGrid](https://sendgrid.com/)
   - Verify your email address

2. **Create API Key**
   - Go to Settings → API Keys
   - Create a new API key with "Full Access"
   - Copy and save securely

3. **Verify Sender Email**
   - Go to Settings → Sender Authentication
   - Verify the email address you'll use as `FROM_EMAIL`

4. **Add to Environment**
```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
FROM_EMAIL=verified@yourdomain.com
```

## 🔑 API Keys Guide

### OpenAI
- Get key: [OpenAI Platform](https://platform.openai.com/api-keys)
- Used for: GPT-4o, GPT-4o-mini models
- Cost: Pay-as-you-go pricing

### Serper
- Get key: [Serper.dev](https://serper.dev/)
- Used for: Web search functionality
- Free tier: 2,500 searches/month

### SendGrid
- Get key: [SendGrid](https://sendgrid.com/)
- Used for: Email delivery
- Free tier: 100 emails/day

### Perplexity (Optional)
- Get key: [Perplexity AI](https://www.perplexity.ai/)
- Used for: Sonar search model
- Alternative: Can use OpenAI for all agents

## 💡 Usage Example

1. **Enter your email address**
2. **Choose a sector** (e.g., "Technology", "Healthcare", "Energy")
3. **Click "Generate Analysis"**
4. **Wait 1-3 minutes** while AI agents research
5. **Receive results** via email and on-screen

### Sample Sectors

- Technology
- Healthcare
- Energy
- Finance
- Consumer Goods
- Real Estate
- Artificial Intelligence
- Renewable Energy
- Biotechnology
- Cybersecurity

## 🎯 How It Works

### The Workflow

```
User Input (Sector)
        ↓
[Trending Company Finder]
   - Searches news for hot companies
   - Identifies 2-3 candidates
        ↓
[Financial Researcher]
   - Deep dive into each company
   - Analyzes market position
   - Evaluates growth prospects
        ↓
[Stock Picker]
   - Reviews all research
   - Selects best opportunity
   - Explains rationale
        ↓
[Manager]
   - Coordinates workflow
   - Ensures quality
        ↓
Email + Web Display
```

### Technical Architecture

```python
# Hierarchical process with manager coordination
StockPicker Crew
├── Manager Agent (GPT-4o)
│   ├── Delegates to Trending Finder
│   ├── Delegates to Researcher
│   └── Delegates to Stock Picker
│
├── Worker Agents
│   ├── Trending Company Finder (Sonar + Search Tools)
│   ├── Financial Researcher (GPT-4o-mini + Research Tools)
│   └── Stock Picker (GPT-4o-mini)
│
└── Output
    ├── JSON: Trending companies
    ├── JSON: Research reports
    └── MD: Final decision
```

## ⚠️ Important Disclaimers

### Not Financial Advice

This tool is for **educational and research purposes only**. It is **NOT financial advice**.

- 🚫 Do not make investment decisions based solely on this tool
- 📚 Always conduct your own thorough due diligence
- 💼 Consult with licensed financial advisors before investing
- 📉 All investments carry risk - you may lose money
- ⏰ Past performance does not guarantee future results

### Data & Privacy

- Your email is used **only** to deliver results
- No personal data is stored or shared
- API keys are never logged or exposed
- All processing happens securely

## 🛠️ Troubleshooting

### Common Issues

**1. "ImportError: cannot import name 'SuperDevTool'"**
- Solution: Use `SerperDevTool` and `ScrapeWebsiteTool` instead
- Already fixed in latest version

**2. "Manager agent should not be included in agents list"**
- Solution: Remove `@agent` decorator from manager
- Specify worker agents manually in crew creation

**3. "API Key not found"**
- Solution: Check environment variables are set correctly
- Verify `.env` file exists and is properly formatted

**4. Email not sending**
- Verify SendGrid API key is valid
- Confirm sender email is verified in SendGrid
- Check SendGrid dashboard for delivery logs

**5. Rate limit errors**
- Wait a few minutes before retrying
- Check API usage on provider dashboards
- Consider upgrading API plans if needed

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ using CrewAI and AI**

*For educational purposes only. Not financial advice.*
