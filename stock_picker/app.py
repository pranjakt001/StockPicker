import gradio as gr
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from crew import StockPicker
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Debug: Check if API keys are loaded
print("=" * 50)
print("Environment Variables Check:")
print(f"PERPLEXITY_API_KEY: {'✅ Set' if os.environ.get('PERPLEXITY_API_KEY') else '❌ Missing'}")
print(f"OPENAI_API_KEY: {'✅ Set' if os.environ.get('OPENAI_API_KEY') else '❌ Missing'}")
print(f"SENDGRID_API_KEY: {'✅ Set' if os.environ.get('SENDGRID_API_KEY') else '❌ Missing'}")
print(f"FROM_EMAIL: {'✅ Set' if os.environ.get('FROM_EMAIL') else '❌ Missing'}")
print("=" * 50)

def send_email(to_email, subject, html_content):
    """Send email using SendGrid - The notification delivery system"""
    try:
        sendgrid_key = os.environ.get('SENDGRID_API_KEY')
        if not sendgrid_key:
            print("Warning: SENDGRID_API_KEY not found")
            return False
            
        sg = SendGridAPIClient(sendgrid_key)
        from_email = Email(os.environ.get('FROM_EMAIL', 'noreply@stockpicker.com'))
        to_email = To(to_email)
        content = Content("text/html", html_content)
        mail = Mail(from_email, to_email, subject, content)
        
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def format_analysis_content(result):
    """Format the analysis content with better HTML structure"""
    
    # Replace markdown-style headers
    result = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', result, flags=re.MULTILINE)
    result = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', result, flags=re.MULTILINE)
    
    # Replace **bold** with <strong>
    result = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', result)
    
    # Replace bullet points
    result = result.replace('- ', '• ')
    
    # Replace newlines with proper breaks
    lines = result.split('\n')
    formatted_lines = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith('<h') and not in_paragraph:
                formatted_lines.append('<p>')
                in_paragraph = True
            formatted_lines.append(line + '<br>')
        else:
            if in_paragraph:
                formatted_lines.append('</p>')
                in_paragraph = False
            formatted_lines.append('<br>')
    
    if in_paragraph:
        formatted_lines.append('</p>')
    
    return ''.join(formatted_lines)

