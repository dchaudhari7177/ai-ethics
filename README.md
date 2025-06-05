# EthicalHire: AI Ethics in Recruitment

A research project demonstrating and mitigating algorithmic bias in AI-based recruitment systems.

## Project Overview

EthicalHire is a full-stack application that explores the ethical implications of using artificial intelligence in recruitment processes. The system demonstrates how machine learning algorithms can inadvertently introduce bias in hiring decisions and provides tools to detect and mitigate such biases.

### Key Features

- 📄 **Resume Analysis System**
  - Upload and parse resumes
  - Extract key features (skills, education, experience)
  - AI-based candidate screening

- 🔍 **Bias Detection**
  - Real-time bias monitoring
  - Gender and demographic bias analysis
  - Fairness metrics visualization

- ⚖️ **Bias Mitigation**
  - Pre-processing techniques
  - In-processing fairness constraints
  - Post-processing adjustments

- 📊 **Ethics Dashboard**
  - Fairness metrics visualization
  - Decision explanations (XAI)
  - Bias impact reports

## Technical Stack

### Frontend
- Next.js with TypeScript
- TailwindCSS for styling
- React Query for state management
- Recharts for data visualization

### Backend
- FastAPI (Python)
- scikit-learn for machine learning
- AIF360 for fairness metrics
- PostgreSQL for data storage

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.8+)
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ethical-hire.git
   cd ethical-hire
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your PostgreSQL credentials and other settings.

5. Initialize the database:
   ```bash
   cd backend
   python app/db/init_db.py
   ```

6. Start the development servers:

   In one terminal (frontend):
   ```bash
   npm run dev
   ```

   In another terminal (backend):
   ```bash
   cd backend
   python run.py
   ```

7. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   ├── core/           # Core configuration
│   │   │   ├── db/             # Database models and utilities
│   │   │   └── ml/             # Machine learning models
│   │   ├── requirements.txt
│   │   └── run.py
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/     # React components
│   │   │   ├── pages/         # Next.js pages
│   │   │   └── styles/        # CSS styles
│   │   └── lib/               # Utilities
│   ├── public/
│   └── package.json
├── README.md
└── LICENSE
```

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Research Paper

This project is part of a research paper titled "Bias in AI Recruitment Systems: An Ethical Evaluation of Algorithmic Hiring Tools". The paper explores:

- Current state of AI in recruitment
- Sources of algorithmic bias
- Impact on different demographic groups
- Mitigation strategies
- Ethical considerations
- Future recommendations

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- IBM AI Fairness 360 team for their fairness metrics toolkit
- The open-source community for various tools and libraries used in this project
- Academic researchers in AI ethics and fairness

## Contact

For questions or feedback about this project, please [open an issue](https://github.com/yourusername/ethical-hire/issues) on GitHub.
