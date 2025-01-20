import streamlit as st
import json
from typing import List, Dict

class LaciaAssessment:
    prompt = """Seu nome é LACia, você é uma Avaliadora de Competências Médicas, experiente e dotada de profissionalismo, que trabalha no ensino de graduação no curso de Medicina na Universidade Católica de Pelotas (UCPel). A sua identidade profissional está alinhada ao Código de Ética Médica, às Diretrizes Curriculares Nacionais para o Curso de Graduação em Medicina, ao Plano de Desenvolvimento Institucional, ao Projeto Pedagógico Institucional, ao Projeto Pedagógico do Curso de Medicina da UCPel, ao Código de Ética Institucional e ao Regimento Institucional. O seu cenário de atuação é um laboratório de simulação chamado SimLab, localizado no Campus da Saúde, na Avenida Fernando Osório, 1586 - Três Vendas, Pelotas–RS, 96055-000. A concepção pedagógica das atividades de ensino em que você atua aplica os princípios da educação para adultos e da avaliação por competências, busca promover a aprendizagem significativa, a reflexão crítica e a autonomia do educando. Nesta escola, você ajuda a formar estudantes com o seguinte perfil do egresso: um médico generalista, ético, comunicativo e sensível às demandas emergentes na sociedade em que vive, comprometido com a defesa da dignidade humana e da vida. Um profissional reconhecido pela sua competência técnico-científica e teórico-prática fundamentada na compreensão das ciências biomédicas, clínicas, sociohumanísticas, epidemiológicas, das políticas de saúde e da gestão do cuidado. Capaz de atualizar a sua prática por meio da educação permanente e aplicação crítica das evidências científicas e inovações da área para a tomada de decisões e o exercício da liderança em equipes multiprofissionais, priorizando a atenção às necessidades em saúde individuais e coletivas, incluídas as ações preventivas, diagnósticas, terapêuticas e de cuidados paliativos, nos distintos níveis de complexidade, com ênfase nos determinantes sociais de saúde e doença loco-regionais e nacionais. Você tem o maior nível de estudo para a avaliação de habilidades e procedimentos médicos em ambientes simulados, área na qual atua há sete anos na UCPel. Tem conhecimento aprofundado e atualizado sobre técnicas de feedback, Semiologia Médica, Urgência e Emergência, Anatomia Humana, Fisiologia Humana e Treinamento de Habilidades e Procedimentos Médicos em manequins. Você foi selecionada para analisar detalhadamente vídeos de procedimentos médicos em manequins de baixa e média fidelidade, realizados por estudantes de Medicina no SimLab. A sua tarefa consiste em avaliar se o estudante de Medicina demonstra o conhecimento, a atitude, as habilidades e a técnica para fazer os procedimentos médicos. Você tem dois objetivos na sua resposta: gerar avaliação somativa (quantitativa) usando o checklist fornecido; e fornecer feedback avaliativo ao estudante, segundo a técnica do diamante com base nos itens do checklist avaliativo. Você responde em português do Brasil, utilizando terminologia médica. Você deve usar comunicação não violenta, ética, empática, inclusiva e encorajadora. A sua resposta deve sempre promover reflexão sobre a própria prática, buscando sempre promover melhoria do alcance da competência avaliada. Você deve realizar a avaliação somativa usando o checklist fornecido; cada item é avaliado como Sim ou Não, onde Sim equivale a 1 ponto, e Não equivale a 0 pontos. A nota final é dada pela soma dos pontos dos Sim. Para o percentual de acertos, calcular usando a fórmula: Percentual = (Total de Sim / Total de Procedimentos) x 100. Você deve montar uma tabela com duas colunas, onde a primeira coluna contém a frase do checklist e a segunda coluna a avaliação do estudante considerando a realização completa do item mencionado na coluna 1. Caso o estudante tenha realizado corretamente, atribuir nota 01 ao item mencionado. Caso o estudante não tenha realizado ou tenha realizado incorretamente, atribuir nota 00 ao item referido. Caso seja impossível avaliar o item, você deve desconsiderar da avaliação e justificar o impeditivo da avaliação não poder ser atribuída. Apresente sugestões de leitura sobre condutas e práticas baseadas nas melhores evidências científicas que podem auxiliar a melhorar o desempenho do estudante. Ao final da sua resposta, sempre envie estas perguntas ao acadêmico: Como você se sentiu durante o procedimento? Quais foram seus principais desafios? O que você faria diferente em um cenário real? Como você pretende aprimorar suas habilidades no procedimento avaliado? Regras: você nunca mente ou inventa informações. Caso não tenha informação suficiente para avaliar determinado ato, você deve simplesmente explicar isso e solicitar informação adicional."""

    def __init__(self):
        pass

    def display_prompt(self):
        st.markdown("### Prompt Completo de LACia")
        st.markdown(self.prompt, unsafe_allow_html=True)

    def evaluate_checklist(self, checklist: Dict[str, any], student_performance: Dict[str, bool]) -> Dict:
        """
        Evaluate student performance based on a checklist
        
        :param checklist: Checklist dictionary with items
        :param student_performance: Dictionary mapping checklist items to boolean performance
        :return: Evaluation results
        """
        total_items = len(checklist['items'])
        passed_items = sum(1 for item, passed in student_performance.items() if passed)
        
        # Calculate percentage
        percentage = (passed_items / total_items) * 100
        
        # Create evaluation table
        evaluation_table = []
        for item in checklist['items']:
            status = student_performance.get(item, False)
            evaluation_table.append({
                'Item': item,
                'Avaliação': '✅ Sim' if status else '❌ Não'
            })
        
        return {
            'checklist_name': checklist['name'],
            'procedure': checklist['procedure'],
            'total_items': total_items,
            'passed_items': passed_items,
            'percentage': percentage,
            'evaluation_table': evaluation_table
        }

    def generate_feedback(self, evaluation_results: Dict) -> str:
        """
        Generate constructive feedback based on evaluation results
        
        :param evaluation_results: Results from checklist evaluation
        :return: Detailed feedback text
        """
        feedback = f"""
### Avaliação do Procedimento: {evaluation_results['checklist_name']}

**Procedimento Avaliado:** {evaluation_results['procedure']}

**Resumo da Avaliação:**
- Total de Itens: {evaluation_results['total_items']}
- Itens Aprovados: {evaluation_results['passed_items']}
- Percentual de Acerto: {evaluation_results['percentage']:.2f}%

**Detalhamento da Avaliação:**
"""
        for item in evaluation_results['evaluation_table']:
            feedback += f"- {item['Item']}: {item['Avaliação']}\n"
        
        feedback += f"""
### Reflexão e Desenvolvimento

**Perguntas para Reflexão:**
1. Como você se sentiu durante o procedimento?
2. Quais foram seus principais desafios?
3. O que você faria diferente em um cenário real?
4. Como você pretende aprimorar suas habilidades no procedimento avaliado?

**Sugestões de Melhoria:**
- Pratique regularmente em ambientes simulados
- Revise literatura médica atualizada
- Busque feedback constante de professores e supervisores
- Mantenha-se atualizado com as últimas diretrizes clínicas
"""
        return feedback

def main():
    st.title("LACia - Avaliação de Competências Médicas")
    
    # Load checklists
    with open('lacia_checklists.json', 'r') as f:
        checklists = json.load(f)
    
    # Checklist selection
    selected_checklist_name = st.selectbox("Selecione o Checklist", list(checklists.keys()))
    selected_checklist = checklists[selected_checklist_name]
    
    # Performance input
    st.subheader(f"Avaliação de {selected_checklist['procedure']}")
    student_performance = {}
    for item in selected_checklist['items']:
        student_performance[item] = st.checkbox(item)
    
    # Evaluate
    if st.button("Gerar Avaliação"):
        lacia = LaciaAssessment()
        evaluation = lacia.evaluate_checklist(selected_checklist, student_performance)
        feedback = lacia.generate_feedback(evaluation)
        
        st.markdown(feedback)

if __name__ == "__main__":
    main()
