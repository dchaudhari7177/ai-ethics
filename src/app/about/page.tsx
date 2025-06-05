export default function AboutPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">About EthicalHire</h1>
        <p className="mt-2 text-gray-600">
          Understanding and mitigating bias in AI-based recruitment
        </p>
      </div>

      {/* Project Overview */}
      <div className="prose prose-indigo max-w-none">
        <h2>Project Overview</h2>
        <p>
          EthicalHire is a research project that explores the ethical implications
          of using artificial intelligence in recruitment processes. Our goal is to
          demonstrate how machine learning algorithms can inadvertently introduce
          bias in hiring decisions and provide tools to detect and mitigate such
          biases.
        </p>

        <h2>Key Features</h2>
        <ul>
          <li>
            <strong>Resume Analysis:</strong> Advanced machine learning algorithms
            analyze resumes for relevant skills and experience while monitoring for
            potential biases.
          </li>
          <li>
            <strong>Bias Detection:</strong> Comprehensive metrics to identify and
            measure various forms of bias in recruitment decisions.
          </li>
          <li>
            <strong>Fairness Metrics:</strong> Implementation of industry-standard
            fairness metrics including demographic parity, equal opportunity, and
            disparate impact.
          </li>
          <li>
            <strong>Mitigation Strategies:</strong> Tools and recommendations to
            reduce identified biases and promote fair decision-making.
          </li>
        </ul>

        <h2>Ethical Considerations</h2>
        <p>
          The use of AI in recruitment raises important ethical considerations that
          we actively address:
        </p>

        <h3>Transparency</h3>
        <p>
          We believe in complete transparency about how our system makes decisions.
          All metrics and decision factors are clearly displayed and explained.
        </p>

        <h3>Fairness</h3>
        <p>
          Our system implements multiple fairness metrics and actively works to
          identify and mitigate biases against protected groups.
        </p>

        <h3>Accountability</h3>
        <p>
          We maintain detailed logs of all decisions and their rationale, enabling
          audit trails and accountability.
        </p>

        <h3>Human Oversight</h3>
        <p>
          While our system provides recommendations, we emphasize the importance of
          human oversight in final hiring decisions.
        </p>

        <h2>Technical Implementation</h2>
        <h3>Frontend</h3>
        <ul>
          <li>Next.js with TypeScript</li>
          <li>TailwindCSS for styling</li>
          <li>React Query for state management</li>
          <li>Recharts for data visualization</li>
        </ul>

        <h3>Backend</h3>
        <ul>
          <li>FastAPI (Python)</li>
          <li>scikit-learn for machine learning</li>
          <li>AIF360 for fairness metrics</li>
          <li>PostgreSQL for data storage</li>
        </ul>

        <h2>Research Paper</h2>
        <p>
          This project is part of a research paper titled "Bias in AI Recruitment
          Systems: An Ethical Evaluation of Algorithmic Hiring Tools". The paper
          explores:
        </p>
        <ul>
          <li>Current state of AI in recruitment</li>
          <li>Sources of algorithmic bias</li>
          <li>Impact on different demographic groups</li>
          <li>Mitigation strategies</li>
          <li>Ethical considerations</li>
          <li>Future recommendations</li>
        </ul>

        <h2>Get Involved</h2>
        <p>
          We welcome contributions from researchers, developers, and industry
          professionals. If you're interested in contributing to this project or
          have suggestions for improvement, please reach out to us.
        </p>
      </div>
    </div>
  );
} 