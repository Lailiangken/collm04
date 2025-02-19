from st_ui.render.render_sidebar import render_sidebar
from st_ui.render.render_main import render_main_content
from st_ui.utils.save_utils import save_result

def main():
    selected_group, selected_model = render_sidebar()
    if not selected_group:
        return
    
    formatted_result, chat_info, last_result = render_main_content(selected_group, selected_model)
    if formatted_result:
        save_result(formatted_result, chat_info, last_result)

if __name__ == "__main__":
    main()   