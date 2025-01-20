import streamlit as st
import json
import os

# File to store checklists
CHECKLISTS_FILE = 'checklists.json'

def load_checklists():
    """Load checklists from JSON file."""
    if os.path.exists(CHECKLISTS_FILE):
        with open(CHECKLISTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_checklists(checklists):
    """Save checklists to JSON file."""
    with open(CHECKLISTS_FILE, 'w') as f:
        json.dump(checklists, f, indent=4)

def main():
    st.title("LACia - Checklist de Competências Médicas")
    
    # Load existing checklists
    checklists = load_checklists()
    
    # Sidebar for navigation
    menu = st.sidebar.selectbox("Menu", 
        ["Criar Checklist", "Listar Checklists", "Editar Checklist", "Excluir Checklist"]
    )
    
    if menu == "Criar Checklist":
        create_checklist(checklists)
    
    elif menu == "Listar Checklists":
        list_checklists(checklists)
    
    elif menu == "Editar Checklist":
        edit_checklist(checklists)
    
    elif menu == "Excluir Checklist":
        delete_checklist(checklists)

def create_checklist(checklists):
    """Create a new checklist."""
    st.header("Criar Novo Checklist")
    
    # Checklist name input
    checklist_name = st.text_input("Nome do Checklist")
    
    # Dynamic item addition
    st.subheader("Itens do Checklist")
    num_items = st.number_input("Número de Itens", min_value=1, max_value=20, value=5)
    
    items = []
    for i in range(num_items):
        item = st.text_input(f"Item {i+1}", key=f"item_{i}")
        if item:
            items.append(item)
    
    if st.button("Salvar Checklist"):
        if checklist_name and items:
            # Check if checklist name already exists
            if checklist_name in checklists:
                st.error("Um checklist com este nome já existe. Escolha outro nome.")
            else:
                # Add new checklist
                checklists[checklist_name] = {
                    "items": items,
                    "created_at": str(st.session_state.get('time', 'N/A'))
                }
                save_checklists(checklists)
                st.success(f"Checklist '{checklist_name}' criado com sucesso!")
        else:
            st.error("Por favor, insira um nome para o checklist e pelo menos um item.")

def list_checklists(checklists):
    """List all existing checklists."""
    st.header("Checklists Existentes")
    
    if not checklists:
        st.info("Nenhum checklist encontrado.")
    
    for name, details in checklists.items():
        with st.expander(name):
            st.write("**Itens:**")
            for idx, item in enumerate(details['items'], 1):
                st.write(f"{idx}. {item}")
            st.write(f"**Criado em:** {details.get('created_at', 'N/A')}")

def edit_checklist(checklists):
    """Edit an existing checklist."""
    st.header("Editar Checklist")
    
    if not checklists:
        st.info("Nenhum checklist disponível para edição.")
        return
    
    # Select checklist to edit
    selected_checklist = st.selectbox("Selecione o Checklist", list(checklists.keys()))
    
    if selected_checklist:
        current_items = checklists[selected_checklist]['items']
        
        # Allow editing items
        st.subheader(f"Editando: {selected_checklist}")
        edited_items = []
        for idx, item in enumerate(current_items, 1):
            edited_item = st.text_input(f"Item {idx}", value=item, key=f"edit_{idx}")
            edited_items.append(edited_item)
        
        if st.button("Salvar Alterações"):
            # Update checklist
            checklists[selected_checklist]['items'] = edited_items
            save_checklists(checklists)
            st.success(f"Checklist '{selected_checklist}' atualizado com sucesso!")

def delete_checklist(checklists):
    """Delete a checklist."""
    st.header("Excluir Checklist")
    
    if not checklists:
        st.info("Nenhum checklist disponível para exclusão.")
        return
    
    # Select checklist to delete
    selected_checklist = st.selectbox("Selecione o Checklist para Excluir", list(checklists.keys()))
    
    if st.button("Confirmar Exclusão"):
        if selected_checklist in checklists:
            del checklists[selected_checklist]
            save_checklists(checklists)
            st.success(f"Checklist '{selected_checklist}' excluído com sucesso!")

if __name__ == "__main__":
    # Configure page
    st.set_page_config(page_title="LACia - Checklists Médicos", page_icon="📋")
    
    # Initialize session state for time
    if 'time' not in st.session_state:
        st.session_state.time = "2025-01-16T10:32:23-03:00"
    
    main()
