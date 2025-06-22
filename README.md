
# 🎯 Contexto Solver

An automated solver for the popular word-guessing game [contexto.me](https://contexto.me) using AI-powered language models.

## 📖 Introduction

Contexto Solver is a Python script that leverages the power of AI language models to automatically solve the daily Contexto puzzle. By using semantic understanding and intelligent word selection, this tool can efficiently navigate through the game's word space to find the target word.

## 🎮 What is Contexto?

[Contexto](https://contexto.me) is an engaging word-guessing game where players attempt to discover a secret word by making guesses. The game provides feedback on how semantically similar each guess is to the target word:

- **Lower numbers** (1-100) indicate very close semantic similarity
- **Medium numbers** (100-500) show moderate similarity
- **Higher numbers** (500+) suggest distant semantic relationships

The objective is to find the secret word in as few guesses as possible by using the numerical feedback to guide your next attempts.

## 🤖 How It Works

This solver utilizes the OpenAI API to:
1. Analyze the semantic feedback from previous guesses
2. Generate contextually relevant word suggestions
3. Strategically narrow down the possibilities
4. Converge on the target word efficiently

The AI model understands the relationships between words and can make intelligent predictions based on the game's feedback patterns.

## 🚀 Different LLMs for Enhanced Performance

While the default implementation uses OpenAI's models, the solver architecture is designed to be flexible. Different Large Language Models (LLMs) could potentially improve solving efficiency:

- **GPT-4**: Better semantic understanding and reasoning capabilities
- **Claude**: Strong contextual awareness and systematic thinking
- **Specialized models**: Fine-tuned models could potentially achieve even better performance

## 📋 Requirements

- Python 3.7 or higher
- OpenAI API key (obtain from [OpenAI Platform](https://platform.openai.com))
- Internet connection for API calls and game interaction
- Required Python packages (see Installation section)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/contexto_solver.git
   cd contexto_solver
