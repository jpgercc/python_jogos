import datetime
from dateutil.relativedelta import relativedelta


def calculate_age(birth_date):
    """Calcula idade precisa usando relativedelta para considerar anos bissextos"""
    today = datetime.datetime.now()
    age_delta = relativedelta(today, birth_date)
    
    # Cálculo mais preciso dos dias restantes
    temp_date = birth_date + relativedelta(years=age_delta.years, months=age_delta.months)
    remaining_days = (today - temp_date).days
    
    return age_delta.years, age_delta.months, remaining_days


def get_base_life_expectancy(age, gender, country="Brazil"):
    """Retorna expectativa de vida base mais realista baseada em dados demográficos"""
    # Dados baseados em estatísticas do IBGE e OMS (aproximados)
    life_expectancy_data = {
        "Brazil": {
            "male": 73.1,
            "female": 79.9
        },
        "World": {
            "male": 70.8,
            "female": 75.9
        }
    }
    
    base_country = life_expectancy_data.get(country, life_expectancy_data["World"])
    base_expectancy = base_country.get(gender, 
                                     (base_country["male"] + base_country["female"]) / 2)
    
    return base_expectancy


def calculate_health_score(health_factors):
    """Calcula um score de saúde mais sofisticado"""
    score = 0
    
    # Fatores de risco (negativos)
    if health_factors["smoking"]:
        if health_factors["smoking_intensity"] == "heavy":  # >20 cigarros/dia
            score -= 12
        elif health_factors["smoking_intensity"] == "moderate":  # 10-20 cigarros/dia
            score -= 8
        else:  # <10 cigarros/dia
            score -= 5
            
    if health_factors["alcohol"] == "heavy":  # >2 drinks/dia
        score -= 6
    elif health_factors["alcohol"] == "moderate":  # 1-2 drinks/dia
        score += 1  # Benefício moderado do álcool
        
    if health_factors["obesity"]:
        bmi_category = health_factors.get("bmi_category", "moderate")
        if bmi_category == "severe":  # BMI > 35
            score -= 8
        elif bmi_category == "moderate":  # BMI 30-35
            score -= 5
        else:  # BMI 25-30 (sobrepeso)
            score -= 2
            
    if health_factors["diabetes"]:
        score -= 6
    if health_factors["hypertension"]:
        score -= 4
    if health_factors["heart_disease"]:
        score -= 10
        
    # Fatores positivos
    if health_factors["healthy_diet"]:
        diet_quality = health_factors.get("diet_quality", "good")
        if diet_quality == "excellent":  # Dieta mediterrânea, etc.
            score += 5
        elif diet_quality == "good":
            score += 3
        else:
            score += 1
            
    if health_factors["regular_exercise"]:
        exercise_intensity = health_factors.get("exercise_intensity", "moderate")
        if exercise_intensity == "high":  # >5x/semana, intenso
            score += 6
        elif exercise_intensity == "moderate":  # 3-5x/semana
            score += 4
        else:  # 1-2x/semana
            score += 2
            
    if health_factors["good_sleep"]:
        score += 2
    if health_factors["stress_management"]:
        score += 3
    if health_factors["social_connections"]:
        score += 2
    if health_factors["regular_checkups"]:
        score += 1
        
    # Fatores genéticos/familiares
    family_longevity = health_factors.get("family_longevity", "average")
    if family_longevity == "high":  # Pais/avós viveram >85 anos
        score += 4
    elif family_longevity == "low":  # Histórico de morte precoce
        score -= 3
        
    return score


