# AI Bulk Blog Generator 🤖✍️

Generate multiple high-quality programming blog articles automatically using Google's Gemini AI API.

## Features ✨

- 📝 Bulk generate 10+ articles at once
- 🎯 SEO-optimized with meta descriptions and keywords
- 💾 Export as HTML or Markdown
- 🎨 Beautiful formatting with code syntax highlighting
- 🔄 Automatic retry logic with error handling
- 📊 Generation summary report

## Prerequisites 📋

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Bulk-Blog-Generator.git
cd AI-Bulk-Blog-Generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
   - Open `config.py`
   - Add your Gemini API key

## Usage 💻

### Quick Start

Run the script with default 10 programming topics:
```bash
python bulk_article_generator.py
```

### Custom Topics

Edit the `ARTICLE_TOPICS` list in the script:
```python
ARTICLE_TOPICS = [
    {
        "title": "Your Article Title",
        "description": "Additional context or requirements"
    },
    # Add more topics...
]
```

### Configuration Options
```python
generate_bulk_articles(
    articles_list=ARTICLE_TOPICS,
    output_format="html",  # or "markdown"
    output_dir="blog"      # output directory
)
```

## Output 📂

Generated articles are saved in the `blog/` directory:
- HTML files with embedded styling
- Meta descriptions and keywords
- `generation_summary.json` with statistics

## Example Output Structure 📁
```
blog/
├── understanding-python-decorators-a-complete-guide.html
├── restful-api-design-best-practices.html
├── introduction-to-docker-for-developers.html
├── ...
└── generation_summary.json
```

## Default Topics Included 📚

1. Understanding Python Decorators
2. RESTful API Design Best Practices
3. Introduction to Docker for Developers
4. Git Branching Strategies for Teams
5. JavaScript Async/Await
6. Database Indexing
7. Microservices Architecture
8. React Hooks Deep Dive
9. SQL vs NoSQL Databases
10. Test-Driven Development (TDD)

## Customization 🎨

### Change Output Format
```python
output_format="markdown"  # Save as .md files
```

### Adjust Article Length

Modify the prompt in `generate_article_with_gemini()`:
```python
1. Write a 2500-3000 word article  # Change word count here
```

### Rate Limiting

Adjust delay between articles:
```python
time.sleep(2)  # Change delay in seconds
```

## Error Handling 🛡️

The script includes:
- Automatic retry with exponential backoff (3 attempts)
- API rate limiting respect
- Graceful error messages with colored output

## API Costs 💰

Google Gemini API offers:
- Free tier: 15 requests per minute
- Generous monthly quota
- Check current pricing: [Google AI Pricing](https://ai.google.dev/pricing)

## Troubleshooting 🔧

### Common Issues

**Model not found error:**
```bash
# Update to latest SDK
pip install --upgrade google-generativeai
```

**Rate limit exceeded:**
- Increase `time.sleep()` delay between articles
- Check your API quota

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Google Gemini AI for the powerful API
- Markdown rendering by [mdonhtml.js](https://github.com/OCEANOFANYTHINGOFFICIAL/mdonhtml.js)

## Author ✍️

Your Name - [RSBEJINI]([https://twitter.com/yourhandle](https://www.linkedin.com/in/ravi-shankar-bejini-5887711b0/))

Project Link: [https://github.com/yourusername/AI-Bulk-Blog-Generator](https://github.com/yourusername/AI-Bulk-Blog-Generator)

## Support ⭐

If you find this project helpful, please give it a ⭐️!

---

**Note:** Keep your API key secure and never commit it to public repositories!
