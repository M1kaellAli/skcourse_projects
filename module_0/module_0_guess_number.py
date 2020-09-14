#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np  # для использования random и mean


# In[2]:


def next_prediction(low_bound, high_bound):
    """Функция для предсказания следующего варианта в функции 'game_core_log2'"""
    return int(low_bound + (high_bound-low_bound)/2)


# In[3]:


def game_core_log2(number):
    """Функция для нахождения числа за log2(100) операций:
    делим пополам интервала возможного ответа на каждой итерации"""
    
    # инициализируем границы интервала возможного ответа
    low_bound = 0
    high_bound = 101
    
    count = 0 # счетчик попыток
    predict = next_prediction(low_bound, high_bound)
    while number != predict:
        count+=1
        if number > predict: 
            low_bound = predict
        elif number < predict:
            high_bound = predict        
        predict = next_prediction(low_bound, high_bound)
        
    return(count) # число найдено, выходим


# In[4]:


# функции с другими вариантами поиска числа, будем их использовать для сравнения методов
def game_core_v1(number):
    '''Просто угадываем на random, никак не используя информацию о больше или меньше.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    while True:
        count+=1
        predict = np.random.randint(1,101) # предполагаемое число
        if number == predict: 
            return(count) # выход из цикла, если угадали
        
        
def game_core_v2(number):
    '''Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того,
       больше оно или меньше нужного. Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    predict = np.random.randint(1,101)
    while number != predict:
        count+=1
        if number > predict: 
            predict += 1
        elif number < predict: 
            predict -= 1
    return(count) # выход из цикла, если угадали


# In[5]:


def compare_methods(seed_val=1, tries_count=1000):
    """Функция сравнения разных вариантов поиска числа:
    1. По среднему количеству попыток; 2. По количеству раз когда метод был лучшим.
    Методы: log2(N), случайный выбор(random) , инкрементация/декрементация в зависимости от сравненя.
    Параметр - число для инициализации генератора случайных чисел."""
    
    # словари для счетчика попыток каждого метода, среднего количества попыток и счетчика лучшего метода в конкретном случае
    counter_dict = {}
    scores_dict = {}
    better_vars_dict = {}
    
    # словарь методов
    funcs_dict = {"log2":game_core_log2, "random":game_core_v1, "inc-dec":game_core_v2}
    
    # инициализация словарей
    for func in funcs_dict.keys():
        counter_dict[func] =[]
        better_vars_dict[func] = 0
        
    np.random.seed(seed_val)  # фиксируем RANDOM SEED, чтобы эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(tries_count))
    for ii, number in enumerate(random_array):
        # запускаем каждый метод и находим какой быстрей в этот раз
        func_name = ''
        current_min = 10000
        for func in funcs_dict.keys():
            count_var = funcs_dict[func](number)
            counter_dict[func].append(count_var)
            if (current_min > count_var):
                current_min = count_var
                func_name = func
            
        # увеличиваем счетчик лучшего метода
        better_vars_dict[func_name] += 1
     
    # выводим информацию по каждому
    for func in funcs_dict.keys():
        scores_dict[func] = int(np.mean(counter_dict[func]))
        print(f"""Алгоритм '{func}' угадывает число в среднем за {scores_dict[func]} попыток(ки)
            и был лучше в '{better_vars_dict[func]}' случаях из {tries_count} (т.е в {100*better_vars_dict[func]/tries_count}%).""")
        
    print()
    
    # вычисляем и выводим лучший по среднему количеству попыток 
    min_ave_val = min(scores_dict.values())
    min_ave_keys = [key for key, value in scores_dict.items() if value==min_ave_val]
    print(f"""Лучший алгоритм(ы) по среднему числу попыток ({min_ave_val}): {min_ave_keys}""")
        
    # вычисляем и выводим лучший по количеству побед 
    max_best_val = max(better_vars_dict.values())
    max_best_keys = [key for key, value in better_vars_dict.items() if value==max_best_val]
    print(f"""Лучший алгоритм(ы) по количеству раз когда был лучшим ({max_best_val}): {max_best_keys}""")    


# In[6]:


# запускаем сравнение с параметрами по умолчанию
compare_methods()


# In[7]:


# запускаем сравнение со своимим параметрами
compare_methods(33, 2000)


# In[ ]:




