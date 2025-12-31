"""
LLM Provider abstraction layer
Supports multiple LLM providers: Hugging Face, OpenAI, Anthropic
"""
from typing import Dict, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)


class LLMProvider:
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize LLM provider
        
        Args:
            config: Provider configuration
        """
        self.config = config
        self.provider_type = config.get('provider')
    
    def generate(self, prompt: str) -> str:
        """
        Generate text from prompt
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        raise NotImplementedError("Subclasses must implement generate()")


class HuggingFaceProvider(LLMProvider):
    """Hugging Face transformers provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = None
        self.tokenizer = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the Hugging Face model and tokenizer"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            model_name = self.config.get('model')
            device = self.config.get('device', 'cpu')
            load_in_8bit = self.config.get('load_in_8bit', False)
            
            logger.info(f"Loading Hugging Face model: {model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model with appropriate settings
            if load_in_8bit and device == 'cuda':
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    load_in_8bit=True,
                    device_map="auto",
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
                )
                self.model.to(device)
            
            logger.info(f"Model loaded successfully on {device}")
            
        except ImportError as e:
            logger.warning(f"Transformers library not installed: {e}")
            logger.warning("Using mock provider for demo - install transformers for full functionality")
            self.model = None
            self.tokenizer = None
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face model: {e}")
            logger.warning("Using mock provider for demo")
            self.model = None
            self.tokenizer = None
    
    def generate(self, prompt: str) -> str:
        """Generate SQL query from prompt"""
        # If model not loaded (demo mode), return a simple query
        if self.model is None or self.tokenizer is None:
            logger.warning("Model not loaded, using fallback SQL generation")
            return self._fallback_generate(prompt)
        
        try:
            import torch
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
            
            if self.config.get('device') == 'cuda':
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=self.config.get('max_length', 512),
                    temperature=self.config.get('temperature', 0.1),
                    top_p=self.config.get('top_p', 0.95),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode output
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract SQL query from generated text
            sql_query = self._extract_sql(generated_text, prompt)
            
            return sql_query
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._fallback_generate(prompt)
    
    def _extract_sql(self, generated_text: str, prompt: str) -> str:
        """Extract SQL query from generated text"""
        # Remove the prompt from generated text
        if prompt in generated_text:
            sql = generated_text.replace(prompt, "").strip()
        else:
            sql = generated_text.strip()
        
        # Clean up common artifacts
        sql = sql.replace("```sql", "").replace("```", "").strip()
        
        # Extract first SQL statement
        if "SELECT" in sql.upper():
            start_idx = sql.upper().find("SELECT")
            sql = sql[start_idx:]
        
        # Remove trailing explanations
        lines = sql.split('\n')
        sql_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith('--'):
                sql_lines.append(line)
            if ';' in line:
                break
        
        sql = '\n'.join(sql_lines).strip()
        
        return sql
    
    def _fallback_generate(self, prompt: str) -> str:
        """Fallback SQL generation for demo purposes"""
        question_lower = prompt.lower()
        
        # Simple pattern matching for common queries
        if "all employees" in question_lower or "show employees" in question_lower:
            return "SELECT * FROM employees"
        elif "all products" in question_lower or "show products" in question_lower:
            return "SELECT * FROM products"
        elif "all customers" in question_lower or "show customers" in question_lower:
            return "SELECT * FROM customers"
        elif "count" in question_lower and "employees" in question_lower:
            if "department" in question_lower:
                return "SELECT department, COUNT(*) as count FROM employees GROUP BY department"
            return "SELECT COUNT(*) as total FROM employees"
        elif "salary" in question_lower and ">" in question_lower:
            # Extract number
            import re
            numbers = re.findall(r'\d+', question_lower)
            if numbers:
                return f"SELECT * FROM employees WHERE salary > {numbers[0]}"
        elif "average" in question_lower or "avg" in question_lower:
            if "salary" in question_lower:
                return "SELECT AVG(salary) as average_salary FROM employees"
            elif "price" in question_lower:
                return "SELECT AVG(price) as average_price FROM products"
        elif "top" in question_lower or "highest" in question_lower:
            import re
            numbers = re.findall(r'\d+', question_lower)
            limit = numbers[0] if numbers else "10"
            if "salary" in question_lower:
                return f"SELECT * FROM employees ORDER BY salary DESC LIMIT {limit}"
            elif "price" in question_lower:
                return f"SELECT * FROM products ORDER BY price DESC LIMIT {limit}"
        
        # Default fallback
        return "SELECT * FROM employees LIMIT 10"


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            
            api_key = self.config.get('api_key')
            if not api_key:
                raise ValueError("OpenAI API key not provided")
            
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized")
            
        except ImportError as e:
            logger.warning(f"OpenAI library not installed: {e}")
            logger.warning("Install 'openai' package to use OpenAI provider")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def generate(self, prompt: str) -> str:
        """Generate SQL query using OpenAI"""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            from .prompts import OPENAI_SYSTEM_PROMPT
            
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'gpt-4'),
                messages=[
                    {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.get('temperature', 0.1),
                max_tokens=self.config.get('max_tokens', 500),
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up formatting
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return sql_query
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Anthropic client"""
        try:
            from anthropic import Anthropic
            
            api_key = self.config.get('api_key')
            if not api_key:
                raise ValueError("Anthropic API key not provided")
            
            self.client = Anthropic(api_key=api_key)
            logger.info("Anthropic client initialized")
            
        except ImportError as e:
            logger.warning(f"Anthropic library not installed: {e}")
            logger.warning("Install 'anthropic' package to use Anthropic provider")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            self.client = None
    
    def generate(self, prompt: str) -> str:
        """Generate SQL query using Anthropic Claude"""
        if not self.client:
            raise RuntimeError("Anthropic client not initialized")
        
        try:
            response = self.client.messages.create(
                model=self.config.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=self.config.get('max_tokens', 500),
                temperature=self.config.get('temperature', 0.1),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            sql_query = response.content[0].text.strip()
            
            # Clean up formatting
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return sql_query
            
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise


def create_llm_provider(config: Dict[str, Any]) -> LLMProvider:
    """
    Factory function to create appropriate LLM provider
    
    Args:
        config: Provider configuration
        
    Returns:
        LLM provider instance
    """
    provider_type = config.get('provider')
    
    if provider_type == 'huggingface':
        return HuggingFaceProvider(config)
    elif provider_type == 'openai':
        return OpenAIProvider(config)
    elif provider_type == 'anthropic':
        return AnthropicProvider(config)
    else:
        raise ValueError(f"Unsupported provider: {provider_type}")