def calculate_medical_advances_bonus(current_age, remaining_years):
    """Calcula o bônus de anos baseado nos avanços médicos esperados"""
    current_year = datetime.datetime.now().year
    
    # Estimativas conservadoras baseadas em tendências históricas e pesquisas atuais
    advances_timeline = {
        # Próximos 10 anos (2025-2035)
        2035: {
            "longevity_gain": 2.5,  # Terapias genéticas, medicina personalizada
            "description": "Medicina personalizada e terapias genéticas"
        },
        # Próximos 20 anos (2025-2045) 
        2045: {
            "longevity_gain": 5.0,  # Regeneração celular, órgãos artificiais
            "description": "Regeneração celular e órgãos bioengenheirados"
        },
        # Próximos 30 anos (2025-2055)
        2055: {
            "longevity_gain": 8.0,  # Nanotecnologia médica, reversão do envelhecimento
            "description": "Nanotecnologia médica e reversão parcial do envelhecimento"
        },
        # Próximos 40+ anos (2025-2065+)
        2065: {
            "longevity_gain": 12.0,  # Avanços revolucionários em longevidade
            "description": "Tecnologias disruptivas de extensão da vida"
        }
    }
    
    total_bonus = 0
    applied_advances = []
    estimated_death_year = current_year + remaining_years
    
    # Para pessoas mais jovens, considerar mais avanços futuros
    age_factor = max(0.3, 1 - (current_age / 100))  # Jovens se beneficiam mais
    
    for milestone_year, data in advances_timeline.items():
        if estimated_death_year >= milestone_year:
            # Aplicar bônus proporcional baseado na idade e na proximidade do avanço
            years_to_milestone = max(0, milestone_year - current_year)
            proximity_factor = max(0.5, 1 - (years_to_milestone / 50))  # Mais próximo = mais provável
            
            advance_bonus = data["longevity_gain"] * age_factor * proximity_factor
            total_bonus += advance_bonus
            applied_advances.append({
                "year": milestone_year,
                "bonus": advance_bonus,
                "description": data["description"]
            })
    
    # Limitar o bônus máximo para ser realista
    max_bonus = min(20, current_age * 0.3)  # Máximo 20 anos ou 30% da idade atual
    total_bonus = min(total_bonus, max_bonus)
    
    return total_bonus, applied_advances


def estimate_life_expectancy(age, gender, health_factors, country="Brazil"):
    """Estimativa mais precisa baseada em múltiplos fatores incluindo avanços médicos"""
    base_life_expectancy = get_base_life_expectancy(age, gender, country)
    
    # Ajuste baseado no score de saúde
    health_adjustment = calculate_health_score(health_factors)
    
    # Ajuste por idade atual (pessoas que já viveram mais têm expectativa ligeiramente maior)
    if age > 65:
        age_bonus = min(2, (age - 65) * 0.1)  # Máximo 2 anos de bônus
        base_life_expectancy += age_bonus
    
    preliminary_life_expectancy = base_life_expectancy + health_adjustment
    preliminary_remaining_years = max(0, preliminary_life_expectancy - age)
    
    # Calcular bônus dos avanços médicos
    medical_bonus, applied_advances = calculate_medical_advances_bonus(age, preliminary_remaining_years)
    
    # Aplicar o bônus médico
    adjusted_life_expectancy = preliminary_life_expectancy + medical_bonus
    
    # Garantir que não seja menor que a idade atual + 1
    adjusted_life_expectancy = max(adjusted_life_expectancy, age + 1)
    
    remaining_years = max(0, adjusted_life_expectancy - age)
    
    return remaining_years, adjusted_life_expectancy, health_adjustment, medical_bonus, applied_advances


def get_yes_no_input(question):
    """Helper function para input sim/não"""
    while True:
        response = input(f"{question} (sim/não): ").lower().strip()
        if response in ['sim', 's', 'yes', 'y']:
            return True
        elif response in ['não', 'nao', 'n', 'no']:
            return False
        else:
            print("Por favor, responda com 'sim' ou 'não'")


def get_choice_input(question, choices):
    """Helper function para múltipla escolha"""
    print(f"\n{question}")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    
    while True:
        try:
            choice_num = int(input("Escolha uma opção (número): "))
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print(f"Por favor, escolha um número entre 1 e {len(choices)}")
        except ValueError:
            print("Por favor, digite um número válido")


def collect_health_data():
    """Coleta dados de saúde mais detalhados"""
    print("\n=== INFORMAÇÕES DE SAÚDE ===")
    
    health_factors = {}
    
    # Gênero
    gender_options = ["male", "female", "other"]
    gender_display = ["Masculino", "Feminino", "Outro"]
    chosen_gender = get_choice_input("Qual seu gênero?", gender_display)
    health_factors["gender"] = gender_options[gender_display.index(chosen_gender)]
    
    # Tabagismo
    health_factors["smoking"] = get_yes_no_input("Você fuma?")
    if health_factors["smoking"]:
        smoking_options = ["light", "moderate", "heavy"]
        smoking_display = ["Leve (<10 cigarros/dia)", "Moderado (10-20 cigarros/dia)", "Pesado (>20 cigarros/dia)"]
        chosen_intensity = get_choice_input("Intensidade do tabagismo:", smoking_display)
        health_factors["smoking_intensity"] = smoking_options[smoking_display.index(chosen_intensity)]
    
    # Álcool
    alcohol_options = ["none", "light", "moderate", "heavy"]
    alcohol_display = ["Não bebo", "Ocasional (1-2x/semana)", "Moderado (1-2 drinks/dia)", "Pesado (>2 drinks/dia)"]
    chosen_alcohol = get_choice_input("Consumo de álcool:", alcohol_display)
    health_factors["alcohol"] = alcohol_options[alcohol_display.index(chosen_alcohol)]
    
    # Peso/Obesidade
    health_factors["obesity"] = get_yes_no_input("Você se considera acima do peso?")
    if health_factors["obesity"]:
        bmi_options = ["mild", "moderate", "severe"]
        bmi_display = ["Sobrepeso leve", "Obesidade moderada", "Obesidade severa"]
        chosen_bmi = get_choice_input("Grau de sobrepeso:", bmi_display)
        health_factors["bmi_category"] = bmi_options[bmi_display.index(chosen_bmi)]
    
    # Condições médicas
    health_factors["diabetes"] = get_yes_no_input("Você tem diabetes?")
    health_factors["hypertension"] = get_yes_no_input("Você tem pressão alta?")
    health_factors["heart_disease"] = get_yes_no_input("Você tem doença cardíaca?")
    
    # Hábitos saudáveis
    health_factors["healthy_diet"] = get_yes_no_input("Você mantém uma dieta saudável?")
    if health_factors["healthy_diet"]:
        diet_options = ["basic", "good", "excellent"]
        diet_display = ["Básica (evito fast food)", "Boa (bastante frutas/vegetais)", "Excelente (dieta balanceada/orgânica)"]
        chosen_diet = get_choice_input("Qualidade da dieta:", diet_display)
        health_factors["diet_quality"] = diet_options[diet_display.index(chosen_diet)]
    
    health_factors["regular_exercise"] = get_yes_no_input("Você pratica exercícios regularmente?")
    if health_factors["regular_exercise"]:
        exercise_options = ["light", "moderate", "high"]
        exercise_display = ["Leve (1-2x/semana)", "Moderado (3-4x/semana)", "Intenso (5+x/semana)"]
        chosen_exercise = get_choice_input("Intensidade dos exercícios:", exercise_display)
        health_factors["exercise_intensity"] = exercise_options[exercise_display.index(chosen_exercise)]
    
    # Outros fatores
    health_factors["good_sleep"] = get_yes_no_input("Você dorme bem (7-8h por noite)?")
    health_factors["stress_management"] = get_yes_no_input("Você consegue gerenciar bem o estresse?")
    health_factors["social_connections"] = get_yes_no_input("Você tem boas conexões sociais/familiares?")
    health_factors["regular_checkups"] = get_yes_no_input("Você faz checkups médicos regulares?")
    
    # Histórico familiar
    family_options = ["low", "average", "high"]
    family_display = ["Baixa (parentes morreram cedo)", "Média (expectativa normal)", "Alta (parentes viveram >85 anos)"]
    chosen_family = get_choice_input("Longevidade familiar:", family_display)
    health_factors["family_longevity"] = family_options[family_display.index(chosen_family)]
    
    return health_factors


def main():
    print("=== CALCULADORA AVANÇADA DE EXPECTATIVA DE VIDA ===\n")
    
    # Dados de nascimento
    print("=== INFORMAÇÕES BÁSICAS ===")
    year_birth = int(input("Ano de nascimento: "))
    month_birth = int(input("Mês de nascimento (1-12): "))
    day_birth = int(input("Dia de nascimento: "))
    hour_birth = int(input("Hora de nascimento (formato 24h, opcional, use 12 se não souber): "))

    birth_date = datetime.datetime(year_birth, month_birth, day_birth, hour_birth)

    years, months, days = calculate_age(birth_date)

    print(f"\n📅 Você tem exatamente {years} anos, {months} meses e {days} dias de vida.")
    
    # Coletar dados de saúde
    health_factors = collect_health_data()
    
    # Calcular expectativa
    remaining_years, total_expectancy, health_score, medical_bonus, applied_advances = estimate_life_expectancy(
        years, health_factors["gender"], health_factors
    )
    
    # Resultados detalhados
    print(f"\n{'='*50}")
    print("📊 RESULTADOS DA ANÁLISE")
    print(f"{'='*50}")
    print(f"🎂 Idade atual: {years} anos")
    print(f"📈 Expectativa de vida total: {total_expectancy:.1f} anos")
    print(f"⏰ Anos restantes estimados: {remaining_years:.1f} anos")
    print(f"📊 Score de saúde: {health_score:+.0f} anos (hábitos de vida)")
    print(f"🔬 Bônus médico: +{medical_bonus:.1f} anos (avanços da medicina)")
    
    # Data estimada
    estimated_death = datetime.datetime.now() + relativedelta(years=int(remaining_years))
    print(f"📅 Data estimada: {estimated_death.strftime('%B de %Y')}")
    
    # Detalhes dos avanços médicos considerados
    if applied_advances:
        print(f"\n{'='*40}")
        print("🔬 AVANÇOS MÉDICOS CONSIDERADOS")
        print(f"{'='*40}")
        for advance in applied_advances:
            print(f"📅 {advance['year']}: +{advance['bonus']:.1f} anos")
            print(f"   💡 {advance['description']}")
    
    # Interpretação do score
    print(f"\n{'='*30}")
    print("💡 INTERPRETAÇÃO")
    print(f"{'='*30}")
    
    if health_score >= 10:
        print("🟢 Excelente! Seus hábitos de vida são muito saudáveis.")
    elif health_score >= 5:
        print("🟡 Bom! Você tem hábitos saudáveis com margem para melhorias.")
    elif health_score >= 0:
        print("🟠 Moderado. Considere melhorar alguns hábitos de vida.")
    elif health_score >= -5:
        print("🔴 Atenção! Alguns fatores de risco importantes identificados.")
    else:
        print("🚨 Crítico! Múltiplos fatores de risco. Procure ajuda médica.")
    
    print(f"\n{'='*50}")
    print("⚠️  AVISO IMPORTANTE")
    print(f"{'='*50}")
    print("Esta é apenas uma estimativa baseada em dados estatísticos gerais")
    print("e projeções conservadoras dos avanços médicos esperados.")
    print("Fatores como genética, acesso à saúde, eventos imprevistos e")
    print("o ritmo real dos avanços tecnológicos podem alterar significativamente")
    print("estes números. As projeções médicas são baseadas em tendências atuais")
    print("e podem ser tanto subestimadas quanto superestimadas.")
    print("Sempre consulte profissionais de saúde para avaliações precisas.")
    print("O mais importante é focar em uma vida saudável e com qualidade! 🌟")


if __name__ == "__main__":
    main()