def format_result_as_html(result, sector):
    """Format the crew result as HTML for email - The presentation layer"""
    
    # Format the content nicely
    result_html = format_analysis_content(result)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Investment Recommendation</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #2c3e50;
                background-color: #f4f7f9;
                padding: 20px;
            }}
            
            .email-container {{
                max-width: 650px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            
            .header p {{
                font-size: 16px;
                opacity: 0.95;
                margin-top: 5px;
            }}
            
            .badge {{
                display: inline-block;
                background-color: rgba(255,255,255,0.2);
                padding: 8px 20px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 15px;
                backdrop-filter: blur(10px);
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .info-section {{
                background-color: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
            }}
            
            .info-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
                align-items: center;
            }}
            
            .info-row:last-child {{
                margin-bottom: 0;
            }}
            
            .info-label {{
                font-weight: 600;
                color: #667eea;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .info-value {{
                color: #2c3e50;
                font-weight: 500;
                font-size: 15px;
            }}
            
            .section-title {{
                font-size: 24px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 20px;
                padding-bottom: 12px;
                border-bottom: 3px solid #667eea;
            }}
            
            .analysis-content {{
                background-color: #ffffff;
                padding: 25px;
                border-radius: 8px;
                border: 1px solid #e1e8ed;
                margin-bottom: 25px;
                line-height: 1.8;
            }}
            
            .analysis-content h2 {{
                color: #667eea;
                margin-top: 25px;
                margin-bottom: 15px;
                font-size: 20px;
            }}
            
            .analysis-content h3 {{
                color: #764ba2;
                margin-top: 20px;
                margin-bottom: 12px;
                font-size: 18px;
            }}
            
            .analysis-content strong {{
                color: #764ba2;
                font-weight: 600;
            }}
            
            .analysis-content p {{
                margin-bottom: 15px;
            }}
            
            .divider {{
                height: 2px;
                background: linear-gradient(90deg, transparent, #667eea, transparent);
                margin: 30px 0;
            }}
            
            .footer {{
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 30px;
                text-align: center;
            }}
            
            .footer p {{
                margin-bottom: 10px;
                font-size: 14px;
            }}
            
            .disclaimer {{
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 8px;
                padding: 20px;
                margin-top: 30px;
            }}
            
            .disclaimer-title {{
                color: #856404;
                font-weight: 700;
                font-size: 16px;
                margin-bottom: 10px;
            }}
            
            .disclaimer-text {{
                color: #856404;
                font-size: 13px;
                line-height: 1.6;
            }}
            
            .icon {{
                font-size: 24px;
                margin-right: 10px;
            }}
            
            @media only screen and (max-width: 600px) {{
                .email-container {{
                    border-radius: 0;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .header h1 {{
                    font-size: 24px;
                }}
                
                .content {{
                    padding: 25px 20px;
                }}
                
                .info-row {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                
                .info-value {{
                    margin-top: 5px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <!-- Header -->
            <div class="header">
                <div class="icon">📈</div>
                <h1>Investment Recommendation</h1>
                <p>AI-Powered Stock Analysis Report</p>
                <div class="badge">{sector} Sector</div>
            </div>
            
            <!-- Content -->
            <div class="content">
                <!-- Info Section -->
                <div class="info-section">
                    <div class="info-row">
                        <span class="info-label">📊 Sector</span>
                        <span class="info-value">{sector}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">📅 Analysis Date</span>
                        <span class="info-value">{datetime.now().strftime("%B %d, %Y at %I:%M %p")}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">🤖 Generated By</span>
                        <span class="info-value">AI Multi-Agent System</span>
                    </div>
                </div>
                
                <div class="divider"></div>
                
                <!-- Main Analysis -->
                <h2 class="section-title">📋 Investment Analysis</h2>
                
                <div class="analysis-content">
                    {result_html}
                </div>
                
                <!-- Disclaimer -->
                <div class="disclaimer">
                    <div class="disclaimer-title">⚠️ Important Disclaimer</div>
                    <div class="disclaimer-text">
                        This is an automated AI-generated research report for <strong>educational purposes only</strong>. 
                        This is <strong>NOT financial advice</strong>. Always conduct your own thorough due diligence and 
                        consult with qualified financial advisors before making any investment decisions. Past performance 
                        does not guarantee future results. Investments carry risk, and you may lose money.
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p style="font-size: 16px; font-weight: 600; margin-bottom: 15px;">
                    🚀 Powered by AI Stock Picker
                </p>
                <p style="opacity: 0.8;">
                    Multi-agent AI system powered by CrewAI & Perplexity
                </p>
                <p style="opacity: 0.7; font-size: 12px; margin-top: 15px;">
                    © {datetime.now().year} AI Stock Picker. For educational purposes only.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def run_stock_analysis(email, sector, progress=gr.Progress()):
    """Main function to run stock analysis - The kitchen coordinator"""
    
    # Validation - Check if orders are valid
    if not email or '@' not in email:
        return "❌ Please enter a valid email address.", "❌ Invalid input"
    
    if not sector or len(sector.strip()) == 0:
        return "❌ Please enter an investment sector.", "❌ Invalid input"
    
    try:
        # Update progress - Kitchen is opening
        progress(0.1, desc="🚀 Initializing AI agents (Opening the kitchen)...")
        
        # Prepare inputs - Getting the order ready
        inputs = {
            'sector': sector.strip()
        }
        
        # Update progress - Ingredient sourcing begins
        progress(0.3, desc="🔍 Finding trending companies (Sourcing fresh ingredients)...")
        
        # Run the crew - The kitchen starts working!
        stock_picker_crew = StockPicker()
        crew_instance = stock_picker_crew.crew()
        result = crew_instance.kickoff(inputs=inputs)
        
        # Update progress - Quality inspection phase
        progress(0.7, desc="📊 Analyzing investment opportunities (Inspecting quality)...")
        
        # Get the output - The final dish is ready
        output = result.raw if hasattr(result, 'raw') else str(result)
        
        # Update progress - Plating and delivery
        progress(0.9, desc="📧 Sending email (Delivering the dish)...")
        
        # Send email - Serve to customer
        html_content = format_result_as_html(output, sector)
        email_sent = send_email(
            to_email=email,
            subject=f"📈 Stock Investment Recommendation: {sector}",
            html_content=html_content
        )
        
        # Update progress - Service complete!
        progress(1.0, desc="✅ Complete!")
        
        # Prepare success message
        email_status = "✅ **Email sent successfully!**" if email_sent else "⚠️ **Results generated but email delivery failed.**"
        
        final_output = f"""
{email_status}

---

## 📈 Stock Investment Recommendation

**Sector:** `{sector}`  
**Analysis Date:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}  
**Delivered to:** {email}

---

{output}

---

### ⚠️ Disclaimer
*This is an automated AI-generated research report for educational purposes only. Always conduct your own due diligence and consult with a qualified financial advisor before making any investment decisions. Past performance does not guarantee future results.*
"""
        
        return final_output, "✅ Analysis complete!"
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        error_msg = f"""
## ❌ Analysis Failed

**Error:** {str(e)}

Please check:
- API keys are configured correctly in Space settings (PERPLEXITY_API_KEY, OPENAI_API_KEY, SENDGRID_API_KEY, FROM_EMAIL)
- Rate limits haven't been exceeded
- Try again in a few moments

**Technical Details:**
```
{error_details}
```

If the issue persists, please check your configuration files (agents.yaml, tasks.yaml).
"""
        return error_msg, "❌ Failed"

# Create Gradio Interface - The Restaurant Entrance
with gr.Blocks(theme=gr.themes.Soft(), title="AI Stock Picker", css="""
    .gradio-container {max-width: 1200px !important}
    footer {visibility: hidden}
""") as demo:
    
    gr.Markdown(
        """
        # 📈 AI-Powered Stock Investment Advisor
        
        Get personalized stock recommendations powered by multi-agent AI that researches the latest market trends in real-time.
        
        ### 🤖 How it works (The Kitchen Process):
        1. **Enter** your email address and investment sector
        2. **Ingredient Sourcer** (trending_company_finder) finds 2-3 trending companies
        3. **Quality Inspector** (financial_researcher) deeply analyzes each company
        4. **Head Chef** (stock_picker) selects the best investment
        5. **Manager** coordinates the entire workflow
        6. **Receive** detailed analysis via email and in-app
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Your Information")
            
            email_input = gr.Textbox(
                label="📧 Email Address",
                placeholder="your.email@example.com",
                info="Results will be sent to this email",
                lines=1
            )
            
            sector_input = gr.Textbox(
                label="💼 Investment Sector",
                placeholder="e.g., Technology, Healthcare, Energy",
                info="Which sector interests you?",
                lines=1
            )
            
            gr.Markdown("**💡 Popular sectors:**")
            sector_examples = gr.Examples(
                examples=[
                    ["Technology"],
                    ["Healthcare"],
                    ["Energy"],
                    ["Finance"],
                    ["Consumer Goods"],
                    ["Real Estate"],
                    ["Artificial Intelligence"],
                    ["Renewable Energy"],
                    ["Biotechnology"],
                    ["Cybersecurity"]
                ],
                inputs=[sector_input],
                label=""
            )
            
            submit_btn = gr.Button(
                "🚀 Generate Analysis", 
                variant="primary", 
                size="lg",
                scale=1
            )
            
            status_output = gr.Textbox(
                label="⏳ Status",
                placeholder="Ready to analyze...",
                interactive=False,
                lines=1
            )
        
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Investment Analysis")
            
            result_output = gr.Markdown(
                value="*Your detailed investment analysis will appear here...*\n\n*The AI kitchen is ready to serve!*"
            )
    
    gr.Markdown(
        """
        ---
        
        ### ⚠️ Important Disclaimer
        
        This AI tool provides **automated research for educational purposes only**. It is **NOT financial advice**.
        
        - 🚫 Do not make investment decisions based solely on this analysis
        - 📚 Always conduct thorough due diligence
        - 💼 Consult with licensed financial advisors
        - 📉 Investments carry risk - you may lose money
        
        ### 🔒 Privacy & Data
        
        - Your email is used **only** to deliver analysis results
        - No data is stored or shared with third parties
        - All processing is done securely
        
        ### 🛠️ Powered By
        
        - **CrewAI** - Multi-agent orchestration (The Kitchen Management System)
        - **Perplexity AI (Sonar)** - Real-time web research (Market Intelligence)
        - **OpenAI GPT-4** - Financial analysis (Expert Chefs)
        - **SendGrid** - Email delivery (Customer Notification)
        
        ### 🧑‍💼 The AI Crew (Kitchen Staff)
        
        1. **Trending Company Finder** - Searches news for hot companies (Ingredient Sourcer)
        2. **Financial Researcher** - Deep analysis of each company (Quality Inspector)
        3. **Stock Picker** - Selects best investment (Head Chef)
        4. **Manager** - Coordinates all agents (Kitchen Manager)
        """
    )
    
    # Connect the button to the function - Taking orders
    submit_btn.click(
        fn=run_stock_analysis,
        inputs=[email_input, sector_input],
        outputs=[result_output, status_output]
    )

# Launch the app - Open for business!
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )