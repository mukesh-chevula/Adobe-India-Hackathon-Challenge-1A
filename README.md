# Challenge 1A: PDF Outline Extraction

## Quick Start

### Super Simple (One Command)

```bash
# Build and run everything
./run.sh
```

### Usage

- Put PDF files in `input/` folder
- Run `./run.sh`
- Get JSON files in `output/` folder

That's it!

## What It Does

Converts PDF files to structured JSON outlines:

**Input:** `document.pdf`
**Output:** `document.json`

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Chapter 1", "page": 1 },
    { "level": "H2", "text": "Section 1.1", "page": 2 }
  ]
}
```

## Overview

This solution extracts structured outlines from PDF documents, identifying the title and hierarchical headings (H1, H2, H3) with their corresponding page numbers. The system is optimized for speed and accuracy, processing up to 50-page PDFs in under 10 seconds.

## Solution Architecture

### Core Components

1. **PDF Processor** (`src/pdf_processor.py`)``

   - PDF text extraction using PyMuPDF
   - Page-by-page content analysis
   - Font and style metadata extraction

2. **Outline Extractor** (`src/outline_extractor.py`)

   - Multi-strategy heading detection
   - Hierarchical structure analysis
   - Title identification from document metadata and content

3. **Main Entry Point** (`process_pdfs.py`)
   - Docker container entry point
   - Batch processing of PDFs from input directory
   - JSON output generation to output directory

### Detection Strategies

#### Title Detection

1. **Metadata extraction** from PDF properties
2. **First page analysis** for large, prominent text
3. **Font-based detection** using size and weight heuristics

#### Heading Detection

1. **Font-size based analysis** - Larger fonts typically indicate headings
2. **Font-weight analysis** - Bold text often represents headings
3. **Whitespace analysis** - Headers typically have spacing above/below
4. **Pattern matching** - Common heading patterns (numbers, bullets, etc.)
5. **Position analysis** - Headers often appear at specific positions

### Output Format

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Section",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Subsection",
      "page": 2
    },
    {
      "level": "H3",
      "text": "Sub-subsection",
      "page": 3
    }
  ]
}
```

## Technical Implementation

### Dependencies

- **PyMuPDF (fitz)**: Fast PDF text extraction and metadata access
- **re (regex)**: Pattern matching for heading detection
- **json**: Output formatting
- **pathlib**: File path handling

### Performance Optimizations

- **Streaming processing**: Process pages sequentially to minimize memory usage
- **Efficient text extraction**: Use PyMuPDF's optimized text extraction
- **Smart caching**: Cache font information to avoid repeated calculations
- **Early termination**: Stop processing when sufficient structure is found

### Multilingual Support

- **Unicode handling**: Proper support for non-ASCII characters
- **Language-agnostic patterns**: Detection based on structure rather than language
- **Font analysis**: Works across different writing systems

## Docker Configuration

### **Dockerfile Specification**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "process_pdfs.py"]
```

### **Docker Build Command**

```bash
docker build -t challenge1a-processor .
```

### **Docker Run Command**

```bash
docker run --rm \
  -v "$(pwd)/input":/app/input:ro \
  -v "$(pwd)/output":/app/output \
  challenge1a-processor
```

### Base Image

- `python:3.10-slim` for minimal footprint
- AMD64 platform compatibility
- Offline operation (no network access)

### Container Specifications

- **Input**: Read-only mount at `/app/input`
- **Output**: Write mount at `/app/output`
- **Memory**: Optimized for 16GB constraint
- **CPU**: Utilizes 8 available cores

## Usage

### **Docker Commands (Recommended)**

#### Using Shell Script (Easiest)

```bash
# One command - builds and runs everything
./run.sh
```

#### Manual Docker Commands

```bash
# Build the Docker image
docker build -t challenge1a-processor .

# Run the container
docker run --rm \
  -v "$(pwd)/input":/app/input:ro \
  -v "$(pwd)/output":/app/output \
  challenge1a-processor
```

### **Local Python (Alternative)**

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run locally
python3 process_pdfs.py
```

### Input/Output

- **Input**: Place PDF files in `input/` directory
- **Output**: JSON files generated in `output/` directory
- **Naming**: `document.pdf` → `document.json`

## Performance Metrics

### Target Performance

- **Processing Time**: ≤ 10 seconds for 50-page PDF
- **Memory Usage**: ≤ 16GB RAM
- **Model Size**: ≤ 200MB total
- **CPU Efficiency**: Optimal use of 8 cores

### Monitoring

- Processing time per PDF
- Memory consumption tracking
- Accuracy metrics for heading detection
- Output quality validation

## Troubleshooting

### Common Issues

1. **Font detection failures**: Fallback to text pattern analysis
2. **Unicode encoding**: Proper UTF-8 handling
3. **Memory limits**: Streaming processing for large files
4. **Performance bottlenecks**: Profiling and optimization

### Debugging

- Verbose logging available via environment variables
- Intermediate output for analysis
- Error handling with graceful degradation

---

**Note**: This solution prioritizes accuracy and performance while maintaining simplicity and reliability for the competition environment.
