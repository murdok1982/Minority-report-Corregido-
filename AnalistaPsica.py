import os
import sqlite3
from openai import OpenAI
from typing import Optional, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client with environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration
MODEL_NAME = os.getenv('GPT_MODEL', 'gpt-4')
DOWNLOAD_DB_NAME = "downloaded_comments.db"

class PsychologicalAnalyzer:
    """Analyzes user comments for behavioral patterns using GPT."""
    
    def __init__(self, model_name: str = MODEL_NAME):
        """Initialize the analyzer.
        
        Args:
            model_name: The GPT model to use for analysis
        """
        self.model_name = model_name
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it as environment variable."
            )
    
    def analyze_comment(self, comment: str, user_name: str, user_id: str) -> Optional[Dict]:
        """Analyze a comment for psychological patterns.
        
        Args:
            comment: The comment text to analyze
            user_name: Username of the commenter
            user_id: User ID
            
        Returns:
            Dictionary with analysis results or None if error
        """
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a psychological behavior analyst. "
                            "Analyze comments for patterns of violent, dangerous, "
                            "or concerning behavior. Provide objective assessment "
                            "focusing on: threat level (low/medium/high/critical), "
                            "behavioral indicators, recommended actions, and confidence level."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Comment: {comment}\n"
                            f"User: {user_name}\n"
                            f"User ID: {user_id}\n\n"
                            "Provide a structured psychological evaluation."
                        )
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'user_name': user_name,
                'user_id': user_id,
                'comment': comment,
                'analysis': analysis,
                'model_used': self.model_name,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            logger.error(f"Error analyzing comment for user {user_name}: {e}")
            return None
    
    def process_all_comments(self, db_path: str = DOWNLOAD_DB_NAME) -> list:
        """Process all comments from the database.
        
        Args:
            db_path: Path to SQLite database
            
        Returns:
            List of analysis results
        """
        results = []
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query all comments
            cursor.execute(
                "SELECT user_name, user_id, post_id, comment "
                "FROM comentarios_descargados"
            )
            comments = cursor.fetchall()
            
            logger.info(f"Processing {len(comments)} comments...")
            
            for user_name, user_id, post_id, comment in comments:
                logger.info(f"Analyzing comment from {user_name} ({user_id})...")
                
                analysis_result = self.analyze_comment(comment, user_name, user_id)
                
                if analysis_result:
                    analysis_result['post_id'] = post_id
                    results.append(analysis_result)
                    
                    # Log the analysis
                    logger.info(f"Analysis completed:\n{analysis_result['analysis']}\n")
                    
                    # Store result back to database
                    self._store_analysis(cursor, analysis_result)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Processing complete. {len(results)} comments analyzed.")
            return results
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return results
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return results
    
    def _store_analysis(self, cursor, result: Dict):
        """Store analysis results in database.
        
        Args:
            cursor: Database cursor
            result: Analysis result dictionary
        """
        try:
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS psychological_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,
                    user_id TEXT,
                    post_id TEXT,
                    comment TEXT,
                    analysis TEXT,
                    model_used TEXT,
                    tokens_used INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert analysis
            cursor.execute("""
                INSERT INTO psychological_analysis 
                (user_name, user_id, post_id, comment, analysis, model_used, tokens_used)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                result['user_name'],
                result['user_id'],
                result.get('post_id', 'N/A'),
                result['comment'],
                result['analysis'],
                result['model_used'],
                result['tokens_used']
            ))
            
        except sqlite3.Error as e:
            logger.error(f"Error storing analysis: {e}")


def main():
    """Main function to run psychological analysis."""
    print("="*50)
    print("Psychological Behavior Analyzer")
    print("="*50)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\nERROR: OPENAI_API_KEY environment variable not set.")
        print("Please set it using:")
        print("  export OPENAI_API_KEY='your-api-key-here'  # Linux/Mac")
        print("  set OPENAI_API_KEY=your-api-key-here       # Windows")
        return
    
    # Initialize analyzer
    try:
        analyzer = PsychologicalAnalyzer()
        
        # Process all comments
        results = analyzer.process_all_comments()
        
        print(f"\nAnalysis complete!")
        print(f"Total comments analyzed: {len(results)}")
        print(f"Results stored in database: {DOWNLOAD_DB_NAME}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
