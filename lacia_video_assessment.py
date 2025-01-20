import streamlit as st
import os
import json
from utils.lacia_prompt import LaciaAssessment
import google.generativeai as genai
from dotenv import load_dotenv

class LaciaVideoAssessment:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.checklists_file = 'lacia_checklists.json'

    def load_checklists(self):
        """Load checklists from JSON file."""
        if os.path.exists(self.checklists_file):
            with open(self.checklists_file, 'r') as f:
                return json.load(f)
        return {}

    def generate_markdown_assessment(self, video_file, selected_checklist):
        """
        Generate markdown assessment for the uploaded video
        
        :param video_file: Uploaded video file
        :param selected_checklist: Selected checklist details
        :return: Markdown assessment
        """
        # Prepare the prompt with checklist details
        prompt = f"""
Você é LACia, avaliadora de competências médicas. 
Você receberá um vídeo de um procedimento médico e um checklist para avaliação.

Checklist Selecionado: {selected_checklist['name']}
Procedimento: {selected_checklist['procedure']}

Itens do Checklist:
{chr(10).join([f"- {item}" for item in selected_checklist['items']]}

Por favor, analise o vídeo e forneça uma avaliação detalhada seguindo os critérios do checklist.
Gere um relatório em markdown que inclua:
1. Avaliação de cada item do checklist
2. Percentual de acertos
3. Feedback construtivo
4. Sugestões de melhoria
5. Perguntas reflexivas para o estudante
"""
        
        # Generate assessment using Gemini
        try:
            # Note: This is a placeholder. In a real scenario, you'd need to process the video
            response = self.model.generate_content(prompt)
            
            # Convert response to markdown
            markdown_assessment = f"""
# Avaliação de Procedimento Médico - {selected_checklist['name']}

## Detalhes do Procedimento
- **Procedimento:** {selected_checklist['procedure']}
- **Checklist:** {selected_checklist['name']}

## Avaliação Detalhada
{response.text}

## Reflexão e Desenvolvimento

### Perguntas para o Acadêmico
1. Como você se sentiu durante o procedimento?
2. Quais foram seus principais desafios?
3. O que você faria diferente em um cenário real?
4. Como você pretende aprimorar suas habilidades no procedimento avaliado?
"""
            return markdown_assessment
        
        except Exception as e:
            return f"Erro na geração do relatório: {str(e)}"

def main():
    st.set_page_config(page_title="LACia - Avaliação de Vídeo", page_icon="🩺")
    
    # Sidebar navigation
    st.sidebar.title("🩺 LACia Avaliação de Vídeo")
    
    # Initialize assessment manager
    video_assessor = LaciaVideoAssessment()
    
    # Load checklists
    checklists = video_assessor.load_checklists()
    
    # Main content
    st.title("Avaliação de Procedimento Médico por Vídeo")
    
    # Video upload
    uploaded_video = st.file_uploader("Faça upload do vídeo do procedimento", type=['mp4', 'avi', 'mov'])
    
    # Checklist selection
    if checklists:
        selected_checklist_name = st.selectbox(
            "Selecione o Checklist para Avaliação", 
            list(checklists.keys())
        )
        selected_checklist = checklists[selected_checklist_name]
    else:
        st.warning("Nenhum checklist disponível. Crie um checklist primeiro.")
        return
    
    # Generate assessment button
    if uploaded_video and st.button("Gerar Avaliação"):
        # Save uploaded video temporarily
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_video.getbuffer())
        
        # Generate markdown assessment
        markdown_report = video_assessor.generate_markdown_assessment(
            "temp_video.mp4", 
            selected_checklist
        )
        
        # Display markdown report
        st.markdown("## Relatório de Avaliação")
        st.markdown(markdown_report)
        
        # Option to download markdown
        st.download_button(
            label="Baixar Relatório",
            data=markdown_report,
            file_name=f"relatorio_{selected_checklist_name}.md",
            mime="text/markdown"
        )
        
        # Clean up temporary video
        os.remove("temp_video.mp4")

if __name__ == "__main__":
    main()
