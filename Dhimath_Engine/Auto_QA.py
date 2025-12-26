import re
import pandas as pd

from .Get_Answers import manual_input

def generate_questions(global_session_variables):
    question = f"""Role: Document Analyst responsibile for generating questions based on the documents available.
        Task: Generate {global_session_variables["num_questions"]} insightful technical or subjective questions.
        Requirement: Carefully examine as many pages to create questions that are specific, detailed, and demonstrate a deep understanding of the content. No repetitive topics must be taken while generation. Strictly Avoid generic questions, any genric questions genrated will be strongly discouraged. The questions must be highly specific to the document provided.
        Instructions: Search as many pages of the set of documents. Each question should be formatted in a numbered list (1., 2., etc.) and any extra newline characters before the first question must be removed, the output must not be generated without the removal of newline characters. Ensure the questions are excellent and reflective of a human-level comprehension.
        """
    global_session_variables["question"] = question
    answer = manual_input(global_session_variables)
    global_session_variables["answer"] = answer
    answer_text = answer[0]
    questions = answer_text.split("\n")
    cleaned_questions = [re.sub(r'^\d+\.\s*', '', q) for q in questions]
    num_answers = max(global_session_variables["num_questions"], len(cleaned_questions))
    questions_df = pd.DataFrame({
        'Question': cleaned_questions[0:num_answers]
    })
    questions_df['ID'] = range(1, len(questions_df) + 1)
    questions_df['Edited_Questions'] = questions_df['Question']
    questions_df['Answers'] = ""
    questions_df['Edited_Answers'] = ""

    global_session_variables["auto_qa_df"] = questions_df

    return questions_df

def generate_answers(global_session_variables):
    answers = []
    execution_times = []
    metadata_list = []
    answers_df = global_session_variables["auto_qa_df"]
    for idx, row in answers_df.iterrows():
        question = row['Edited_Questions']
        global_session_variables["question"] = question
        answer, _, _, qa_exec_time, metadata = manual_input(global_session_variables)
        answers.append(str(answer))
        execution_times.append(qa_exec_time)
        metadata_list.append(metadata)

    answers_df['Answers'] = answers
    answers_df['Exec_Time'] = execution_times
    answers_df['Metadata'] = metadata_list

    return answers_df