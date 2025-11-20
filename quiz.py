import streamlit as st
import json
import random
from typing import Dict, List, Any

def load_questions_from_file(uploaded_file) -> List[Dict[str, Any]]:
    """Load questions from uploaded JSON file"""
    try:
        content = uploaded_file.read()
        questions = json.loads(content)
        return questions
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return []

def initialize_session_state():
    """Initialize session state variables"""
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'answered_questions' not in st.session_state:
        st.session_state.answered_questions = 0
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'shuffled_questions' not in st.session_state:
        st.session_state.shuffled_questions = []
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False

def start_quiz():
    """Start the quiz by shuffling questions"""
    if st.session_state.questions:
        st.session_state.shuffled_questions = st.session_state.questions.copy()
        random.shuffle(st.session_state.shuffled_questions)
        st.session_state.quiz_started = True
        st.session_state.current_question_index = 0
        st.session_state.answered_questions = 0
        st.session_state.show_result = False
        st.session_state.quiz_completed = False

def reset_quiz():
    """Reset the quiz to initial state"""
    st.session_state.quiz_started = False
    st.session_state.current_question_index = 0
    st.session_state.answered_questions = 0
    st.session_state.show_result = False
    st.session_state.shuffled_questions = []
    st.session_state.quiz_completed = False

def next_question():
    """Move to next question"""
    st.session_state.current_question_index += 1
    st.session_state.show_result = False

    # Check if all questions are answered
    if st.session_state.current_question_index >= len(st.session_state.shuffled_questions):
        st.session_state.quiz_completed = True

def display_question(question: Dict[str, Any]):
    """Display current question with options"""
    st.markdown("### Question")

    # Display question in both languages
    st.markdown(f"**English:** {question['question']}")
    st.markdown(f"**한국어:** {question['question_korean']}")

    # Create options for radio button
    options_display = []
    for i, (eng_opt, kor_opt) in enumerate(zip(question['options'], question['options_korean'])):
        options_display.append(f"{eng_opt} | {kor_opt}")

    # User selection
    selected_option = st.radio(
        "Select your answer:",
        options_display,
        key=f"question_{question['id']}_{st.session_state.current_question_index}"
    )

    return selected_option

def check_answer(selected_option: str, question: Dict[str, Any]):
    """Check if the selected answer is correct"""
    # Extract the letter from selected option (A, B, C, or D)
    selected_letter = selected_option.split('.')[0]
    correct_letter = question['correct_answer'].split('.')[0]

    return selected_letter == correct_letter

def display_result(is_correct: bool, question: Dict[str, Any], selected_option: str):
    """Display the result of the answer"""
    if is_correct:
        st.success("✅ Correct!")
    else:
        st.error("❌ Wrong!")
        st.markdown(f"**Correct Answer:** {question['correct_answer']} | {question['correct_answer_korean']}")

    # Show explanation
    st.info(f"**Explanation:** {question['explanation']}")

    st.session_state.answered_questions += 1

def main():
    st.set_page_config(
        page_title="My Quiz App",
        page_icon="🧠",
        layout="wide"
    )

    # Initialize session state
    initialize_session_state()

    # Header
    st.title("🧠 My Quiz App")
    st.markdown("---")

    # Reset button (only show when quiz is active and not completed)
    if st.session_state.quiz_started and st.session_state.shuffled_questions and not st.session_state.quiz_completed:
        if st.button("🔄 Reset Quiz", type="secondary"):
            reset_quiz()
            st.rerun()

    # File upload section
    if not st.session_state.quiz_started:
        st.subheader("📁 Upload Question Pool")
        uploaded_file = st.file_uploader(
            "Choose a JSON file containing questions",
            type=['json'],
            help="Upload a JSON file with questions in the specified format"
        )

        if uploaded_file is not None:
            questions = load_questions_from_file(uploaded_file)
            if questions:
                st.session_state.questions = questions
                st.success(f"✅ Successfully loaded {len(questions)} questions!")

                # Show sample question format
                with st.expander("📋 Preview Questions"):
                    for i, q in enumerate(questions[:2]):  # Show first 2 questions
                        st.markdown(f"**Question {i+1}:** {q['question'][:100]}...")

                # Start quiz button
                if st.button("🚀 Start Quiz", type="primary"):
                    start_quiz()
                    st.rerun()

    # Quiz completed section
    elif st.session_state.quiz_completed:
        st.balloons()
        st.success("🎉 Quiz Completed!")

        st.markdown("---")
        st.info("📊 You have completed the quiz!")

        # Restart options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Quiz", type="primary"):
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("📁 Upload New Questions", type="secondary"):
                reset_quiz()
                st.session_state.questions = []
                st.rerun()

    # Quiz in progress section
    elif st.session_state.quiz_started and st.session_state.shuffled_questions:
        # Current question
        current_q = st.session_state.shuffled_questions[st.session_state.current_question_index]

        # Display question
        selected_option = display_question(current_q)

        # Answer submission
        col1, col2 = st.columns([1, 4])

        with col1:
            if st.button("Submit Answer", type="primary") and not st.session_state.show_result:
                if selected_option:
                    is_correct = check_answer(selected_option, current_q)
                    st.session_state.show_result = True
                    st.session_state.current_result = {
                        'is_correct': is_correct,
                        'question': current_q,
                        'selected': selected_option
                    }
                    st.rerun()

        # Show result if answer was submitted
        if st.session_state.show_result and hasattr(st.session_state, 'current_result'):
            result = st.session_state.current_result
            display_result(result['is_correct'], result['question'], result['selected'])

            # Next question button or finish quiz
            if st.session_state.current_question_index < len(st.session_state.shuffled_questions) - 1:
                if st.button("➡️ Next Question", type="secondary"):
                    next_question()
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", type="primary"):
                    next_question()  # This will set quiz_completed to True
                    st.rerun()

    # Instructions
    if not st.session_state.quiz_started:
        st.markdown("---")
        st.subheader("📖 Instructions")
        st.markdown("""
        1. **Upload** a JSON file containing your question pool
        2. **Start** the quiz - all questions will be shown in random order
        3. **Answer** each question by selecting an option
        4. **View** immediate feedback with explanations
        5. **Navigate** through all questions one by one
        6. **Complete** all questions to finish the quiz
        7. **Reset** anytime to start over with the same questions

        **JSON Format Example:**
        ```json
        [
          {
            "id": 1,
            "question": "English question text",
            "question_korean": "Korean question text",
            "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
            "options_korean": ["A. 선택지 1", "B. 선택지 2", "C. 선택지 3", "D. 선택지 4"],
            "correct_answer": "A. Option 1",
            "correct_answer_korean": "A. 선택지 1",
            "explanation": "Explanation text"
          }
        ]
        ```
        """)

if __name__ == "__main__":
    main()
