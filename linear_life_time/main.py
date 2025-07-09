import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st


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


def streamlit_app():
    """Interface Streamlit para a calculadora de expectativa de vida"""
    st.set_page_config(
        page_title="Calculadora de Expectativa de Vida", 
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Calculadora Avançada de Expectativa de Vida")
    st.markdown("---")
    
    # Sidebar com informações
    st.sidebar.title("ℹ️ Sobre")
    st.sidebar.markdown("""
    Esta calculadora estima sua expectativa de vida baseada em:
    - Dados demográficos
    - Hábitos de vida
    - Histórico familiar
    - Avanços médicos futuros
    """)
    
    st.sidebar.warning("⚠️ Esta é apenas uma estimativa estatística. Consulte sempre profissionais de saúde.")
    
    # Seção 1: Informações Básicas
    st.header("📅 Informações Básicas")
    col1, col2 = st.columns(2)
    
    with col1:
        year_birth = st.number_input("Ano de nascimento", min_value=1900, max_value=2025, value=1990)
        month_birth = st.selectbox("Mês de nascimento", range(1, 13), index=0)
        
    with col2:
        day_birth = st.number_input("Dia de nascimento", min_value=1, max_value=31, value=1)
        hour_birth = st.number_input("Hora de nascimento (0-23h)", min_value=0, max_value=23, value=12)
    
    # Seção 2: Informações de Saúde
    st.header("🏥 Informações de Saúde")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dados Básicos")
        gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"], index=0)
        country = st.selectbox("País", ["Brazil", "World"], index=0)
        
        st.subheader("Fatores de Risco")
        smoking = st.checkbox("Fuma?")
        smoking_intensity = None
        if smoking:
            smoking_intensity = st.selectbox(
                "Intensidade do tabagismo",
                ["Leve (<10 cigarros/dia)", "Moderado (10-20 cigarros/dia)", "Pesado (>20 cigarros/dia)"]
            )
        
        alcohol = st.selectbox(
            "Consumo de álcool",
            ["Não bebo", "Ocasional (1-2x/semana)", "Moderado (1-2 drinks/dia)", "Pesado (>2 drinks/dia)"]
        )
        
        obesity = st.checkbox("Acima do peso?")
        bmi_category = None
        if obesity:
            bmi_category = st.selectbox(
                "Grau de sobrepeso",
                ["Sobrepeso leve", "Obesidade moderada", "Obesidade severa"]
            )
        
        diabetes = st.checkbox("Tem diabetes?")
        hypertension = st.checkbox("Tem pressão alta?")
        heart_disease = st.checkbox("Tem doença cardíaca?")
    
    with col2:
        st.subheader("Hábitos Saudáveis")
        healthy_diet = st.checkbox("Mantém dieta saudável?")
        diet_quality = None
        if healthy_diet:
            diet_quality = st.selectbox(
                "Qualidade da dieta",
                ["Básica (evito fast food)", "Boa (bastante frutas/vegetais)", "Excelente (dieta balanceada/orgânica)"]
            )
        
        regular_exercise = st.checkbox("Pratica exercícios regularmente?")
        exercise_intensity = None
        if regular_exercise:
            exercise_intensity = st.selectbox(
                "Intensidade dos exercícios",
                ["Leve (1-2x/semana)", "Moderado (3-4x/semana)", "Intenso (5+x/semana)"]
            )
        
        good_sleep = st.checkbox("Dorme bem (7-8h por noite)?")
        stress_management = st.checkbox("Consegue gerenciar bem o estresse?")
        social_connections = st.checkbox("Tem boas conexões sociais/familiares?")
        regular_checkups = st.checkbox("Faz checkups médicos regulares?")
        
        st.subheader("Histórico Familiar")
        family_longevity = st.selectbox(
            "Longevidade familiar",
            ["Baixa (parentes morreram cedo)", "Média (expectativa normal)", "Alta (parentes viveram >85 anos)"]
        )
    
    # Botão para calcular
    if st.button("🔍 Calcular Expectativa de Vida", type="primary"):
        try:
            # Criar objeto datetime
            birth_date = datetime.datetime(year_birth, month_birth, day_birth, hour_birth)
            
            # Calcular idade
            years, months, days = calculate_age(birth_date)
            
            # Mapear valores do Streamlit para o formato da função
            gender_map = {"Masculino": "male", "Feminino": "female", "Outro": "other"}
            alcohol_map = {
                "Não bebo": "none",
                "Ocasional (1-2x/semana)": "light", 
                "Moderado (1-2 drinks/dia)": "moderate",
                "Pesado (>2 drinks/dia)": "heavy"
            }
            
            smoking_intensity_map = {
                "Leve (<10 cigarros/dia)": "light",
                "Moderado (10-20 cigarros/dia)": "moderate", 
                "Pesado (>20 cigarros/dia)": "heavy"
            }
            
            bmi_map = {
                "Sobrepeso leve": "mild",
                "Obesidade moderada": "moderate",
                "Obesidade severa": "severe"
            }
            
            diet_map = {
                "Básica (evito fast food)": "basic",
                "Boa (bastante frutas/vegetais)": "good",
                "Excelente (dieta balanceada/orgânica)": "excellent"
            }
            
            exercise_map = {
                "Leve (1-2x/semana)": "light",
                "Moderado (3-4x/semana)": "moderate",
                "Intenso (5+x/semana)": "high"
            }
            
            family_map = {
                "Baixa (parentes morreram cedo)": "low",
                "Média (expectativa normal)": "average",
                "Alta (parentes viveram >85 anos)": "high"
            }
            
            # Construir dicionário de fatores de saúde
            health_factors = {
                "gender": gender_map[gender],
                "smoking": smoking,
                "alcohol": alcohol_map[alcohol],
                "obesity": obesity,
                "diabetes": diabetes,
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "healthy_diet": healthy_diet,
                "regular_exercise": regular_exercise,
                "good_sleep": good_sleep,
                "stress_management": stress_management,
                "social_connections": social_connections,
                "regular_checkups": regular_checkups,
                "family_longevity": family_map[family_longevity]
            }
            
            # Adicionar intensidades se aplicável
            if smoking and smoking_intensity:
                health_factors["smoking_intensity"] = smoking_intensity_map[smoking_intensity]
            if obesity and bmi_category:
                health_factors["bmi_category"] = bmi_map[bmi_category]
            if healthy_diet and diet_quality:
                health_factors["diet_quality"] = diet_map[diet_quality]
            if regular_exercise and exercise_intensity:
                health_factors["exercise_intensity"] = exercise_map[exercise_intensity]
            
            # Calcular expectativa
            remaining_years, total_expectancy, health_score, medical_bonus, applied_advances = estimate_life_expectancy(
                years, health_factors["gender"], health_factors, country
            )
            
            # Exibir resultados
            st.markdown("---")
            st.header("📊 Resultados da Análise")
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎂 Idade Atual", f"{years} anos")
                st.caption(f"{months} meses e {days} dias")
            
            with col2:
                st.metric("📈 Expectativa Total", f"{total_expectancy:.1f} anos")
                
            with col3:
                st.metric("⏰ Anos Restantes", f"{remaining_years:.1f} anos")
                
            with col4:
                estimated_death = datetime.datetime.now() + relativedelta(years=int(remaining_years))
                st.metric("📅 Data Estimada", estimated_death.strftime("%Y"))
                st.caption(estimated_death.strftime("%B"))
            
            # Detalhes dos scores
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Score de Saúde")
                score_color = "green" if health_score >= 5 else "orange" if health_score >= 0 else "red"
                st.markdown(f"<h3 style='color: {score_color};'>{health_score:+.0f} anos</h3>", unsafe_allow_html=True)
                
                if health_score >= 10:
                    st.success("🟢 Excelente! Seus hábitos de vida são muito saudáveis.")
                elif health_score >= 5:
                    st.info("🟡 Bom! Você tem hábitos saudáveis com margem para melhorias.")
                elif health_score >= 0:
                    st.warning("🟠 Moderado. Considere melhorar alguns hábitos de vida.")
                elif health_score >= -5:
                    st.error("🔴 Atenção! Alguns fatores de risco importantes identificados.")
                else:
                    st.error("🚨 Crítico! Múltiplos fatores de risco. Procure ajuda médica.")
            
            with col2:
                st.subheader("🔬 Bônus Médico")
                st.markdown(f"<h3 style='color: blue;'>+{medical_bonus:.1f} anos</h3>", unsafe_allow_html=True)
                st.caption("Baseado em avanços médicos esperados")
            
            # Detalhes dos avanços médicos
            if applied_advances:
                st.subheader("🔬 Avanços Médicos Considerados")
                for advance in applied_advances:
                    with st.expander(f"📅 {advance['year']}: +{advance['bonus']:.1f} anos"):
                        st.write(f"💡 {advance['description']}")
            
            # Gráfico de expectativa
            st.subheader("📈 Visualização da Expectativa de Vida")
            
            # Criar dois tipos de gráficos mais informativos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🍰 Composição da Expectativa")
                # Gráfico de pizza mostrando os componentes
                import matplotlib.pyplot as plt
                
                base_expectancy = get_base_life_expectancy(years, health_factors["gender"], country)
                components = []
                labels = []
                colors = []
                
                # Expectativa base
                components.append(base_expectancy)
                labels.append(f'Expectativa base\n({base_expectancy:.1f} anos)')
                colors.append('#808080')
                
                # Ajuste de saúde (pode ser positivo ou negativo)
                if health_score > 0:
                    components.append(health_score)
                    labels.append(f'Hábitos saudáveis\n(+{health_score:.1f} anos)')
                    colors.append('#4CAF50')
                elif health_score < 0:
                    components.append(abs(health_score))
                    labels.append(f'Fatores de risco\n({health_score:.1f} anos)')
                    colors.append('#F44336')
                
                # Bônus médico
                if medical_bonus > 0:
                    components.append(medical_bonus)
                    labels.append(f'Avanços médicos\n(+{medical_bonus:.1f} anos)')
                    colors.append('#2196F3')
                
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                wedges, texts, autotexts = ax1.pie(components, labels=labels, colors=colors, 
                                                  autopct='%1.1f%%', startangle=90)
                ax1.set_title('Composição da Expectativa de Vida')
                
                st.pyplot(fig1)
            
            with col2:
                st.subheader("📊 Linha do Tempo da Vida")
                # Gráfico de barras horizontais mostrando a vida
                import numpy as np
                
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                
                # Barra da vida total
                total_bar_width = 0.6
                
                # Vida já vivida (verde)
                ax2.barh(1, years, height=total_bar_width, color='#4CAF50', 
                        label=f'Vida vivida ({years} anos)', alpha=0.8)
                
                # Vida restante (azul claro)
                ax2.barh(1, remaining_years, left=years, height=total_bar_width, 
                        color='#81C784', label=f'Vida restante ({remaining_years:.1f} anos)', alpha=0.8)
                
                # Expectativa base como referência (linha)
                base_exp = get_base_life_expectancy(years, health_factors["gender"], country)
                ax2.axvline(x=base_exp, color='gray', linestyle='--', 
                           label=f'Expectativa base ({base_exp:.1f} anos)')
                
                # Marcos importantes
                if years < 65:
                    ax2.axvline(x=65, color='orange', linestyle=':', alpha=0.7, label='Aposentadoria (65)')
                if total_expectancy > 80:
                    ax2.axvline(x=80, color='purple', linestyle=':', alpha=0.7, label='80 anos')
                
                ax2.set_xlim(0, max(100, total_expectancy + 5))
                ax2.set_ylim(0.5, 1.5)
                ax2.set_xlabel('Idade (anos)')
                ax2.set_title('Linha do Tempo da Sua Vida')
                ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                ax2.set_yticks([])
                ax2.grid(True, alpha=0.3, axis='x')
                
                # Adicionar anotações
                ax2.annotate(f'Você está aqui\n({years} anos)', 
                           xy=(years, 1), xytext=(years, 1.3),
                           ha='center', va='bottom',
                           arrowprops=dict(arrowstyle='->', color='red'),
                           fontsize=10, color='red', weight='bold')
                
                ax2.annotate(f'Expectativa final\n({total_expectancy:.1f} anos)', 
                           xy=(total_expectancy, 1), xytext=(total_expectancy, 0.7),
                           ha='center', va='top',
                           arrowprops=dict(arrowstyle='->', color='blue'),
                           fontsize=10, color='blue', weight='bold')
                
                plt.tight_layout()
                st.pyplot(fig2)
            
            # Gráfico adicional: Comparação com médias
            st.subheader("📈 Comparação com Médias Populacionais")
            
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            
            categories = ['Expectativa\nBase', 'Média\nMundial', 'Sua\nExpectativa']
            base_exp = get_base_life_expectancy(years, health_factors["gender"], country)
            world_exp = get_base_life_expectancy(years, health_factors["gender"], "World")
            
            values = [base_exp, world_exp, total_expectancy]
            colors = ['#FFC107', '#FF9800', '#4CAF50']
            
            bars = ax3.bar(categories, values, color=colors, alpha=0.8)
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{value:.1f} anos', ha='center', va='bottom', fontweight='bold')
            
            ax3.set_ylabel('Expectativa de Vida (anos)')
            ax3.set_title('Comparação de Expectativa de Vida')
            ax3.grid(True, alpha=0.3, axis='y')
            ax3.set_ylim(0, max(values) + 10)
            
            # Destacar a diferença
            if total_expectancy > base_exp:
                diff = total_expectancy - base_exp
                ax3.annotate(f'+{diff:.1f} anos\nacima da base!', 
                           xy=(2, total_expectancy), xytext=(2.3, total_expectancy),
                           ha='left', va='center',
                           arrowprops=dict(arrowstyle='->', color='green'),
                           fontsize=12, color='green', weight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
            
            st.pyplot(fig3)
            
        except Exception as e:
            st.error(f"Erro no cálculo: {str(e)}")
            st.error("Verifique se todas as datas são válidas.")


# Executar a app Streamlit se o script for chamado com streamlit
if __name__ == "__main__":
    # Verificar se está rodando no Streamlit
    try:
        # Esta é uma forma de detectar se estamos no Streamlit
        import sys
        if 'streamlit' in sys.modules:
            streamlit_app()
        else:
            main()
    except:
        main()