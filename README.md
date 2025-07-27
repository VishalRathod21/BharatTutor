# Bharat Tutor AI

An AI-powered educational assistant designed to help Indian students with their studies using the Gemini AI model.

![Bharat Tutor AI](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📋 Overview

Bharat Tutor AI is an intelligent tutoring system that leverages Google's Gemini AI to provide personalized learning experiences for Indian students. The application offers features like doubt clarification, study material generation, and interactive learning sessions.

## ✨ Features

- **AI-Powered Tutoring**: Get instant help with academic subjects using Gemini AI
- **Personalized Learning**: Tailored content based on class level and subject
- **Interactive Interface**: Clean, modern UI with dark mode support
- **Doubt Resolution**: Ask questions and get detailed explanations
- **Curriculum-Aligned**: Content aligned with Indian educational standards

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bharat-tutor-ai.git
   cd bharat-tutor-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

### Running the Application

```bash
streamlit run app.py
```

## 🛠️ Project Structure

```
bharat-tutor-ai/
├── app.py                 # Main Streamlit application
├── gemini_client.py       # Gemini AI client implementation
├── knowledge_base.py      # Knowledge base management
├── styles.css             # Custom styling
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- All the amazing open-source contributors

---

<div align="center">
  Made with ❤️ for Indian Education
</div>