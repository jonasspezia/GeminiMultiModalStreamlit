import streamlit as st
import json
import os
from datetime import datetime

# File to store checklists
CHECKLISTS_FILE = 'lacia_checklists.json'

class LaciaChecklistManager:
    @staticmethod
    def load_checklists():
        """Load checklists from JSON file."""
        if os.path.exists(CHECKLISTS_FILE):
            with open(CHECKLISTS_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_checklists(checklists):
        """Save checklists to JSON file."""
        with open(CHECKLISTS_FILE, 'w') as f:
            json.dump(checklists, f, indent=4)

    @staticmethod
    def create_checklist(name, procedure, items):
        """Create a new checklist."""
        checklists = LaciaChecklistManager.load_checklists()
        
        # Ensure unique checklist name
        if name in checklists:
            st.error(f"Checklist '{name}' já existe. Escolha outro nome.")
            return False
        
        # Create checklist
        checklist = {
            'name': name,
            'procedure': procedure,
            'items': items,
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }
        
        checklists[name] = checklist
        LaciaChecklistManager.save_checklists(checklists)
        return True

    @staticmethod
    def edit_checklist(original_name, new_name, procedure, items):
        """Edit an existing checklist."""
        checklists = LaciaChecklistManager.load_checklists()
        
        # Check if original checklist exists
        if original_name not in checklists:
            st.error(f"Checklist '{original_name}' não encontrado.")
            return False
        
        # If name is changed, remove old entry and create new
        if original_name != new_name:
            del checklists[original_name]
        
        # Create/Update checklist
        checklist = {
            'name': new_name,
            'procedure': procedure,
            'items': items,
            'created_at': checklists.get(original_name, {}).get('created_at', datetime.now().isoformat()),
            'last_modified': datetime.now().isoformat()
        }
        
        checklists[new_name] = checklist
        LaciaChecklistManager.save_checklists(checklists)
        return True

    @staticmethod
    def delete_checklist(name):
        """Delete a checklist."""
        checklists = LaciaChecklistManager.load_checklists()
        
        if name in checklists:
            del checklists[name]
            LaciaChecklistManager.save_checklists(checklists)
            return True
        return False

def main():
    st.set_page_config(page_title="LACia - Gerenciador de Checklists", page_icon="📋")
    
    # Sidebar navigation with icons
    st.sidebar.title("🩺 LACia Checklists")
    
    # Main menu in sidebar
    menu = st.sidebar.radio("Navegação", [
        "📋 Criar Checklist", 
        "📄 Listar Checklists", 
        "✏️ Editar Checklist", 
        "🗑️ Excluir Checklist",
        "📊 Avaliar Procedimento",
        "📜 Prompt LACia"
    ], key="main_menu")

    # Main content area
    st.title("Gerenciador de Checklists Médicos")

    if menu == "📋 Criar Checklist":
        st.header("Criar Novo Checklist")
        
        # Checklist details
        name = st.text_input("Nome do Checklist", help="Um nome único para identificar o checklist")
        procedure = st.text_input("Procedimento Médico", help="Descreva o procedimento médico a ser avaliado")
        
        # Dynamic item addition
        st.subheader("Itens do Checklist")
        num_items = st.number_input("Número de Itens", min_value=1, max_value=20, value=5)
        
        items = []
        for i in range(num_items):
            item = st.text_area(f"Item {i+1}", help="Descreva um critério específico para avaliação")
            if item:
                items.append(item)
        
        if st.button("Salvar Checklist"):
            if name and procedure and items:
                if LaciaChecklistManager.create_checklist(name, procedure, items):
                    st.success(f"Checklist '{name}' criado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    elif menu == "📄 Listar Checklists":
        st.header("Checklists Existentes")
        checklists = LaciaChecklistManager.load_checklists()
        
        if not checklists:
            st.info("Nenhum checklist encontrado.")
        
        for name, details in checklists.items():
            with st.expander(f"{name} - {details['procedure']}"):
                st.write("**Detalhes do Checklist:**")
                st.write(f"**Procedimento:** {details['procedure']}")
                st.write("**Itens:**")
                for idx, item in enumerate(details['items'], 1):
                    st.write(f"{idx}. {item}")
                st.write(f"**Criado em:** {details['created_at']}")
                st.write(f"**Última modificação:** {details['last_modified']}")

    elif menu == "✏️ Editar Checklist":
        st.header("Editar Checklist")
        checklists = LaciaChecklistManager.load_checklists()
        
        if not checklists:
            st.info("Nenhum checklist disponível para edição.")
            return
        
        # Select checklist to edit
        selected_checklist = st.selectbox("Selecione o Checklist", list(checklists.keys()))
        
        if selected_checklist:
            current_details = checklists[selected_checklist]
            
            # Editable fields
            name = st.text_input("Nome do Checklist", value=current_details['name'])
            procedure = st.text_input("Procedimento Médico", value=current_details['procedure'])
            
            # Edit items
            st.subheader("Itens do Checklist")
            edited_items = []
            for idx, item in enumerate(current_details['items'], 1):
                edited_item = st.text_area(f"Item {idx}", value=item)
                edited_items.append(edited_item)
            
            if st.button("Salvar Alterações"):
                if LaciaChecklistManager.edit_checklist(selected_checklist, name, procedure, edited_items):
                    st.success(f"Checklist '{name}' atualizado com sucesso!")

    elif menu == "🗑️ Excluir Checklist":
        st.header("Excluir Checklist")
        checklists = LaciaChecklistManager.load_checklists()
        
        if not checklists:
            st.info("Nenhum checklist disponível para exclusão.")
            return
        
        # Select checklist to delete
        selected_checklist = st.selectbox("Selecione o Checklist para Excluir", list(checklists.keys()))
        
        if st.button("Confirmar Exclusão"):
            if LaciaChecklistManager.delete_checklist(selected_checklist):
                st.success(f"Checklist '{selected_checklist}' excluído com sucesso!")

    elif menu == "📊 Avaliar Procedimento":
        st.header("Avaliação de Procedimento Médico")
        
        # Load checklists
        checklists = LaciaChecklistManager.load_checklists()
        
        if not checklists:
            st.info("Nenhum checklist disponível para avaliação.")
            return
        
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
            from utils.lacia_prompt import LaciaAssessment
            
            lacia = LaciaAssessment()
            evaluation = lacia.evaluate_checklist(selected_checklist, student_performance)
            feedback = lacia.generate_feedback(evaluation)
            
            st.markdown(feedback)

    elif menu == "📜 Prompt LACia":
        st.header("Prompt Completo de LACia")
        from utils.lacia_prompt import LaciaAssessment
        
        lacia = LaciaAssessment()
        st.markdown("### Identidade Profissional")
        st.markdown("""
        LACia é uma Avaliadora de Competências Médicas na Universidade Católica de Pelotas (UCPel), 
        especializada em avaliação de habilidades e procedimentos médicos em ambientes simulados.
        """)
        
        st.markdown("### Prompt Completo")
        st.markdown(lacia.prompt, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
