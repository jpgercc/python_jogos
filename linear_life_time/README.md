# Calculadora Avançada de Expectativa de Vida

Uma aplicação Python que estima a expectativa de vida baseada em dados demográficos atualizados, hábitos de vida e projeções de avanços médicos.

## 🌍 Países Suportados

A calculadora agora inclui dados estatísticos atualizados para 23 países e regiões:

### América
- **Brasil**: IBGE 2023 (♂️ 73.1 | ♀️ 79.9 anos)
- **EUA**: CDC 2023 (♂️ 76.3 | ♀️ 81.2 anos)  
- **Canadá**: Statistics Canada 2023 (♂️ 80.2 | ♀️ 84.1 anos)
- **México**: (♂️ 72.1 | ♀️ 77.8 anos)
- **Argentina**: INDEC 2023 (♂️ 73.0 | ♀️ 79.8 anos)
- **Chile**: (♂️ 77.4 | ♀️ 82.3 anos)

### Europa
- **Alemanha**: Eurostat 2023 (♂️ 78.6 | ♀️ 83.4 anos)
- **França**: (♂️ 79.8 | ♀️ 85.7 anos)
- **Itália**: (♂️ 81.0 | ♀️ 85.6 anos)
- **Espanha**: (♂️ 80.7 | ♀️ 86.2 anos)
- **Reino Unido**: ONS 2023 (♂️ 79.4 | ♀️ 83.1 anos)
- **Suécia**: (♂️ 80.8 | ♀️ 84.3 anos)
- **Noruega**: (♂️ 81.1 | ♀️ 84.6 anos)
- **Suíça**: (♂️ 81.8 | ♀️ 85.6 anos)
- **Rússia**: Rosstat 2023 (♂️ 68.2 | ♀️ 78.0 anos)

### Ásia-Pacífico
- **Japão**: (♂️ 81.5 | ♀️ 87.6 anos) - Maior expectativa do mundo
- **Coreia do Sul**: (♂️ 79.7 | ♀️ 85.9 anos)
- **Austrália**: ABS 2023 (♂️ 81.2 | ♀️ 85.3 anos)
- **China**: National Bureau 2023 (♂️ 75.0 | ♀️ 79.9 anos)
- **Índia**: Ministry of Health 2023 (♂️ 67.4 | ♀️ 70.0 anos)

### África e Oriente Médio
- **África do Sul**: (♂️ 62.3 | ♀️ 67.5 anos)
- **Nigéria**: (♂️ 53.4 | ♀️ 55.0 anos)
- **Egito**: (♂️ 70.2 | ♀️ 74.1 anos)

### Global
- **Média Mundial**: OMS 2023 (♂️ 70.8 | ♀️ 75.9 anos)

## 🚀 Funcionalidades

### Interface de Linha de Comando
- Coleta detalhada de dados pessoais e de saúde
- Cálculo preciso de idade considerando anos bissextos
- Análise de fatores de risco e proteção
- Projeções de avanços médicos futuros

### Interface Web (Streamlit)
- Interface moderna e intuitiva
- Seleção de país com informações contextuais
- Ranking mundial de expectativa de vida
- Visualizações interativas
- Métricas em tempo real

## 📊 Fatores Considerados

### Dados Demográficos
- País de residência
- Gênero
- Idade atual

### Hábitos de Vida
- **Fatores de Risco**: Tabagismo, álcool, obesidade, doenças crônicas
- **Fatores Protetivos**: Dieta saudável, exercícios, sono, gestão do estresse
- **Suporte Social**: Conexões familiares e sociais
- **Cuidados Médicos**: Checkups regulares

### Histórico Familiar
- Longevidade dos parentes
- Fatores genéticos

### Avanços Médicos (2025-2065)
- **2035**: Medicina personalizada (+2.5 anos)
- **2045**: Regeneração celular (+5.0 anos)
- **2055**: Nanotecnologia médica (+8.0 anos)
- **2065+**: Tecnologias disruptivas (+12.0 anos)

## 🔧 Como Usar

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Interface de Linha de Comando
```bash
python main.py
```

### Interface Web
```bash
streamlit run main.py
```

## ⚠️ Importante

Esta é uma ferramenta de estimativa estatística baseada em:
- Dados demográficos oficiais (OMS, IBGE, CDC, Eurostat, etc.)
- Estudos epidemiológicos
- Projeções conservadoras de avanços médicos

**Não substitui consulta médica profissional**. Use apenas como referência educacional.

## 📈 Fontes dos Dados

- **Brasil**: Instituto Brasileiro de Geografia e Estatística (IBGE)
- **EUA**: Centers for Disease Control and Prevention (CDC)
- **Europa**: Eurostat - Serviço de Estatísticas da União Europeia
- **Global**: Organização Mundial da Saúde (OMS)
- **Outros**: Institutos nacionais de estatística de cada país

Dados atualizados em 2023-2024.
- ✅ Brasil: Homens 73.1 anos, Mulheres 79.9 anos
- ✅ Ajuste por idade atual (sobreviventes têm expectativa ligeiramente maior)

### 3. **Sistema de Score de Saúde Sofisticado**

#### Fatores de Risco (Negativos)
- **Tabagismo**: -5 a -12 anos (baseado na intensidade)
- **Álcool pesado**: -6 anos
- **Obesidade**: -2 a -8 anos (baseado no grau)
- **Diabetes**: -6 anos
- **Hipertensão**: -4 anos
- **Doença cardíaca**: -10 anos

#### Fatores Protetivos (Positivos)
- **Dieta saudável**: +1 a +5 anos (baseado na qualidade)
- **Exercício regular**: +2 a +6 anos (baseado na intensidade)
- **Sono adequado**: +2 anos
- **Gerenciamento de estresse**: +3 anos
- **Conexões sociais**: +2 anos
- **Checkups regulares**: +1 ano
- **Álcool moderado**: +1 ano (benefício comprovado)

#### Fatores Genéticos
- **Longevidade familiar alta**: +4 anos
- **Histórico familiar de morte precoce**: -3 anos

### 4. **Interface Melhorada**
- ✅ Perguntas em português brasileiro
- ✅ Sistema de múltipla escolha para respostas mais precisas
- ✅ Validação de entrada
- ✅ Resultados detalhados com interpretação
- ✅ Avisos sobre limitações da estimativa

### 5. **Precisão Científica**
Os ajustes são baseados em estudos epidemiológicos reais:
- Framingham Heart Study
- Blue Zones Research
- WHO Global Health Observatory
- Dados do Ministério da Saúde do Brasil

## Como Usar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o programa
python main.py
```

## Exemplo de Saída

```
📊 RESULTADOS DA ANÁLISE
==================================================
🎂 Idade atual: 30 anos
📈 Expectativa de vida total: 82.5 anos
⏰ Anos restantes estimados: 52.5 anos
📊 Score de saúde: +5 (ajuste em anos)
📅 Data estimada: março de 2077

💡 INTERPRETAÇÃO
==============================
🟡 Bom! Você tem hábitos saudáveis com margem para melhorias.
```

## Limitações

Esta calculadora fornece estimativas baseadas em dados estatísticos populacionais. Fatores individuais como:
- Genética específica
- Acesso aos cuidados de saúde
- Avanços médicos futuros
- Eventos imprevistos

Podem alterar significativamente os resultados. Sempre consulte profissionais de saúde para avaliações personalizadas.
