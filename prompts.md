# AI Study Pack Generator — Prompt Design

This file documents the prompts used by workflow.py.

## 1. Planning Prompt
Goal: Convert user requirements into a realistic personalized roadmap.
Inputs: topic, skill level, duration, learning goal.
Output: objectives, ordered topics, schedule, effort estimates, mini-project.

## 2. Content Generation Prompt
Goal: Turn the approved plan into learning material.
Context passed: original student information + planning output.
Output: explanations, concepts, examples, mistakes, practice activities.

## 3. Assessment Prompt
Goal: Test the content that was actually generated.
Context passed: plan + content.
Output: MCQs, answer key, short-answer questions, practical questions.

## 4. Review Prompt
Goal: Quality-control the plan, content, and assessment.
Checks: accuracy, alignment, difficulty, coverage, repetition, assessment quality.
Output: PASS/NEEDS_REFINEMENT plus actionable feedback.

## 5. Refinement Prompt
Goal: Produce the final study pack.
Context passed: original inputs + plan + content + assessment + review.
Output: polished final study pack with revision checklist and mini-project.

## Context-passing design

context = {
    "topic": ...,
    "level": ...,
    "duration": ...,
    "goal": ...,
    "plan": ...,
    "content": ...,
    "assessment": ...,
    "review": ...,
    "final_pack": ...
}

Each stage reads the relevant earlier outputs instead of starting from scratch.
