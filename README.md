# Coursera-Course-Automation

Automated quiz solver for Coursera courses using Selenium and AI (OpenAI/Azure OpenAI). This tool automatically navigates to Coursera quizzes, extracts questions and answers, uses AI to select the best answers, and submits the quiz.

<img width="805" height="707" alt="image" src="https://github.com/user-attachments/assets/940fde45-0e0a-4b3b-8a33-0f73792aced0" />

## ⚠️ Disclaimer

This project is for **educational purposes only**. Using automated tools to complete quizzes may violate Coursera's Terms of Service. The author is not responsible for any consequences of using this tool. Use at your own risk.

## ✨ Features

- **Automated Login**: Uses cookies to authenticate with Coursera
- **Question Extraction**: Automatically scrapes quiz questions and multiple-choice options
- **AI-Powered Answers**: Leverages OpenAI/Azure OpenAI to select the most appropriate answers
- **Auto-Submission**: Automatically fills in name, checks agreement, and submits the quiz
- **Grade Display**: Shows the quiz grade after submission
- **Retry Logic**: Implements retry mechanism for API calls to handle failures gracefully

## 🛠️ Technologies Used

- **Python 3.x**
- **Selenium WebDriver**: For browser automation
- **OpenAI API**: For AI-powered answer selection
- **python-dotenv**: For environment variable management

## 📋 Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)
- OpenAI API key or Azure OpenAI credentials

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Coursera-Course-Automation.git
   cd Coursera-Course-Automation
   ```

2. **Install dependencies**
   ```bash
   pip install selenium openai python-dotenv
   ```

3. **Download ChromeDriver**
   - Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
   - Ensure it matches your Chrome browser version
   - Add ChromeDriver to your system PATH

## ⚙️ Configuration

1. **Create a `.env` file** in the project root:
   ```env
   API_KEY=your_openai_api_key_here
   API_MODEL=gpt-4
   API_BASE_URL=https://api.openai.com/v1
   ```

   For Azure OpenAI:
   ```env
   API_KEY=your_azure_openai_key
   API_MODEL=gpt-4
   API_BASE_URL=https://your-resource.openai.azure.com/
   ```

2. **Get Coursera Cookies**:
   - Open your browser and log in to Coursera
   - Use a browser extension (like EditThisCookie or Cookie Editor) to export cookies
   - Copy the cookies JSON and replace the `COOKIES` variable in `quiz_solving.py`

3. **Set Quiz URL**:
   - Update the `QUIZ_URL` variable in `quiz_solving.py` with your target quiz URL

4. **Update Your Name**:
   - In `QuizSolver.py`, update the name in `name_input.send_keys("Muammar Mufid")` with your legal name

## 📖 Usage

1. **Run the automation script**:
   ```bash
   python quiz_solving.py
   ```

2. **The script will**:
   - Open Chrome browser
   - Navigate to Coursera and authenticate using cookies
   - Go to the specified quiz URL
   - Click the start button
   - Extract all questions and answers
   - Send questions to AI for answer selection
   - Automatically select the AI-recommended answers
   - Fill in your name and submit the quiz
   - Display your grade

3. **Wait for completion** - The browser will remain open until you press Enter

## 📁 Project Structure

```
Coursera-Course-Automation/
├── QuizSolver.py          # Main quiz solver class with automation logic
├── quiz_solving.py        # Entry point script
├── README.md              # Project documentation
├── LICENSE                # License file
└── .env                   # Environment variables (create this)
```

## 🔧 How It Works

1. **Authentication**: Uses exported cookies to maintain logged-in session
2. **Navigation**: Selenium WebDriver navigates to the quiz and clicks start
3. **Extraction**: Scrapes question text and all answer options using CSS selectors
4. **AI Processing**: 
   - Formats questions into a prompt
   - Sends to OpenAI API
   - Receives structured JSON response with selected options
5. **Answer Selection**: Automatically clicks the checkboxes for selected answers
6. **Submission**: Checks agreement, fills name, and submits the quiz
7. **Result**: Displays the grade received

## 🎯 Key Components

### QuizSolver Class

- `solve_quiz(quiz_url)`: Main method that orchestrates the entire quiz-solving process
- `ask_ai(prompt, max_retries=3)`: Sends questions to AI and handles retries

### Helper Functions

- `create_prompt(qas)`: Formats questions and answers into an AI-friendly prompt
- `print_qas(qas)`: Utility function to print questions and answers

## 🐛 Troubleshooting

**ChromeDriver Issues**:
- Ensure ChromeDriver version matches your Chrome browser
- Add ChromeDriver to system PATH

**Cookie Authentication Fails**:
- Export fresh cookies from a logged-in Coursera session
- Ensure all required cookies are included

**AI API Errors**:
- Verify API key is correct in `.env`
- Check API rate limits and quotas
- Ensure the model name is correct

**Element Not Found**:
- Coursera may have updated their UI
- Update CSS selectors in `QuizSolver.py`

## 📝 Customization

You can customize the AI behavior by modifying:
- **System prompt** in `ask_ai()` method
- **Temperature** setting (currently 0 for deterministic answers)
- **Model** in `.env` file (e.g., gpt-3.5-turbo, gpt-4)
- **Wait times** in WebDriverWait calls

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## ⚖️ Legal Notice

This tool is provided for educational and research purposes only. Automated quiz completion may violate Coursera's Terms of Service and academic integrity policies. The developers do not endorse or encourage cheating or violation of any terms of service. Users are solely responsible for how they use this software.

## 🙏 Acknowledgments

- Selenium WebDriver for browser automation capabilities
- OpenAI for providing powerful AI models
- Coursera for educational content (please use responsibly)

---

**Note**: Always respect academic integrity and use automation tools ethically and responsibly.
