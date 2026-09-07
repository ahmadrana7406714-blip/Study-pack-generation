"""
workflow.py
Multi-stage AI workflow for a personalized study-pack generator.

Stages:
1. Planning
2. Content Generation
3. Assessment
4. Review
5. Refinement

The workflow keeps a shared context dictionary and passes outputs from
one stage to the next. It uses an OpenAI-compatible API endpoint so it
can work with providers such as Groq by changing environment variables.
"""

import os
from typing import Dict, Any

from openai import OpenAI


def get_client() -> OpenAI:
    """Create an OpenAI-compatible client from Streamlit secrets or env vars."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("GROQ_BASE_URL")

    if not api_key:
        raise ValueError(
            "API key not found. Add OPENAI_API_KEY or GROQ_API_KEY "
            "to your Streamlit secrets/environment variables."
        )

    # Default to OpenAI endpoint if no custom endpoint is supplied.
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)

    return OpenAI(api_key=api_key)


def call_ai(prompt: str, model: str, temperature: float = 0.4) -> str:
    """Make one AI call and return plain text."""
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert educational AI. Create accurate, "
                    "clear, age-appropriate, practical learning material. "
                    "Follow the requested format exactly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    text = response.choices[0].message.content
    if not text:
        raise RuntimeError("The AI returned an empty response.")

    return text.strip()


def planning_stage(context: Dict[str, Any], model: str) -> str:
    prompt = f"""
Create a personalized study plan.

Student/topic information:
- Topic: {context['topic']}
- Skill level: {context['level']}
- Study duration: {context['duration']}
- Learning goal: {context['goal']}

Return:
1. Learning objectives
2. Week-by-week or session-by-session roadmap
3. Topics in logical order
4. Estimated effort for each section
5. A final mini-project or practical goal

Keep the plan realistic for the stated duration and skill level.
"""
    return call_ai(prompt, model)


def content_generation_stage(context: Dict[str, Any], model: str) -> str:
    prompt = f"""
Generate the core study content using the student's information and plan below.

Student:
- Topic: {context['topic']}
- Level: {context['level']}
- Duration: {context['duration']}
- Goal: {context['goal']}

PLAN:
{context['plan']}

For each major topic, provide:
- Simple explanation
- Important concepts
- Examples
- Common mistakes
- A short practice activity

Do not add unrelated topics. Keep the difficulty aligned with the student's level.
"""
    return call_ai(prompt, model)


def assessment_stage(context: Dict[str, Any], model: str) -> str:
    prompt = f"""
Create an assessment based strictly on the study plan and generated content.

Topic: {context['topic']}
Level: {context['level']}

PLAN:
{context['plan']}

CONTENT:
{context['content']}

Create:
- 8 multiple-choice questions with 4 options each
- Answer key
- 5 short-answer questions
- 3 practical/application questions

Questions must test concepts actually covered in the content.
Avoid duplicate questions.
"""
    return call_ai(prompt, model)


def review_stage(context: Dict[str, Any], model: str) -> str:
    prompt = f"""
Act as a strict educational quality reviewer.

Review the following study pack components.

PLAN:
{context['plan']}

CONTENT:
{context['content']}

ASSESSMENT:
{context['assessment']}

Check:
1. Accuracy and internal consistency
2. Alignment with the plan
3. Suitability for the student's level
4. Coverage of important topics
5. Assessment quality and answer correctness
6. Repetition or irrelevant material
7. Clarity and organization

Return:
- REVIEW STATUS: PASS or NEEDS_REFINEMENT
- Strengths
- Specific issues found
- Exact recommendations for improvement

Do not rewrite the whole study pack in this stage.
"""
    return call_ai(prompt, model, temperature=0.2)


def refinement_stage(context: Dict[str, Any], model: str) -> str:
    prompt = f"""
Create the final personalized study pack by improving the draft according
to the review feedback.

STUDENT:
- Topic: {context['topic']}
- Level: {context['level']}
- Duration: {context['duration']}
- Goal: {context['goal']}

PLAN:
{context['plan']}

CONTENT:
{context['content']}

ASSESSMENT:
{context['assessment']}

REVIEW:
{context['review']}

Apply the review recommendations. Correct errors, remove unnecessary
repetition, and preserve useful material.

Return a polished final study pack with these sections:
# Personalized Study Plan
# Learning Notes
# Key Points
# Practice Activities
# Assessment
# Answer Key
# Final Revision Checklist
# Mini Project

Make the final pack practical and easy to follow.
"""
    return call_ai(prompt, model, temperature=0.3)


def generate_study_pack(topic: str, level: str, duration: str, goal: str,
                        model: str = "llama-3.3-70b-versatile") -> Dict[str, Any]:
    """Run all workflow stages with shared context."""
    context: Dict[str, Any] = {
        "topic": topic.strip(),
        "level": level,
        "duration": duration.strip(),
        "goal": goal.strip(),
    }

    # Stage 1: Planning
    context["plan"] = planning_stage(context, model)

    # Stage 2: Content
    context["content"] = content_generation_stage(context, model)

    # Stage 3: Assessment
    context["assessment"] = assessment_stage(context, model)

    # Stage 4: Review
    context["review"] = review_stage(context, model)

    # Stage 5: Refinement
    context["final_pack"] = refinement_stage(context, model)

    return context
