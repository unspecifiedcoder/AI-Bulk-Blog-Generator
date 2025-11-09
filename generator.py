import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic._internal._config")

import os
import json
import time
import google.generativeai as genai
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure Gemini API
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

def print_step(step_text):
    """Print a step message with Cyan color."""
    print(f"{Fore.CYAN}[*] {step_text}{Style.RESET_ALL}")

def print_success(step_text):
    """Print a success message with Green color."""
    print(f"{Fore.GREEN}[+] {step_text}{Style.RESET_ALL}")

def print_warning(step_text):
    """Print a warning message with Yellow color."""
    print(f"{Fore.YELLOW}[!] {step_text}{Style.RESET_ALL}")

def print_error(step_text):
    """Print an error message with Red color."""
    print(f"{Fore.RED}[X] {step_text}{Style.RESET_ALL}")

def generate_article_with_gemini(title, description="", max_retries=3):
    """
    Generate a blog article using Gemini API.
    
    Args:
        title (str): The title of the blog article
        description (str): Additional context or requirements
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        dict: Generated article content with metadata
    """
    
    prompt = f"""
You are a professional technical content writer specializing in programming and software development.

Create a comprehensive, well-structured blog article on the following topic:

**Title**: {title}

**Additional Context**: {description if description else "Cover the topic comprehensively for intermediate to advanced developers"}

**Requirements**:
1. Write a 1500-2000 word article in Markdown format
2. Include an engaging introduction that hooks the reader
3. Create 8-12 well-organized sections with clear headings (use ## for main sections, ### for subsections)
4. Provide practical code examples where relevant (use proper code blocks with language specification)
5. Include real-world use cases and best practices
6. Add tips, warnings, or important notes in callout format
7. End with a strong conclusion summarizing key takeaways
8. Write in a conversational yet professional tone
9. Ensure content is technically accurate and up-to-date
10. Make it SEO-friendly with natural keyword usage

**Format**: Return ONLY the article content in Markdown format, starting with the title as # heading.

Do NOT include any preamble, explanations, or meta-commentary. Start directly with the article.
"""

    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    for attempt in range(max_retries):
        try:
            print_step(f"Generating article for: '{title}' (Attempt {attempt + 1}/{max_retries})")
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=4096,
                )
            )
            
            content = response.text.strip()
            
            # Clean up the content
            content = content.replace("```markdown", "").replace("```", "").strip()
            
            # Ensure title is at the top if not present
            if not content.startswith("# "):
                content = f"# {title}\n\n" + content
            
            # Generate meta description
            meta_description = generate_meta_description(content)
            
            # Generate keywords
            keywords = generate_keywords(title, content)
            
            print_success(f"Successfully generated article: '{title}'")
            
            return {
                "title": title,
                "content": content,
                "meta_description": meta_description,
                "keywords": keywords,
                "word_count": len(content.split())
            }
            
        except Exception as e:
            print_error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print_warning(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print_error(f"Failed to generate article after {max_retries} attempts")
                return None

def generate_meta_description(content):
    """Generate SEO meta description from content."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"""Generate a concise, SEO-friendly meta description (150-160 characters) for this article. 
Return ONLY the description text, no quotes or extra formatting:

{content[:500]}..."""
        
        response = model.generate_content(prompt)
        description = response.text.strip().strip('"\'')
        return description[:160]  # Ensure it's within limit
    except:
        # Fallback: Use first sentence
        first_paragraph = content.split('\n\n')[1] if len(content.split('\n\n')) > 1 else content[:200]
        return first_paragraph[:157] + "..."

def generate_keywords(title, content):
    """Generate SEO keywords from title and content."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"""Generate 8-10 relevant SEO keywords for this article. Return as comma-separated list:

Title: {title}
Content: {content[:300]}..."""
        
        response = model.generate_content(prompt)
        keywords = response.text.strip()
        return keywords
    except:
        # Fallback: Use title words
        return ", ".join(title.lower().split())

def save_article_as_html(article_data, output_dir="blog"):
    """Save article as HTML file."""
    Path(output_dir).mkdir(exist_ok=True)
    
    filename = article_data['title'].lower().replace(' ', '-').replace('/', '-')
    filename = ''.join(c for c in filename if c.isalnum() or c == '-')
    filepath = Path(output_dir) / f"{filename}.html"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="description" content="{article_data['meta_description']}">
    <meta name="keywords" content="{article_data['keywords']}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>

<body>
    <markdown>
{article_data['content']}
    </markdown>
    <script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>
</body>

</html>"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print_success(f"Saved: {filepath}")
    return str(filepath)

def save_article_as_markdown(article_data, output_dir="blog"):
    """Save article as Markdown file."""
    Path(output_dir).mkdir(exist_ok=True)
    
    filename = article_data['title'].lower().replace(' ', '-').replace('/', '-')
    filename = ''.join(c for c in filename if c.isalnum() or c == '-')
    filepath = Path(output_dir) / f"{filename}.md"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article_data['content'])
    
    print_success(f"Saved: {filepath}")
    return str(filepath)

def generate_bulk_articles(articles_list, output_format="html", output_dir="blog"):
    """
    Generate multiple articles from a list of titles and descriptions.
    
    Args:
        articles_list (list): List of dicts with 'title' and optional 'description'
        output_format (str): 'html' or 'markdown'
        output_dir (str): Directory to save articles
    
    Returns:
        list: Generated article data
    """
    
    print_step(f"Starting bulk generation of {len(articles_list)} articles...")
    print_step(f"Output format: {output_format.upper()}")
    print_step(f"Output directory: {output_dir}")
    print()
    
    results = []
    
    for i, article_info in enumerate(articles_list, 1):
        print(f"\n{'='*80}")
        print(f"Article {i}/{len(articles_list)}")
        print(f"{'='*80}\n")
        
        title = article_info.get('title', '')
        description = article_info.get('description', '')
        
        if not title:
            print_warning(f"Skipping article {i}: No title provided")
            continue
        
        # Generate article
        article_data = generate_article_with_gemini(title, description)
        
        if article_data:
            # Save article
            if output_format.lower() == 'html':
                filepath = save_article_as_html(article_data, output_dir)
            else:
                filepath = save_article_as_markdown(article_data, output_dir)
            
            article_data['filepath'] = filepath
            results.append(article_data)
            
            # Add delay to respect API rate limits
            if i < len(articles_list):
                time.sleep(2)
        else:
            print_error(f"Failed to generate article: {title}")
    
    print(f"\n{'='*80}")
    print_success(f"Bulk generation complete! Generated {len(results)}/{len(articles_list)} articles")
    print(f"{'='*80}\n")
    
    # Save summary
    save_generation_summary(results, output_dir)
    
    return results

def save_generation_summary(results, output_dir):
    """Save a summary of generated articles."""
    summary_path = Path(output_dir) / "generation_summary.json"
    
    summary = {
        "total_articles": len(results),
        "generation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "articles": [
            {
                "title": r['title'],
                "filepath": r['filepath'],
                "word_count": r['word_count'],
                "meta_description": r['meta_description']
            }
            for r in results
        ]
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print_success(f"Generation summary saved: {summary_path}")

# Example usage with 10 programming topics
if __name__ == "__main__":
    
    # Define your 10 article topics here
    ARTICLE_TOPICS = [
        {
            "title": "Understanding Python Decorators: A Complete Guide",
            "description": "Explain decorators with practical examples, common patterns, and best practices"
        },
        {
            "title": "RESTful API Design Best Practices",
            "description": "Cover REST principles, HTTP methods, status codes, versioning, and security"
        },
        {
            "title": "Introduction to Docker for Developers",
            "description": "Docker basics, containers, images, Docker Compose, and common use cases"
        },
        {
            "title": "Git Branching Strategies for Teams",
            "description": "Git Flow, GitHub Flow, trunk-based development, and when to use each"
        },
        {
            "title": "JavaScript Async/Await: From Callbacks to Modern Async",
            "description": "Evolution from callbacks to Promises to async/await with examples"
        },
        {
            "title": "Database Indexing: When and How to Use Indexes",
            "description": "Index types, performance impact, when to add indexes, and common pitfalls"
        },
        {
            "title": "Building Scalable Microservices Architecture",
            "description": "Microservices patterns, communication, service discovery, and challenges"
        },
        {
            "title": "React Hooks: A Practical Deep Dive",
            "description": "useState, useEffect, custom hooks, and advanced patterns"
        },
        {
            "title": "SQL vs NoSQL: Choosing the Right Database",
            "description": "Compare relational and NoSQL databases, use cases, and decision criteria"
        },
        {
            "title": "Test-Driven Development (TDD) in Practice",
            "description": "TDD principles, writing testable code, common patterns, and benefits"
        }
    ]
    
    # Generate all articles
    results = generate_bulk_articles(
        articles_list=ARTICLE_TOPICS,
        output_format="html",  # or "markdown"
        output_dir="blog"
    )
    
    # Print final summary
    print("\n" + "="*80)
    print("GENERATION SUMMARY")
    print("="*80)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Words: {result['word_count']} | File: {result['filepath']}")
    print("="*80)
