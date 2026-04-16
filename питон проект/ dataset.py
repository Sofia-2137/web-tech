import pandas as pd
import json

# Загрузка вопросов
questions_df = pd.read_csv('questions.csv')

# Загрузка рекомендаций
recommendations_df = pd.read_csv('recommendations.csv')
recommendations_dict = recommendations_df.set_index('category').to_dict('index')

# Категории
categories = ['anxiety', 'fatigue', 'lack_of_interest', 'overwhelm', 'physiological']

# Функция подсчета результатов
def calculate_results(answers):
    """
    answers: список словарей [{'question_id': 1, 'answer': 'yes'}, ...]
    """
    scores = {cat: 0 for cat in categories}
    
    for answer in answers:
        q_id = answer['question_id']
        user_answer = answer['answer']  # 'yes', 'no', 'sometimes'
        
        # Получаем вопрос из датафрейма
        question = questions_df[questions_df['id'] == q_id].iloc[0]
        
        # Определяем вес ответа
        if user_answer == 'yes':
            points = question['weight']
        elif user_answer == 'sometimes':
            points = question['weight'] * 0.5
        else:  # 'no'
            points = 0
        
        # Добавляем баллы в каждую категорию
        for cat in categories:
            if question[f'category_{cat}'] == 1:
                scores[cat] += points
    
    # Находим основную причину
    primary_cause = max(scores, key=scores.get)
    
    # Получаем рекомендацию
    recommendation = recommendations_dict[primary_cause]
    
    return {
        'scores': scores,
        'primary_cause': primary_cause,
        'primary_title': recommendation['title'],
        'recommendation': recommendation['recommendation_text'],
        'action_items': recommendation['action_items'].split(';')
    }

# Пример использования
answers = [
    {'question_id': 1, 'answer': 'yes'},
    {'question_id': 2, 'answer': 'yes'},
    # ... остальные ответы
]

result = calculate_results(answers)
print(json.dumps(result, ensure_ascii=False, indent=2))