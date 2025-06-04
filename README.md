# AllyIn Compass - Discovery & Intelligence Engine

AllyIn Compass is a powerful multi-modal intelligence engine that combines structured data analysis, unstructured document processing, and advanced retrieval capabilities to provide comprehensive insights and answers.

## 🌟 Features

- **Multi-Modal Data Processing**
  - Structured data handling with DuckDB
  - Unstructured document parsing (PDF, EML)
  - Vector embeddings for semantic search
  - Graph-based relationship analysis

- **Advanced Retrieval System**
  - SQL-based structured data retrieval
  - Vector similarity search
  - Graph-based relationship traversal
  - RAG (Retrieval Augmented Generation) capabilities

- **User Interface**
  - Streamlit-based interactive dashboard
  - Real-time feedback collection
  - Performance metrics visualization
  - Query testing interface

- **Security & Compliance**
  - PII detection and filtering
  - Compliance tagging system
  - Data privacy safeguards

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cxx5208/allyin-compass.git
cd allyin-compass
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

### Project Structure
```
allyin-compass/
├── data/
│   ├── structured/      # CSV files and DuckDB database
│   └── unstructured/    # PDF, EML files and parsed data
├── src/
│   ├── agents/         # Multi-tool agent implementation
│   ├── ingest/         # Data ingestion modules
│   ├── retrievers/     # Different retrieval strategies
│   └── tools/          # RAG and other tools
├── ui/                 # Streamlit interface
├── security/           # PII and compliance modules
├── feedback/           # Feedback logging system
├── dashboards/         # Metrics and analytics
└── examples/           # Use case examples
```

## 💡 Usage

### 1. Data Ingestion

Process structured data:
```bash
python src/ingest/structured_loader.py
```

Process unstructured documents:
```bash
python src/ingest/document_parser.py
```

Generate embeddings:
```bash
python src/ingest/embedder.py
```

### 2. Running the UI

Start the Streamlit interface:
```bash
streamlit run ui/app.py
```

### 3. Testing Use Cases

Example queries and use cases are available in `examples/use_case_tests.json`.

## 🔧 Components

### Data Processing
- **Structured Loader**: Handles CSV data ingestion into DuckDB
- **Document Parser**: Processes PDF and EML files
- **Embedder**: Generates vector embeddings for semantic search

### Retrieval System
- **SQL Retriever**: Query structured data using SQL
- **Vector Retriever**: Perform semantic search using embeddings
- **Graph Retriever**: Analyze relationships between entities

### Security
- **PII Filter**: Detect and filter personally identifiable information
- **Compliance Tagger**: Tag content based on compliance requirements

### UI & Feedback
- **Streamlit App**: Interactive interface for queries and results
- **Feedback Logger**: Collect and store user feedback
- **Metrics Dashboard**: Visualize system performance

## 📊 Performance Monitoring

The system includes built-in metrics tracking:
- Query success rates
- Response times
- User feedback analysis
- System resource usage

## 🔒 Security & Compliance

- PII detection and filtering
- Compliance tagging system
- Data privacy safeguards
- Secure data storage

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- DuckDB for efficient structured data processing
- ChromaDB for vector storage
- Streamlit for the user interface
- Sentence Transformers for embeddings

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 